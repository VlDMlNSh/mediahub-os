from __future__ import annotations

import inspect

import pytest

from ops.mediahub_cluster_lifecycle import (
    ClusterWorkloadLifecycle,
    FailureClass,
    LifecycleDenied,
    LifecycleState,
    WorkloadIdentity,
)


@pytest.fixture
def identity() -> WorkloadIdentity:
    return WorkloadIdentity("w1", "a1", "n1", "r1", "sha1")


@pytest.fixture
def lifecycle() -> ClusterWorkloadLifecycle:
    return ClusterWorkloadLifecycle()


def test_admit_start_complete(lifecycle: ClusterWorkloadLifecycle, identity: WorkloadIdentity) -> None:
    assert lifecycle.admit(identity).state is LifecycleState.ADMITTED
    assert lifecycle.transition("w1", LifecycleState.RUNNING).state is LifecycleState.RUNNING
    assert lifecycle.transition("w1", LifecycleState.COMPLETED).state is LifecycleState.COMPLETED


def test_unknown_workload_denied(lifecycle: ClusterWorkloadLifecycle) -> None:
    with pytest.raises(LifecycleDenied):
        lifecycle.transition("missing", LifecycleState.RUNNING)


def test_missing_identity_or_provenance_denied(lifecycle: ClusterWorkloadLifecycle) -> None:
    with pytest.raises(LifecycleDenied):
        lifecycle.admit(WorkloadIdentity("", "a1", "n1", "r1", "sha1"))
    with pytest.raises(LifecycleDenied):
        lifecycle.admit(WorkloadIdentity("w1", "a1", "n1", "r1", ""))


def test_duplicate_workload_and_assignment_denied(
    lifecycle: ClusterWorkloadLifecycle, identity: WorkloadIdentity
) -> None:
    lifecycle.admit(identity)
    with pytest.raises(LifecycleDenied):
        lifecycle.admit(identity)
    with pytest.raises(LifecycleDenied):
        lifecycle.admit(WorkloadIdentity("w2", "a1", "n1", "r1", "sha1"))


def test_invalid_transition_denied(lifecycle: ClusterWorkloadLifecycle, identity: WorkloadIdentity) -> None:
    lifecycle.admit(identity)
    with pytest.raises(LifecycleDenied):
        lifecycle.transition("w1", LifecycleState.RECOVERED)


def test_ambiguous_failure_is_fail_closed(lifecycle: ClusterWorkloadLifecycle, identity: WorkloadIdentity) -> None:
    lifecycle.admit(identity)
    lifecycle.transition("w1", LifecycleState.RUNNING)
    decision = lifecycle.failover("w1", FailureClass.AMBIGUOUS)
    assert not decision.allowed
    assert lifecycle.record("w1").state is LifecycleState.RUNNING


def test_failed_node_allows_bounded_failover(lifecycle: ClusterWorkloadLifecycle, identity: WorkloadIdentity) -> None:
    lifecycle.admit(identity)
    lifecycle.transition("w1", LifecycleState.RUNNING)
    decision = lifecycle.failover("w1", FailureClass.NODE_FAILED)
    assert decision.allowed
    assert lifecycle.record("w1").state is LifecycleState.FAILED


def test_reassignment_requires_failed_state(lifecycle: ClusterWorkloadLifecycle, identity: WorkloadIdentity) -> None:
    lifecycle.admit(identity)
    with pytest.raises(LifecycleDenied):
        lifecycle.reassign("w1", "a2", "n2")


def test_reassignment_identity_is_new_and_provenance_preserved(
    lifecycle: ClusterWorkloadLifecycle, identity: WorkloadIdentity
) -> None:
    lifecycle.admit(identity)
    lifecycle.transition("w1", LifecycleState.RUNNING)
    lifecycle.failover("w1", FailureClass.NODE_FAILED)
    record = lifecycle.reassign("w1", "a2", "n2")
    assert record.state is LifecycleState.REASSIGNED
    assert record.identity.assignment_id == "a2"
    assert record.identity.node_id == "n2"
    assert record.identity.source_sha == "sha1"
    with pytest.raises(LifecycleDenied):
        lifecycle.reassign("w1", "a2", "n3")


def test_reassignment_verification_and_recovery(lifecycle: ClusterWorkloadLifecycle, identity: WorkloadIdentity) -> None:
    lifecycle.admit(identity)
    lifecycle.transition("w1", LifecycleState.RUNNING)
    lifecycle.failover("w1", FailureClass.NODE_FAILED)
    lifecycle.reassign("w1", "a2", "n2")
    lifecycle.transition("w1", LifecycleState.VERIFIED)
    assert lifecycle.transition("w1", LifecycleState.RECOVERED).state is LifecycleState.RECOVERED


def test_terminal_states_cannot_be_reassigned(lifecycle: ClusterWorkloadLifecycle, identity: WorkloadIdentity) -> None:
    lifecycle.admit(identity)
    lifecycle.transition("w1", LifecycleState.RUNNING)
    lifecycle.transition("w1", LifecycleState.COMPLETED)
    with pytest.raises(LifecycleDenied):
        lifecycle.failover("w1", FailureClass.WORKLOAD_FAILED)


def test_lifecycle_has_no_authority_or_network_imports() -> None:
    source = inspect.getsource(__import__("ops.mediahub_cluster_lifecycle", fromlist=["x"]))
    forbidden = ("requests", "urllib", "socket", "subprocess", "state_authority", "home_assistant")
    assert not any(token in source.lower() for token in forbidden)

def test_admit_rejects_malformed_identity_types(lifecycle):
    for value in (object(), None, 1, True):
        with pytest.raises(LifecycleDenied):
            lifecycle.admit(value)
    with pytest.raises(LifecycleDenied):
        lifecycle.admit(WorkloadIdentity(1, "a1", "n1", "r1", "sha1"))
    with pytest.raises(LifecycleDenied):
        lifecycle.admit(WorkloadIdentity("w1", True, "n1", "r1", "sha1"))
    with pytest.raises(LifecycleDenied):
        lifecycle.admit(WorkloadIdentity("w1", "a1", "n1", None, "sha1"))
