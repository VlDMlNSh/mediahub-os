#!/usr/bin/env python3
"""Bounded Astra GOLD qualification executor.

Runs only deterministic, repository-local qualification checks. It never
creates/cancels GitHub Actions runs, launches workers, reads secrets, or
promotes evidence to PASS without live evidence.
"""
from __future__ import annotations

import json
import os
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / "evidence"
REQUIRED = (
    "transport-health.json",
    "runtime-e2e.json",
    "scheduler-e2e.json",
    "fencing.json",
    "recovery.json",
    "backup-restore.json",
    "provider-model.json",
)


def run(argv: list[str], timeout: int = 300) -> dict:
    p = subprocess.run(argv, cwd=ROOT, text=True, capture_output=True, timeout=timeout, check=False)
    return {
        "command": " ".join(argv),
        "returncode": p.returncode,
        "stdout": p.stdout[-12000:],
        "stderr": p.stderr[-8000:],
    }


def main() -> int:
    started = time.time()
    checks = []
    checks.append(run(["python3", "-m", "compileall", "-q", "runtime", "tests", "astra_github_agent.py"]))
    checks.append(run(["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], 600))
    bundle = run(["python3", "ops/qualification/verify_pre_soak_bundle.py", "evidence"])
    checks.append(bundle)

    evidence = {}
    for name in REQUIRED:
        path = EVIDENCE / name
        if not path.is_file():
            evidence[name] = "MISSING"
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            evidence[name] = data.get("status", "INVALID_STATUS")
        except Exception:
            evidence[name] = "INVALID_JSON"

    git = run(["git", "status", "--short"])
    head = run(["git", "rev-parse", "HEAD"])
    blocked_reasons = []
    if any(c["returncode"] != 0 for c in checks):
        blocked_reasons.append("qualification_check_failed")
    if any(v != "PASS" for v in evidence.values()):
        blocked_reasons.append("fresh_pre_soak_bundle_not_all_PASS")
    if git["returncode"] != 0 or git["stdout"].strip():
        blocked_reasons.append("worktree_not_clean")

    result = {
        "schema": "mediahub.astra-gold-qualification.v1",
        "status": "PASS" if not blocked_reasons else "BLOCKED",
        "executor": "test-astra",
        "head": head["stdout"].strip(),
        "checks": checks,
        "pre_soak_evidence_status": evidence,
        "blocked_reasons": blocked_reasons,
        "secret_values": "SUPPRESSED",
        "elapsed_seconds": round(time.time() - started, 3),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
