"""Static contract tests for the controller-only Gemini reusable-workflow transport."""
from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github" / "workflows" / "gemini-batch-dispatch-controller.yml"
CHILD_WORKFLOWS = (
    ("agent1", "gemini-autonomous-engineering.yml", "GEMINI_API_KEY"),
    ("agent2", "gemini-agent-2.yml", "GEMINI_API_KEY_2"),
    ("agent3", "gemini-agent-3.yml", "GEMINI_API_KEY_3"),
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
        for job_id, _, _ in CHILD_WORKFLOWS:
            self.assertEqual(
                self.workflow["jobs"][job_id]["if"],
                "github.event_name == 'workflow_dispatch' && inputs.mode == 'agents' && inputs.confirm == 'yes'",
            )
        self.assertEqual(dispatch["inputs"]["mode"]["default"], "probe")
        self.assertEqual(dispatch["inputs"]["mode"]["options"], ["probe", "agents"])

    def test_builtin_github_token_has_no_workflow_level_permissions(self):
        self.assertEqual(self.workflow["permissions"], {})

    def test_transport_pat_removed_and_provider_secrets_are_explicit(self):
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", self.source)
        self.assertNotIn("api.github.com/repos/", self.source)
        self.assertNotIn("secrets: inherit", self.source)
        for job_id, _, secret in CHILD_WORKFLOWS:
            with self.subTest(job=job_id):
                job = self.workflow["jobs"][job_id]
                self.assertEqual(job["secrets"], {secret: chr(36) + "{{ secrets." + secret + " }}"})
                self.assertEqual(job["permissions"], {
                    "contents": "write",
                    "pull-requests": "write",
                    "issues": "read",
                })

    def test_only_the_three_fixed_reusable_workflows_are_called(self):
        for job_id, workflow, _ in CHILD_WORKFLOWS:
            with self.subTest(workflow=workflow):
                job = self.workflow["jobs"][job_id]
                self.assertEqual(job["uses"], "./.github/workflows/" + workflow)
                self.assertEqual(job["with"]["base_ref"], "main")
                self.assertEqual(job["with"]["scope"], "contour-a")
                self.assertIn("Wave 243", job["with"]["task"])

    def test_aggregate_summary_fails_closed(self):
        summary = self.workflow["jobs"]["summarize"]
        self.assertEqual(summary["needs"], ["agent1", "agent2", "agent3"])
        self.assertEqual(
            summary["if"],
            "always() && github.event_name == 'workflow_dispatch' && inputs.mode == 'agents' && inputs.confirm == 'yes'",
        )
        step = summary["steps"][0]
        self.assertEqual(step["env"]["AGENT1_RESULT"], chr(36) + "{{ needs.agent1.result }}")
        self.assertEqual(step["env"]["AGENT2_RESULT"], chr(36) + "{{ needs.agent2.result }}")
        self.assertEqual(step["env"]["AGENT3_RESULT"], chr(36) + "{{ needs.agent3.result }}")
        self.assertIn("fails closed", step["run"])


if __name__ == "__main__":
    unittest.main()
