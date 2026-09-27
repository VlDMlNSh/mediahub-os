"""Bounded, provider-neutral streaming event boundary.

Streaming is treated as untrusted transport data. The boundary accepts only
bounded JSON events and never grants authority, capabilities, or mutation rights.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

MAX_EVENT_BYTES = 256 * 1024
MAX_EVENTS = 4096
ALLOWED_TYPES = frozenset({"response.output_text.delta", "message_start", "message_delta", "message_stop"})


class StreamingProtocolError(ValueError):
    """Raised when a streaming event violates the bounded contract."""


@dataclass(frozen=True)
class StreamEvent:
    event_type: str
    data: dict[str, Any]


def parse_event(line: str | bytes) -> StreamEvent:
    raw = line.encode() if isinstance(line, str) else line
    if len(raw) > MAX_EVENT_BYTES:
        raise StreamingProtocolError("stream event exceeds bounded size")
    try:
        obj = json.loads(raw.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StreamingProtocolError("malformed stream event") from exc
    if not isinstance(obj, dict):
        raise StreamingProtocolError("stream event must be an object")
    event_type = obj.get("type")
    data = obj.get("data", {})
    if event_type not in ALLOWED_TYPES:
        raise StreamingProtocolError("unsupported stream event type")
    if not isinstance(data, dict):
        raise StreamingProtocolError("stream event data must be an object")
    return StreamEvent(str(event_type), data)


def parse_stream(lines: list[str | bytes]) -> tuple[StreamEvent, ...]:
    if len(lines) > MAX_EVENTS:
        raise StreamingProtocolError("stream contains too many events")
    return tuple(parse_event(line) for line in lines)
