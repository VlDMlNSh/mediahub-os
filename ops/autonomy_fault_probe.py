#!/usr/bin/env python3
"""Bounded, repository-owned resilience probes for MediaHub autonomous runtime."""
from __future__ import annotations

import argparse
import json
import os
import signal
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / ".autonomous"
HEARTBEAT = STATE / "astra_heartbeat.json"
LOOP_PID = STATE / "loop.pid"
COMMAND_BUS_PID = STATE / "astra_command_bus.pid"
STOP = STATE / "STOP"

@dataclass(frozen=True)
class ProcIdentity:
    pid: int
    start: str
    cmd: str

def proc_identity(pid: int) -> ProcIdentity | None:
    if pid <= 0 or not Path(f"/proc/{pid}").exists():
        return None
    try:
        start = Path(f"/proc/{pid}/stat").read_text().split()[21]
        cmd = " ".join(Path(f"/proc/{pid}/cmdline").read_bytes().decode(errors="replace").split("\0")[:-1])
        return ProcIdentity(pid, start, cmd)
    except (OSError, IndexError):
        return None

def pid_from_file(path: Path) -> int | None:
    try:
        raw = path.read_text().strip()
        value = raw.split(":", 1)[0]
        return int(value) if value.isdigit() else None
    except (OSError, ValueError):
        return None

def heartbeat() -> dict:
    return json.loads(HEARTBEAT.read_text())

def wait_until(predicate, timeout: float = 20.0, interval: float = 0.5):
    deadline = time.time() + timeout
    last = None
    while time.time() < deadline:
        last = predicate()
        if last:
            return last
        time.sleep(interval)
    raise TimeoutError(f"condition not met within {timeout}s; last={last!r}")

def fixed_identity(pid: int, allowed: tuple[str, ...]) -> ProcIdentity:
    ident = proc_identity(pid)
    if ident is None or not any(token in ident.cmd for token in allowed):
        raise RuntimeError(f"refusing to signal unexpected process pid={pid}: {ident}")
    return ident

def find_owned_process(fragment: str) -> int | None:
    try:
        result = subprocess.run(["/usr/bin/pgrep", "-f", fragment], text=True, capture_output=True, check=False)
    except OSError:
        return None
    for line in result.stdout.splitlines():
        try:
            pid = int(line.strip())
        except ValueError:
            continue
        if pid != os.getpid() and proc_identity(pid) is not None:
            return pid
    return None

def terminate_owned(pid: int, allowed: tuple[str, ...]) -> ProcIdentity:
    ident = fixed_identity(pid, allowed)
    os.kill(pid, signal.SIGTERM)
    wait_until(lambda: proc_identity(pid) is None, timeout=8.0)
    return ident

def scenario_astra_restart() -> dict:
    pid = pid_from_file(STATE / "astra.pid")
    if pid is None:
        # heartbeat supplies a verified current PID when the pidfile is transiently absent.
        pid = int(heartbeat()["hybrid_controller_pid"])
        raise RuntimeError(f"astra pidfile unavailable; refusing ambiguous restart (observed hybrid pid={pid})")
    # Astra is the only fixed supervisor command this probe may terminate.
    ident = fixed_identity(pid, ("ops/astra_orchestrator.py",))
    before = heartbeat()
    terminate_owned(pid, ("ops/astra_orchestrator.py",))
    after = wait_until(lambda: heartbeat() if heartbeat().get("state") == "RUNNING" and heartbeat().get("head") else None)
    def new_astra_pid():
        candidate = pid_from_file(STATE / "astra.pid")
        return candidate if candidate and candidate != pid and proc_identity(candidate) else None
    new_pid = wait_until(new_astra_pid)
    return {"scenario":"astra-restart","before_pid":pid,"after_pid":new_pid,"old_start":ident.start,"result":"PASS","before":before,"after":after}

