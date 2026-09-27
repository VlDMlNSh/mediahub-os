"""Admission-aware Local Cluster failover and deterministic recovery evidence."""
from __future__ import annotations

from dataclasses import dataclass

from ops.mediahub_cluster_health import LocalClusterHealth, NodeHealth
from ops.mediahub_cluster_lifecycle import (
    ClusterWorkloadLifecycle,
    FailureClass,
    LifecycleDenied,
    LifecycleRecord,
    LifecycleState,
    WorkloadIdentity,
)
from ops.mediahub_cluster_membership import LocalClusterMembership, MembershipDenied
from ops.mediahub_cluster_resources import (
    ClusterResourceLedger,
    ResourceCapacity,
    ResourceDenied,
    ResourceReservation,
)
from ops.mediahub_local_cluster import ClusterNode, ClusterWorkload, NodeState


class FailoverDenied(PermissionError):
    """Raised when replacement admission cannot be proven safe."""


@dataclass(frozen=True)
class RecoveryEvidence:
    workload_id: str
    request_id: str
    source_sha: str
    previous_assignment_id: str
    previous_node_id: str
    replacement_assignment_id: str
    replacement_node_id: str
    failure: FailureClass
    verified: bool
    evidence_id: str


class AdmissionAwareFailover:
    """Coordinate failover admission without authority, network, or execution side effects."""

    def __init__(
        self,
        lifecycle: ClusterWorkloadLifecycle,
        membership: LocalClusterMembership,
        health: LocalClusterHealth,
        resources: ClusterResourceLedger,
        nodes: tuple[ClusterNode, ...],
    ) -> None:
        self._lifecycle = lifecycle
        self._membership = membership
        self._health = health
        self._resources = resources
        self._nodes = {node.node_id: node for node in nodes}
        self._evidence: dict[str, RecoveryEvidence] = {}

    def failover(
        self,
        workload: ClusterWorkload,
        failure: FailureClass,
        new_assignment_id: str,
        new_node_id: str,
        critical: bool = False,
    ) -> RecoveryEvidence:
        self._validate_workload(workload)
        if not new_assignment_id or not new_node_id:
            raise FailoverDenied("replacement identity is required")
        current = self._lifecycle.record(workload.workload_id)
        if current.state is not LifecycleState.RUNNING:
            raise FailoverDenied("failover requires running workload")
        if current.identity.source_sha != workload.source_sha:
            raise FailoverDenied("workload provenance mismatch")
        if current.identity.request_id == "":
            raise FailoverDenied("request identity is required")
        if new_node_id == current.identity.node_id:
            raise FailoverDenied("replacement node must differ from failed node")
        self._admit_replacement(workload, new_node_id, critical)
        old_reservation = self._resources.reserved(workload.workload_id)
        if old_reservation is None or old_reservation.node_id != current.identity.node_id:
            raise FailoverDenied("current resource reservation is required")
        replacement = ResourceReservation(
            workload.workload_id,
            new_node_id,
            ResourceCapacity(workload.cpu, workload.memory_mb, workload.gpu),
        )
        if not self._resources.can_replace(replacement):
            raise FailoverDenied("replacement resources are not admissible")
        try:
            decision = self._lifecycle.failover(workload.workload_id, failure)
            if not decision.allowed:
                raise FailoverDenied(decision.reason)
            replacement = ResourceReservation(
                workload.workload_id,
                new_node_id,
                ResourceCapacity(workload.cpu, workload.memory_mb, workload.gpu),
            )
            self._resources.replace(replacement)
            record = self._lifecycle.reassign(workload.workload_id, new_assignment_id, new_node_id)
        except (LifecycleDenied, ResourceDenied) as exc:
            self._resources.replace(old_reservation)
            raise FailoverDenied(str(exc)) from exc
        evidence = self._record_evidence(current.identity, record, failure)
        self._evidence[workload.workload_id] = evidence
        return evidence

    def evidence(self, workload_id: str) -> RecoveryEvidence | None:
        return self._evidence.get(workload_id)

    def verify_and_recover(self, workload_id: str) -> RecoveryEvidence:
        evidence = self._evidence.get(workload_id)
        if evidence is None:
            raise FailoverDenied("recovery evidence is required")
        if self._lifecycle.record(workload_id).state is not LifecycleState.REASSIGNED:
            raise FailoverDenied("verification requires reassigned workload")
        self._lifecycle.transition(workload_id, LifecycleState.VERIFIED)
        self._lifecycle.transition(workload_id, LifecycleState.RECOVERED)
        verified = RecoveryEvidence(
            evidence.workload_id, evidence.request_id, evidence.source_sha,
            evidence.previous_assignment_id, evidence.previous_node_id,
            evidence.replacement_assignment_id, evidence.replacement_node_id,
            evidence.failure, True, evidence.evidence_id,
        )
        self._evidence[workload_id] = verified
        return verified

    def _admit_replacement(self, workload: ClusterWorkload, node_id: str, critical: bool) -> None:
        node = self._nodes.get(node_id)
        if node is None:
            raise FailoverDenied("unknown replacement node")
        if node.state is not NodeState.READY:
            raise FailoverDenied("replacement node is not ready")
        try:
            self._membership.require_active(node_id)
        except MembershipDenied as exc:
            raise FailoverDenied(str(exc)) from exc
        observation = self._health.get(node_id)
        if observation is None or observation.health is not NodeHealth.HEALTHY:
            if critical and observation is not None and observation.health is NodeHealth.DEGRADED:
                raise FailoverDenied("degraded node cannot receive critical workload")
            raise FailoverDenied("replacement node health is not healthy")
        if observation.source_sha != self._membership.require_active(node_id).identity.source_sha:
            raise FailoverDenied("node health provenance mismatch")
        if node.cpu_capacity < workload.cpu or node.memory_mb < workload.memory_mb or node.gpu_count < workload.gpu:
            raise FailoverDenied("replacement node lacks requested resources")

    @staticmethod
    def _validate_workload(workload: ClusterWorkload) -> None:
        if not isinstance(workload, ClusterWorkload):
            raise FailoverDenied("malformed workload")
        if not all(isinstance(value, str) for value in (workload.workload_id, workload.source_sha)):
            raise FailoverDenied("malformed workload identity")
        if not all(isinstance(value, int) and not isinstance(value, bool)
                   for value in (workload.cpu, workload.memory_mb, workload.gpu)):
            raise FailoverDenied("malformed workload resources")
        if not workload.workload_id or not workload.source_sha:
            raise FailoverDenied("workload identity and provenance are required")
        if workload.cpu <= 0 or workload.memory_mb <= 0 or workload.gpu < 0:
            raise FailoverDenied("invalid workload resource request")

    @staticmethod
    def _record_evidence(
        previous: WorkloadIdentity, current: LifecycleRecord, failure: FailureClass
    ) -> RecoveryEvidence:
        if current.state is not LifecycleState.REASSIGNED:
            raise FailoverDenied("replacement was not recorded")
        identity = current.identity
        evidence_id = (
            f"{identity.workload_id}:{previous.assignment_id}:{identity.assignment_id}:"
            f"{previous.node_id}:{identity.node_id}:{failure.value}:{identity.source_sha}"
        )
        return RecoveryEvidence(
            identity.workload_id, identity.request_id, identity.source_sha,
            previous.assignment_id, previous.node_id, identity.assignment_id,
            identity.node_id, failure, False, evidence_id,
        )
