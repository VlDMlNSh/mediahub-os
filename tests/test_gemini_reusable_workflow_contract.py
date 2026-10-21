"""Architecture contract tests for the GitHub API controller and signed Gemini children."""
from pathlib import Path
import unittest
import yaml
ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILD_PATHS = (ROOT / ".github/workflows/gemini-autonomous-engineering.yml", ROOT / ".github/workflows/gemini-agent-2.yml", ROOT / ".github/workflows/gemini-agent-3.yml")
EXPECTED_KEYS = ("GEMINI_API_KEY", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3")
class GeminiReusableWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller_source = CONTROLLER_PATH.read_text(encoding="utf-8")
        cls.controller = yaml.load(cls.controller_source, Loader=yaml.BaseLoader)
        cls.child_sources = [p.read_text(encoding="utf-8") for p in CHILD_PATHS]
        cls.children = [yaml.load(s, Loader=yaml.BaseLoader) for s in cls.child_sources]
    def test_current_contract_is_valid(self):
        self.assertEqual(self.controller["permissions"], {})
        self.assertIn("workflow_dispatch", self.controller["on"])
        self.assertIn("pull_request", self.controller["on"])
        self.assertIn("secrets.MEDIAHUB_GITHUB_TOKEN", self.controller_source)
        self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", self.controller_source)
        for child, source, key in zip(self.children, self.child_sources, EXPECTED_KEYS):
            self.assertIn("workflow_dispatch", child["on"])
            self.assertNotIn("workflow_call", child["on"])
            self.assertIn(key, source)
            self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", source)
            self.assertIn("hmac.compare_digest", source)
            self.assertIn("needs.authorize_dispatch.result == 'success'", child["jobs"]["engineer"]["if"])
    def test_probe_is_no_secret_and_children_cannot_receive_transport_token(self):
        probe = str(self.controller["jobs"]["probe"])
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", probe)
        self.assertNotIn("GEMINI_API_KEY", probe)
        self.assertNotIn("DISPATCH_HMAC_KEY", probe)
        for source in self.child_sources:
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
            self.assertNotIn("/actions/workflows/", source)
    def test_only_fixed_child_workflows_are_dispatched(self):
        for name in ("gemini-autonomous-engineering.yml", "gemini-agent-2.yml", "gemini-agent-3.yml"):
            self.assertIn('dispatch_one "' + name + '"', self.controller_source)
    def test_child_authorization_is_cryptographic_not_path_substring(self):
        for source in self.child_sources:
            self.assertIn("hmac.compare_digest", source)
            self.assertIn("Invalid controller signature", source)
            self.assertIn('os.environ.get("REF_NAME")!="refs/heads/main"', source)
if __name__ == "__main__":
    unittest.main()
