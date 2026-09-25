#!/usr/bin/env python3
"""Resident Astra development Coordinator for the MediaHub autonomous loop.

Astra is a supervisory coordinator, not a second source of truth. It observes
the existing local controller state, reconciles liveness, and restarts only
fixed, repository-owned components. It never accepts arbitrary shell input.
"""
from __future__ import annotations

import fcntl
import json
import os
import signal
import subprocess  # nosec B404
import time
from pathlib import Path

ROOT = Path(os.environ.get("MEDIAHUB_ROOT", "/home/mediahub/dev/mediahub-os-autonomous")).resolve()
STATE = ROOT / ".autonomous"
LOCK = STATE / "astra.lock"
PIDFILE = STATE / "astra.pid"
HEARTBEAT = STATE / "astra_heartbeat.json"
STOPFILE = STATE / "STOP"
INTERVAL = 15
MAX_STALE = 45
LOOP_SCRIPT = ROOT / "ops" / "autonomous_os_loop.sh"
HYBRID_SCRIPT = ROOT / "ops" / "hybrid_orchestrator.py"
LOOP_PIDFILE = STATE / "loop.pid"
CONTROLLER_PIDFILE = STATE / "controller.pid"

class AstraState:
    def __init__(self) -> None:
        self.failures = 0
        self.last_action = "BOOT"
        self.last_error = ""

def _proc_starttime(pid: int) -> str:
    try:
        return Path(f"/proc/{pid}/stat").read_text(encoding="utf-8").split()[21]
    except (OSError, IndexError, ValueError):
        return ""

def _owned_pid(path: Path, expected: str) -> int | None:
    try:
        raw = path.read_text(encoding="utf-8").strip()
        pid_s, start = raw.split(":", 1)
        pid = int(pid_s)
    except (OSError, ValueError):
        return None
    if pid <= 1 or not start or _proc_starttime(pid) != start:
        return None
    try:
        cmd = Path(f"/proc/{pid}/cmdline").read_bytes().decode("utf-8", "replace").replace("\x00", " ")
    except OSError:
        return None
    return pid if expected in cmd else None

def _write_json(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)

def _git(*args: str) -> str:
    result = subprocess.run(
        ["/usr/bin/git", *args],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )  # nosec B603
    return result.stdout.strip()

def _r4_ok() -> bool:
    result = subprocess.run(
        ["/usr/bin/git", "merge-base", "--is-ancestor",
         "471f709f5633feab7aeb62dd3ea52effad6d2bc4", "HEAD"],
        cwd=ROOT, text=True, capture_output=True, check=False,
    )  # nosec B603
    return result.returncode == 0

def _snapshot(loop_pid: int | None, hybrid_pid: int | None, state: AstraState) -> dict:
    return {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "state": "RUNNING",
        "head": _git("rev-parse", "HEAD") or "UNKNOWN",
        "tree": _git("rev-parse", "HEAD^{tree}") or "UNKNOWN",
        "clean": not bool(_git("status", "--porcelain")),
        "r4_ancestry": _r4_ok(),
        "loop_pid": loop_pid,
        "hybrid_controller_pid": hybrid_pid,
        "current_cycle": (STATE / "current_cycle").read_text(encoding="utf-8").strip()
            if (STATE / "current_cycle").exists() else "",
        "current_result": (STATE / "current_result").read_text(encoding="utf-8").strip()
            if (STATE / "current_result").exists() else "",
        "last_action": state.last_action,
        "failure_streak": state.failures,
        "last_error": state.last_error,
    }
def _find_process(fragment: str) -> int | None:
    result = subprocess.run(
        ["/usr/bin/pgrep", "-f", fragment],
        text=True, capture_output=True, check=False,
    )  # nosec B603
    for line in result.stdout.splitlines():
        try:
            candidate = int(line.strip())
        except ValueError:
            continue
        if candidate != os.getpid():
            return candidate
    return None

def _start_loop() -> None:
    subprocess.Popen(  # nosec B603
        ["/usr/bin/env", "bash", str(LOOP_SCRIPT)],
        cwd=ROOT,
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def _start_hybrid() -> None:
    subprocess.Popen(  # nosec B603
        ["/usr/bin/python3", str(HYBRID_SCRIPT)],
        cwd=ROOT,
        start_new_session=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

def run() -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    lock_handle = LOCK.open("a+", encoding="utf-8")
    try:
        fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock_handle.close()
        return 30

    os.environ["MEDIAHUB_ROOT"] = str(ROOT)
    pid = os.getpid()
    PIDFILE.write_text(f"{pid}:{_proc_starttime(pid)}\n", encoding="utf-8")
    state = AstraState()

    def stop(_signum: int, _frame: object) -> None:
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    try:
        while not STOPFILE.exists():
            loop_pid = _owned_pid(LOOP_PIDFILE, "autonomous_os_loop.sh") or _find_process("ops/autonomous_os_loop.sh")
            hybrid_pid = _owned_pid(CONTROLLER_PIDFILE, "hybrid_orchestrator.py") or _find_process("ops/hybrid_orchestrator.py")

            if loop_pid is None:
                state.last_action = "RECONCILE_LOOP_START"
                _start_loop()
                loop_pid = None
            elif hybrid_pid is None:
                state.last_action = "RECONCILE_HYBRID_START"
                _start_hybrid()
                hybrid_pid = None
            else:
                state.last_action = "OBSERVE"

            state.failures = 0
            state.last_error = ""
            _write_json(HEARTBEAT, _snapshot(loop_pid, hybrid_pid, state))
            time.sleep(INTERVAL)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        state.failures += 1
        state.last_error = f"{type(exc).__name__}: {exc}"
        payload = _snapshot(None, None, state)
        payload["state"] = "BLOCKED"
        _write_json(HEARTBEAT, payload)
        return 70
    finally:
        try:
            PIDFILE.unlink()
        except FileNotFoundError:
            pass
        lock_handle.close()
    return 0

if __name__ == "__main__":
    raise SystemExit(run())
