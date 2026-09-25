"""Deterministic provider execution coordinator.

Connects qualified native adapters to the existing resilience and gateway
primitives. It owns no durable state and never stores credential values.
"""
from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from time import sleep

from ops.mediahub_canonical_protocol import (
    CanonicalFailure,
    CanonicalRequest,
    CanonicalResponse,
    CapabilityMatrix,
    FailureClass,
    Protocol,
)
from ops.mediahub_provider_adapters import (
    ADAPTERS,
    AdapterResult,
    NativeProviderAdapter,
    execute_adapter,
)
from ops.mediahub_provider_gateway import ProviderGateway
from ops.mediahub_resilience import ResilienceEngine, RetryPolicy


_OPERATION = {
    Protocol.OPENAI_RESPONSES: "responses",
    Protocol.OPENAI_CHAT: "chat_completions",
    Protocol.ANTHROPIC_MESSAGES: "messages",
    Protocol.GEMINI_GENERATE_CONTENT: "generate_content",
}


class ProviderExecutionCoordinator:
    """Execute one canonical request across qualified providers, fail-closed."""

    def __init__(
        self,
        gateway: ProviderGateway,
        *,
        adapters: Sequence[NativeProviderAdapter] | None = None,
        credential_for: Callable[[str], str | None],
        send: Callable[[object, float], AdapterResult],
        retry_policy: RetryPolicy | None = None,
        sleep_fn: Callable[[float], None] = sleep,
    ) -> None:
        self.gateway = gateway
        self.engine = ResilienceEngine(gateway, retry_policy)
        self.adapters = tuple(adapters) if adapters is not None else tuple(cls() for cls in ADAPTERS.values())
        self.credential_for = credential_for
        self.send = send
        self.sleep_fn = sleep_fn

    def _qualified(self, request: CanonicalRequest) -> Mapping[str, NativeProviderAdapter]:
        operation = _OPERATION[request.protocol]
        matrix = CapabilityMatrix(tuple(capability for adapter in self.adapters for capability in adapter.capabilities()))
        qualified: dict[str, NativeProviderAdapter] = {}
        for adapter in self.adapters:
            if matrix.supports(adapter.provider, request.model, request.protocol, operation):
                qualified.setdefault(adapter.provider, adapter)
        return qualified

    def execute(self, request: CanonicalRequest) -> CanonicalResponse | CanonicalFailure:
        qualified = self._qualified(request)
        if not qualified:
            return CanonicalFailure(
                request.request_id, "gateway", FailureClass.POLICY_BLOCKED,
                "requested provider capability is not qualified", retryable=False,
                policy_blocked=True,
            )

        excluded = frozenset(set(self.gateway.circuits) - set(qualified))
        decision = self.engine.first(excluded=excluded)
        attempt = decision.attempt
        last_failure: CanonicalFailure | None = None

        while decision.provider is not None:
            provider = decision.provider
            adapter = qualified[provider]
            credential = self.credential_for(provider)
            if not credential:
                failure = CanonicalFailure(
                    request.request_id, provider, FailureClass.POLICY_BLOCKED,
                    "provider credential is unavailable", retryable=False, policy_blocked=True,
                )
            else:
                failure = execute_adapter(adapter, request, credential, self.send)

            if isinstance(failure, CanonicalResponse):
                self.gateway.record(provider, FailureClass.SUCCESS)
                return failure

            last_failure = failure
            if failure.outcome_ambiguous and request.provider_extensions.get("allow_ambiguous_replay") is not True:
                return failure
            excluded = frozenset(set(excluded) | {provider})
            decision = self.engine.after_failure(
                provider,
                failure.status_code,
                failure.message,
                attempt=attempt,
                retry_after=failure.retry_after_seconds,
                excluded=excluded,
            )
            if decision.provider is None:
                return last_failure
            if decision.delay_seconds:
                self.sleep_fn(decision.delay_seconds)
            attempt = decision.attempt

        return last_failure or CanonicalFailure(
            request.request_id, "gateway", FailureClass.TRANSIENT,
            "all qualified providers unavailable", retryable=False,
        )
