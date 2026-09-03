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


def _proposal(action="configuration.propose", expires_delta=timedelta(minutes=5)):
    return Proposal(
        proposal_id="p-1",
        requested_action=action,
        target="runtime",
        confidence=0.5,
        generation="g-1",
        expires_at=datetime.now(timezone.utc) + expires_delta,
    )


def test_proposal_boundary_is_inert():
    boundary = ProposalPluginBoundary()
    result = boundary.accept_proposal(
        _proposal(), AuthorizationContext("ai", "configuration.propose")
    )
    assert type(result) is InertProposal
    assert not hasattr(boundary, "execute_proposal")
    assert not hasattr(boundary, "mutate")


def test_expired_proposal_fails_closed():
    with pytest.raises(Exception):
        ProposalPluginBoundary().accept_proposal(
            _proposal(expires_delta=timedelta(seconds=-1)),
            AuthorizationContext("ai", "configuration.propose"),
        )


def test_proposal_cannot_escape_p0_07_capability_inventory():
    with pytest.raises(PermissionError):
        ProposalPluginBoundary().accept_proposal(
            _proposal("shell.execute"),
            AuthorizationContext("ai", "configuration.propose"),
        )


def test_plugin_grant_is_exact_and_non_wildcard():
    for capability in P0_07_CAPABILITIES:
        grant = PluginCapabilityGrant("plugin-1", capability)
        assert grant.capability == capability
    with pytest.raises(ValueError):
        PluginCapabilityGrant("plugin-1", "configuration.*")


def test_plugin_grant_has_no_dynamic_grant_primitive():
    boundary = ProposalPluginBoundary()
    assert not hasattr(boundary, "grant_capability")
    assert not hasattr(boundary, "revoke_capability")


def test_plugin_grant_is_immutable():
    grant = PluginCapabilityGrant("plugin-1", "configuration.read")
    with pytest.raises(AttributeError):
        grant.capability = "configuration.delete"


def test_plugin_id_is_bounded():
    with pytest.raises(ValueError):
        PluginCapabilityGrant("x" * 129, "configuration.read")


def test_all_p0_07_capabilities_are_explicit():
    assert P0_07_CAPABILITIES == frozenset(
        {
            "configuration.read",
            "configuration.validate",
            "configuration.propose",
            "configuration.update",
            "configuration.replace",
            "configuration.reset",
            "configuration.delete",
            "policy.read",
            "policy.validate",
            "policy.propose",
            "policy.update",
            "policy.replace",
            "policy.reset",
            "policy.delete",
        }
    )
