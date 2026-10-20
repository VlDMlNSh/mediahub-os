"""Static contract tests for the non-launching reusable-workflow caller-context probe."""

from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / ".github" / "workflows" / "gemini-caller-context-probe.yml"
ASTRA_VERIFY_PATH = ROOT / ".github" / "workflows" / "astra-verify.yml"
EXPECTED_GUARD = (
    "github.event_name == 'workflow_dispatch' && "
    "github.workflow_ref == "
    "'VlDMlNSh/mediahub-os/.github/workflows/"
    "gemini-batch-dispatch-controller.yml@refs/heads/main'"
)
FORBIDDEN_PROVIDER_MARKERS = (
    "GEMINI_API_KEY",
    "GEMINI_API_KEY_2",
    "GEMINI_API_KEY_3",
    "run-gemini-cli",
    "github-mcp-server",
    "MEDIAHUB_GITHUB_TOKEN",
    "secrets: inherit",
)


class GeminiCallerContextProbeContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.probe_source = PROBE_PATH.read_text(encoding="utf-8")
        cls.verify_source = ASTRA_VERIFY_PATH.read_text(encoding="utf-8")
        # BaseLoader preserves keys and values such as "on" and "workflow_dispatch" as strings.
        cls.probe = yaml.load(cls.probe_source, Loader=yaml.BaseLoader)
        cls.verify = yaml.load(cls.verify_source, Loader=yaml.BaseLoader)

    def test_probe_uses_the_exact_controller_only_predicate(self):
        self.assertEqual(self.probe["jobs"]["guarded_probe"]["if"], EXPECTED_GUARD)

    def test_probe_exports_the_actual_caller_context_and_job_result(self):
        outputs = self.probe["on"]["workflow_call"]["outputs"]
        self.assertEqual(
            outputs["guarded_job_result"]["value"],
            "${{ jobs.report.outputs.guarded_job_result }}",
        )
        self.assertEqual(
            outputs["caller_event_name"]["value"],
            "${{ jobs.report.outputs.caller_event_name }}",
        )
        self.assertEqual(
            outputs["caller_workflow_ref"]["value"],
            "${{ jobs.report.outputs.caller_workflow_ref }}",
        )
        report = self.probe["jobs"]["report"]
        self.assertEqual(report["if"], "always()")
        self.assertEqual(report["needs"], ["guarded_probe"])
        self.assertEqual(
            report["steps"][0]["env"]["GUARDED_RESULT"],
            "${{ needs.guarded_probe.result }}",
        )
        self.assertEqual(
            report["steps"][0]["env"]["CALLER_EVENT_NAME"],
            "${{ github.event_name }}",
        )
        self.assertEqual(
            report["steps"][0]["env"]["CALLER_WORKFLOW_REF"],
            "${{ github.workflow_ref }}",
        )

    def test_probe_cannot_launch_models_even_if_the_guard_is_wrong(self):
        for marker in FORBIDDEN_PROVIDER_MARKERS:
            with self.subTest(marker=marker):
                self.assertNotIn(marker, self.probe_source)
        # The probe has no external action steps, only inert shell sentinels/context reporting.
        for job in self.probe["jobs"].values():
            for step in job.get("steps", []):
                self.assertNotIn("uses", step)
        self.assertNotIn("secrets", self.probe["on"]["workflow_call"])

    def test_astra_verify_executes_probe_and_asserts_negative_context(self):
        self.assertIn("workflow_dispatch", self.verify["on"])
        jobs = self.verify["jobs"]
        probe_caller = jobs["gemini_caller_context_probe"]
        self.assertEqual(
            probe_caller["uses"],
            "./.github/workflows/gemini-caller-context-probe.yml",
        )
        self.assertEqual(probe_caller["permissions"], {})
        assertion = jobs["assert_gemini_caller_context_probe"]
        self.assertEqual(assertion["if"], "always()")
        self.assertEqual(assertion["needs"], ["gemini_caller_context_probe"])
        env = assertion["steps"][0]["env"]
        self.assertEqual(
            env["GUARDED_RESULT"],
            "${{ needs.gemini_caller_context_probe.outputs.guarded_job_result }}",
        )
        self.assertIn('if [[ "$GUARDED_RESULT" != "skipped" ]]', assertion["steps"][0]["run"])
        self.assertIn("CALLER_EVENT_NAME", assertion["steps"][0]["run"])
        self.assertIn("CALLER_WORKFLOW_REF", assertion["steps"][0]["run"])


if __name__ == "__main__":
    unittest.main()
