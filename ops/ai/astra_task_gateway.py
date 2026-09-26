"""Canonical Astra task ingress over existing MediaHub AI boundaries.
This gateway composes admission, routing, edge execution and reconciliation;
it does not become a state or policy authority.
"""
from __future__ import annotations

from dataclasses import dataclass

from ops.ai.ai_gateway import AIGateway, AIRoutingRequest
from ops.ai.astra_edge_adapter import AstraEdgeAdapter, EdgeResult, EdgeStatus, EdgeTask
from ops.ai.ai_routing import Route
from runtime.mediahub_runtime.consumer_boundary import ConsumerBoundary


class AstraTaskDenied(PermissionError):
    """Raised when a canonical Astra task cannot be admitted."""


@dataclass(frozen=True)
class CanonicalAstraTask:
    request_id: str
    session_id: str
    user_command: str
    approval_state: str
    source_sha: str
    user_authorized: bool = True
    cloud_authorized: bool = False
    data_class: str = "non-sensitive"
    privacy_local_only: bool = False
    requires_distributed_compute: bool = False
    requires_cloud_compute: bool = False


class AstraTaskGateway:
    """Thin composition boundary for the existing MediaHub runtime."""

    def __init__(self, *, ai_gateway: AIGateway | None = None,
                 edge: AstraEdgeAdapter | None = None) -> None:
        self.ai_gateway = ai_gateway or AIGateway()
        self.edge = edge or AstraEdgeAdapter()

    @staticmethod
    def validate(task: CanonicalAstraTask) -> None:
        if not isinstance(task, CanonicalAstraTask):
            raise AstraTaskDenied("invalid_task")
        values = (task.request_id, task.session_id, task.user_command, task.source_sha)
        if any(not isinstance(v, str) or not v or v.strip() != v for v in values):
            raise AstraTaskDenied("invalid_task_identity")
        if task.approval_state not in {"not_required", "approved"}:
            raise AstraTaskDenied("approval_required")
        if len(task.user_command.encode("utf-8")) > 64 * 1024:
            raise AstraTaskDenied("command_too_large")
    def dispatch(self, task: CanonicalAstraTask, boundary: ConsumerBoundary,
                 request, *, expected_generation: int | None = None) -> EdgeResult:
        self.validate(task)
        routing = self.ai_gateway.route(AIRoutingRequest(
            request_id=task.request_id,
            source_sha=task.source_sha,
            user_authorized=task.user_authorized,
            cloud_authorized=task.cloud_authorized,
            data_class=task.data_class,
            local_available=True,
            local_cluster_available=False,
            cloud_available=False,
            privacy_local_only=task.privacy_local_only,
            requires_distributed_compute=task.requires_distributed_compute,
            requires_cloud_compute=task.requires_cloud_compute,
            prompt_chars=len(task.user_command),
        ))
        edge_task = EdgeTask(
            task.request_id, task.session_id, task.user_command, task.approval_state
        )
        if routing.route is Route.LOCAL:
            return self.edge.execute_and_reconcile(
                edge_task, boundary, request,
                expected_generation=expected_generation,
            )
        return EdgeResult(
            task.request_id, routing.route, EdgeStatus.BLOCKED,
            error_code="route_requires_upstream_or_cluster",
        )
