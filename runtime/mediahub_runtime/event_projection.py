"""Projection boundary from internal runtime events to canonical domain events.

This module deliberately performs no state mutation and owns no authority.
It converts a trusted execution record into the frozen canonical Event shape.
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Mapping


class ProjectionError(ValueError):
    """Raised when a runtime event cannot be projected safely."""


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

    def as_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "version": self.version,
            "timestamp": self.timestamp,
            "source": self.source,
            "subject": self.subject,
            "payload": dict(self.payload),
            "severity": self.severity,
            "priority": self.priority,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "metadata": dict(self.metadata),
        }


def project_runtime_event(
    runtime_event: Any,
    *,
    source_identity: str,
    subject: str,
    causation_id: str | None = None,
    timestamp: str | None = None,
    severity: str = "INFO",
    priority: int = 0,
    metadata: Mapping[str, Any] | None = None,
) -> CanonicalEvent:
    """Project a completed runtime event without mutating runtime state.

    The caller must supply provenance that has already been authenticated by
    the governed execution path. This function does not authorize callers or
    mutate StateAuthority.
    """
    required = ("event_id", "command_id", "correlation_id", "operation", "path")
    if any(not hasattr(runtime_event, name) for name in required):
        raise ProjectionError("incomplete runtime event")
    if not isinstance(source_identity, str) or not source_identity:
        raise ProjectionError("source identity required")
    if not isinstance(subject, str) or not subject:
        raise ProjectionError("subject required")
    if causation_id is not None and (not isinstance(causation_id, str) or not causation_id):
        raise ProjectionError("invalid causation id")
    if severity not in {"INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL"}:
        raise ProjectionError("invalid severity")
    if not isinstance(priority, int) or isinstance(priority, bool) or priority < 0:
        raise ProjectionError("invalid priority")

    event_timestamp = timestamp or datetime.now(timezone.utc).isoformat()
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

    return CanonicalEvent(
        id=runtime_event.event_id,
        type=f"state.{runtime_event.operation}",
        version="1.0",
        timestamp=event_timestamp,
        source=source_identity,
        subject=subject,
        payload=payload,
        severity=severity,
        priority=priority,
        correlation_id=runtime_event.correlation_id,
        causation_id=causation_id,
        metadata=event_metadata,
    )
