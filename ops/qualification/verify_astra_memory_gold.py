#!/usr/bin/env python3
"""Independent Astra memory GOLD verifier.

This gate consumes independently captured memory-soak evidence and verifies
the minimum continuity/scope guarantees. It never upgrades missing evidence.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED = (
    "session_continuation",
    "project_recall",
    "restart_recovery",
    "bounded_context",
)
MAX_RECORDS = 12
MAX_CHARS = 12_000


def verify(payload: dict) -> dict:
    blocked = []
    if payload.get("schema") != "mediahub.astra-memory-soak.v1":
        blocked.append("invalid_schema")
    if payload.get("status") != "PASS":
        blocked.append("soak_status_not_PASS")
    if int(payload.get("duration_seconds", 0)) < 86_400:
        blocked.append("soak_duration_below_24h")
    checks = payload.get("checks")
    if not isinstance(checks, dict):
        blocked.append("checks_missing")
    else:
        for name in REQUIRED:
            if checks.get(name) != "PASS":
                blocked.append(f"{name}_not_PASS")
    if int(payload.get("restart_count", 0)) < 1:
        blocked.append("restart_not_observed")
    digest = payload.get("evidence_digest")
    if not isinstance(digest, str) or not digest.startswith("sha256:"):
        blocked.append("evidence_digest_invalid")
    budget = payload.get("context_budget")
    if not isinstance(budget, dict):
        blocked.append("context_budget_missing")
    else:
        if int(budget.get("max_records", 0)) <= 0 or int(budget.get("max_records", 0)) > MAX_RECORDS:
            blocked.append("max_records_out_of_bounds")
        if int(budget.get("max_chars", 0)) <= 0 or int(budget.get("max_chars", 0)) > MAX_CHARS:
            blocked.append("max_chars_out_of_bounds")
    if payload.get("memory_authority") != "advisory_only":
        blocked.append("memory_authority_not_advisory")
    return {
        "schema": "mediahub.astra-memory-gold-verification.v1",
        "status": "PASS" if not blocked else "BLOCKED",
        "blocked_reasons": blocked,
        "secret_values": "SUPPRESSED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    args = parser.parse_args()
    result = verify(json.loads(args.evidence.read_text(encoding="utf-8")))
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
