"""Static checks for the MH-03 Supervisor authority contract."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "security" / "MH-04-supervisor-negative-test-contract-v1.0.yaml"


class SupervisorContractTests(unittest.TestCase):
    def setUp(self):
        self.text = CONTRACT.read_text(encoding="utf-8")

    def test_contract_is_explicitly_non_authorizing(self):
        self.assertIn("status: PROPOSED / NOT VERIFIED", self.text)
        self.assertIn("implementation_authorization: BLOCKED", self.text)
        self.assertIn("negative_test_pass_does_not_equal_architecture_acceptance", self.text)

    def test_six_negative_cases_are_present(self):
        for case_id in [f"SUP-NEG-{i:02d}" for i in range(1, 7)]:
            self.assertIn(f"id: {case_id}", self.text)

    def test_shadow_authority_fails_closed(self):
        self.assertIn("expected: DENY_AND_STOP_MUTATION", self.text)
        self.assertIn("recovery_must_not_create_shadow_authority", self.text)


if __name__ == "__main__":
    unittest.main()
