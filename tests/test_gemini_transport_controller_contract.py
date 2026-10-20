"""Static contract tests for the GitHub-hosted Gemini transport controller."""
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "gemini-batch-dispatch-controller.yml"
CHILD_WORKFLOWS = (
    "gemini-autonomous-engineering.yml",
    "gemini-agent-2.yml",
    "gemini-agent-3.yml",
)


class GeminiTransportControllerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW_PATH.read_text(encoding="utf-8")
        # BaseLoader keeps YAML 1.1 booleans such as "on"/"yes"/"no" as strings.
        cls.workflow = yaml.load(cls.source, Loader=yaml.BaseLoader)

    def test_explicit_confirmation_is_a_string_choice(self):
        dispatch = self.workflow["on"]["workflow_dispatch"]
        confirm = dispatch["inputs"]["confirm"]
        self.assertEqual(confirm["type"], "choice")
        self.assertEqual(confirm["options"], ["no", "yes"])
        self.assertEqual(confirm["default"], "no")
        self.assertEqual(
            self.workflow["jobs"]["dispatch-and-verify"]["if"],
            "${{ inputs.confirm == 'yes' }}",
        )

    def test_builtin_github_token_has_no_permissions(self):
        self.assertEqual(self.workflow["permissions"], {})

    def test_api_secret_is_used_for_dispatch_and_monitoring(self):
        steps = self.workflow["jobs"]["dispatch-and-verify"]["steps"]
        token_bindings = [
            step["env"]["GH_TOKEN"]
            for step in steps
            if "GH_TOKEN" in step.get("env", {})
        ]
        self.assertEqual(
            token_bindings,
            [
                "${{ secrets.MEDIAHUB_GITHUB_TOKEN }}",
                "${{ secrets.MEDIAHUB_GITHUB_TOKEN }}",
            ],
        )
        self.assertNotIn('echo "$GH_TOKEN"', self.source)
        self.assertNotIn('printf \'%s\' "$GH_TOKEN"', self.source)

    def test_only_the_three_fixed_child_workflows_are_dispatched(self):
        steps = self.workflow["jobs"]["dispatch-and-verify"]["steps"]
        dispatch_source = steps[0]["run"]
        monitor_source = steps[1]["run"]
        for workflow in CHILD_WORKFLOWS:
            with self.subTest(workflow=workflow):
                self.assertIn(f'snapshot_latest "{workflow}"', dispatch_source)
                self.assertIn(f'dispatch_one "{workflow}"', dispatch_source)
        for agent, workflow in zip(("agent1", "agent2", "agent3"), CHILD_WORKFLOWS):
            self.assertIn(f'[{agent}]="{workflow}"', monitor_source)
        self.assertIn('ref:"main"', dispatch_source)
        self.assertIn('base_ref:"main"', dispatch_source)
        self.assertIn('scope:"contour-a"', dispatch_source)

    def test_run_correlation_fails_closed_on_ambiguity_and_failure(self):
        monitor_source = self.workflow["jobs"]["dispatch-and-verify"]["steps"][1]["run"]
        self.assertIn("created_at >= $since", monitor_source)
        self.assertIn(".id > $baseline", monitor_source)
        self.assertIn('if [[ "$count" -gt 1 ]]', monitor_source)
        self.assertIn("refusing to guess", monitor_source)
        self.assertIn('!= "completed"', monitor_source)
        self.assertIn('!= "success"', monitor_source)


if __name__ == "__main__":
    unittest.main()
