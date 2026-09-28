#!/usr/bin/env python3
"""Independent unified contract gate for Astra memory qualification evidence.

This verifier validates only supplied evidence. It never executes runtime code and
never upgrades absent or incomplete evidence to PASS.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_CHECKS = (
    "security_gate",
    "scope_isolation",
    "supersession",
    "bounded_context",
    "advisory_only",
    "provenance",
    "raw_history_retained",
)


def verify(payload: dict) -> dict:
    blocked = []
    if payload.get("schema") != "mediahub.astra-memory-contract.v1":
        blocked.append("invalid_schema")
    if payload.get("status") != "PASS":
        blocked.append("contract_status_not_PASS")
    checks = payload.get("checks")
    if not isinstance(checks, dict):
        blocked.append("checks_missing")
    else:
        for name in REQUIRED_CHECKS:
            if checks.get(name) != "PASS":
                blocked.append(f"{name}_not_PASS")
    if payload.get("memory_authority") != "advisory_only":
        blocked.append("memory_authority_not_advisory")
    budget = payload.get("context_budget")
    if not isinstance(budget, dict):
        blocked.append("context_budget_missing")
    else:
        try:
            records = int(budget["max_records"])
            chars = int(budget["max_chars"])
        except (KeyError, TypeError, ValueError):
            blocked.append("context_budget_invalid")
        else:
            if not 1 <= records <= 12:
                blocked.append("max_records_out_of_bounds")
            if not 1 <= chars <= 12_000:
                blocked.append("max_chars_out_of_bounds")
    digest = payload.get("evidence_digest")
    if not isinstance(digest, str) or not digest.startswith("sha256:"):
        blocked.append("evidence_digest_invalid")
    return {
        "schema": "mediahub.astra-memory-contract-verification.v1",
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
