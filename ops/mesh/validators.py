from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Any

from .heartbeat_auth import verify_heartbeat

HEX64 = re.compile(r"^[0-9a-fA-F]{64}$")

@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    reason: str = ""

def _result(ok: bool, reason: str = "") -> ValidationResult:
    return ValidationResult(ok, reason)

def validate_node(record: dict[str, Any]) -> ValidationResult:
    required = {"schema_version","node_id","role","status","capabilities","executors","artifact_transports","resources","last_heartbeat"}
    if not isinstance(record, dict) or not required.issubset(record):
        return _result(False, "missing required node fields")
    if record["schema_version"] != "mediahub.mesh.node.v1":
        return _result(False, "unsupported node schema")
    if record["status"] not in {"DISCOVERED","ACTIVE","STALE","BLOCKED","QUARANTINED","RETIRED"}:
        return _result(False, "invalid node status")
    resources = record["resources"]
    if not isinstance(resources, dict) or resources.get("ram_gib", 0) <= 0 or resources.get("disk_free_gib", -1) < 0:
        return _result(False, "invalid resource profile")
    return _result(True)

def validate_capability(record: dict[str, Any]) -> ValidationResult:
    required = {"schema_version","capability_id","provider","version","executable","identity_sha256","authority","qualification_state"}
    if not isinstance(record, dict) or not required.issubset(record):
        return _result(False, "missing required capability fields")
    if record["schema_version"] != "mediahub.mesh.capability.v1":
        return _result(False, "unsupported capability schema")
    if not HEX64.fullmatch(str(record["identity_sha256"])):
        return _result(False, "invalid executable identity")
    if record["authority"] not in {"NONE","CONTROL","EXECUTION"}:
        return _result(False, "invalid authority")
    return _result(True)

def validate_heartbeat(
    record: dict[str, Any],
    now: datetime,
    max_age_seconds: int = 120,
    *,
    hmac_key: str | None = None,
    expected_node_id: str | None = None,
    last_sequence: int | None = None,
) -> ValidationResult:
    required = {"schema_version","node_id","issued_at","sequence","runtime_state","capability_digest","resource_summary","auth_schema_version","signature"}
    if not isinstance(record, dict) or not required.issubset(record):
        return _result(False, "missing required heartbeat fields")
    if record["schema_version"] != "mediahub.mesh.heartbeat.v1":
        return _result(False, "unsupported heartbeat schema")
    if not HEX64.fullmatch(str(record["capability_digest"])):
        return _result(False, "invalid capability digest")
    key = hmac_key if hmac_key is not None else __import__("os").environ.get("ASTRA_COMMAND_HMAC_KEY", "")
    expected = expected_node_id if expected_node_id is not None else ""
    valid, reason = verify_heartbeat(record, key, expected, now, max_age_seconds, last_sequence)
    if not valid:
        return _result(False, reason)
    return _result(True)

def validate_node_profile(record: dict[str, Any]) -> ValidationResult:
    required = {"schema_version","node_id","role","resources","capabilities","executors","artifact_transports","inventory_source"}
    if not isinstance(record, dict) or not required.issubset(record):
        return _result(False, "missing required node profile fields")
    if record["schema_version"] != "mediahub.mesh.node-profile.v1":
        return _result(False, "unsupported node profile schema")
    if not isinstance(record["node_id"], str) or not record["node_id"]:
        return _result(False, "invalid node identity")
    resources = record["resources"]
    if not isinstance(resources, dict) or resources.get("ram_gib", 0) <= 0:
        return _result(False, "invalid node resources")
    source = record["inventory_source"]
    if not isinstance(source, dict) or source.get("schema_version") != "mediahub.local-component-inventory.v1":
        return _result(False, "invalid inventory source")
    return _result(True)
