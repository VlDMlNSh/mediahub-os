"""Fail-closed Local MediaHub Cluster node identity and membership contract.

Membership is a trust gate, not authorization and not canonical state.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class MembershipState(StrEnum):
    DISCOVERED = "DISCOVERED"
    VERIFIED = "VERIFIED"
    ENROLLED = "ENROLLED"
    ACTIVE = "ACTIVE"
    REVOKED = "REVOKED"
    QUARANTINED = "QUARANTINED"


class MembershipDenied(PermissionError):
    """Raised when node membership cannot be proven admissible."""


@dataclass(frozen=True)
class ClusterNodeIdentity:
    node_id: str
    identity_id: str
    source_sha: str


@dataclass(frozen=True)
class ClusterMembership:
    identity: ClusterNodeIdentity
    state: MembershipState


class LocalClusterMembership:
    """Deterministic enrollment/revocation gate for cluster nodes."""

    def __init__(self) -> None:
        self._members: dict[str, ClusterMembership] = {}

    def enroll(self, identity: ClusterNodeIdentity) -> ClusterMembership:
        self._validate_identity(identity)
        current = self._members.get(identity.node_id)
        if current is not None and current.state is MembershipState.REVOKED:
            raise MembershipDenied("revoked node cannot be re-enrolled")
        membership = ClusterMembership(identity, MembershipState.ENROLLED)
        self._members[identity.node_id] = membership
        return membership

    def activate(self, node_id: str) -> ClusterMembership:
        membership = self._members.get(node_id)
        if membership is None or membership.state is not MembershipState.ENROLLED:
            raise MembershipDenied("only enrolled nodes can become active")
        updated = ClusterMembership(membership.identity, MembershipState.ACTIVE)
        self._members[node_id] = updated
        return updated

    def revoke(self, node_id: str) -> ClusterMembership:
        membership = self._members.get(node_id)
        if membership is None:
            raise MembershipDenied("unknown node cannot be revoked into membership")
        updated = ClusterMembership(membership.identity, MembershipState.REVOKED)
        self._members[node_id] = updated
        return updated

    def require_active(self, node_id: str) -> ClusterMembership:
        membership = self._members.get(node_id)
        if membership is None or membership.state is not MembershipState.ACTIVE:
            raise MembershipDenied("node is not an active trusted member")
        return membership

    @staticmethod
    def _validate_identity(identity: ClusterNodeIdentity) -> None:
        if not identity.node_id or not identity.identity_id or not identity.source_sha:
            raise MembershipDenied("node identity and provenance are required")
