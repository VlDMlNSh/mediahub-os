"""MediaHub-owned deterministic AI execution-tier gateway.

The gateway selects a compute tier only. It never executes providers, mutates
State Authority, or grants authority to an AI system.
"""
from __future__ import annotations

from dataclasses import dataclass

from ops.ai.ai_routing import ProviderState, Route, RoutingDecision


class AIGatewayDenied(PermissionError):
    """Raised when a routing request cannot be admitted safely."""


@dataclass(frozen=True)
class AIRoutingRequest:
    request_id: str
    source_sha: str
    user_authorized: bool
    cloud_authorized: bool
    data_class: str = "non-sensitive"
    local_available: bool = True
    local_cluster_available: bool = False
    cloud_available: bool = False
    local_capable: bool = True
    local_cluster_capable: bool = True
    cloud_capable: bool = True
    privacy_local_only: bool = False
    requires_distributed_compute: bool = False
    requires_cloud_compute: bool = False


@dataclass(frozen=True)
class AIRoutingPolicy:
    exportable_data_classes: frozenset[str] = frozenset({"non-sensitive"})


class AIGateway:
    """Deterministic tier selection with deny-by-default cloud escalation."""

    def __init__(self, policy: AIRoutingPolicy | None = None) -> None:
        self.policy = policy or AIRoutingPolicy()

    def route(self, request: AIRoutingRequest) -> RoutingDecision:
        if not request.request_id or not request.source_sha:
            raise AIGatewayDenied("request identity and provenance are required")
        if not request.user_authorized:
            raise AIGatewayDenied("user authorization is required")

        if request.privacy_local_only:
            if request.local_available and request.local_capable:
                return RoutingDecision(Route.LOCAL, ProviderState.AVAILABLE, False, "privacy requires local")
            return self._safe_stop("local-only request has no local route")

        if request.requires_distributed_compute:
            if request.local_cluster_available and request.local_cluster_capable:
                return RoutingDecision(Route.LOCAL_CLUSTER, ProviderState.AVAILABLE, False, "distributed compute required")
            if request.requires_cloud_compute:
                return self._cloud_or_stop(request, "distributed compute unavailable locally")
            if request.local_available and request.local_capable:
                return RoutingDecision(Route.LOCAL, ProviderState.AVAILABLE, False, "bounded local fallback")
            return self._safe_stop("distributed compute unavailable")

        if request.local_available and request.local_capable and not request.requires_cloud_compute:
            return RoutingDecision(Route.LOCAL, ProviderState.AVAILABLE, False, "local-first route")

        if request.local_cluster_available and request.local_cluster_capable and not request.requires_cloud_compute:
            return RoutingDecision(Route.LOCAL_CLUSTER, ProviderState.AVAILABLE, False, "local cluster route")

        return self._cloud_or_stop(request, "local capacity unavailable")

    def _cloud_or_stop(self, request: AIRoutingRequest, reason: str) -> RoutingDecision:
        if not request.cloud_authorized:
            return self._safe_stop("cloud authorization is absent")
        if request.data_class not in self.policy.exportable_data_classes:
            return self._safe_stop("data class is not exportable")
        if not request.cloud_available or not request.cloud_capable:
            if request.local_cluster_available and request.local_cluster_capable:
                return RoutingDecision(Route.LOCAL_CLUSTER, ProviderState.TRANSIENT_FAILURE, False, "cloud unavailable; local cluster fallback")
            if request.local_available and request.local_capable:
                return RoutingDecision(Route.LOCAL, ProviderState.TRANSIENT_FAILURE, False, "cloud unavailable; local fallback")
            return self._safe_stop("cloud unavailable and no local route")
        return RoutingDecision(Route.CLOUD, ProviderState.AVAILABLE, False, reason)

    @staticmethod
    def _safe_stop(reason: str) -> RoutingDecision:
        return RoutingDecision(Route.SAFE_STOP, ProviderState.QUARANTINED, False, reason)
