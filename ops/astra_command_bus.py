#!/usr/bin/env python3
"""GitHub-backed command bus for the resident Astra Coordinator.

The bus is intentionally narrow: GitHub issues labelled 'astra-command' are
the human/ChatGPT command ingress. Only a fixed command grammar is accepted.
Issue text is never executed as shell input.
"""
from __future__ import annotations

import json
import re
import subprocess
import time
from pathlib import Path

ROOT = Path("/home/mediahub/dev/mediahub-os-autonomous")
STATE = ROOT / ".autonomous"
GH = "/home/mediahub/.local/gh-bootstrap/root/usr/bin/gh"
REPO = "VlDMlNSh/mediahub-os"
LABEL = "astra-command"
POLL_SECONDS = 30
COMMAND_RE = re.compile(r"^\[ASTRA\]\s+(CONTINUE|STATUS|STOP|RESUME)$", re.IGNORECASE)


def _gh(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([GH, *args], cwd=ROOT, text=True,
                          capture_output=True, check=False)  # nosec B603


def _issues() -> list[dict]:
    result = _gh("api", "--method", "GET",
                 f"repos/{REPO}/issues?state=open&labels={LABEL}&per_page=50")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "github query failed")
    return json.loads(result.stdout or "[]")


def _parse(issue: dict) -> str | None:
    match = COMMAND_RE.fullmatch(str(issue.get("title", "")).strip())
    return match.group(1).upper() if match else None


def _state_snapshot() -> str:
    heartbeat = STATE / "astra_heartbeat.json"
    if not heartbeat.exists():
        return "ASTRA_STATUS: heartbeat unavailable"
    try:
        data = json.loads(heartbeat.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "ASTRA_STATUS: heartbeat malformed"
    return (
        "ASTRA_STATUS: "
        f"state={data.get('state')} action={data.get('last_action')} "
        f"head={data.get('head')} loop_pid={data.get('loop_pid')} "
        f"controller_pid={data.get('hybrid_controller_pid')} "
        f"failure_streak={data.get('failure_streak')}"
    )


def _comment(issue: int, body: str) -> None:
    result = _gh("issue", "comment", str(issue), "--repo", REPO, "--body", body)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "github comment failed")


def _close(issue: int) -> None:
    result = _gh("issue", "close", str(issue), "--repo", REPO)
    if result.returncode:
        raise RuntimeError(result.stderr.strip() or "github close failed")


def process_once() -> int:
    count = 0
    for issue in _issues():
        command = _parse(issue)
        if command is None:
            continue
        number = int(issue["number"])
        if command == "STOP":
            (STATE / "STOP").touch()
            reply = "ASTRA ACK: STOP accepted; autonomous execution remains fail-closed."
        elif command == "RESUME":
            (STATE / "STOP").unlink(missing_ok=True)
            reply = "ASTRA ACK: RESUME accepted; coordinator may reconcile the existing queue."
        elif command == "STATUS":
            reply = _state_snapshot()
        else:
            (STATE / "STOP").unlink(missing_ok=True)
            (STATE / "command.request").write_text(
                json.dumps({"command": "CONTINUE", "issue": number, "ts": time.time()}) + "\n",
                encoding="utf-8",
            )
            reply = "ASTRA ACK: CONTINUE accepted; only repository-qualified bounded work may execute."
        _comment(number, reply)
        _close(number)
        count += 1
    return count


def run_forever() -> int:
    STATE.mkdir(parents=True, exist_ok=True)
    while True:
        try:
            processed = process_once()
            (STATE / "command_bus.json").write_text(
                json.dumps({"state": "RUNNING", "processed": processed,
                            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
                           indent=2) + "\n", encoding="utf-8")
        except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
            (STATE / "command_bus.json").write_text(
                json.dumps({"state": "DEGRADED", "error": f"{type(exc).__name__}: {exc}",
                            "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())},
                           indent=2) + "\n", encoding="utf-8")
        time.sleep(POLL_SECONDS)
    return 0


if __name__ == "__main__":
    raise SystemExit(run_forever())
