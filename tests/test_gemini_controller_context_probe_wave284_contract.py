"""Contracts for a separate no-secret context probe and signed dispatch authorization."""
from pathlib import Path
import unittest
import yaml
ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / ".github/workflows/gemini-controller-context-probe-wave284.yml"
OBSERVER_PATH = ROOT / ".github/workflows/gemini-reusable-context-probe-wave284.yml"
CONTROLLER_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILD_PATHS = (ROOT / ".github/workflows/gemini-autonomous-engineering.yml", ROOT / ".github/workflows/gemini-agent-2.yml", ROOT / ".github/workflows/gemini-agent-3.yml")
class GeminiCallerContextProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.probe_source = PROBE_PATH.read_text(encoding="utf-8")
        cls.probe = yaml.load(cls.probe_source, Loader=yaml.BaseLoader)
        cls.observer_source = OBSERVER_PATH.read_text(encoding="utf-8")
        cls.controller = yaml.load(CONTROLLER_PATH.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        cls.child_sources = [p.read_text(encoding="utf-8") for p in CHILD_PATHS]
        cls.children = [yaml.load(s, Loader=yaml.BaseLoader) for s in cls.child_sources]
    def test_standalone_probe_is_non_launching_and_secret_free(self):
        self.assertIn("workflow_dispatch", self.probe["on"])
        self.assertIn("pull_request", self.probe["on"])
        for source in (self.probe_source, self.observer_source):
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
            self.assertNotIn("GEMINI_API_KEY", source)
            self.assertNotIn("DISPATCH_HMAC_KEY", source)
        self.assertEqual(self.probe["permissions"], {})
    def test_controller_probe_has_no_credentials(self):
        probe = self.controller["jobs"]["probe"]
        self.assertEqual(probe["permissions"], {})
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", str(probe))
        self.assertNotIn("GEMINI_API_KEY", str(probe))
    def test_every_child_keeps_fail_closed_signed_dispatch_gate(self):
        for child, source in zip(self.children, self.child_sources):
            with self.subTest(child=child["name"]):
                self.assertIn("workflow_dispatch", child["on"])
                self.assertNotIn("workflow_call", child["on"])
                self.assertIn("authorize_dispatch", child["jobs"])
                self.assertIn("needs.authorize_dispatch.result == 'success'", child["jobs"]["engineer"]["if"])
                self.assertIn("hmac.compare_digest", source)
                self.assertIn("Invalid controller signature", source)
                self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
if __name__ == "__main__":
    unittest.main()
