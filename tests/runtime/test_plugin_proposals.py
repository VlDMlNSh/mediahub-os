import pytest

from mediahub_runtime.plugin_capabilities import CapabilityRequest
from mediahub_runtime.plugin_proposals import InertPluginProposal, PluginProposalError


def request():
    return CapabilityRequest("example.plugin", "media.read", "read")


def test_proposal_is_inert_data():
    proposal = InertPluginProposal("example.plugin", request(), {"item": "value"})
    assert proposal.is_inert
    assert proposal.to_observation()["operation"] == "read"


def test_proposal_payload_is_deeply_immutable():
    payload = {"items": [{"value": "original"}]}
    proposal = InertPluginProposal("example.plugin", request(), payload)
    payload["items"][0]["value"] = "changed"
    assert proposal.payload["items"][0]["value"] == "original"
    with pytest.raises(TypeError):
        proposal.payload["items"][0]["value"] = "blocked"


def test_proposal_identity_must_match_request():
    with pytest.raises(PluginProposalError):
        InertPluginProposal("forged.plugin", request(), {})


def test_proposal_rejects_oversized_structure():
    with pytest.raises(PluginProposalError):
        InertPluginProposal("example.plugin", request(), {"items": list(range(600))})


def test_proposal_has_no_execution_or_authority_surface():
    proposal = InertPluginProposal("example.plugin", request(), {})
    for name in ("execute", "commit", "authorize", "grant", "state_authority", "persistence", "filesystem", "network", "subprocess"):
        with pytest.raises(AttributeError):
            getattr(proposal, name)
