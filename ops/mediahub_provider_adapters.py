"""Native provider adapter boundaries for MediaHub development lanes.

The adapters translate canonical requests into provider HTTP envelopes.
Credentials are supplied separately and are never stored in adapter state.
"""
from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from urllib.parse import quote

from ops.mediahub_zhipu_adapter import ZhipuGLMAdapter

from ops.mediahub_canonical_protocol import (
    CanonicalFailure,
    CanonicalRequest,
    CanonicalResponse,
    Capability,
    FailureClass,
    Protocol,
    ProviderAdapter,
)


@dataclass(frozen=True)
class AdapterResult:
    status: int
    headers: Mapping[str, str]
    body: bytes


@dataclass(frozen=True)
class HttpRequest:
    url: str
    headers: Mapping[str, str]
    body: bytes


class NativeProviderAdapter(ProviderAdapter):
    provider: str
    endpoint: str

    def build_http_request(self, request: CanonicalRequest, credential: str) -> HttpRequest:
        if not credential:
            raise PermissionError("provider credential is required")
        endpoint, headers, body = self.encode(request)
        return HttpRequest(endpoint, {**headers, **self.auth_headers(credential)}, body)

    def auth_headers(self, credential: str) -> Mapping[str, str]:
        return {"authorization": f"Bearer {credential}"}

    def capabilities(self) -> tuple[Capability, ...]:
        raise NotImplementedError

    def encode(self, request: CanonicalRequest) -> tuple[str, Mapping[str, str], bytes]:
        raise NotImplementedError

    def decode_response(self, request: CanonicalRequest, result: AdapterResult) -> CanonicalResponse:
        raise NotImplementedError

    def decode_failure(
        self, request: CanonicalRequest, status_code: int | None, payload: bytes,
        headers: Mapping[str, str] | None = None,
    ) -> CanonicalFailure:
        raise NotImplementedError


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class OpenAIResponsesAdapter(NativeProviderAdapter):
    provider = "openai"
    endpoint = "https://api.openai.com/v1/responses"

    def capabilities(self) -> tuple[Capability, ...]:
        return (Capability(self.provider, "*", Protocol.OPENAI_RESPONSES, "responses"),)

    def encode(self, request: CanonicalRequest) -> tuple[str, Mapping[str, str], bytes]:
        if request.protocol is not Protocol.OPENAI_RESPONSES:
            raise PermissionError("OpenAI adapter requires Responses protocol")
        payload = {"model": request.model, "input": request.input}
        payload.update(request.generation)
        if request.tools:
            payload["tools"] = list(request.tools)
        return self.endpoint, {"content-type": "application/json"}, _json_bytes(payload)

    def decode_response(self, request: CanonicalRequest, payload: bytes) -> CanonicalResponse:
        return _decode_json_response(request, self.provider, AdapterResult(200, {}, payload))

    def decode_failure(self, request: CanonicalRequest, status_code: int | None, payload: bytes, headers: Mapping[str, str] | None = None) -> CanonicalFailure:
        return _failure(request, self.provider, status_code, retry_after=_retry_after(headers or {}))


class OpenAIChatAdapter(NativeProviderAdapter):
    provider = "openai"
    endpoint = "https://api.openai.com/v1/chat/completions"

    def capabilities(self) -> tuple[Capability, ...]:
        return (Capability(self.provider, "*", Protocol.OPENAI_CHAT, "chat_completions"),)

    def encode(self, request: CanonicalRequest) -> tuple[str, Mapping[str, str], bytes]:
        if request.protocol is not Protocol.OPENAI_CHAT:
            raise PermissionError("OpenAI adapter requires Chat Completions protocol")
        payload = {"model": request.model, "messages": request.input}
        payload.update(request.generation)
        if request.tools:
            payload["tools"] = list(request.tools)
        return self.endpoint, {"content-type": "application/json"}, _json_bytes(payload)

    def decode_response(self, request: CanonicalRequest, payload: bytes) -> CanonicalResponse:
        return _decode_json_response(request, self.provider, AdapterResult(200, {}, payload))

    def decode_failure(self, request: CanonicalRequest, status_code: int | None, payload: bytes, headers: Mapping[str, str] | None = None) -> CanonicalFailure:
        return _failure(request, self.provider, status_code, retry_after=_retry_after(headers or {}))


class AnthropicMessagesAdapter(NativeProviderAdapter):
    provider = "anthropic"
    endpoint = "https://api.anthropic.com/v1/messages"
    anthropic_version = "2023-06-01"

    def capabilities(self) -> tuple[Capability, ...]:
        return (Capability(self.provider, "*", Protocol.ANTHROPIC_MESSAGES, "messages"),)

    def auth_headers(self, credential: str) -> Mapping[str, str]:
        return {"x-api-key": credential, "anthropic-version": self.anthropic_version}

    def encode(self, request: CanonicalRequest) -> tuple[str, Mapping[str, str], bytes]:
        if request.protocol is not Protocol.ANTHROPIC_MESSAGES:
            raise PermissionError("Anthropic adapter requires Messages protocol")
        payload = {"model": request.model, "messages": request.input}
        payload.update(request.generation)
        if request.tools:
            payload["tools"] = list(request.tools)
        return self.endpoint, {"content-type": "application/json"}, _json_bytes(payload)

    def decode_response(self, request: CanonicalRequest, payload: bytes) -> CanonicalResponse:
        return _decode_json_response(request, self.provider, AdapterResult(200, {}, payload))

    def decode_failure(self, request: CanonicalRequest, status_code: int | None, payload: bytes, headers: Mapping[str, str] | None = None) -> CanonicalFailure:
        return _failure(request, self.provider, status_code, retry_after=_retry_after(headers or {}))


