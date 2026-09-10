import json

import pytest

from ops.mediahub_streaming_boundary import (
    StreamingProtocolError,
    parse_event,
    parse_stream,
)


def test_valid_event_is_bounded_and_provider_neutral():
    event = parse_event(json.dumps({"type": "response.output_text.delta", "data": {"text": "ok"}}))
    assert event.event_type == "response.output_text.delta"
    assert event.data == {"text": "ok"}


@pytest.mark.parametrize("payload", ["not-json", "[]", json.dumps({"type": "unknown", "data": {}})])
def test_malformed_or_unknown_event_fails_closed(payload):
    with pytest.raises(StreamingProtocolError):
        parse_event(payload)


def test_oversized_event_is_rejected():
    with pytest.raises(StreamingProtocolError):
        parse_event(json.dumps({"type": "message_delta", "data": {"x": "a" * (256 * 1024)}}))


def test_oversized_stream_is_rejected():
    event = json.dumps({"type": "message_start", "data": {}})
    with pytest.raises(StreamingProtocolError):
        parse_stream([event] * 4097)
