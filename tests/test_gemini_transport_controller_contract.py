"""Static contract tests for the GitHub API Gemini transport controller."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "gemini-batch-dispatch-controller.yml"
CHILDREN = (
    ("gemini-autonomous-engineering.yml", "GEMINI_API_KEY"),
    ("gemini-agent-2.yml", "GEMINI_API_KEY_2"),
    ("gemini-agent-3.yml", "GEMINI_API_KEY_3"),
)

class GeminiTransportControllerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.workflow = yaml.load(cls.source, Loader=yaml.BaseLoader)

    def test_default_is_non_launching_probe_and_explicit_confirmation_required(self):
        dispatch = self.workflow["on"]["workflow_dispatch"]["inputs"]
        self.assertEqual(dispatch["mode"]["default"], "probe")
        self.assertEqual(dispatch["mode"]["options"], ["probe", "agents"])
        self.assertEqual(dispatch["confirm"]["default"], "no")
        self.assertEqual(self.workflow["jobs"]["dispatch-and-verify"]["if"],
                         "github.event_name == 'workflow_dispatch' && inputs.mode == 'agents' && inputs.confirm == 'yes'")

    def test_transport_secret_only_bound_to_controller_steps(self):
        steps = self.workflow["jobs"]["dispatch-and-verify"]["steps"]
        bindings = [step.get("env", {}).get("GH_TOKEN") for step in steps if "GH_TOKEN" in step.get("env", {})]
        self.assertEqual(bindings, ["${{ secrets.MEDIAHUB_GITHUB_TOKEN }}", "${{ secrets.MEDIAHUB_GITHUB_TOKEN }}"])
        self.assertNotIn('echo "$GH_TOKEN"', self.source)
        self.assertNotIn('printf \'%s\' "$GH_TOKEN"', self.source)
        self.assertNotIn("secrets: inherit", self.source)
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", self.workflow["jobs"]["probe"]["steps"][0].get("env", {}))

    def test_only_fixed_workflows_and_fixed_refs_are_dispatched(self):
        dispatch_source = self.workflow["jobs"]["dispatch-and-verify"]["steps"][0]["run"]
        monitor_source = self.workflow["jobs"]["dispatch-and-verify"]["steps"][1]["run"]
        for workflow, _ in CHILDREN:
            self.assertIn(f'snapshot_latest "{workflow}"', dispatch_source)
            self.assertIn(f'dispatch_one "{workflow}"', dispatch_source)
        self.assertIn('ref:"main"', dispatch_source)
        self.assertIn('base_ref:"main"', dispatch_source)
        self.assertIn('scope:"contour-a"', dispatch_source)
        self.assertIn('git/ref/heads/main', dispatch_source)
        self.assertIn('target_sha" =~ ^[0-9a-f]{40}', dispatch_source)
        self.assertIn('base_ref:$target_sha', dispatch_source)
        self.assertIn("Immutable source/main SHA", dispatch_source)
        self.assertIn("created_at >= $since", monitor_source)
        self.assertIn("refusing to guess", monitor_source)
        self.assertIn('!= "success"', monitor_source)

    def test_each_child_is_standalone_dispatch_and_only_has_its_provider_key(self):
        for workflow_name, secret in CHILDREN:
            child = yaml.load((ROOT / ".github" / "workflows" / workflow_name).read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
            self.assertIn("workflow_dispatch", child["on"])
            source = (ROOT / ".github" / "workflows" / workflow_name).read_text(encoding="utf-8")
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
            self.assertNotIn("workflow_call", child["on"])
            self.assertIn("secrets." + secret, source)
            self.assertEqual(child["on"]["workflow_dispatch"]["inputs"]["base_ref"]["type"], "string")
            self.assertNotIn("secrets: inherit", source)

    def test_probe_never_dispatches_agents_or_receives_secrets(self):
        probe = self.workflow["jobs"]["probe"]
        self.assertEqual(probe["permissions"], {})
        self.assertNotIn("secrets", str(probe))
        self.assertIn("mode == 'probe'", probe["if"])

if __name__ == "__main__":
    unittest.main()
