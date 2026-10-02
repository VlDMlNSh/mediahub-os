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


    def test_expanded_candidate_inventory_is_not_implicitly_qualified(self):
        data = self.load()
        candidates = data["candidate_review_inventory"]["candidates"]
        ids = {item["id"] for item in candidates}
        expected = {
            "openopc", "sol-pi", "colibri", "webtool-deepseek",
            "deepseek-harness", "stagewise", "minicpm-v-4.5-8b-1mk",
            "free-coding-models", "freellmapi", "unlazy", "naabu",
            "codex-chatgpt-web",
        }
        self.assertTrue(expected.issubset(ids))
        for item in candidates:
            self.assertEqual(item["status"], "NOT_PROVEN")
        admission = data["candidate_review_inventory"]["admission"]
        self.assertEqual(admission["minimum_fresh_rounds"], 23)
        self.assertTrue(admission["fresh_evidence_only"])
        self.assertTrue(admission["no_implicit_promotion"])
        self.assertTrue(admission["no_self_qualification"])


    def test_category_specific_candidate_controls_exist(self):
        data = self.load()
        controls = data["candidate_review_inventory"]["category_specific_controls"]
        for category in ["local_model", "gateway_or_router", "browser_bridge",
                         "coding_harness_or_ide", "security_tool", "unresolved_identity"]:
            self.assertIn(category, controls)
        self.assertIn("minicpm-v-4.5-8b-1mk", controls["local_model"]["examples"])
        self.assertIn("freellmapi", controls["gateway_or_router"]["examples"])
        self.assertIn("free-coding-models", controls["gateway_or_router"]["examples"])
        self.assertIn("webtool-deepseek", controls["browser_bridge"]["examples"])
        self.assertIn("codex-chatgpt-web", controls["browser_bridge"]["examples"])
        self.assertIn("naabu", controls["security_tool"]["examples"])
        self.assertIn("colibri", controls["unresolved_identity"]["examples"])
        self.assertIn("unlazy", controls["unresolved_identity"]["examples"])

    def test_reference_architecture_and_unified_model_alignment_contract(self):
        reference = Path("architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md").read_text(encoding="utf-8")
        unified = yaml.safe_load(Path("architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml").read_text(encoding="utf-8"))
        self.assertIn("Human is the final authority", reference)
        self.assertIn("RECONCILIATION_REQUIRED", reference)
        self.assertEqual(unified["reference_architecture"], "architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md")
        self.assertEqual(unified["qualification_contract"], "architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml")
        self.assertTrue(unified["contract_alignment"].startswith("CANONICAL"))
        self.assertTrue(unified["reconciliation"]["required"])
        self.assertEqual(unified["reconciliation"]["failure_state"], "RECONCILIATION_REQUIRED")
        self.assertEqual(len(unified["qualification"]["gate_contract"]), 12)
        self.assertTrue(unified["rules"]["missing_or_contradictory_evidence_blocks"])
        self.assertTrue(unified["rules"]["gold_active_requires_human_launch"])
        self.assertTrue(unified["rules"]["evidence_is_immutable"])

    def test_session_115_wave_contract_is_exact_and_fail_closed(self):
        source = Path("ops/qualification/session_115_wave.py").read_text(encoding="utf-8")
        self.assertIn('"total_observations_minimum":115', source)
        self.assertIn('"rounds_minimum_per_path":ROUNDS', source)
        self.assertIn('ROUNDS=23', source)
        for path in ["CODEX_FCC", "CLAUDE_FCC", "CODEX_OMNIROUTE",
                     "CLAUDE_OMNIROUTE", "CLAUDE_CODE_DIRECT"]:
            self.assertIn(f'"{path}"', source)
        self.assertIn('status="BLOCKED"', source)
        self.assertIn('"verification_status":"UNVERIFIED"', source)

if __name__ == "__main__":
    unittest.main()
