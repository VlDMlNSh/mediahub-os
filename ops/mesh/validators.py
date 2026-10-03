from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Any

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


def validate_heartbeat(record: dict[str, Any], now: datetime, max_age_seconds: int = 120) -> ValidationResult:
    required = {"schema_version","node_id","issued_at","sequence","runtime_state","capability_digest","resource_summary"}
    if not isinstance(record, dict) or not required.issubset(record):
        return _result(False, "missing required heartbeat fields")
    if record["schema_version"] != "mediahub.mesh.heartbeat.v1":
        return _result(False, "unsupported heartbeat schema")
    if not HEX64.fullmatch(str(record["capability_digest"])):
        return _result(False, "invalid capability digest")
    try:
        issued = datetime.fromisoformat(record["issued_at"].replace("Z", "+00:00"))
        if issued.tzinfo is None:
            issued = issued.replace(tzinfo=timezone.utc)
        age = (now.astimezone(timezone.utc) - issued.astimezone(timezone.utc)).total_seconds()
    except (TypeError, ValueError):
        return _result(False, "invalid heartbeat timestamp")
    if age < -30:
        return _result(False, "heartbeat timestamp is from the future")
    if age > max_age_seconds:
        return _result(False, "heartbeat is stale")
    if not isinstance(record["sequence"], int) or record["sequence"] < 0:
        return _result(False, "invalid heartbeat sequence")
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
