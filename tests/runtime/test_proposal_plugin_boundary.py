from datetime import datetime, timedelta, timezone

import pytest

from mediahub_runtime.authorization import AuthorizationContext
from mediahub_runtime.configuration_policy_authorization import P0_07_CAPABILITIES
from mediahub_runtime.proposal_plugin_boundary import (
    InertProposal,
    PluginCapabilityGrant,
    ProposalPluginBoundary,
)
from mediahub_runtime.proposals import Proposal


def make_proposal(action="configuration.propose"):
    return Proposal(
        proposal_id="p-1",
        requested_action=action,
        target="runtime",
        confidence=0.9,
        generation="g-1",
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=5),
    )


def test_accept_proposal_returns_inert_value():
    boundary = ProposalPluginBoundary()
    result = boundary.accept_proposal(
        make_proposal(), AuthorizationContext("ai", "configuration.propose")
    )
    assert type(result) is InertProposal
    assert result.proposal.proposal_id == "p-1"


def test_expired_proposal_is_rejected():
    boundary = ProposalPluginBoundary()
    proposal = Proposal(
        proposal_id="p-1",
        requested_action="configuration.propose",
        target="runtime",
        confidence=0.9,
        generation="g-1",
        expires_at=datetime.now(timezone.utc) - timedelta(seconds=1),
    )
    with pytest.raises(Exception):
        boundary.accept_proposal(proposal, AuthorizationContext("ai", "configuration.propose"))


def test_non_p0_07_proposal_action_is_denied():
    with pytest.raises(PermissionError):
        ProposalPluginBoundary().accept_proposal(
            make_proposal("shell.execute"),
            AuthorizationContext("ai", "configuration.propose"),
        )


def test_plugin_grant_requires_exact_capability():
    for capability in P0_07_CAPABILITIES:
        assert PluginCapabilityGrant("plugin-1", capability).capability == capability
    with pytest.raises(ValueError):
        PluginCapabilityGrant("plugin-1", "configuration.*")


def test_plugin_grant_is_immutable_and_validation_only():
    boundary = ProposalPluginBoundary()
    grant = PluginCapabilityGrant("plugin-1", "configuration.read")
    assert boundary.validate_plugin_grant(grant) == grant
    with pytest.raises(AttributeError):
        grant.capability = "configuration.delete"
    assert not hasattr(boundary, "grant_capability")
    assert not hasattr(boundary, "execute_proposal")
