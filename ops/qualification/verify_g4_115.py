#!/usr/bin/env python3
"""Independent, fail-closed verifier for the canonical G4 115-round contract."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "control" / "qualification" / "g4-115.json"

EXPECTED_IDENTITY = {
    "CODEX_FCC": ("codex", "fcc"),
    "CLAUDE_FCC": ("claude", "fcc"),
    "CODEX_OMNIROUTE": ("codex", "omniroute"),
    "CLAUDE_OMNIROUTE": ("claude", "omniroute"),
    "CLAUDE_CODE_DIRECT": ("claude_code", "native"),
}


def digest(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def verify(evidence: dict, contract: dict, expected_sha: str | None = None) -> dict:
    blocked: list[str] = []
    if evidence.get("schema") != "mediahub.astra-gold.g4-115-evidence.v1":
        blocked.append("invalid_evidence_schema")
    if evidence.get("status") != "PASS":
        blocked.append("evidence_status_not_PASS")
    source_sha = evidence.get("source_sha")
    if source_sha != (expected_sha or source_sha):
        blocked.append("source_sha_missing_or_mismatch")

    paths = contract["mandatory_paths"]
    rounds = evidence.get("rounds")
    if not isinstance(rounds, list):
        blocked.append("rounds_missing")
        rounds = []

    if len(rounds) != contract["total_rounds"]:
        blocked.append(f"round_count={len(rounds)}_expected={contract['total_rounds']}")

    seen_commands: set[str] = set()
    seen_pairs: set[tuple[str, int]] = set()
    counts = {path: 0 for path in paths}
    for index, item in enumerate(rounds, 1):
        if not isinstance(item, dict):
            blocked.append(f"round_{index}_not_object")
            continue
        missing = [key for key in contract["required_round_fields"] if key not in item]
        if missing:
            blocked.append(f"round_{index}_missing:{','.join(missing)}")
            continue

        path = item.get("path")
        round_no = item.get("round")
        if path not in counts:
            blocked.append(f"round_{index}_unknown_path")
        else:
            counts[path] += 1
            expected_executor, expected_transport = EXPECTED_IDENTITY[path]
            if item.get("executor_identity") != expected_executor:
                blocked.append(f"round_{index}_executor_identity_mismatch")
            if item.get("provider_or_transport_identity") != expected_transport:
                blocked.append(f"round_{index}_transport_identity_mismatch")

        if not isinstance(round_no, int) or not 1 <= round_no <= contract["rounds_per_path"]:
            blocked.append(f"round_{index}_number_invalid:{round_no}")
        command_id = item.get("command_id")
        if not isinstance(command_id, str) or not command_id:
            blocked.append(f"round_{index}_command_id_invalid")
        elif command_id in seen_commands:
            blocked.append(f"duplicate_command_id:{command_id}")
        seen_commands.add(command_id or f"__invalid_{index}")

        pair = (str(path), round_no if isinstance(round_no, int) else -1)
        if pair in seen_pairs:
            blocked.append(f"duplicate_path_round:{path}:{round_no}")
        seen_pairs.add(pair)

        if item.get("source_sha") != source_sha:
            blocked.append(f"round_{index}_source_sha_mismatch")
        if not isinstance(item.get("workspace"), str) or not item["workspace"]:
            blocked.append(f"round_{index}_workspace_missing")
        started = item.get("started_at")
        completed = item.get("completed_at")
        if not isinstance(started, (int, float)) or not isinstance(completed, (int, float)) or completed < started:
            blocked.append(f"round_{index}_timestamps_invalid")
        if item.get("exit_status") != 0:
            blocked.append(f"round_{index}_nonzero_exit")
        if item.get("timeout") is not False:
            blocked.append(f"round_{index}_timeout_not_false")
        if item.get("marker_present") is not True:
            blocked.append(f"round_{index}_marker_missing")
        if item.get("result_schema") != "g4-round-v1":
            blocked.append(f"round_{index}_result_schema_invalid")
        if item.get("verification_status") != "PASS":
            blocked.append(f"round_{index}_verification_not_PASS")

        item_digest = item.get("evidence_digest")
        if not isinstance(item_digest, str) or not item_digest.startswith("sha256:"):
            blocked.append(f"round_{index}_digest_invalid")
        else:
            unsigned = {k: v for k, v in item.items() if k != "evidence_digest"}
            if item_digest != digest(unsigned):
                blocked.append(f"round_{index}_digest_mismatch")

    for path, count in counts.items():
        if count != contract["rounds_per_path"]:
            blocked.append(f"{path}_round_count={count}_expected={contract['rounds_per_path']}")

    expected_digest = evidence.get("evidence_digest")
    if not isinstance(expected_digest, str) or not expected_digest.startswith("sha256:"):
        blocked.append("evidence_digest_invalid")
    else:
        unsigned_evidence = {k: v for k, v in evidence.items() if k != "evidence_digest"}
        if expected_digest != digest(unsigned_evidence):
            blocked.append("evidence_digest_mismatch")

    return {
        "schema": "mediahub.astra-gold.g4-115-verification.v1",
        "status": "PASS" if not blocked else "BLOCKED",
        "blocked_reasons": blocked,
        "rounds_verified": len(rounds),
        "path_counts": counts,
        "secret_values": "SUPPRESSED",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("--expected-sha")
    args = parser.parse_args()
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    result = verify(json.loads(args.evidence.read_text(encoding="utf-8")), contract, args.expected_sha)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
