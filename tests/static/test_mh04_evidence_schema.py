import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


class MH04EvidenceSchemaTests(unittest.TestCase):
    def setUp(self):
        self.schema = (ROOT / "verification/MH-04-evidence-record.schema.yaml").read_text(encoding="utf-8")

    def test_required_top_level_record_sections_exist(self):
        for section in ("record:", "environment:", "execution:", "input:", "observation:", "evidence:", "assessment:"):
            self.assertIn(section, self.schema)

    def test_identity_and_execution_fields_are_required(self):
        for field in ("test_id: required", "contract: required", "git_sha: required", "branch: required", "command: required", "started_at: required", "completed_at: required", "exit_code: required", "command_id: required", "correlation_id: required"):
            self.assertIn(field, self.schema)

    def test_observation_fields_are_required(self):
        for field in ("pre_state: required", "post_state: required", "authorization_result: required", "validation_result: required", "mutation_result: required", "emitted_events: required"):
            self.assertIn(field, self.schema)

    def test_assessment_values_and_non_authority_rules_are_present(self):
        for value in ("NOT_VERIFIED", "TESTED", "QUALIFIED", "BLOCKED"):
            self.assertRegex(self.schema, rf"- {re.escape(value)}")
        for rule in ("evidence_is_observational", "evidence_cannot_mutate_canonical_state", "missing_execution_evidence_means_NOT_VERIFIED", "test_pass_does_not_equal_QUALIFIED", "no_record_can_grant_implementation_authorization", "no_record_can_change_contract_or_invariant_semantics"):
            self.assertIn(rule, self.schema)


if __name__ == "__main__":
    unittest.main()