class GeminiGenerateContentAdapter(NativeProviderAdapter):
    provider = "gemini"
    endpoint = "https://generativelanguage.googleapis.com"

    def capabilities(self) -> tuple[Capability, ...]:
        return (Capability(self.provider, "*", Protocol.GEMINI_GENERATE_CONTENT, "generate_content"),)

    def auth_headers(self, credential: str) -> Mapping[str, str]:
        return {"x-goog-api-key": credential}

    def encode(self, request: CanonicalRequest) -> tuple[str, Mapping[str, str], bytes]:
        if request.protocol is not Protocol.GEMINI_GENERATE_CONTENT:
            raise PermissionError("Gemini adapter requires generateContent protocol")
        contents = request.input if isinstance(request.input, list) else [{"role": "user", "parts": [{"text": str(request.input)}]}]
        payload = {"contents": contents}
        if request.generation:
            payload["generationConfig"] = dict(request.generation)
        if request.tools:
            payload["tools"] = list(request.tools)
        url = f"{self.endpoint}/v1beta/models/{quote(request.model, safe='')}:generateContent"
        return url, {"content-type": "application/json"}, _json_bytes(payload)

    def decode_response(self, request: CanonicalRequest, payload: bytes) -> CanonicalResponse:
        return _decode_json_response(request, self.provider, AdapterResult(200, {}, payload))

    def decode_failure(self, request: CanonicalRequest, status_code: int | None, payload: bytes, headers: Mapping[str, str] | None = None) -> CanonicalFailure:
        return _failure(request, self.provider, status_code, retry_after=_retry_after(headers or {}))


class OpenRouterAdapter(OpenAIChatAdapter):
    provider = "openrouter"
    endpoint = "https://openrouter.ai/api/v1/chat/completions"

    def capabilities(self) -> tuple[Capability, ...]:
        return (Capability(self.provider, "*", Protocol.OPENAI_CHAT, "chat_completions"),)


def _retry_after(headers: Mapping[str, str]) -> float | None:
    raw = headers.get("retry-after") or headers.get("Retry-After")
    try:
        value = float(raw) if raw is not None else None
    except (TypeError, ValueError):
        return None
    return value if value is not None and value >= 0 else None


def _failure(request: CanonicalRequest, provider: str, status: int | None, *, retry_after: float | None = None) -> CanonicalFailure:
    transient = status in {408, 425, 429, 500, 502, 503, 504} or status is None
    policy = status in {401, 403}
    return CanonicalFailure(request.request_id, provider, FailureClass.POLICY_BLOCKED if policy else FailureClass.TRANSIENT if transient else FailureClass.PERMANENT, "provider request failed", status, retry_after_seconds=retry_after, retryable=transient, policy_blocked=policy)


def _decode_json_response(request: CanonicalRequest, provider: str, result: AdapterResult) -> CanonicalResponse:
    if not 200 <= result.status < 300:
        raise ValueError("non-success response")
    if not result.body:
        raise ValueError("empty provider response")
    try:
        body = json.loads(result.body)
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise ValueError("malformed JSON response") from exc
    if not isinstance(body, dict):
        raise ValueError("response JSON must be an object")
    return CanonicalResponse(request.request_id, provider, request.model, body)


def execute_adapter(adapter: NativeProviderAdapter, request: CanonicalRequest, credential: str, send: Callable[[HttpRequest, float], AdapterResult]) -> CanonicalResponse | CanonicalFailure:
    """Execute exactly one bounded transport attempt; retries belong to orchestration."""
    http_request = adapter.build_http_request(request, credential)
    try:
        result = send(http_request, request.timeout_seconds)
    except (TimeoutError, ConnectionError, OSError):
        return _failure(request, adapter.provider, None)
    if 200 <= result.status < 300:
        try:
            return adapter.decode_response(request, result.body)
        except (ValueError, TypeError, json.JSONDecodeError):
            return CanonicalFailure(request.request_id, adapter.provider, FailureClass.PERMANENT, "malformed provider success response", result.status, retryable=False)
    return adapter.decode_failure(request, result.status, result.body, result.headers)


ADAPTERS = {
    "openai": OpenAIResponsesAdapter,
    "openai-chat": OpenAIChatAdapter,
    "anthropic": AnthropicMessagesAdapter,
    "gemini": GeminiGenerateContentAdapter,
    "openrouter": OpenRouterAdapter,
    "zhipu": ZhipuGLMAdapter,
}
