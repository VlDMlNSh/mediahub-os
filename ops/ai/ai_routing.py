"""Deterministic, fail-closed AI routing safety state machine."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ProviderState(StrEnum):
    AVAILABLE = "AVAILABLE"
    TRANSIENT_FAILURE = "TRANSIENT_FAILURE"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    QUARANTINED = "QUARANTINED"


class Route(StrEnum):
    LOCAL = "LOCAL"
    LOCAL_CLUSTER = "LOCAL_CLUSTER"
    CLOUD = "CLOUD"
    SAFE_STOP = "SAFE_STOP"


@dataclass(frozen=True)
class RoutingDecision:
    route: Route
    provider_state: ProviderState
    retry_allowed: bool
    reason: str


_POLICY_BLOCK_MARKERS = (
    "403",
    "access denied by security policy",
    "country, region, or territory not supported",
    "not authorized",
)


def classify_provider_failure(message: str) -> ProviderState:
    """Classify external failures without treating policy denial as transient."""
    normalized = message.casefold()
    if any(marker in normalized for marker in _POLICY_BLOCK_MARKERS):
        return ProviderState.POLICY_BLOCKED
    if not normalized.strip():
        return ProviderState.TRANSIENT_FAILURE
    return ProviderState.TRANSIENT_FAILURE


def decide_cloud_failure(
    state: ProviderState,
    *,
    local_cluster_available: bool,
    local_available: bool,
) -> RoutingDecision:
    """Select only the explicitly approved local fallback chain."""
    if state is ProviderState.POLICY_BLOCKED:
        if local_cluster_available:
            return RoutingDecision(Route.LOCAL_CLUSTER, state, False, "cloud policy blocked")
        if local_available:
            return RoutingDecision(Route.LOCAL, state, False, "cloud policy blocked")
        return RoutingDecision(Route.SAFE_STOP, state, False, "cloud policy blocked; no local route")

    if state is ProviderState.QUARANTINED:
        if local_cluster_available:
            return RoutingDecision(Route.LOCAL_CLUSTER, state, False, "cloud quarantined")
        if local_available:
            return RoutingDecision(Route.LOCAL, state, False, "cloud quarantined")
        return RoutingDecision(Route.SAFE_STOP, state, False, "cloud quarantined; no local route")

    if state is ProviderState.TRANSIENT_FAILURE:
        if local_cluster_available:
            return RoutingDecision(Route.LOCAL_CLUSTER, state, False, "cloud transient failure")
        if local_available:
            return RoutingDecision(Route.LOCAL, state, False, "cloud transient failure")
        return RoutingDecision(Route.SAFE_STOP, state, False, "cloud transient failure; no local route")

    return RoutingDecision(Route.CLOUD, ProviderState.AVAILABLE, False, "cloud available")
