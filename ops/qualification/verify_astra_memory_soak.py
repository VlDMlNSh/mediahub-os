#!/usr/bin/env python3
"""Verify Astra memory soak evidence without manufacturing runtime evidence."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

MIN_DURATION_SECONDS = 86_400
REQUIRED_CHECKS = (
    "session_continuation",
    "project_recall",
    "restart_recovery",
    "bounded_context",
)


def verify(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    reasons = []
    if data.get("schema") != "mediahub.astra-memory-soak.v1":
        reasons.append("invalid_schema")
    if data.get("status") != "PASS":
        reasons.append(f"status={data.get('status')!r}")
    if float(data.get("duration_seconds", 0)) < MIN_DURATION_SECONDS:
        reasons.append("duration_below_24h")
    checks = data.get("checks")
    if not isinstance(checks, dict):
        reasons.append("checks_missing")
    else:
        for name in REQUIRED_CHECKS:
            if checks.get(name) != "PASS":
                reasons.append(f"check_{name}={checks.get(name)!r}")
    if data.get("restart_count", 0) < 1:
        reasons.append("restart_not_observed")
    if not data.get("evidence_digest"):
        reasons.append("evidence_digest_missing")
    return {
        "status": "PASS" if not reasons else "BLOCKED",
        "blocked_reasons": reasons,
        "secret_values": "SUPPRESSED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    result = verify(args.evidence)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
