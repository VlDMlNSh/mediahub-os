"""Target-gated dispatcher for bounded hybrid development agents.

This module joins the existing session, conversation, delivery, transport,
sandbox, credential and native-agent boundaries without granting any product
or production authority.
"""
from __future__ import annotations

from dataclasses import dataclass

from ops.ai.task_delivery import DeliveryDenied, DeliveryState, TaskDeliveryJournal
from ops.hybrid_cloud_api_egress_adapter import CloudAPIUnavailable
from ops.hybrid_cloud_egress import HybridCloudEgressAdapter
from ops.cloud_development_adapter import CloudDevelopmentAdapter, ProviderRequest, ProviderResult, SandboxSpec
from ops.mediahub_credential_broker import CredentialBroker
from ops.mediahub_model_registry import ModelRegistry


class DispatchDenied(PermissionError):
    """Raised whenever target-gated dispatch cannot be proven safe."""


@dataclass(frozen=True)
class DispatchAuthorization:
    status: str = "target-gated"
    human_production_authorized: bool = False
    allow_cloud_agent: bool = False


@dataclass(frozen=True)
class DispatchRequest:
    task_id: str
    envelope: str
    provider: str
    model: str
    endpoint: str
    source_sha: str
    egress: str
    capabilities: frozenset[str] = frozenset()
    data_class: str = "non-sensitive"
    timeout_seconds: int = 60


@dataclass
class HybridAgentDispatcher:
    delivery: TaskDeliveryJournal
    egress: HybridCloudEgressAdapter
    adapter: CloudDevelopmentAdapter
    broker: CredentialBroker
    registry: ModelRegistry
    sandbox: SandboxSpec
    authorization: DispatchAuthorization = DispatchAuthorization()

    @staticmethod
    def registry_provider(agent: str) -> str:
        mapping = {"codex": "openai", "claude": "anthropic"}
        try:
            return mapping[agent]
        except KeyError as exc:
            raise DispatchDenied("native agent is not qualified") from exc

    def admit(self, request: DispatchRequest, *, session_id: str,
              conversation_id: str, generation: int) -> ProviderRequest:
        if self.authorization.status != "target-gated":
            raise DispatchDenied("dispatcher is not target-gated")
        if self.authorization.human_production_authorized:
            raise DispatchDenied("dispatcher cannot hold production authority")
        if not self.authorization.allow_cloud_agent:
            raise DispatchDenied("cloud-agent target is not explicitly enabled")
        if not session_id or not conversation_id or generation < 1:
            raise DispatchDenied("current session identity is required")
        try:
            delivery = self.delivery.delivery
            if delivery is None:
                raise DispatchDenied("task delivery has not been prepared")
            if (delivery.task_id != request.task_id or delivery.session_id != session_id
                    or delivery.conversation_id != conversation_id or delivery.generation != generation):
                raise DispatchDenied("task identity does not match current session")
            if delivery.state is not DeliveryState.PREPARED:
                raise DispatchDenied(f"delivery state is not dispatchable: {delivery.state}")
            if request.egress not in self.adapter.allowed_egress:
                raise DispatchDenied("request egress is not adapter-allowlisted")
            if request.endpoint != request.egress:
                raise DispatchDenied("endpoint and egress identity must match")
            self.registry.require(self.registry_provider(request.provider), request.model)
            self.adapter.authorize(self.adapter.allowed_egress)
            provider_request = ProviderRequest(
                task_id=request.task_id, provider=request.provider, prompt=request.envelope,
                capabilities=request.capabilities, egress=frozenset({request.egress}),
                timeout_seconds=request.timeout_seconds, source_sha=request.source_sha,
                data_class=request.data_class,
            )
            self.adapter.admit(provider_request)
            return provider_request
        except (DeliveryDenied, PermissionError, CloudAPIUnavailable) as exc:
            raise DispatchDenied("dispatch admission failed closed") from exc

    def dispatch(self, request: DispatchRequest, *, session_id: str,
                 conversation_id: str, generation: int) -> ProviderResult:
        provider_request = self.admit(request, session_id=session_id,
                                      conversation_id=conversation_id, generation=generation)
        try:
            probe = self.egress.require_stable_transport(request.endpoint)
            if not probe.healthy:
                raise CloudAPIUnavailable("transport is not healthy")
            self.delivery.mark_dispatched()
            return self.adapter.execute_native_agent(
                provider_request, self.sandbox, self.broker, self.registry,
                request.model, request.endpoint,
            )
        except Exception as exc:
            delivery = self.delivery.delivery
            if delivery is not None and delivery.state is DeliveryState.DISPATCHED:
                try:
                    self.delivery.mark_transport_unknown("agent outcome unknown")
                except DeliveryDenied as transition_error:
                    raise DispatchDenied("dispatch failed and reconciliation transition failed") from transition_error
            if isinstance(exc, DispatchDenied):
                raise
            raise DispatchDenied("agent dispatch failed closed; reconciliation required") from exc

    def acknowledge(self, response: str) -> None:
        try:
            self.delivery.mark_acknowledged(response)
        except DeliveryDenied as exc:
            raise DispatchDenied("provider result cannot be acknowledged") from exc

    def restore_for_current_session(self, *, session_id: str,
                                    conversation_id: str, generation: int):
        """Restore a durable delivery only when its identity matches exactly."""
        try:
            delivery = self.delivery.restore()
        except DeliveryDenied as exc:
            raise DispatchDenied("delivery checkpoint cannot be restored") from exc
        if (delivery.session_id != session_id or delivery.conversation_id != conversation_id
                or delivery.generation != generation):
            raise DispatchDenied("restored delivery identity does not match current session")
        if delivery.state is DeliveryState.SAFE_STOP:
            raise DispatchDenied("restored delivery is in SAFE_STOP")
        return delivery

    def reconcile_required(self) -> bool:
        delivery = self.delivery.delivery
        return delivery is not None and delivery.state is DeliveryState.RECONCILIATION_REQUIRED
