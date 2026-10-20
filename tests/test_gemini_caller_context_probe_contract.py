"""Static contract for the actual, non-launching GitHub caller-context probe."""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / ".github/workflows/gemini-caller-context-probe.yml"
CHILD_PATHS = (
    (ROOT / ".github/workflows/gemini-autonomous-engineering.yml", "GEMINI_API_KEY"),
    (ROOT / ".github/workflows/gemini-agent-2.yml", "GEMINI_API_KEY_2"),
    (ROOT / ".github/workflows/gemini-agent-3.yml", "GEMINI_API_KEY_3"),
)
TRUSTED_CONTROLLER_REF = (
    "VlDMlNSh/mediahub-os/.github/workflows/"
    "gemini-batch-dispatch-controller.yml@refs/heads/main"
)


class GeminiCallerContextProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.probe_source = PROBE_PATH.read_text(encoding="utf-8")
        cls.probe = yaml.load(cls.probe_source, Loader=yaml.BaseLoader)
        cls.children = [
            (path.name, yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader), secret)
            for path, secret in CHILD_PATHS
        ]

    def test_probe_has_no_provider_secret_or_model_step(self):
        self.assertEqual(
            self.probe["permissions"],
            {"contents": "read", "issues": "read"},
        )
        self.assertEqual(
            self.probe["jobs"]["assert_untrusted_context"]["permissions"], {}
        )
        probe_job = self.probe["jobs"]["probe"]
        # The reusable child declares read-only contents/issues permissions for
        # its engineer job; only this skipped probe call must grant that ceiling.
        self.assertEqual(
            probe_job["permissions"],
            {"contents": "read", "issues": "read"},
        )
        self.assertNotIn("secrets", probe_job, "the probe must not forward any provider secrets")
        self.assertEqual(probe_job["with"]["probe_only"], "true")
        self.assertNotIn("GEMINI_API_KEY", self.probe_source)
        self.assertNotIn("run-gemini-cli", self.probe_source)
        self.assertIn("assert_untrusted_context", self.probe["jobs"])

    def test_probe_asserts_real_untrusted_caller_context(self):
        verify = self.probe["jobs"]["assert_untrusted_context"]
        run_script = verify["steps"][0]["run"]
        self.assertIn('[[ "$OBSERVED_EVENT_NAME" == "pull_request" ]]', run_script)
        self.assertIn('gemini-caller-context-probe.yml@', run_script)
        self.assertIn('[[ "$OBSERVED_TRUSTED_CONTROLLER" == "false" ]]', run_script)
        self.assertIn('[[ "$OBSERVED_WORKFLOW_REF" != "$TRUSTED_CONTROLLER_REF" ]]', run_script)

    def test_every_child_has_probe_only_input_and_context_outputs(self):
        for name, child, secret in self.children:
            with self.subTest(child=name):
                call = child["on"]["workflow_call"]
                self.assertEqual(call["inputs"]["probe_only"]["type"], "boolean")
                self.assertEqual(call["inputs"]["probe_only"]["default"], "false")
                self.assertEqual(call["secrets"][secret]["required"], "false")
                self.assertIn("caller_event_name", call["outputs"])
                self.assertIn("caller_workflow_ref", call["outputs"])
                self.assertIn("caller_trusted_controller", call["outputs"])

                jobs = child["jobs"]
                self.assertEqual(jobs["caller_context"]["permissions"], {})
                self.assertEqual(jobs["reject_untrusted_caller"]["permissions"], {})
                self.assertIn("inputs.probe_only != true", jobs["reject_untrusted_caller"]["if"])
                self.assertIn("inputs.probe_only != true", jobs["engineer"]["if"])
                self.assertIn("needs.caller_context.outputs.trusted_controller == 'true'", jobs["engineer"]["if"])
                self.assertEqual(jobs["engineer"]["needs"], ["caller_context", "reject_untrusted_caller"])
                self.assertIn(TRUSTED_CONTROLLER_REF, jobs["engineer"]["if"])

    def test_probe_workflow_only_calls_a_fixed_child_in_probe_mode(self):
        self.assertEqual(
            self.probe["jobs"]["probe"]["uses"],
            "./.github/workflows/gemini-agent-2.yml",
        )
        self.assertIn("pull_request", self.probe["on"])
        self.assertEqual(self.probe["jobs"]["probe"]["with"]["scope"], "contour-a")
        self.assertIn("Non-launching", self.probe["jobs"]["probe"]["with"]["task"])


if __name__ == "__main__":
    unittest.main()
