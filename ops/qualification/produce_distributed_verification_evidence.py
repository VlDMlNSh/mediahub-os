#!/usr/bin/env python3
"""Fail-closed aggregator for fresh three-node distributed verification evidence."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import platform
import re
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

CANONICAL_NODE = "mh-dev-01"
REQUIRED_NODES = (
    "mh-dev-01",
    "mh-dev-02",
    "Voktors-Mac-mini.local",
)
SCHEMA = "mediahub.astra.distributed-node-attestation.v1"
OUTPUT_SCHEMA = "mediahub.astra.distributed-verification.v1"
PHASE = "distributed_verification"
PRODUCER_IDENTITY = "canonical-distributed-verification-producer-v1"
AUTH_SCHEMA = "mediahub.astra.distributed.auth.v1"
SAFE_ID_RE = re.compile(r"^[A-Za-z0-9._:-]{1,128}$")
SHA_RE = re.compile(r"^[0-9a-fA-F]{40,64}$")


@dataclass(frozen=True)
class ContextResult:
    status: str
    blocked_reasons: tuple[str, ...]


def _valid_id(value: object) -> bool:
    return isinstance(value, str) and bool(SAFE_ID_RE.fullmatch(value))


def _valid_sha(value: object) -> bool:
    return isinstance(value, str) and bool(SHA_RE.fullmatch(value))


def current_head(root: Path) -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        text=True,
        capture_output=True,
        timeout=15,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError("unable_to_resolve_current_head")
    return completed.stdout.strip()


def validate_context(
    *,
    command_id: str,
    node_id: str,
    target_sha: str,
    current_head: str,
) -> ContextResult:
    blocked: list[str] = []
    if not _valid_id(command_id):
        blocked.append("missing_command_id" if not command_id else "invalid_command_id")
    if node_id != CANONICAL_NODE:
        blocked.append("canonical_node_mismatch")
    if not _valid_sha(target_sha):
        blocked.append("missing_target_sha" if not target_sha else "invalid_target_sha")
    if not _valid_sha(current_head):
        blocked.append("current_head_unavailable")
    elif _valid_sha(target_sha) and target_sha.lower() != current_head.lower():
        blocked.append("target_sha_mismatch")
    return ContextResult("PASS" if not blocked else "BLOCKED", tuple(blocked))


def _validate_attestation(
    path: Path,
    *,
    expected_node: str,
    command_id: str,
    target_sha: str,
    now: int,
    max_age_seconds: int,
    hmac_key: str,
) -> list[str]:
    blocked: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return [f"{expected_node}_invalid_json"]

    if data.get("schema") != SCHEMA:
        blocked.append(f"{expected_node}_schema_mismatch")
    if data.get("command_id") != command_id:
        blocked.append(f"{expected_node}_command_id_mismatch")
    if data.get("node_id") != expected_node:
        blocked.append(f"{expected_node}_node_id_mismatch")
    if data.get("target_sha") != target_sha:
        blocked.append(f"{expected_node}_target_sha_mismatch")
    if data.get("current_head") != target_sha:
        blocked.append(f"{expected_node}_current_head_mismatch")
    expected_identity = f"node-agent:{expected_node}"
    if not isinstance(data.get("producer_identity"), str) or not data.get("producer_identity"):
        blocked.append(f"{expected_node}_producer_identity_missing")
    elif data.get("producer_identity") != expected_identity:
        blocked.append(f"{expected_node}_producer_identity_mismatch")
    if data.get("phase") != PHASE:
        blocked.append(f"{expected_node}_phase_mismatch")
    if data.get("status") != "PASS":
        blocked.append(f"{expected_node}_not_PASS")
    if data.get("returncode") != 0:
        blocked.append(f"{expected_node}_returncode_not_zero")
    if data.get("auth_schema_version") != AUTH_SCHEMA:
        blocked.append(f"{expected_node}_auth_schema_mismatch")
    signature = data.get("signature")
    if not isinstance(signature, str) or not signature:
        blocked.append(f"{expected_node}_signature_missing")
    elif not hmac_key:
        blocked.append(f"{expected_node}_hmac_key_missing")
    else:
        body = json.dumps(
            {k: v for k, v in data.items() if k != "signature"},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        expected_signature = hmac.new(
            hmac_key.encode("utf-8"), body, hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_signature):
            blocked.append(f"{expected_node}_signature_invalid")

    completed_at = data.get("completed_at")
    if not isinstance(completed_at, int) or isinstance(completed_at, bool):
        blocked.append(f"{expected_node}_completed_at_invalid")
    else:
        age = now - completed_at
        if age > max_age_seconds:
            blocked.append(f"{expected_node}_stale")
        if age < -30:
            blocked.append(f"{expected_node}_future_timestamp")

    observations = data.get("observations")
    if not isinstance(observations, dict) or not observations:
        blocked.append(f"{expected_node}_observations_missing")
    elif any(value is not True for value in observations.values()):
        blocked.append(f"{expected_node}_observations_not_PASS")
    return blocked


def aggregate(
    evidence_dir: Path,
    *,
    command_id: str,
    node_id: str,
    target_sha: str,
    current_head: str,
    now: int | None = None,
    max_age_seconds: int = 900,
    hmac_key: str = "",
) -> dict[str, Any]:
    now = int(time.time()) if now is None else int(now)
    context = validate_context(
        command_id=command_id,
        node_id=node_id,
        target_sha=target_sha,
        current_head=current_head,
    )
    blocked = list(context.blocked_reasons)

    checked: list[str] = []
    for expected_node in REQUIRED_NODES:
        checked.append(expected_node)
        path = evidence_dir / f"{expected_node}.json"
        if not path.is_file():
            blocked.append(f"{expected_node}_missing")
            continue
        blocked.extend(
            _validate_attestation(
                path,
                expected_node=expected_node,
                command_id=command_id,
                target_sha=target_sha,
                now=now,
                max_age_seconds=max_age_seconds,
                hmac_key=hmac_key,
            )
        )

    status = "PASS" if not blocked else "BLOCKED"
    return {
        "schema": OUTPUT_SCHEMA,
        "status": status,
        "phase": PHASE,
        "returncode": 0 if status == "PASS" else 2,
        "command_id": command_id,
        "node_id": node_id,
        "target_sha": target_sha,
        "producer_identity": PRODUCER_IDENTITY,
        "captured_at": now,
        "checked_nodes": tuple(checked),
        "blocked_reasons": sorted(set(blocked)),
        "secret_values": "SUPPRESSED",
    }


def main() -> int:
    root = Path(os.environ.get("ASTRA_WORKTREE", Path(__file__).resolve().parents[2]))
    command_id = os.environ.get("ASTRA_COMMAND_ID", "")
    node_id = os.environ.get("ASTRA_NODE_ID", platform.node())
    target_sha = os.environ.get("ASTRA_TARGET_SHA", "")
    evidence_dir = Path(
        os.environ.get(
            "ASTRA_DISTRIBUTED_EVIDENCE_DIR",
            str(root / ".astra-state" / "distributed-verification" / command_id),
        )
    )
    output_path = Path(
        os.environ.get(
            "ASTRA_DISTRIBUTED_VERIFICATION_OUTPUT",
            str(root / ".astra-state" / "distributed-verification-result.json"),
        )
    )
    try:
        head = current_head(root)
        context = validate_context(
            command_id=command_id,
            node_id=node_id,
            target_sha=target_sha,
            current_head=head,
        )
        if context.status != "PASS":
            result = {
                "schema": OUTPUT_SCHEMA,
                "status": "BLOCKED",
                "phase": PHASE,
                "returncode": 2,
                "command_id": command_id,
                "node_id": node_id,
                "target_sha": target_sha,
                "producer_identity": PRODUCER_IDENTITY,
                "captured_at": int(time.time()),
                "checked_nodes": REQUIRED_NODES,
                "blocked_reasons": sorted(context.blocked_reasons),
                "secret_values": "SUPPRESSED",
            }
        else:
            result = aggregate(
                evidence_dir,
                command_id=command_id,
                node_id=node_id,
                target_sha=target_sha,
                current_head=head,
                max_age_seconds=max(60, int(os.environ.get("ASTRA_DISTRIBUTED_MAX_AGE_SECONDS", "900"))),
                hmac_key=os.environ.get("ASTRA_COMMAND_HMAC_KEY", ""),
            )
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(result, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(json.dumps(result, indent=2, sort_keys=True))
        return int(result["returncode"])
    except Exception as exc:
        result = {
            "schema": OUTPUT_SCHEMA,
            "status": "BLOCKED",
            "phase": PHASE,
            "returncode": 2,
            "command_id": command_id,
            "node_id": node_id,
            "target_sha": target_sha,
            "producer_identity": PRODUCER_IDENTITY,
            "captured_at": int(time.time()),
            "checked_nodes": REQUIRED_NODES,
            "blocked_reasons": [f"producer_exception:{type(exc).__name__}"],
            "secret_values": "SUPPRESSED",
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
