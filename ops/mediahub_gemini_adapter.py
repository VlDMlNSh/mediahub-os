"""Native Gemini GenerateContent adapter for MediaHub development lanes.

Gemini remains provider-neutral at the routing layer: this adapter only
translates the canonical request and never owns credentials or routing state.
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
class GeminiAdapterResult:
    status: int
    headers: Mapping[str, str]
    body: bytes


def _json_bytes(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


class GeminiGenerateContentAdapter:
    provider = "google-gemini"
    protocols = frozenset({Protocol.GEMINI_GENERATE_CONTENT})
    api_version = "v1beta"
    base_url = "https://generativelanguage.googleapis.com/v1beta"

    def capabilities(self) -> tuple[Capability, ...]:
        return tuple(
            Capability(self.provider, model, Protocol.GEMINI_GENERATE_CONTENT, "generateContent")
            for model in (
                "gemini-2.5-flash",
                "gemini-2.5-flash-lite",
            )
        )

    def endpoint(self, model: str) -> str:
        if not any(c.model_pattern == model for c in self.capabilities()):
            raise PermissionError(f"Gemini model is not qualified: {model}")
        return f"{self.base_url}/models/{model}:generateContent"

    def encode(self, request: CanonicalRequest) -> GeminiAdapterResult:
        if request.protocol is not Protocol.GEMINI_GENERATE_CONTENT:
            raise PermissionError("Gemini adapter requires GenerateContent protocol")
        self.endpoint(request.model)
        contents = request.input
        if isinstance(contents, str):
            contents = [{"role": "user", "parts": [{"text": contents}]}]
        payload: dict[str, object] = {"contents": contents}
        if request.generation:
            payload["generationConfig"] = dict(request.generation)
        if request.tools:
            payload["tools"] = list(request.tools)
        return GeminiAdapterResult(
            0,
            {"content-type": "application/json"},
            _json_bytes(payload),
        )

    def decode_response(
        self, request: CanonicalRequest, result: GeminiAdapterResult
    ) -> CanonicalResponse:
        if not 200 <= result.status < 300:
            raise ValueError("non-success response")
        body = json.loads(result.body or b"{}")
        candidates = body.get("candidates", [])
        finish_reason = candidates[0].get("finishReason") if candidates else None
        return CanonicalResponse(
            request.request_id,
            self.provider,
            request.model,
            body,
            finish_reason=finish_reason,
            usage=body.get("usageMetadata", {}),
        )

    def decode_failure(
        self, request: CanonicalRequest, result: GeminiAdapterResult
    ) -> CanonicalFailure:
        transient = result.status in {408, 425, 429, 500, 502, 503, 504}
        policy = result.status == 403
        return CanonicalFailure(
            request.request_id,
            self.provider,
            FailureClass.POLICY_BLOCKED if policy else FailureClass.TRANSIENT if transient else FailureClass.PERMANENT,
            "provider request failed",
            result.status,
            retryable=transient and not policy,
            policy_blocked=policy,
        )
