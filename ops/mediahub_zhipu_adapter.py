"""Zhipu AI GLM-5.2 provider adapter.

Uses Zhipu's OpenAI-compatible Chat Completions API. Credentials are
injected by the gateway and are never stored in adapter state.
"""
from __future__ import annotations

import json
from collections.abc import Mapping

from ops.mediahub_canonical_protocol import (
    CanonicalFailure,
    CanonicalRequest,
    CanonicalResponse,
    Capability,
    FailureClass,
    Protocol,
    ProviderAdapter,
)


class ZhipuGLMAdapter(ProviderAdapter):
    provider = "zhipu"
    model = "glm-5.2"
    endpoint = "https://api.z.ai/api/paas/v4/chat/completions"

    def capabilities(self) -> tuple[Capability, ...]:
        return (Capability(self.provider, self.model, Protocol.OPENAI_CHAT, "chat_completions"),)

    def encode(self, request: CanonicalRequest) -> tuple[str, Mapping[str, str], bytes]:
        if request.protocol is not Protocol.OPENAI_CHAT:
            raise PermissionError("Zhipu GLM adapter requires OpenAI Chat Completions protocol")
        if request.model != self.model:
            raise PermissionError("Zhipu adapter is qualified only for GLM-5.2")
        payload = {"model": request.model, "messages": request.input}
        payload.update(request.generation)
        if request.tools:
            payload["tools"] = list(request.tools)
        return self.endpoint, {"content-type": "application/json"}, json.dumps(
            payload, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")

    def decode_response(self, request: CanonicalRequest, payload: bytes) -> CanonicalResponse:
        body = json.loads(payload or b"{}")
        return CanonicalResponse(request.request_id, self.provider, request.model, body)

    def decode_failure(
        self, request: CanonicalRequest, status_code: int | None, payload: bytes
    ) -> CanonicalFailure:
        transient = status_code in {408, 425, 429, 500, 502, 503, 504} or status_code is None
        policy = status_code in {401, 403}
        return CanonicalFailure(
            request.request_id,
            self.provider,
            FailureClass.POLICY_BLOCKED if policy else FailureClass.TRANSIENT if transient else FailureClass.PERMANENT,
            "Zhipu provider request failed",
            status_code,
            retryable=transient,
            policy_blocked=policy,
        )
