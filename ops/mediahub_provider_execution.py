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
from runtime.mediahub_control_plane.model import OperationStatus
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
        operation_service=None,
    ) -> None:
        self.gateway = gateway
        self.engine = ResilienceEngine(gateway, retry_policy)
        self.adapters = tuple(adapters) if adapters is not None else tuple(cls() for cls in ADAPTERS.values())
        self.credential_for = credential_for
        self.send = send
        self.sleep_fn = sleep_fn
        self.operation_service = operation_service

    def _qualified(self, request: CanonicalRequest) -> Mapping[str, NativeProviderAdapter]:
        operation = _OPERATION[request.protocol]
        matrix = CapabilityMatrix(tuple(capability for adapter in self.adapters for capability in adapter.capabilities()))
        qualified: dict[str, NativeProviderAdapter] = {}
        for adapter in self.adapters:
            if matrix.supports(adapter.provider, request.model, request.protocol, operation):
                qualified.setdefault(adapter.provider, adapter)
        return qualified

    def _begin_operation(self, request: CanonicalRequest, provider: str):
        if self.operation_service is None:
            return None
        ext=request.provider_extensions
        required=(ext.get("task_id"),ext.get("agent_id"),ext.get("generation"))
        if any(value is None for value in required):
            return None
        logical_key=str(ext.get("operation_key") or request.request_id)
        key=f"{logical_key}:{provider}"
        existing=self.operation_service.repository.get_operation_by_key(key)
        operation=self.operation_service.begin_external_operation(
            str(ext["task_id"]),str(ext["agent_id"]),int(ext["generation"]),provider,request.model,key
        )
        return operation, existing is not None

    def _mark_operation_ambiguous(self, request: CanonicalRequest, operation, failure: CanonicalFailure):
        if self.operation_service is None or operation is None:
            return
        ext=request.provider_extensions
        self.operation_service.mark_external_ambiguous(
            operation.operation_id,str(ext["agent_id"]),int(ext["generation"]),failure.message
        )

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
                operation_state = self._begin_operation(request, provider)
                operation, existed = operation_state if operation_state is not None else (None, False)
                if existed and operation is not None and operation.status is OperationStatus.RESOLVED:
                    body = None
                    if isinstance(operation.result, dict):
                        evidence = operation.result.get("evidence", operation.result)
                        body = evidence.get("body") if isinstance(evidence, dict) else None
                    else:
                        body = operation.result
                    if body is not None:
                        return CanonicalResponse(request.request_id, operation.provider, operation.model, body)
                    return CanonicalFailure(request.request_id, provider, FailureClass.POLICY_BLOCKED, "resolved operation has no replayable response", retryable=False, policy_blocked=True)
                if existed and operation is not None and operation.status in {OperationStatus.IN_FLIGHT, OperationStatus.RECONCILIATION_REQUIRED, OperationStatus.REPLAY_AUTHORIZED}:
                    return CanonicalFailure(request.request_id, provider, FailureClass.POLICY_BLOCKED, "operation requires reconciliation before replay", retryable=False, policy_blocked=True)
                failure = execute_adapter(adapter, request, credential, self.send)
                if isinstance(failure, CanonicalResponse) and operation is not None:
                    self.operation_service.reconcile_external_operation(operation.operation_id, request.provider_extensions["agent_id"], "SUCCEEDED", {"provider": provider, "request_id": request.request_id, "body": failure.output})
                elif not isinstance(failure, CanonicalResponse) and operation is not None:
                    if failure.outcome_ambiguous:
                        self._mark_operation_ambiguous(request, operation, failure)
                    else:
                        self.operation_service.reconcile_external_operation(operation.operation_id, request.provider_extensions["agent_id"], "FAILED", {"provider": provider, "request_id": request.request_id, "failure": failure.failure_class.value})

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
