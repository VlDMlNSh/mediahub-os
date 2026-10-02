from pathlib import Path
import yaml

SCHEMA = Path("architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml")

def load():
    return yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))

def test_canonical_gate_order_and_fail_closed():
    data = load()
    assert list(data["gates"]) == [
        "G0_IDENTITY", "G1_BOUNDARY", "G2_CONTROL_PLANE", "G3_EXECUTION_PATH",
        "G4_23_WAVE_QUALIFICATION", "G5_CONCURRENCY", "G6_RECOVERY",
        "G7_INTEGRATED_A3", "G8_PRE_SOAK", "G9_24H_SOAK",
        "G10_LAUNCH_READY", "G11_LAUNCH"
    ]
    assert data["principles"]["fail_closed"] is True
    assert data["principles"]["launch_without_a3"] is False
    assert data["principles"]["launch_without_soak"] is False

def test_mandatory_executor_matrix_is_exactly_defined():
    q = load()["gates"]["G4_23_WAVE_QUALIFICATION"]
    assert q["mandatory_paths"] == [
        "CODEX_FCC", "CLAUDE_FCC", "CODEX_OMNIROUTE",
        "CLAUDE_OMNIROUTE", "CLAUDE_CODE_DIRECT"
    ]
    assert q["minimum_rounds_per_mandatory_path"] == 23

def test_launch_requires_human_and_full_evidence():
    data = load()
    assert data["gates"]["G11_LAUNCH"]["human_authorization_required"] is True
    assert data["launch_contract"]["decision"] == "HUMAN_ONLY"
    assert "A3_verification_record" in data["launch_contract"]["required_inputs"]
    assert "soak_record" in data["launch_contract"]["required_inputs"]

def test_local_model_and_desktop_agent_cannot_gain_authority():
    data = load()
    model = data["component_specific_admission"]["local_model"]
    agent = data["component_specific_admission"]["candidate_desktop_agent"]
    assert model["model_is_not_executor"] is True
    assert model["model_is_not_authority"] is True
    assert agent["agent_is_not_authority"] is True
