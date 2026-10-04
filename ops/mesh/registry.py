from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .validators import validate_node, validate_heartbeat
from .state import transition_node_state

DEFAULT_SEQUENCE_DIR = "/var/lib/mediahub-mesh/heartbeat-sequences"

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

def _sequence_path(node_id: str, state_path: str | None) -> Path:
    root = Path(state_path or os.environ.get("MEDIAHUB_MESH_HEARTBEAT_STATE_DIR", DEFAULT_SEQUENCE_DIR))
    if not node_id or "/" in node_id or "\" in node_id or node_id in {".", ".."}:
        raise ValueError("invalid node identity for heartbeat state")
    return root / f"{node_id}.seq"

def _read_sequence(path: Path) -> int | None:
    try:
        return int(path.read_text(encoding="utf-8").strip())
    except FileNotFoundError:
        return None
    except (OSError, ValueError):
        raise ValueError("persisted heartbeat sequence is unreadable")

def _persist_sequence(path: Path, sequence: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(str(sequence) + "\n", encoding="utf-8")
    tmp.replace(path)

def record_heartbeat(
    record: dict[str, Any],
    now: datetime,
    current_status: str = "STALE",
    *,
    expected_node_id: str | None = None,
    state_path: str | None = None,
    hmac_key: str | None = None,
) -> RegistryResult:
    node_id = expected_node_id or ""
    try:
        path = _sequence_path(node_id, state_path)
        last_sequence = _read_sequence(path)
    except (OSError, ValueError) as exc:
        return RegistryResult(False, str(exc))
    vr = validate_heartbeat(
        record,
        now,
        hmac_key=hmac_key,
        expected_node_id=expected_node_id,
        last_sequence=last_sequence,
    )
    if not vr.valid:
        return RegistryResult(False, vr.reason)
    try:
        _persist_sequence(path, int(record["sequence"]))
    except OSError as exc:
        return RegistryResult(False, f"heartbeat sequence persistence failed: {exc}")
    if current_status == "RETIRED":
        return RegistryResult(False, "retired node cannot reactivate")
    return RegistryResult(True)

def activate_from_heartbeat(current_status: str) -> str:
    return transition_node_state(current_status, "heartbeat")
