"""Static contract verification for the MH-03 Supervisor authority boundary.

This test intentionally verifies only the contract inventory and fail-closed
semantics. It does not claim runtime qualification or architecture acceptance.
"""

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "security" / "MH-04-supervisor-negative-test-contract-v1.0.yaml"

EXPECTED = [
    "SUP-NEG-01",
    "SUP-NEG-02",
    "SUP-NEG-03",
    "SUP-NEG-04",
    "SUP-NEG-05",
    "SUP-NEG-06",
]


class SupervisorContractTests(unittest.TestCase):
    def test_contract_exists_and_is_blocked_until_execution(self):
        text = CONTRACT.read_text(encoding="utf-8")
        self.assertIn("status: PROPOSED / NOT VERIFIED", text)
        self.assertIn("implementation_authorization: BLOCKED", text)
        self.assertIn("actual_runtime_execution_required", text)
        self.assertIn("independent_security_review_required", text)

    def test_all_supervisor_negative_cases_are_present(self):
        text = CONTRACT.read_text(encoding="utf-8")
        for case_id in EXPECTED:
            self.assertIn(f"id: {case_id}", text)

    def test_shadow_authority_is_fail_closed(self):
        text = CONTRACT.read_text(encoding="utf-8")
        self.assertIn("expected: DENY_AND_STOP_MUTATION", text)
        self.assertIn("recovery_must_not_create_shadow_authority", text)


if __name__ == "__main__":
    unittest.main()
