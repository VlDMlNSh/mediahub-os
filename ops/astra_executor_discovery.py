#!/usr/bin/env python3
"""Bounded, fail-closed executor capability discovery for Astra.
Never reads or emits secret values and never executes repository/user input.
"""
from __future__ import annotations
import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(os.environ.get("MEDIAHUB_ROOT", "/home/mediahub/dev/mediahub-os-autonomous")).resolve()
STATE = ROOT / ".autonomous"
STATUS = STATE / "executor_capabilities.json"
TIMEOUT = 8
@dataclass(frozen=True)
class ExecutorSpec:
    name: str
    command: str
    capabilities: tuple[str, ...]
    secret_requirements: tuple[str, ...]
    version_args: tuple[str, ...]

SPECS = (
    ExecutorSpec("aider", "aider", ("code_generation", "refactoring", "bug_analysis"), ("ANTHROPIC_API_KEY", "OPENROUTER_API_KEY"), ("--version",)),
    ExecutorSpec("goose", "goose", ("code_generation", "refactoring", "bug_analysis", "test_design"), ("OPENROUTER_API_KEY",), ("--version",)),
    ExecutorSpec("openhands", "openhands", ("code_generation", "refactoring", "architecture"), ("OPENAI_API_KEY", "OPENROUTER_API_KEY"), ("--version",)),
    ExecutorSpec("qodo", "qodo", ("code_review", "test_design", "bug_analysis"), ("GEMINI_API_KEY",), ("--version",)),
    ExecutorSpec("pr-agent", "pr-agent", ("code_review", "bug_analysis"), ("GEMINI_API_KEY",), ("--version",)),
    ExecutorSpec("pullfrog", "pullfrog", ("code_generation", "bug_analysis"), ("OPENROUTER_API_KEY",), ("--version",)),
    ExecutorSpec("sweep", "sweep", ("code_generation", "refactoring"), ("OPENAI_API_KEY",), ("--version",)),
    ExecutorSpec("tabby", "tabby", ("code_generation", "indexing"), ("TABBY_API_KEY",), ("--version",)),
)

def _probe(spec: ExecutorSpec) -> dict:
    path = shutil.which(spec.command)
    if not path:
        for candidate in (Path("/home/mediahub/.local/bin") / spec.command,
                          Path("/usr/local/bin") / spec.command,
                          Path("/usr/bin") / spec.command):
            if candidate.is_file() and os.access(candidate, os.X_OK):
                path = str(candidate)
                break
    env_state = {key: ("PRESENT" if os.environ.get(key) else "ABSENT")
                 for key in spec.secret_requirements}
    if not path:
        return {"name": spec.name, "command": spec.command, "status": "UNINSTALLED",
                "qualification": "UNQUALIFIED", "path": None,
                "capabilities": list(spec.capabilities), "secret_requirements": env_state}
    try:
        proc = subprocess.run([path, *spec.version_args], cwd=ROOT, text=True,
                              capture_output=True, timeout=TIMEOUT, check=False)
        version = (proc.stdout or proc.stderr).strip().splitlines()
        version_line = version[0][:160] if version else ""
        healthy = proc.returncode == 0
    except (OSError, subprocess.SubprocessError):
        version_line = ""
        healthy = False
    return {"name": spec.name, "command": spec.command, "status": "HEALTHY" if healthy else "DEGRADED",
            "qualification": "QUALIFIED" if healthy else "UNQUALIFIED", "path": path,
            "version": version_line, "capabilities": list(spec.capabilities),
            "secret_requirements": env_state}
def discover() -> dict:
    STATE.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    executors = [_probe(spec) for spec in SPECS]
    payload = {
        "schema_version": 1,
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "host": os.uname().nodename,
        "policy": "fail-closed-no-secret-values-no-arbitrary-commands",
        "executors": executors,
        "duration_ms": int((time.monotonic() - started) * 1000),
    }
    tmp = STATUS.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, STATUS)
    return payload

def run() -> int:
    pidfile = STATE / "astra_executor_discovery.pid"
    pidfile.write_text(f"{os.getpid()}\n", encoding="utf-8")
    try:
        while True:
            discover()
            time.sleep(max(300, int(os.environ.get("MEDIAHUB_EXECUTOR_DISCOVERY_INTERVAL", "900"))))
    finally:
        try:
            pidfile.unlink()
        except FileNotFoundError:
            pass
    return 0

if __name__ == "__main__":
    raise SystemExit(run())
