import unittest
from pathlib import Path
import yaml

SCHEMA = Path("architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml")

class TestAstraGoldQualificationLaunchSchema(unittest.TestCase):
    @classmethod
    def load(cls):
        return yaml.safe_load(SCHEMA.read_text(encoding="utf-8"))

    def test_canonical_gate_order_and_fail_closed(self):
        data = self.load()
        self.assertEqual(list(data["gates"]), [
            "G0_IDENTITY", "G1_BOUNDARY", "G2_CONTROL_PLANE", "G3_EXECUTION_PATH",
            "G4_23_WAVE_QUALIFICATION", "G5_CONCURRENCY", "G6_RECOVERY",
            "G7_INTEGRATED_A3", "G8_PRE_SOAK", "G9_24H_SOAK",
            "G10_LAUNCH_READY", "G11_LAUNCH"
        ])
        self.assertTrue(data["principles"]["fail_closed"])
        self.assertFalse(data["principles"]["launch_without_a3"])
        self.assertFalse(data["principles"]["launch_without_soak"])

    def test_mandatory_executor_matrix_is_exactly_defined(self):
        q = self.load()["gates"]["G4_23_WAVE_QUALIFICATION"]
        self.assertEqual(q["mandatory_paths"], [
            "CODEX_FCC", "CLAUDE_FCC", "CODEX_OMNIROUTE",
            "CLAUDE_OMNIROUTE", "CLAUDE_CODE_DIRECT"
        ])
        self.assertEqual(q["minimum_rounds_per_mandatory_path"], 23)

    def test_launch_requires_human_and_full_evidence(self):
        data = self.load()
        self.assertTrue(data["gates"]["G11_LAUNCH"]["human_authorization_required"])
        self.assertEqual(data["launch_contract"]["decision"], "HUMAN_ONLY")
        self.assertIn("A3_verification_record", data["launch_contract"]["required_inputs"])
        self.assertIn("soak_record", data["launch_contract"]["required_inputs"])

    def test_local_model_and_desktop_agent_cannot_gain_authority(self):
        data = self.load()
        model = data["component_specific_admission"]["local_model"]
        agent = data["component_specific_admission"]["candidate_desktop_agent"]
        self.assertTrue(model["model_is_not_executor"])
        self.assertTrue(model["model_is_not_authority"])
        self.assertTrue(agent["agent_is_not_authority"])


    def test_openopc_candidate_is_qualified_separately_without_authority(self):
        data = self.load()
        candidate = data["candidate_component_admission"]["autonomous_development_system"]
        openopc = candidate["openopc"]
        self.assertEqual(openopc["qualification"], "NOT_PROVEN")
        self.assertEqual(openopc["authority"], "none")
        self.assertFalse(openopc["provider_selection"])
        self.assertFalse(openopc["credential_creation"])
        self.assertFalse(openopc["state_authority"])
        self.assertFalse(openopc["architecture_authority"])
        self.assertFalse(openopc["self_promotion"])
        self.assertFalse(openopc["self_qualification"])
        self.assertEqual(openopc["qualification_rounds"]["minimum"], 23)
        self.assertTrue(openopc["qualification_rounds"]["fresh_evidence_per_round"])
        self.assertTrue(openopc["qualification_rounds"]["isolated_workspace_per_round"])
        self.assertTrue(openopc["security_attention"]["versioned_release_required_for_gold"])

if __name__ == "__main__":
    unittest.main()
