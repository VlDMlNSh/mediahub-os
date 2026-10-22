"""Static contracts for signed GitHub API Gemini dispatch (Wave 312)."""
from pathlib import Path
import unittest
import yaml
ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILDREN = [ROOT / ".github/workflows/gemini-autonomous-engineering.yml", ROOT / ".github/workflows/gemini-agent-2.yml", ROOT / ".github/workflows/gemini-agent-3.yml"]
class ControllerTransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = CONTROLLER.read_text()
        cls.data = yaml.load(cls.source, Loader=yaml.BaseLoader)
        cls.sources = [p.read_text() for p in CHILDREN]
        cls.children = [yaml.load(s, Loader=yaml.BaseLoader) for s in cls.sources]
    def test_probe_default_and_minimal_controller_permissions(self):
        i = self.data["on"]["workflow_dispatch"]["inputs"]
        self.assertEqual(i["mode"]["default"], "probe")
        self.assertEqual(i["confirm"]["type"], "boolean")
        self.assertEqual(i["confirm"]["default"], "false")
        self.assertEqual(self.data["permissions"], {})
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", str(self.data["jobs"]["probe"]))
        self.assertNotIn("GEMINI_API_KEY", str(self.data["jobs"]["probe"]))
    def test_transport_token_controller_only_and_no_inherit(self):
        self.assertIn("secrets.MEDIAHUB_GITHUB_TOKEN", self.source)
        self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", self.source)
        self.assertIn("/actions/workflows/{wf}/dispatches", self.source)
        self.assertNotIn("secrets: inherit", self.source)
        for s in self.sources:
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", s)
            self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", s)
    def test_children_require_signed_workflow_dispatch_and_shared_sha(self):
        for data, source in zip(self.children, self.sources):
            self.assertIn("workflow_dispatch", data["on"])
            self.assertNotIn("workflow_call", data["on"])
            self.assertIn("authorize_dispatch", data["jobs"])
            self.assertEqual(data["jobs"]["authorize_dispatch"]["permissions"], {})
            self.assertIn("needs.authorize_dispatch.result == 'success'", data["jobs"]["engineer"]["if"])
            self.assertIn("inputs.target_sha", str(data["jobs"]["engineer"]["steps"][0]))
            self.assertIn("hmac.compare_digest", source)
    def test_shared_target_and_fail_closed_monitor(self):
        self.assertIn('target=ref["object"]["sha"]', self.source)
        self.assertIn("Shared immutable target SHA", self.source)
        self.assertIn("NOT_COMPLETED_BEFORE_TIMEOUT", self.source)
        condition = self.data["jobs"]["dispatch_and_monitor"]["if"]
        self.assertIn("github.ref == 'refs/heads/main'", condition)
        self.assertIn("inputs.mode == 'agents' && inputs.confirm == true", condition)
        self.assertIn("github.event.comment.author_association == 'OWNER'", condition)
        self.assertIn("github.event.comment.body == '/next'", condition)
if __name__ == "__main__":
    unittest.main()
