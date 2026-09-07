"""Projection boundary from trusted runtime events to canonical domain events."""

from dataclasses import dataclass
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
    severity: str = "INFO",
    priority: int = 0,
    metadata: Mapping[str, Any] | None = None,
) -> CanonicalEvent:
    """Project a trusted completed runtime event without mutation authority.

    Provenance, timestamp and causation are intentionally read only from the
    immutable runtime event. Callers cannot substitute these security-relevant
    fields at the projection boundary.
    """
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
    if severity not in {"INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL"}:
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

    return CanonicalEvent(
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
