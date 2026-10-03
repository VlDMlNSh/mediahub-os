from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any
from .validators import validate_node, validate_heartbeat
from .state import transition_node_state

@dataclass(frozen=True)
class RegistryResult:
    accepted: bool
    reason: str = ""

def register_node(record: dict[str, Any], existing_ids: set[str] | None = None) -> RegistryResult:
    vr = validate_node(record)
    if not vr.valid:
        return RegistryResult(False, vr.reason)
    existing_ids = existing_ids if existing_ids is not None else set()
    if record["node_id"] in existing_ids:
        return RegistryResult(False, "duplicate node identity")
    if record["status"] == "ACTIVE" and not record.get("last_heartbeat"):
        return RegistryResult(False, "active node requires heartbeat")
    return RegistryResult(True)

def record_heartbeat(record: dict[str, Any], now: datetime, current_status: str = "STALE") -> RegistryResult:
    vr = validate_heartbeat(record, now)
    if not vr.valid:
        return RegistryResult(False, vr.reason)
    if current_status == "RETIRED":
        return RegistryResult(False, "retired node cannot reactivate")
    return RegistryResult(True)

def activate_from_heartbeat(current_status: str) -> str:
    return transition_node_state(current_status, "heartbeat")
