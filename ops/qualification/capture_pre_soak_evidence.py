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
EVIDENCE = Path(__import__("os").environ.get("ASTRA_EVIDENCE_DIR", str(ROOT / "evidence")))
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
    workers = subprocess.run(["pgrep", "-af", "[a]stra_github_agent.py"],
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

    # Provider/model evidence is produced by the live qualification engine.
    provider_script = ROOT / "ops" / "qualification" / "qualify_execution_backends.py"
    provider = subprocess.run([str(Path(__import__("sys").executable)), str(provider_script)],
                              cwd=ROOT, text=True, capture_output=True, timeout=120, check=False)
    provider_payload = {}
    try:
        provider_payload = json.loads(provider.stdout.strip().splitlines()[-1])
    except Exception:
        provider_payload = {"status": "BLOCKED", "reason": "invalid_provider_qualification_output"}
    provider_status = "PASS" if provider.returncode == 0 and provider_payload.get("status") == "PASS" else "BLOCKED"
    if provider_status != "PASS":
        blocked = True
    write("provider-model.json", provider_status, "cloud_provider_live_qualification",
          "" if provider_status == "PASS" else "no qualified provider/model was observed",
          qualification=provider_payload)

    # Remaining gates intentionally remain fail-closed until their dedicated
    # live producers exist. They are not inferred from unit tests.
    for name, check, reason in (
        ("scheduler-e2e.json", "scheduler_live_e2e",
         "no dedicated live scheduler evidence producer is implemented"),
        ("fencing.json", "multi_node_fencing",
         "no dedicated live fencing evidence producer is implemented"),
        ("recovery.json", "runtime_recovery",
         "no dedicated live recovery evidence producer is implemented"),
        ("backup-restore.json", "backup_restore",
         "no dedicated live backup/restore evidence producer is implemented"),
    ):
        blocked = True
        write(name, "BLOCKED", check, reason)

    return 2 if blocked else 0


if __name__ == "__main__":
    raise SystemExit(main())
