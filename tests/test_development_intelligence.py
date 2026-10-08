import unittest

from mediahub_runtime.development_intelligence import (
    capability_contract,
    checkpoint_record,
    classify_failure,
    classify_project,
    compile_roadmap_blocks,
    split_block_into_units,
    universal_first_action,
    validate_knowledge_entry,
)


class DevelopmentIntelligenceTests(unittest.TestCase):
    def test_classifier_and_blocks_are_deterministic(self):
        profile = classify_project("Mobile Flutter iOS Android with backend API and tests")
        self.assertEqual(profile.project_type, "mobile")
        self.assertIn("Flutter", profile.frameworks)
        blocks = compile_roadmap_blocks("# Architecture\n## Execution\n## Verification")
        self.assertEqual([b.block_id for b in blocks], ["MD-001", "MD-002", "MD-003"])
        self.assertEqual(blocks[1].dependencies, ("MD-001",))

    def test_units_require_validation_and_recovery(self):
        units = split_block_into_units("- Define API\n- Add tests", "MD-001")
        self.assertEqual(len(units), 2)
        self.assertTrue(all(u["validation_required"] and u["recovery_required"] for u in units))

    def test_first_action_and_failure_classification(self):
        self.assertIn("resolve latest confirmed project/file/unit checkpoint", universal_first_action())
        self.assertEqual(classify_failure("pytest runner unavailable in GitHub Actions"), "test_infrastructure")
        self.assertEqual(classify_failure("package dependency missing"), "dependency")

    def test_knowledge_requires_confirmed_fix(self):
        entry = {
            "ERROR_ID": "E-1",
            "CATEGORY": "Universal",
            "SYMPTOM": "x",
            "ROOT_CAUSE": "y",
            "CONFIRMED_FIX": "z",
            "VALIDATION": "tests",
            "APPLICABILITY": "all",
            "CONFIDENCE": "Confirmed",
            "CONFIRMED": True,
        }
        self.assertEqual(validate_knowledge_entry(entry), (True, []))
        entry["CONFIRMED"] = False
        self.assertFalse(validate_knowledge_entry(entry)[0])

    def test_capability_contract_and_checkpoint_are_non_authoritative(self):
        contract = capability_contract({
            "required_capabilities": ["security", "security"],
            "preferred_roles": ["security-reviewer"],
            "verification": ["tests"],
            "qualification": {"evidence_required": True, "commit_binding": True},
        })
        self.assertEqual(contract["required_capabilities"], ["security"])
        checkpoint = checkpoint_record("UNIT", "a" * 40, {"unit_id": "U-1"})
        self.assertEqual(checkpoint["schema"], "mediahub.astra.checkpoint.v1")


if __name__ == "__main__":
    unittest.main()
