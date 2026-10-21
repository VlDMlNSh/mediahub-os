"""Static security contracts for the no-secret controller probe and API transport."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILD_PATHS = (
    ROOT / ".github/workflows/gemini-autonomous-engineering.yml",
    ROOT / ".github/workflows/gemini-agent-2.yml",
    ROOT / ".github/workflows/gemini-agent-3.yml",
)

class GeminiPositiveContextProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = CONTROLLER_PATH.read_text(encoding="utf-8")
        cls.controller = yaml.load(cls.source, Loader=yaml.BaseLoader)

    def test_probe_is_default_and_secret_free(self):
        inputs = self.controller["on"]["workflow_dispatch"]["inputs"]
        self.assertEqual(inputs["mode"]["default"], "probe")
        self.assertEqual(inputs["confirm"]["default"], "no")
        probe = self.controller["jobs"]["probe"]
        self.assertEqual(probe["permissions"], {})
        env = probe["steps"][0].get("env", {})
        self.assertEqual(set(env), {"EVENT_NAME", "WORKFLOW_REF"})
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", str(env))
        self.assertNotIn("GEMINI_API_KEY", str(env))
        self.assertNotIn("run-gemini-cli", str(probe))

    def test_model_dispatch_requires_agents_mode_and_explicit_confirmation(self):
        job = self.controller["jobs"]["dispatch-and-verify"]
        self.assertIn("github.event_name == 'workflow_dispatch'", job["if"])
        self.assertIn("inputs.mode == 'agents'", job["if"])
        self.assertIn("inputs.confirm == 'yes'", job["if"])
        envs = [step.get("env", {}) for step in job["steps"]]
        self.assertEqual(sum("GH_TOKEN" in env for env in envs), 2)

    def test_controller_dispatches_only_three_fixed_workflows(self):
        script = self.controller["jobs"]["dispatch-and-verify"]["steps"][0]["run"]
        for name in ("gemini-autonomous-engineering.yml", "gemini-agent-2.yml", "gemini-agent-3.yml"):
            self.assertIn(f'dispatch_one "{name}"', script)
        self.assertIn("git/ref/heads/main", script)
        self.assertIn("base_ref:$target_sha", script)
        self.assertIn("refusing to guess", self.controller["jobs"]["dispatch-and-verify"]["steps"][1]["run"])

    def test_children_are_dispatch_targets_and_keep_pinned_actions(self):
        for path in CHILD_PATHS:
            child = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
            with self.subTest(workflow=child["name"]):
                self.assertIn("workflow_dispatch", child["on"])
                self.assertNotIn("workflow_call", child["on"])
                self.assertIn("ghcr.io/github/github-mcp-server@sha256:", path.read_text(encoding="utf-8"))
                self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", path.read_text(encoding="utf-8"))

    def test_pull_request_path_runs_only_the_no_secret_probe(self):
        pr = self.controller["on"]["pull_request"]
        self.assertIn(".github/workflows/gemini-batch-dispatch-controller.yml", pr["paths"])
        self.assertIn("tests/test_gemini_controller_positive_context_probe_wave292_contract.py", pr["paths"])
        self.assertIn("github.event_name == 'pull_request'", self.controller["jobs"]["probe"]["if"])
        self.assertIn("github.event_name == 'workflow_dispatch'", self.controller["jobs"]["dispatch-and-verify"]["if"])

if __name__ == "__main__":
    unittest.main()
