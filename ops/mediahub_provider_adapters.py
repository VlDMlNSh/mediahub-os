"""Native provider adapter boundaries for MediaHub development lanes.

The adapters translate canonical requests into provider HTTP envelopes.
Credentials are supplied separately and are never stored in adapter state.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass

from ops.mediahub_canonical_protocol import (
    CanonicalFailure,
    CanonicalRequest,
    CanonicalResponse,
    Capability,
    FailureClass,
    Protocol,
)


@dataclass(frozen=True)
class AdapterResult:
    status: int
    headers: Mapping[str, str]
    body: bytes


class NativeProviderAdapter:
    provider: str
    protocols: frozenset[Protocol]

    def capabilities(self) -> tuple[Capability, ...]:
        return tuple(Capability(self.provider, "*", p, "responses") for p in self.protocols)

    def encode(self, request: CanonicalRequest) -> AdapterResult:
        raise NotImplementedError

    def decode_response(self, request: CanonicalRequest, result: AdapterResult) -> CanonicalResponse:
        raise NotImplementedError

    def decode_failure(self, request: CanonicalRequest, result: AdapterResult) -> CanonicalFailure:
        raise NotImplementedError


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class OpenAIResponsesAdapter(NativeProviderAdapter):
    provider = "openai"
    protocols = frozenset({Protocol.OPENAI_RESPONSES})

    def encode(self, request: CanonicalRequest) -> AdapterResult:
        if request.protocol not in self.protocols:
            raise PermissionError("OpenAI adapter requires Responses protocol")
        payload = {"model": request.model, "input": request.input}
        payload.update(request.generation)
        if request.tools:
            payload["tools"] = list(request.tools)
        return AdapterResult(0, {"content-type": "application/json"}, _json_bytes(payload))

    def decode_response(self, request: CanonicalRequest, result: AdapterResult) -> CanonicalResponse:
        if not 200 <= result.status < 300:
            raise ValueError("non-success response")
        body = json.loads(result.body or b"{}")
        return CanonicalResponse(request.request_id, self.provider, request.model, body)

    def decode_failure(self, request: CanonicalRequest, result: AdapterResult) -> CanonicalFailure:
        return CanonicalFailure(request.request_id, self.provider, FailureClass.TRANSIENT if result.status in {408,425,429,500,502,503,504} else FailureClass.PERMANENT, "provider request failed", result.status, retryable=result.status in {408,425,429,500,502,503,504})


class AnthropicMessagesAdapter(NativeProviderAdapter):
    provider = "anthropic"
    protocols = frozenset({Protocol.ANTHROPIC_MESSAGES})
    anthropic_version = "2023-06-01"

    def encode(self, request: CanonicalRequest) -> AdapterResult:
        if request.protocol not in self.protocols:
            raise PermissionError("Anthropic adapter requires Messages protocol")
        payload = {"model": request.model, "messages": request.input}
        payload.update(request.generation)
        if request.tools:
            payload["tools"] = list(request.tools)
        return AdapterResult(0, {"content-type": "application/json", "anthropic-version": self.anthropic_version}, _json_bytes(payload))

    def decode_response(self, request: CanonicalRequest, result: AdapterResult) -> CanonicalResponse:
        if not 200 <= result.status < 300:
            raise ValueError("non-success response")
        body = json.loads(result.body or b"{}")
        return CanonicalResponse(request.request_id, self.provider, request.model, body)

    def decode_failure(self, request: CanonicalRequest, result: AdapterResult) -> CanonicalFailure:
        return CanonicalFailure(request.request_id, self.provider, FailureClass.TRANSIENT if result.status in {408,425,429,500,502,503,504} else FailureClass.PERMANENT, "provider request failed", result.status, retryable=result.status in {408,425,429,500,502,503,504})


ADAPTERS = {"openai": OpenAIResponsesAdapter, "anthropic": AnthropicMessagesAdapter}
