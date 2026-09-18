import pytest

from ops.mediahub_cluster_membership import (
    ClusterNodeIdentity,
    LocalClusterMembership,
    MembershipDenied,
    MembershipState,
)


def identity(node_id="node-a", identity_id="identity-a", source_sha="sha"):
    return ClusterNodeIdentity(node_id, identity_id, source_sha)


def test_enrollment_requires_identity_and_provenance():
    membership = LocalClusterMembership()
    with pytest.raises(MembershipDenied):
        membership.enroll(identity(source_sha=""))
    with pytest.raises(MembershipDenied):
        membership.enroll(identity(identity_id=""))
    with pytest.raises(MembershipDenied):
        membership.enroll(identity(node_id=""))


def test_enrolled_node_is_not_active_until_explicit_activation():
    membership = LocalClusterMembership()
    enrolled = membership.enroll(identity())
    assert enrolled.state is MembershipState.ENROLLED
    with pytest.raises(MembershipDenied):
        membership.require_active("node-a")


def test_active_membership_requires_enrollment():
    membership = LocalClusterMembership()
    with pytest.raises(MembershipDenied):
        membership.activate("unknown")


def test_enrolled_node_can_be_activated():
    membership = LocalClusterMembership()
    membership.enroll(identity())
    active = membership.activate("node-a")
    assert active.state is MembershipState.ACTIVE
    assert membership.require_active("node-a") == active


def test_unknown_node_fails_closed():
    with pytest.raises(MembershipDenied):
        LocalClusterMembership().require_active("unknown")


def test_revocation_is_terminal_for_reenrollment():
    membership = LocalClusterMembership()
    membership.enroll(identity())
    revoked = membership.revoke("node-a")
    assert revoked.state is MembershipState.REVOKED
    with pytest.raises(MembershipDenied):
        membership.enroll(identity())
    with pytest.raises(MembershipDenied):
        membership.require_active("node-a")


def test_revocation_of_unknown_node_is_denied():
    with pytest.raises(MembershipDenied):
        LocalClusterMembership().revoke("unknown")


def test_discovered_or_quarantined_states_are_not_active():
    membership = LocalClusterMembership()
    assert MembershipState.DISCOVERED is not MembershipState.ACTIVE
    assert MembershipState.QUARANTINED is not MembershipState.ACTIVE
    membership.enroll(identity())
    membership.revoke("node-a")
    with pytest.raises(MembershipDenied):
        membership.require_active("node-a")


def test_membership_preserves_node_identity_and_provenance():
    membership = LocalClusterMembership()
    enrolled = membership.enroll(identity("node-b", "identity-b", "source-b"))
    assert enrolled.identity.node_id == "node-b"
    assert enrolled.identity.identity_id == "identity-b"
    assert enrolled.identity.source_sha == "source-b"


def test_membership_does_not_expose_authority_or_network_access():
    membership = LocalClusterMembership()
    assert not hasattr(membership, "state_authority")
    assert not hasattr(membership, "network")


def test_active_node_can_be_quarantined_and_is_not_active():
    membership = LocalClusterMembership()
    membership.enroll(identity())
    membership.activate("node-a")
    quarantined = membership.quarantine("node-a")
    assert quarantined.state is MembershipState.QUARANTINED
    with pytest.raises(MembershipDenied):
        membership.require_active("node-a")

def test_enrollment_rejects_malformed_identity_types():
    membership = LocalClusterMembership()
    for value in (object(), None, 1, True):
        with pytest.raises(MembershipDenied):
            membership.enroll(value)
    with pytest.raises(MembershipDenied):
        membership.enroll(identity(node_id=1))
    with pytest.raises(MembershipDenied):
        membership.enroll(identity(identity_id=True))
    with pytest.raises(MembershipDenied):
        membership.enroll(identity(source_sha=None))
