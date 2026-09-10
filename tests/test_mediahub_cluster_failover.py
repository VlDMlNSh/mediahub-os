from __future__ import annotations

import inspect

import pytest

from ops.mediahub_cluster_failover import AdmissionAwareFailover, FailoverDenied
from ops.mediahub_cluster_health import (
    LocalClusterHealth,
    NodeHealth,
    NodeHealthObservation,
)
from ops.mediahub_cluster_lifecycle import (
    ClusterWorkloadLifecycle,
    FailureClass,
    LifecycleDenied,
    LifecycleState,
    WorkloadIdentity,
)
from ops.mediahub_cluster_membership import ClusterNodeIdentity, LocalClusterMembership
from ops.mediahub_cluster_resources import (
    ClusterResourceLedger,
    ResourceCapacity,
    ResourceReservation,
)
from ops.mediahub_local_cluster import (
    ClusterNode,
    ClusterWorkload,
    NodeState,
    WorkloadClass,
)


def make_env(health=NodeHealth.HEALTHY, node_state=NodeState.READY, quarantine=False):
    lifecycle = ClusterWorkloadLifecycle()
    membership = LocalClusterMembership()
    node = ClusterNode("node-b", node_state, 8, 8192, 1)
    membership.enroll(ClusterNodeIdentity("node-b", "identity-b", "sha-node"))
    membership.activate("node-b")
    if health is NodeHealth.FAILED:
        membership.revoke("node-b")
    elif health is NodeHealth.DEGRADED and quarantine:
        membership.quarantine("node-b")
    cluster_health = LocalClusterHealth()
    cluster_health.observe(NodeHealthObservation("node-b", health, "sha-node"))
    resources = ClusterResourceLedger({"node-a": ResourceCapacity(8, 8192, 1), "node-b": ResourceCapacity(8, 8192, 1)})
    identity = WorkloadIdentity("w1", "a1", "node-a", "req-1", "sha-work")
    lifecycle.admit(identity)
    lifecycle.transition("w1", LifecycleState.RUNNING)
    resources.reserve(ResourceReservation("w1", "node-a", ResourceCapacity(2, 1024, 0)))
    workload = ClusterWorkload("w1", WorkloadClass.INFERENCE, 2, 1024, 0, "sha-work")
    return AdmissionAwareFailover(lifecycle, membership, cluster_health, resources, (node,)), lifecycle, resources, workload


def test_failover_admits_trusted_healthy_replacement():
    coordinator, lifecycle, resources, workload = make_env()
    evidence = coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
    assert evidence.verified is False
    assert evidence.source_sha == "sha-work"
    assert resources.reserved("w1").node_id == "node-b"
    assert lifecycle.record("w1").state is LifecycleState.REASSIGNED


def test_verify_and_recover_records_deterministic_evidence():
    coordinator, lifecycle, _, workload = make_env()
    first = coordinator.failover(workload, FailureClass.WORKLOAD_FAILED, "a2", "node-b")
    second = coordinator.evidence("w1")
    assert second == first
    recovered = coordinator.verify_and_recover("w1")
    assert recovered.verified is True
    assert recovered.evidence_id == first.evidence_id
    assert lifecycle.record("w1").state is LifecycleState.RECOVERED


def test_revoked_replacement_denied():
    coordinator, lifecycle, resources, workload = make_env(health=NodeHealth.FAILED)
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
    assert lifecycle.record("w1").state is LifecycleState.RUNNING
    assert resources.reserved("w1").node_id == "node-a"


def test_quarantined_replacement_denied():
    coordinator, lifecycle, _, workload = make_env(health=NodeHealth.DEGRADED)
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b", critical=True)
    assert lifecycle.record("w1").state is LifecycleState.RUNNING


def test_unknown_replacement_denied():
    coordinator, lifecycle, _, workload = make_env()
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "missing")
    assert lifecycle.record("w1").state is LifecycleState.RUNNING


def test_resource_overcommit_denied():
    coordinator, lifecycle, _, workload = make_env()
    coordinator._resources.reserve(ResourceReservation("other", "node-b", ResourceCapacity(7, 7000, 1)))
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
    assert lifecycle.record("w1").state is LifecycleState.RUNNING


def test_cpu_memory_gpu_capacity_denied():
    for cpu, memory, gpu in [(9, 1024, 0), (2, 9000, 0), (2, 1024, 2)]:
        coordinator, lifecycle, _, _ = make_env()
        workload = ClusterWorkload("w1", WorkloadClass.INFERENCE, cpu, memory, gpu, "sha-work")
        with pytest.raises(FailoverDenied):
            coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
        assert lifecycle.record("w1").state is LifecycleState.RUNNING


def test_provenance_mismatch_denied():
    coordinator, lifecycle, _, _ = make_env()
    workload = ClusterWorkload("w1", WorkloadClass.INFERENCE, 2, 1024, 0, "other-sha")
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
    assert lifecycle.record("w1").state is LifecycleState.RUNNING


def test_ambiguous_failure_is_fail_closed_without_mutation():
    coordinator, lifecycle, resources, workload = make_env()
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.AMBIGUOUS, "a2", "node-b")
    assert lifecycle.record("w1").state is LifecycleState.RUNNING
    assert resources.reserved("w1").node_id == "node-a"


def test_duplicate_reassignment_and_invalid_lifecycle_denied():
    coordinator, lifecycle, _, workload = make_env()
    coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.NODE_FAILED, "a3", "node-b")
    with pytest.raises(LifecycleDenied):
        lifecycle.transition("w1", LifecycleState.ADMITTED)


def test_request_identity_is_preserved_and_boundary_has_no_bypass():
    coordinator, _, _, workload = make_env()
    evidence = coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
    assert evidence.request_id == "req-1"
    source = inspect.getsource(__import__("ops.mediahub_cluster_failover", fromlist=["x"]))
    forbidden = ("requests", "urllib", "socket", "subprocess", "state_authority", "home_assistant")
    assert not any(token in source.lower() for token in forbidden)
    assert not hasattr(coordinator, "state_authority")


def test_degraded_health_denies_critical_replacement():
    coordinator, lifecycle, _, workload = make_env(health=NodeHealth.DEGRADED)
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b", critical=True)
    assert lifecycle.record("w1").state is LifecycleState.RUNNING


def test_quarantined_membership_denies_replacement():
    coordinator, lifecycle, _, workload = make_env(health=NodeHealth.DEGRADED, quarantine=True)
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
    assert lifecycle.record("w1").state is LifecycleState.RUNNING


def test_not_ready_replacement_denied():
    coordinator, lifecycle, _, workload = make_env(node_state=NodeState.DEGRADED)
    with pytest.raises(FailoverDenied):
        coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
    assert lifecycle.record("w1").state is LifecycleState.RUNNING
