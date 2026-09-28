#!/usr/bin/env python3
"""Independent verifier for Codex/Cursor execution-backend evidence.

The verifier consumes evidence only. It never probes hosts, executes commands,
reads credentials, or promotes missing evidence to PASS.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REQUIRED_BACKENDS = ("codex", "cursor")
REQUIRED_CHECKS = ("node_identity", "binary_identity", "bounded_execution")


def verify(payload: dict, expected_revision: str | None = None) -> dict:
    blocked: list[str] = []
    if payload.get("schema") != "mediahub.execution-backends.v1":
        blocked.append("invalid_schema")
    if payload.get("status") != "PASS":
        blocked.append("evidence_status_not_PASS")
    if payload.get("node_id") != "mh-dev-01":
        blocked.append("node_identity_invalid")
    if expected_revision is not None and payload.get("repo_revision") != expected_revision:
        blocked.append("repo_revision_mismatch")
    if payload.get("command_id") is not None and payload.get("command_id") != "execution-backend-qualification-20260928T1014Z":
        blocked.append("command_id_mismatch")
    if payload.get("target_sha") and payload.get("execution_head") and payload.get("target_sha") != payload.get("execution_head"):
        blocked.append("execution_head_mismatch")
    backends = payload.get("backends")
    if not isinstance(backends, dict):
        blocked.append("backends_missing")
    else:
        for backend_id in REQUIRED_BACKENDS:
            item = backends.get(backend_id)
            if not isinstance(item, dict):
                blocked.append(f"{backend_id}_missing")
                continue
            if item.get("node_id") != "mh-dev-01":
                blocked.append(f"{backend_id}_node_identity_invalid")
            if item.get("verification_state") != "VERIFIED":
                blocked.append(f"{backend_id}_not_VERIFIED")
            checks = item.get("checks")
            if not isinstance(checks, dict):
                blocked.append(f"{backend_id}_checks_missing")
            else:
                for check in REQUIRED_CHECKS:
                    if checks.get(check) != "PASS":
                        blocked.append(f"{backend_id}_{check}_not_PASS")
            if item.get("output_sha256") and not str(item["output_sha256"]).startswith("sha256:"):
                blocked.append(f"{backend_id}_output_digest_invalid")
            if "secret_values" in item and item["secret_values"] != "SUPPRESSED":
                blocked.append(f"{backend_id}_secret_disclosure")
    digest = payload.get("evidence_digest")
    if not isinstance(digest, str) or not digest.startswith("sha256:"):
        blocked.append("evidence_digest_invalid")
    return {
        "schema": "mediahub.execution-backends-verification.v1",
        "status": "PASS" if not blocked else "BLOCKED",
        "blocked_reasons": blocked,
        "secret_values": "SUPPRESSED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--expected-revision")
    args = parser.parse_args()
    result = verify(json.loads(args.evidence.read_text(encoding="utf-8")), args.expected_revision)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
