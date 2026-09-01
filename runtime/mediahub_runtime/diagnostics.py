"""Sanitized diagnostic event boundary."""

from dataclasses import dataclass
from datetime import datetime, timezone

_SENSITIVE_KEYS = frozenset({
    "password", "passwd", "secret", "token", "authorization",
    "credential", "credentials", "voice", "raw_voice", "api_key",
})
_REDACTED = "[REDACTED]"


@dataclass(frozen=True)
class DiagnosticEvent:
    event_type: str
    timestamp: str
    fields: dict


def _sanitize_value(value):
    if isinstance(value, dict):
        sanitized = {}
        for key, nested_value in value.items():
            normalized = str(key).lower()
            if normalized in _SENSITIVE_KEYS:
                sanitized[key] = _REDACTED
            else:
                sanitized[key] = _sanitize_value(nested_value)
        return sanitized
    if isinstance(value, list):
        return [_sanitize_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_sanitize_value(item) for item in value)
    return value


def sanitize_fields(fields):
    if not isinstance(fields, dict):
        raise TypeError("diagnostic fields must be a dictionary")
    return _sanitize_value(fields)


def make_event(event_type, fields=None):
    if not event_type or not isinstance(event_type, str):
        raise ValueError("event_type must be a non-empty string")
    return DiagnosticEvent(
        event_type=event_type,
        timestamp=datetime.now(timezone.utc).isoformat(),
        fields=sanitize_fields(fields or {}),
    )
