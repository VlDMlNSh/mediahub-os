"""Static contract tests for token-backed GitHub API Gemini dispatch."""
from pathlib import Path
import unittest
import yaml
ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILD_PATHS = (ROOT / ".github/workflows/gemini-autonomous-engineering.yml", ROOT / ".github/workflows/gemini-agent-2.yml", ROOT / ".github/workflows/gemini-agent-3.yml")
class GeminiTransportControllerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = CONTROLLER_PATH.read_text(encoding="utf-8")
        cls.workflow = yaml.load(cls.source, Loader=yaml.BaseLoader)
        cls.child_sources = [p.read_text(encoding="utf-8") for p in CHILD_PATHS]
        cls.children = [yaml.load(s, Loader=yaml.BaseLoader) for s in cls.child_sources]
    def test_explicit_confirmation_and_probe_default(self):
        inputs = self.workflow["on"]["workflow_dispatch"]["inputs"]
        self.assertEqual(inputs["mode"]["options"], ["probe", "agents"])
        self.assertEqual(inputs["mode"]["default"], "probe")
        self.assertEqual(inputs["confirm"]["options"], ["no", "yes"])
        self.assertEqual(inputs["confirm"]["default"], "no")
        self.assertIn("inputs.mode == 'agents' && inputs.confirm == 'yes'", self.source)
    def test_transport_token_is_controller_only(self):
        self.assertIn("secrets.MEDIAHUB_GITHUB_TOKEN", self.source)
        self.assertIn("actions/workflows/$workflow/dispatches", self.source)
        self.assertNotIn("secrets: inherit", self.source)
        for child in self.child_sources:
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", child)
            self.assertNotIn("GITHUB_PERSONAL_ACCESS_TOKEN", child)
    def test_dispatches_exactly_three_fixed_workflows(self):
        source = self.source
        for name in ("gemini-autonomous-engineering.yml", "gemini-agent-2.yml", "gemini-agent-3.yml"):
            with self.subTest(workflow=name):
                self.assertIn('dispatch_one "' + name + '"', source)
        self.assertIn("target_sha", source)
        self.assertIn("baseline_", source)
        self.assertIn("Ambiguous new runs", source)
        self.assertIn("conclusion", source)
    def test_children_require_hmac_authorization_before_engineer_job(self):
        for child, source in zip(self.children, self.child_sources):
            with self.subTest(workflow=child["name"]):
                self.assertIn("workflow_dispatch", child["on"])
                self.assertNotIn("workflow_call", child["on"])
                self.assertIn("authorize_dispatch", child["jobs"])
                self.assertIn("needs.authorize_dispatch.result == 'success'", child["jobs"]["engineer"]["if"])
                self.assertIn("hmac.compare_digest", source)
                self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", source)
                self.assertEqual(child["jobs"]["authorize_dispatch"]["permissions"], {})
    def test_shared_target_sha_and_fail_closed_results(self):
        for source in self.child_sources:
            self.assertIn("ref: ${{ inputs.target_sha }}", source)
        self.assertIn("Immutable target SHA", self.source)
        self.assertIn("All three Gemini workflow runs completed successfully", self.source)
        self.assertNotIn("secrets: inherit", self.source)
if __name__ == "__main__":
    unittest.main()
