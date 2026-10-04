from __future__ import annotations

import hashlib
import hmac
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

AUTH_SCHEMA_VERSION = "mediahub.mesh.heartbeat.auth.v1"
MAX_FUTURE_SKEW_SECONDS = 30
DEFAULT_MAX_AGE_SECONDS = 120


def canonical_heartbeat_body(record: dict[str, Any]) -> bytes:
    return json.dumps(
        {k: v for k, v in record.items() if k != "signature"},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sign_heartbeat(record: dict[str, Any], key: str) -> dict[str, Any]:
    if not key:
        raise ValueError("ASTRA_COMMAND_HMAC_KEY is required")
    signed = dict(record)
    signed["auth_schema_version"] = AUTH_SCHEMA_VERSION
    signed.pop("signature", None)
    signed["signature"] = hmac.new(
        key.encode("utf-8"), canonical_heartbeat_body(signed), hashlib.sha256
    ).hexdigest()
    return signed


def verify_heartbeat(
    record: dict[str, Any],
    key: str,
    expected_node_id: str,
    now: datetime,
    max_age_seconds: int = DEFAULT_MAX_AGE_SECONDS,
    last_sequence: int | None = None,
) -> tuple[bool, str]:
    if not key:
        return False, "heartbeat authentication key is unavailable"
    if not expected_node_id:
        return False, "expected node identity is required"
    if not isinstance(record, dict):
        return False, "heartbeat must be an object"
    if record.get("auth_schema_version") != AUTH_SCHEMA_VERSION:
        return False, "unsupported heartbeat auth schema"
    if record.get("node_id") != expected_node_id:
        return False, "heartbeat node binding mismatch"
    signature = record.get("signature")
    if not isinstance(signature, str) or not signature:
        return False, "heartbeat signature missing"
    try:
        issued = datetime.fromisoformat(str(record["issued_at"]).replace("Z", "+00:00"))
        if issued.tzinfo is None:
            issued = issued.replace(tzinfo=timezone.utc)
    except (KeyError, TypeError, ValueError):
        return False, "invalid heartbeat timestamp"
    age = (now.astimezone(timezone.utc) - issued.astimezone(timezone.utc)).total_seconds()
    if age < -MAX_FUTURE_SKEW_SECONDS:
        return False, "heartbeat timestamp is from the future"
    if age > max_age_seconds:
        return False, "heartbeat is stale"
    sequence = record.get("sequence")
    if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
        return False, "invalid heartbeat sequence"
    if last_sequence is not None and sequence <= last_sequence:
        return False, "heartbeat sequence replay or regression"
    expected = hmac.new(
        key.encode("utf-8"), canonical_heartbeat_body(record), hashlib.sha256
    ).hexdigest()
    if not hmac.compare_digest(signature, expected):
        return False, "invalid heartbeat signature"
    return True, ""
