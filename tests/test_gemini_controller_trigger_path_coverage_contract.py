"""Regression contract: controller no-secret PR probe must cover Gemini transport changes."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
VALIDATION = ROOT / ".github/workflows/gemini-workflow-contract-validation-wave284.yml"

class GeminiControllerTriggerPathCoverageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller = yaml.load(CONTROLLER.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        cls.validation = yaml.load(VALIDATION.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)

    def test_controller_probe_triggers_for_hmac_contract_change_set(self):
        paths = set(self.controller["on"]["pull_request"]["paths"])
        required = {
            ".github/workflows/gemini-batch-dispatch-controller.yml",
            ".github/workflows/gemini-workflow-contract-validation-wave284.yml",
            "tests/test_gemini_child_signed_dispatch_runtime_contract.py",
            "tests/test_gemini_transport_controller_contract.py",
            "tests/test_gemini_controller_trigger_path_coverage_contract.py",
        }
        self.assertTrue(required.issubset(paths), f"controller probe path filter missing: {sorted(required - paths)}")

    def test_issue_comment_probe_is_owner_only_and_never_dispatches_agents(self):
        probe_if = self.controller["jobs"]["probe"]["if"]
        assert_if = self.controller["jobs"]["assert_probe_context"]["if"]
        readiness_if = self.controller["jobs"]["readiness_gate"]["if"]
        dispatch_if = self.controller["jobs"]["dispatch_and_monitor"]["if"]
        self.assertIn("comment.body == '/probe'", probe_if)
        self.assertIn("author_association == 'OWNER'", probe_if)
        self.assertIn("comment.body == '/probe'", assert_if)
        self.assertNotIn("comment.body == '/probe'", readiness_if)
        self.assertNotIn("comment.body == '/probe'", dispatch_if)
        reusable = (ROOT / ".github/workflows/gemini-reusable-context-probe-wave284.yml").read_text()
        self.assertIn("GITHUB_EVENT_NAME == \"issue_comment\"", reusable)
        self.assertIn('comment.get("body")=="/probe"', reusable)
        self.assertIn('comment.get("author_association")=="OWNER"', reusable)

    def test_contract_validation_executes_this_regression_contract(self):
        pull_request = self.validation["on"]["pull_request"]
        self.assertEqual(pull_request.get("branches"), ["main"])
        self.assertNotIn("paths", pull_request)
        steps = self.validation["jobs"]["validate"]["steps"]
        commands = "\n".join(step.get("run", "") for step in steps)
        self.assertIn("test_gemini_controller_trigger_path_coverage_contract.py", commands)

if __name__ == "__main__":
    unittest.main()
