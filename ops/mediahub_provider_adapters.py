"""Native provider adapter contracts for MediaHub development lanes.

Adapters own protocol-specific request/response translation. Credentials,
policy, egress and routing remain outside the adapter boundary.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping

from ops.mediahub_canonical_protocol import CanonicalRequest, CanonicalResponse, Protocol

@dataclass(frozen=True)
class AdapterResult:
    status: int
    headers: Mapping[str, str]
    body: bytes

class ProviderAdapter:
    provider: str
    protocols: frozenset[Protocol]
    def encode(self, request: CanonicalRequest) -> AdapterResult: raise NotImplementedError
    def decode_response(self, result: AdapterResult) -> CanonicalResponse: raise NotImplementedError

class OpenAIResponsesAdapter(ProviderAdapter):
    provider = "openai"
    protocols = frozenset({Protocol.OPENAI_RESPONSES})

    def encode(self, request: CanonicalRequest) -> AdapterResult:
        if request.protocol is not Protocol.OPENAI_RESPONSES:
            raise ValueError("OpenAI adapter requires Responses protocol")
        return AdapterResult(200, {"Content-Type": "application/json"}, request.body)

    def decode_response(self, result: AdapterResult) -> CanonicalResponse:
        if not 200 <= result.status < 300:
            raise ValueError("non-success response")
        return CanonicalResponse(protocol=Protocol.OPENAI_RESPONSES, body=result.body)

class AnthropicMessagesAdapter(ProviderAdapter):
    provider = "anthropic"
    protocols = frozenset({Protocol.ANTHROPIC_MESSAGES})

    def encode(self, request: CanonicalRequest) -> AdapterResult:
        if request.protocol is not Protocol.ANTHROPIC_MESSAGES:
            raise ValueError("Anthropic adapter requires Messages protocol")
        return AdapterResult(200, {"Content-Type": "application/json"}, request.body)

    def decode_response(self, result: AdapterResult) -> CanonicalResponse:
        if not 200 <= result.status < 300:
            raise ValueError("non-success response")
        return CanonicalResponse(protocol=Protocol.ANTHROPIC_MESSAGES, body=result.body)

ADAPTERS = {"openai": OpenAIResponsesAdapter, "anthropic": AnthropicMessagesAdapter}
