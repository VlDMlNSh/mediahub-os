"""Security contracts for GitHub API-dispatched, HMAC-authorized Gemini children."""
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILD_PATHS = (
    ROOT / ".github/workflows/gemini-autonomous-engineering.yml",
    ROOT / ".github/workflows/gemini-agent-2.yml",
    ROOT / ".github/workflows/gemini-agent-3.yml",
)
EXPECTED_SECRETS = ("GEMINI_API_KEY", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3")


class GeminiSignedDispatchContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller_source = CONTROLLER.read_text(encoding="utf-8")
        cls.controller = yaml.load(cls.controller_source, Loader=yaml.BaseLoader)
        cls.sources = [p.read_text(encoding="utf-8") for p in CHILD_PATHS]
        cls.children = [yaml.load(s, Loader=yaml.BaseLoader) for s in cls.sources]

    def test_controller_is_the_only_transport_token_holder(self):
        self.assertIn("secrets.MEDIAHUB_GITHUB_TOKEN", self.controller_source)
        self.assertIn("api.github.com", self.controller_source)
        self.assertIn("/actions/workflows/{wf}/dispatches", self.controller_source)
        self.assertNotIn("secrets: inherit", self.controller_source)
        for source in self.sources:
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
            self.assertNotIn("secrets: inherit", source)

    def test_probe_is_default_and_agent_dispatch_is_main_only(self):
        inputs = self.controller["on"]["workflow_dispatch"]["inputs"]
        self.assertEqual(inputs["mode"]["default"], "probe")
        self.assertEqual(inputs["confirm"]["default"], "no")
        self.assertEqual(self.controller["permissions"], {})
        condition = self.controller["jobs"]["dispatch_and_monitor"]["if"]
        self.assertIn("github.ref == 'refs/heads/main'", condition)
        self.assertIn("inputs.mode == 'agents'", condition)
        self.assertIn("inputs.confirm == 'yes'", condition)
        self.assertEqual(self.controller["jobs"]["probe"]["permissions"], {})

    def test_all_children_require_hmac_before_provider_execution(self):
        for index, (workflow, source, secret) in enumerate(zip(self.children, self.sources, EXPECTED_SECRETS), 1):
            with self.subTest(child=index):
                self.assertIn("workflow_dispatch", workflow["on"])
                self.assertNotIn("workflow_call", workflow["on"])
                self.assertIn("authorize_dispatch", workflow["jobs"])
                self.assertEqual(workflow["jobs"]["authorize_dispatch"]["permissions"], {})
                self.assertIn("hmac.compare_digest", source)
                self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", source)
                self.assertIn(secret, source)
                self.assertIn("needs.authorize_dispatch.result == 'success'", workflow["jobs"]["engineer"]["if"])
                self.assertIn("inputs.target_sha", str(workflow["jobs"]["engineer"]["steps"][0]))
                self.assertIn("refs/heads/main", source)
                self.assertIn('BASE_REF")!="main"', source)
                self.assertIn('SCOPE")!="contour-a"', source)

    def test_external_actions_and_mcp_container_are_pinned(self):
        for index, source in enumerate(self.sources, 1):
            with self.subTest(child=index):
                for line in source.splitlines():
                    if "uses:" in line and "./.github/workflows/" not in line:
                        self.assertRegex(line, r"uses:\s+[^\s@]+@[0-9a-f]{40}(?:\s|$)")
                self.assertIn("ghcr.io/github/github-mcp-server@sha256:", source)
                self.assertNotIn("ghcr.io/github/github-mcp-server:v0.27.0", source)

    def test_controller_pins_one_target_and_correlates_each_child(self):
        self.assertIn('target=ref["object"]["sha"]', self.controller_source)
        self.assertIn("Shared immutable target SHA", self.controller_source)
        self.assertIn("dispatch_id", self.controller_source)
        self.assertIn("NOT_COMPLETED_BEFORE_TIMEOUT", self.controller_source)
        self.assertIn("conclusion", self.controller_source)

    def test_mutable_action_ref_fixture_is_rejected_by_contract(self):
        source = self.sources[0].replace(
            "google-github-actions/run-gemini-cli@f77273f4c914e4bf38440cf36a0369cb64a37489",
            "google-github-actions/run-gemini-cli@v0",
        )
        self.assertRegex(source, r"uses:\s+google-github-actions/run-gemini-cli@v0(?:\s|$)")


if __name__ == "__main__":
    unittest.main()
