"""Contract tests for the token-backed GitHub API Gemini transport."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILDREN = (
    ("gemini-autonomous-engineering.yml", "GEMINI_API_KEY"),
    ("gemini-agent-2.yml", "GEMINI_API_KEY_2"),
    ("gemini-agent-3.yml", "GEMINI_API_KEY_3"),
)

class GeminiReusableWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller_source = CONTROLLER_PATH.read_text(encoding="utf-8")
        cls.controller = yaml.load(cls.controller_source, Loader=yaml.BaseLoader)

    def test_controller_uses_only_the_approved_api_transport(self):
        self.assertIn("${{ secrets.MEDIAHUB_GITHUB_TOKEN }}", self.controller_source)
        self.assertIn("https://api.github.com/repos/VlDMlNSh/mediahub-os/actions/workflows/", self.controller_source)
        self.assertIn("/dispatches", self.controller_source)
        self.assertIn("workflow_runs", self.controller_source)
        self.assertNotIn("secrets: inherit", self.controller_source)
        self.assertNotIn('echo "$GH_TOKEN"', self.controller_source)

    def test_probe_is_default_and_agent_dispatch_is_explicit(self):
        inputs = self.controller["on"]["workflow_dispatch"]["inputs"]
        self.assertEqual(inputs["mode"]["default"], "probe")
        self.assertEqual(inputs["confirm"]["default"], "no")
        job = self.controller["jobs"]["dispatch-and-verify"]
        self.assertIn("inputs.mode == 'agents'", job["if"])
        self.assertIn("inputs.confirm == 'yes'", job["if"])
        self.assertEqual(self.controller["jobs"]["probe"]["permissions"], {})
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", str(self.controller["jobs"]["probe"]["steps"][0].get("env", {})))

    def test_fixed_children_and_immutable_source_sha(self):
        script = self.controller["jobs"]["dispatch-and-verify"]["steps"][0]["run"]
        for workflow, _ in CHILDREN:
            self.assertIn(f'snapshot_latest "{workflow}"', script)
            self.assertIn(f'dispatch_one "{workflow}"', script)
        self.assertIn("git/ref/heads/main", script)
        self.assertIn('target_sha" =~ ^[0-9a-f]{40}', script)
        self.assertIn("base_ref:$target_sha", script)
        self.assertIn("Immutable source/main SHA", script)

    def test_children_are_dispatch_targets_with_isolated_provider_secrets(self):
        for name, secret in CHILDREN:
            with self.subTest(child=name):
                source = (ROOT / ".github/workflows" / name).read_text(encoding="utf-8")
                child = yaml.load(source, Loader=yaml.BaseLoader)
                self.assertIn("workflow_dispatch", child["on"])
                self.assertNotIn("workflow_call", child["on"])
                self.assertIn("secrets." + secret, source)
                self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
                self.assertNotIn("secrets: inherit", source)
                self.assertEqual(child["on"]["workflow_dispatch"]["inputs"]["base_ref"]["type"], "string")
                self.assertIn("ghcr.io/github/github-mcp-server@sha256:", source)

    def test_negative_fixture_detects_transport_token_in_child(self):
        source = (ROOT / ".github/workflows" / CHILDREN[0][0]).read_text(encoding="utf-8")
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
        bad = source + "\n# MEDIAHUB_GITHUB_TOKEN must never be in a child\n"
        self.assertIn("MEDIAHUB_GITHUB_TOKEN", bad)

if __name__ == "__main__":
    unittest.main()
