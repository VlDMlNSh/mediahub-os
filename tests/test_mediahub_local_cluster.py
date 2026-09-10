import pytest

from ops.mediahub_local_cluster import (
    ClusterDenied,
    ClusterNode,
    ClusterWorkload,
    LocalClusterScheduler,
    NodeState,
    WorkloadClass,
)


def scheduler() -> LocalClusterScheduler:
    return LocalClusterScheduler(
        (
            ClusterNode("node-b", NodeState.READY, 16, 32768, 2),
            ClusterNode("node-a", NodeState.READY, 8, 16384, 1),
            ClusterNode("node-q", NodeState.QUARANTINED, 64, 131072, 8),
        )
    )


def test_schedule_is_deterministic_and_provenance_bound():
    workload = ClusterWorkload("w1", WorkloadClass.INFERENCE, 4, 4096, 0, "r4-sha")
    first = scheduler().schedule(workload)
    second = scheduler().schedule(workload)
    assert first == second
    assert first.node_id == "node-a"
    assert first.source_sha == "r4-sha"


def test_quarantined_and_degraded_nodes_are_not_eligible():
    nodes = (
        ClusterNode("bad", NodeState.QUARANTINED, 64, 65536, 8),
        ClusterNode("slow", NodeState.DEGRADED, 64, 65536, 8),
    )
    with pytest.raises(ClusterDenied):
        LocalClusterScheduler(nodes).schedule(
            ClusterWorkload("w1", WorkloadClass.BATCH, 1, 1, 0, "sha")
        )


def test_missing_provenance_and_identity_fail_closed():
    cluster = scheduler()
    with pytest.raises(ClusterDenied):
        cluster.schedule(ClusterWorkload("", WorkloadClass.MEDIA, 1, 1, 0, "sha"))
    with pytest.raises(ClusterDenied):
        cluster.schedule(ClusterWorkload("w", WorkloadClass.MEDIA, 1, 1, 0, ""))


def test_resource_overcommit_is_denied():
    cluster = scheduler()
    with pytest.raises(ClusterDenied):
        cluster.schedule(ClusterWorkload("w", WorkloadClass.INFERENCE, 99, 1, 0, "sha"))
    with pytest.raises(ClusterDenied):
        cluster.schedule(ClusterWorkload("w", WorkloadClass.INFERENCE, 1, 1, 99, "sha"))


def test_negative_resources_are_denied():
    cluster = scheduler()
    with pytest.raises(ClusterDenied):
        cluster.schedule(ClusterWorkload("w", WorkloadClass.MEDIA, 0, 1, 0, "sha"))
    with pytest.raises(ClusterDenied):
        cluster.schedule(ClusterWorkload("w", WorkloadClass.MEDIA, 1, 1, -1, "sha"))


def test_cluster_emits_assignment_only_and_cannot_mutate_authority():
    assignment = scheduler().schedule(
        ClusterWorkload("w", WorkloadClass.MEDIA, 1, 1, 0, "sha")
    )
    assert assignment.policy == "local-cluster-v1"
    assert not hasattr(assignment, "state")
