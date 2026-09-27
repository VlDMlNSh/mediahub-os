#!/usr/bin/env python3
"""Bounded FCM model discovery for the resident Astra supervisor.

The reconciler may refresh the FCM router's configured set, but it never reads,
prints, persists, or transports provider credentials. Credentials are supplied
only through FCM's normal environment/config mechanisms.
"""
from __future__ import annotations
import json, os, subprocess, time
from pathlib import Path

ROOT = Path(os.environ.get("MEDIAHUB_ROOT", "/home/mediahub/dev/mediahub-os-autonomous")).resolve()
STATE = ROOT / ".autonomous"
PIDFILE = STATE / "fcm_model_reconciler.pid"
STATUS = STATE / "fcm_model_reconciler.json"
INTERVAL = max(300, int(os.environ.get("MEDIAHUB_FCM_DISCOVERY_INTERVAL", "900")))
SET_NAME = os.environ.get("MEDIAHUB_FCM_SET", "fast-coding")


def _identity(pid: int) -> str:
    try:
        return Path(f"/proc/{pid}/stat").read_text().split()[21]
    except (OSError, IndexError):
        return ""


def _write(data: dict) -> None:
    tmp = STATUS.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, STATUS)


def reconcile() -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    pid = os.getpid()
    PIDFILE.write_text(f"{pid}:{_identity(pid)}\n", encoding="utf-8")
    try:
        while True:
            started = time.time()
            env = os.environ.copy()
            env["FREE_CODING_MODELS_TELEMETRY"] = "0"
            cmd = ["/home/mediahub/.nvm/versions/node/v22.23.2/bin/free-coding-models", "--sync-set", SET_NAME, "--json", "--no-telemetry"]
            proc = subprocess.run(cmd, cwd=ROOT, env=env, text=True, capture_output=True, timeout=120, check=False)  # nosec B603
            # Only retain aggregate status; stdout may contain provider metadata.
            _write({
                "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "set": SET_NAME,
                "returncode": proc.returncode,
                "duration_ms": int((time.time()-started)*1000),
                "credential_source": "fcm-native-env-or-config",
                "credentials_emitted": False,
            })
            time.sleep(INTERVAL)
    finally:
        try: PIDFILE.unlink()
        except FileNotFoundError: pass
    return 0

if __name__ == "__main__":
    raise SystemExit(reconcile())
