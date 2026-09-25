import json

from ops.mediahub_canonical_protocol import CanonicalRequest, Protocol
from ops.mediahub_provider_adapters import (
    AnthropicMessagesAdapter,
    GeminiGenerateContentAdapter,
    OpenAIChatAdapter,
    OpenAIResponsesAdapter,
    OpenRouterAdapter,
    ZhipuGLMAdapter,
    AdapterResult,
    execute_adapter,
)


def req(protocol):
    return CanonicalRequest("r1", "model-x", protocol, "hello", 30.0, generation={"max_output_tokens": 8})

def test_openai_encodes_native_responses_shape():
    result = OpenAIResponsesAdapter().encode(req(Protocol.OPENAI_RESPONSES))
    body = json.loads(result[2])
    assert body["model"] == "model-x" and body["input"] == "hello"
    assert result[1]["content-type"] == "application/json"

def test_anthropic_encodes_native_messages_shape():
    r=req(Protocol.ANTHROPIC_MESSAGES); r=CanonicalRequest(r.request_id,r.model,r.protocol,[{"role":"user","content":"hi"}],r.timeout_seconds,generation={"max_tokens":8})
    result=AnthropicMessagesAdapter().encode(r); body=json.loads(result[2])
    assert body["messages"][0]["role"] == "user"
    assert result[1]["content-type"] == "application/json"

def test_zhipu_glm52_encodes_chat_completions():
    request = CanonicalRequest(
        "r2", "glm-5.2", Protocol.OPENAI_CHAT,
        [{"role": "user", "content": "hello"}], 30.0,
        generation={"max_tokens": 8},
    )
    result = ZhipuGLMAdapter().encode(request)
    body = json.loads(result[2])
    assert result[0] == "https://api.z.ai/api/paas/v4/chat/completions"
    assert body["model"] == "glm-5.2"
    assert body["messages"][0]["role"] == "user"


def test_zhipu_rejects_unqualified_model():
    request = CanonicalRequest("r3", "glm-5.3", Protocol.OPENAI_CHAT, [], 30.0)
    try:
        ZhipuGLMAdapter().encode(request)
    except PermissionError:
        pass
    else:
        assert False


def test_protocol_mismatch_denied():
    try: OpenAIResponsesAdapter().encode(req(Protocol.ANTHROPIC_MESSAGES))
    except PermissionError: pass
    else: assert False


def test_openai_http_contract_injects_bearer_without_storing_credential():
    r = req(Protocol.OPENAI_RESPONSES)
    http = OpenAIResponsesAdapter().build_http_request(r, "secret")
    assert http.url.endswith("/v1/responses")
    assert http.headers["authorization"] == "Bearer secret"
    assert "secret" not in http.body.decode()


def test_anthropic_http_contract_uses_x_api_key():
    r = CanonicalRequest("r4", "claude-model", Protocol.ANTHROPIC_MESSAGES, [{"role":"user","content":"hi"}], 12.0, generation={"max_tokens": 8})
    http = AnthropicMessagesAdapter().build_http_request(r, "secret")
    assert http.headers["x-api-key"] == "secret"
    assert http.headers["anthropic-version"] == "2023-06-01"


def test_gemini_http_contract_uses_header_not_query_secret():
    r = CanonicalRequest("r5", "gemini-model", Protocol.GEMINI_GENERATE_CONTENT, "hello", 12.0)
    http = GeminiGenerateContentAdapter().build_http_request(r, "secret")
    assert ":generateContent" in http.url and "secret" not in http.url
    assert http.headers["x-goog-api-key"] == "secret"


def test_openrouter_uses_openai_chat_contract():
    r = req(Protocol.OPENAI_CHAT)
    http = OpenRouterAdapter().build_http_request(r, "secret")
    assert http.url == "https://openrouter.ai/api/v1/chat/completions"
    assert http.headers["authorization"] == "Bearer secret"


def test_401_403_are_policy_blocked_and_non_retryable():
    adapter = OpenAIResponsesAdapter(); r = req(Protocol.OPENAI_RESPONSES)
    for status in (401, 403):
        result = adapter.decode_failure(r, status, b"{}")
        assert result.failure_class is __import__("ops.mediahub_canonical_protocol", fromlist=["FailureClass"]).FailureClass.POLICY_BLOCKED
        assert result.retryable is False and result.policy_blocked is True


def test_429_preserves_retry_after_and_is_transient():
    adapter = OpenAIResponsesAdapter(); r = req(Protocol.OPENAI_RESPONSES)
    result = adapter.decode_failure(r, 429, b"{}", {"retry-after": "3.5"})
    assert result.failure_class.value == "transient" and result.retryable is True
    assert result.retry_after_seconds == 3.5


def test_5xx_and_timeout_are_transient():
    adapter = OpenAIResponsesAdapter(); r = req(Protocol.OPENAI_RESPONSES)
    assert adapter.decode_failure(r, 503, b"{}").retryable is True
    out = execute_adapter(adapter, r, "secret", lambda *_: (_ for _ in ()).throw(TimeoutError()))
    assert out.failure_class.value == "transient" and out.retryable is True


def test_malformed_success_is_permanent():
    adapter = OpenAIResponsesAdapter(); r = req(Protocol.OPENAI_RESPONSES)
    out = execute_adapter(adapter, r, "secret", lambda *_: AdapterResult(200, {}, b"not-json"))
    assert out.failure_class.value == "permanent" and out.retryable is False


def test_execute_contract_passes_canonical_timeout_to_transport():
    adapter = OpenAIResponsesAdapter(); r = req(Protocol.OPENAI_RESPONSES)
    seen = {}
    def send(http, timeout):
        seen["timeout"] = timeout; seen["url"] = http.url; return AdapterResult(200, {}, b"{}")
    out = execute_adapter(adapter, r, "secret", send)
    assert out.request_id == "r1" and seen == {"timeout": 30.0, "url": adapter.endpoint}
