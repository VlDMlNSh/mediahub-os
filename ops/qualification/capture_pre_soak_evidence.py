#!/usr/bin/env python3
"""Capture fresh pre-soak evidence on the canonical Astra node.

This producer never fabricates PASS. Each artifact records the exact current
revision, capture time, and a bounded observable check or an explicit blocker.
Secrets are never read or emitted.
"""
from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence"
AGENT = ROOT / "astra_github_agent.py"
NODE = platform.node()
NOW = int(time.time())


def run(argv: list[str], timeout: int = 90) -> tuple[int, str, str]:
    p = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True,
                       timeout=timeout, check=False)
    return p.returncode, p.stdout[-4000:], p.stderr[-4000:]


def write(name: str, status: str, check: str, reason: str = "", **extra: object) -> None:
    payload = {
        "schema": "mediahub.pre-soak-evidence.v1",
        "status": status,
        "captured_at": NOW,
        "target_sha": run(["git", "rev-parse", "HEAD"], 10)[1].strip(),
        "node_id": NODE,
        "check": check,
        "reason": reason,
        "secret_values": "SUPPRESSED",
        **extra,
    }
    (EVIDENCE / name).write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8")


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    blocked = False

    # Transport identity is directly observable on the canonical worker.
    agent_sha = hashlib.sha256(AGENT.read_bytes()).hexdigest()
    workers = subprocess.run(["pgrep", "-af", "astra_github_agent.py"],
                             cwd=ROOT, text=True, capture_output=True, check=False)
    if NODE == "mh-dev-01" and workers.returncode == 0 and agent_sha:
        write("transport-health.json", "PASS", "canonical_worker_identity",
              agent_source_sha=agent_sha, worker_present=True)
    else:
        blocked = True
        write("transport-health.json", "BLOCKED", "canonical_worker_identity",
              "canonical mh-dev-01 worker identity could not be independently observed",
              agent_source_sha=agent_sha, worker_present=workers.returncode == 0)

    # Runtime E2E: use the installed local model only; no network or secrets.
    ollama = shutil.which("ollama")
    if not ollama:
        blocked = True
        write("runtime-e2e.json", "BLOCKED", "ollama_live_smoke",
              "ollama executable is not available on the canonical node")
    else:
        rc, out, err = run([ollama, "run", "qwen2.5-coder:3b",
                            "Return exactly MEDIAHUB_OLLAMA_LIVE_OK and nothing else."], 90)
        if rc == 0 and "MEDIAHUB_OLLAMA_LIVE_OK" in out:
            write("runtime-e2e.json", "PASS", "ollama_live_smoke",
                  model="qwen2.5-coder:3b", marker_present=True)
        else:
            blocked = True
            write("runtime-e2e.json", "BLOCKED", "ollama_live_smoke",
                  "bounded live marker was not observed", returncode=rc,
                  marker_present="MEDIAHUB_OLLAMA_LIVE_OK" in out)

    # These gates require dedicated live producers; a generic unit test is not
    # promoted to runtime evidence.
    for name, check, reason in (
        ("scheduler-e2e.json", "scheduler_live_e2e",
         "no dedicated live scheduler evidence producer is implemented"),
        ("fencing.json", "multi_node_fencing",
         "no dedicated live fencing evidence producer is implemented"),
        ("recovery.json", "runtime_recovery",
         "no dedicated live recovery evidence producer is implemented"),
        ("backup-restore.json", "backup_restore",
         "no dedicated live backup/restore evidence producer is implemented"),
        ("provider-model.json", "cloud_provider_live_qualification",
         "fresh provider evidence must come from the live provider qualification path; stale repository evidence is not promoted"),
    ):
        blocked = True
        write(name, "BLOCKED", check, reason)

    return 2 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
