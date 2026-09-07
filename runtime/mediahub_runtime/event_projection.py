"""Projection boundary from trusted runtime events to canonical domain events."""

import json
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from types import MappingProxyType
from typing import Any


class ProjectionError(ValueError):
    """Raised when a runtime event cannot be projected safely."""


CANONICAL_EVENT_KEYS = frozenset({
    "id", "type", "version", "timestamp", "source", "subject", "payload",
    "severity", "priority", "correlation_id", "causation_id", "metadata",
})
CANONICAL_SEVERITIES = frozenset({"INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL"})


def _freeze(value: Any) -> Any:
    """Recursively freeze JSON-like event data so nested state cannot mutate."""
    if isinstance(value, Mapping):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    if isinstance(value, set):
        return frozenset(_freeze(item) for item in value)
    return value


def _thaw(value: Any) -> Any:
    """Return a JSON-serializable detached representation of frozen data."""
    if isinstance(value, Mapping):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    if isinstance(value, frozenset):
        return sorted((_thaw(item) for item in value), key=repr)
    return value


@dataclass(frozen=True)
class CanonicalEvent:
    id: str
    type: str
    version: str
    timestamp: str
    source: str
    subject: str
    payload: Mapping[str, Any]
    severity: str
    priority: int
    correlation_id: str | None
    causation_id: str | None
    metadata: Mapping[str, Any]

    def __post_init__(self) -> None:
        object.__setattr__(self, "payload", _freeze(self.payload))
        object.__setattr__(self, "metadata", _freeze(self.metadata))

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "version": self.version,
            "timestamp": self.timestamp,
            "source": self.source,
            "subject": self.subject,
            "payload": _thaw(self.payload),
            "severity": self.severity,
            "priority": self.priority,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "metadata": _thaw(self.metadata),
        }

    def evidence_fingerprint(self) -> str:
        """Return a deterministic hash binding evidence to this exact event."""
        event_dict = self.as_dict()
        validate_canonical_event(event_dict)
        serialized = json.dumps(event_dict, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return sha256(serialized.encode("utf-8")).hexdigest()


def validate_canonical_event(event: Mapping[str, Any]) -> None:
    """Validate the executable subset of the canonical JSON Event schema."""
    if not isinstance(event, Mapping) or set(event) != CANONICAL_EVENT_KEYS:
        raise ProjectionError("canonical event keys do not match schema")
    for field in ("id", "type", "version", "timestamp", "source", "subject"):
        if not isinstance(event[field], str) or not event[field]:
            raise ProjectionError(f"invalid canonical event {field}")
    if not isinstance(event["payload"], Mapping) or not isinstance(event["metadata"], Mapping):
        raise ProjectionError("payload and metadata must be objects")
    if event["severity"] not in CANONICAL_SEVERITIES:
        raise ProjectionError("invalid canonical event severity")
    if not isinstance(event["priority"], int) or isinstance(event["priority"], bool) or event["priority"] < 0:
        raise ProjectionError("invalid canonical event priority")
    for field in ("correlation_id", "causation_id"):
        if event[field] is not None and (not isinstance(event[field], str) or not event[field]):
            raise ProjectionError(f"invalid canonical event {field}")
    try:
        parsed = datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise ProjectionError("invalid canonical event timestamp") from exc
    if parsed.tzinfo is None:
        raise ProjectionError("canonical event timestamp must include timezone")


def project_runtime_event(
    runtime_event: Any,
    *,
    severity: str = "INFO",
    priority: int = 0,
    metadata: Mapping[str, Any] | None = None,
) -> CanonicalEvent:
    """Project a trusted completed runtime event without mutation authority."""
    required = (
        "event_id", "command_id", "correlation_id", "operation", "path",
        "source_identity", "causation_id", "timestamp", "generation",
        "state_version", "state_digest", "sequence",
    )
    if any(not hasattr(runtime_event, name) for name in required):
        raise ProjectionError("incomplete trusted runtime event")
    if not isinstance(runtime_event.source_identity, str) or not runtime_event.source_identity:
        raise ProjectionError("source identity required")
    if runtime_event.causation_id is not None and (
        not isinstance(runtime_event.causation_id, str) or not runtime_event.causation_id
    ):
        raise ProjectionError("invalid causation id")
    if not isinstance(runtime_event.timestamp, str) or not runtime_event.timestamp:
        raise ProjectionError("event timestamp required")
    if severity not in CANONICAL_SEVERITIES:
        raise ProjectionError("invalid severity")
    if not isinstance(priority, int) or isinstance(priority, bool) or priority < 0:
        raise ProjectionError("invalid priority")

    subject = "state:" + "/".join(runtime_event.path)
    if not subject or subject == "state:":
        raise ProjectionError("event subject cannot be empty")

    payload = {
        "operation": runtime_event.operation,
        "path": list(runtime_event.path),
        "generation": runtime_event.generation,
        "state_version": runtime_event.state_version,
        "state_digest": runtime_event.state_digest,
    }
    event_metadata = {
        "command_id": runtime_event.command_id,
        "runtime_sequence": runtime_event.sequence,
    }
    if metadata:
        event_metadata.update(dict(metadata))

    canonical = CanonicalEvent(
        id=runtime_event.event_id,
        type=f"state.{runtime_event.operation}",
        version="1.0",
        timestamp=runtime_event.timestamp,
        source=runtime_event.source_identity,
        subject=subject,
        payload=payload,
        severity=severity,
        priority=priority,
        correlation_id=runtime_event.correlation_id,
        causation_id=runtime_event.causation_id,
        metadata=event_metadata,
    )
    validate_canonical_event(canonical.as_dict())
    return canonical
