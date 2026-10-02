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

if __name__ == "__main__":
    unittest.main()
