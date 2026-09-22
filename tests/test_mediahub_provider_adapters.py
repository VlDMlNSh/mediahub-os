import json

from ops.mediahub_canonical_protocol import CanonicalRequest, Protocol
from ops.mediahub_provider_adapters import (
    AnthropicMessagesAdapter,
    OpenAIResponsesAdapter,
    ZhipuGLMAdapter,
)


def req(protocol):
    return CanonicalRequest("r1", "model-x", protocol, "hello", 30.0, generation={"max_output_tokens": 8})

def test_openai_encodes_native_responses_shape():
    result = OpenAIResponsesAdapter().encode(req(Protocol.OPENAI_RESPONSES))
    body = json.loads(result.body)
    assert body["model"] == "model-x" and body["input"] == "hello"
    assert result.headers["content-type"] == "application/json"

def test_anthropic_encodes_native_messages_shape():
    r=req(Protocol.ANTHROPIC_MESSAGES); r=CanonicalRequest(r.request_id,r.model,r.protocol,[{"role":"user","content":"hi"}],r.timeout_seconds,generation={"max_tokens":8})
    result=AnthropicMessagesAdapter().encode(r); body=json.loads(result.body)
    assert body["messages"][0]["role"] == "user"
    assert result.headers["anthropic-version"] == "2023-06-01"

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