def scenario_loop_restart() -> dict:
    pid = pid_from_file(LOOP_PID)
    if pid is None:
        raise RuntimeError("loop pid unavailable")
    ident = fixed_identity(pid, ("ops/autonomous_os_loop.sh",))
    before = heartbeat()
    terminate_owned(pid, ("ops/autonomous_os_loop.sh",))
    def new_loop_pid():
        candidate = pid_from_file(LOOP_PID)
        return candidate if candidate and candidate != pid and proc_identity(candidate) else None
    new_pid = wait_until(new_loop_pid)
    after = wait_until(lambda: heartbeat() if heartbeat().get("loop_pid") == new_pid else None)
    return {"scenario":"controller-restart","before_pid":pid,"after_pid":new_pid,"old_start":ident.start,"result":"PASS","before":before,"after":after}

def scenario_command_bus_restart() -> dict:
    pid = pid_from_file(COMMAND_BUS_PID) or find_owned_process("ops/astra_command_bus.py")
    if pid is None:
        raise RuntimeError("command-bus pid unavailable")
    ident = fixed_identity(pid, ("ops/astra_command_bus.py",))
    terminate_owned(pid, ("ops/astra_command_bus.py",))
    def new_command_bus_pid():
        candidate = pid_from_file(COMMAND_BUS_PID) or find_owned_process("ops/astra_command_bus.py")
        return candidate if candidate and candidate != pid and proc_identity(candidate) else None
    new_pid = wait_until(new_command_bus_pid)
    return {"scenario":"command-bus-restart","before_pid":pid,"after_pid":new_pid,"old_start":ident.start,"result":"PASS"}

def scenario_stop_resume() -> dict:
    before = heartbeat()
    STOP.write_text("fault-probe\n")
    stopped = wait_until(lambda: heartbeat() if heartbeat().get("state") == "RUNNING" and not proc_identity(int(heartbeat().get("loop_pid",0))) else None)
    astra_pid = pid_from_file(STATE / "astra.pid")
    if astra_pid is None or proc_identity(astra_pid) is None:
        raise RuntimeError("Astra did not remain resident during STOP")
    STOP.unlink(missing_ok=True)
    resumed_pid = wait_until(lambda: pid_from_file(LOOP_PID) if pid_from_file(LOOP_PID) and proc_identity(pid_from_file(LOOP_PID)) else None)
    after = wait_until(lambda: heartbeat() if heartbeat().get("loop_pid") == resumed_pid else None)
    return {"scenario":"stop-resume","astra_pid":astra_pid,"stopped":stopped,"resumed_loop_pid":resumed_pid,"result":"PASS","before":before,"after":after}

def scenario_idle() -> dict:
    hb = heartbeat()
    if hb.get("state") != "RUNNING" or hb.get("failure_streak") != 0:
        raise RuntimeError(f"runtime not healthy: {hb}")
    return {"scenario":"clean-idle","result":"PASS","heartbeat":hb}

SCENARIOS = {
    "astra-restart": scenario_astra_restart,
    "controller-restart": scenario_loop_restart,
    "command-bus-restart": scenario_command_bus_restart,
    "stop-resume": scenario_stop_resume,
    "clean-idle": scenario_idle,
}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scenario", choices=sorted(SCENARIOS))
    parser.add_argument("--apply", action="store_true", help="perform the bounded process fault injection")
    args = parser.parse_args()
    started = time.time()
    if not args.apply and args.scenario != "clean-idle":
        print(json.dumps({"scenario":args.scenario,"result":"BLOCKED","reason":"--apply required"}, sort_keys=True))
        return 30
    try:
        result = SCENARIOS[args.scenario]()
        result["elapsed_seconds"] = round(time.time() - started, 3)
        print(json.dumps(result, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({"scenario":args.scenario,"result":"UNVERIFIED","error":f"{type(exc).__name__}: {exc}","elapsed_seconds":round(time.time()-started,3)}, sort_keys=True))
        return 20

if __name__ == "__main__":
    raise SystemExit(main())
