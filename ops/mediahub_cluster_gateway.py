"""Governed boundary from AI routing to Local Cluster execution.

The gateway creates execution proposals only; it never mutates State Authority.
"""
from __future__ import annotations

from dataclasses import dataclass

from ops.ai.ai_routing import Route, RoutingDecision
from ops.mediahub_local_cluster import (
    ClusterAssignment,
    ClusterDenied,
    ClusterWorkload,
    LocalClusterScheduler,
)


class ClusterGatewayDenied(PermissionError):
    """Raised when the Local Cluster route cannot be proven admissible."""


@dataclass(frozen=True)
class ClusterExecutionProposal:
    request_id: str
    assignment: ClusterAssignment
    route: Route
    source_sha: str


class LocalClusterGateway:
    """Translate an approved LOCAL_CLUSTER decision into a bounded proposal."""

    def __init__(self, scheduler: LocalClusterScheduler) -> None:
        self._scheduler = scheduler

    def propose(
        self,
        request_id: str,
        workload: ClusterWorkload,
        decision: RoutingDecision,
    ) -> ClusterExecutionProposal:
        if not request_id:
            raise ClusterGatewayDenied("request identity is required")
        if decision.route is not Route.LOCAL_CLUSTER:
            raise ClusterGatewayDenied("LOCAL_CLUSTER route authorization required")
        if decision.provider_state.value not in {"AVAILABLE", "TRANSIENT_FAILURE", "POLICY_BLOCKED", "QUARANTINED"}:
            raise ClusterGatewayDenied("unknown routing state")
        if not workload.source_sha:
            raise ClusterGatewayDenied("workload provenance is required")
        try:
            assignment = self._scheduler.schedule(workload)
        except ClusterDenied as exc:
            raise ClusterGatewayDenied(str(exc)) from exc
        return ClusterExecutionProposal(request_id, assignment, Route.LOCAL_CLUSTER, workload.source_sha)
