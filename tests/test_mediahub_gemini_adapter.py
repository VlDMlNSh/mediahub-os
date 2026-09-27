import json

from ops.mediahub_canonical_protocol import CanonicalRequest, Protocol
from ops.mediahub_gemini_adapter import (
    GeminiAdapterResult,
    GeminiGenerateContentAdapter,
)


def req(model="gemini-2.5-flash"):
    return CanonicalRequest(
        "g1", model, Protocol.GEMINI_GENERATE_CONTENT, "hello", 30.0,
        generation={"maxOutputTokens": 8},
    )


def test_gemini_encodes_generate_content_shape():
    result = GeminiGenerateContentAdapter().encode(req())
    body = json.loads(result.body)
    assert body["contents"][0]["parts"][0]["text"] == "hello"
    assert body["generationConfig"]["maxOutputTokens"] == 8


def test_gemini_endpoint_is_fixed_to_google_api():
    assert GeminiGenerateContentAdapter().endpoint("gemini-2.5-flash").startswith(
        "https://generativelanguage.googleapis.com/v1beta/"
    )


def test_gemini_unknown_model_is_denied():
    try:
        GeminiGenerateContentAdapter().encode(req("gemini-unknown"))
    except PermissionError:
        pass
    else:
        raise AssertionError("unknown Gemini model must be denied")


def test_gemini_403_is_policy_blocked_and_not_retryable():
    result = GeminiGenerateContentAdapter().decode_failure(
        req(), GeminiAdapterResult(403, {}, b"{}")
    )
    assert result.policy_blocked is True
    assert result.retryable is False


def test_gemini_429_is_transient_and_retryable():
    result = GeminiGenerateContentAdapter().decode_failure(
        req(), GeminiAdapterResult(429, {}, b"{}")
    )
    assert result.retryable is True
