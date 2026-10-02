import json
from pathlib import Path


def load_registry():
    return json.loads(Path("profiles/agent-registry.json").read_text(encoding="utf-8"))


def test_openflux_is_qualification_gated_and_non_authoritative():
    data = load_registry()
    agent = next(a for a in data["agents"] if a["id"] == "openflux")
    assert agent["tier"] == "candidate_desktop_agent"
    assert agent["qualification"] == "pending"
    assert agent["authority"] == "none"
    assert agent["provider_selection"] is False
    assert agent["credential_creation"] is False
    assert agent["state_authority"] is False
    assert data["hybrid_fabric"]["qualification_states"]["openflux"] == "NOT_PROVEN"
    assert "openflux" in data["hybrid_fabric"]["candidate_desktop_agents"]


def test_openflux_does_not_become_a_control_plane_role():
    data = load_registry()
    agent = next(a for a in data["agents"] if a["id"] == "openflux")
    forbidden = {"A0-ASTRA", "A1", "A2", "A3"}
    assert agent["authority"] not in forbidden
    assert "openflux" not in data["hybrid_fabric"].get("local_agents", [])
