"""Static contracts for a least-privilege, non-launching reusable-workflow probe."""
from pathlib import Path
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROBE_PATH = ROOT / ".github/workflows/gemini-controller-context-probe-wave284.yml"
OBSERVER_PATH = ROOT / ".github/workflows/gemini-reusable-context-probe-wave284.yml"
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
        cls.observer_source = OBSERVER_PATH.read_text(encoding="utf-8")
        cls.observer = yaml.load(cls.observer_source, Loader=yaml.BaseLoader)
        cls.children = [
            (path.name, yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader), secret)
            for path, secret in CHILD_PATHS
        ]

    def test_probe_has_no_token_authority_provider_secret_or_model_step(self):
        self.assertEqual(self.probe["permissions"], {})
        probe_job = self.probe["jobs"]["probe"]
        self.assertEqual(probe_job["permissions"], {})
        self.assertNotIn("secrets", probe_job, "the probe must not forward provider secrets")
        self.assertNotIn("GEMINI_API_KEY", self.probe_source)
        self.assertNotIn("run-gemini-cli", self.probe_source)
        self.assertNotIn("probe_only", probe_job.get("with", {}))
        self.assertEqual(self.probe["jobs"]["assert_untrusted_context"]["permissions"], {})

    def test_probe_asserts_real_untrusted_caller_context(self):
        verify = self.probe["jobs"]["assert_untrusted_context"]
        run_script = verify["steps"][0]["run"]
        self.assertIn('[[ "$OBSERVED_EVENT_NAME" == "pull_request" ]]', run_script)
        self.assertIn("gemini-controller-context-probe-wave284.yml@", run_script)
        self.assertIn('[[ "$OBSERVED_TRUSTED_CONTROLLER" == "false" ]]', run_script)
        self.assertIn('[[ "$OBSERVED_WORKFLOW_REF" != "$TRUSTED_CONTROLLER_REF" ]]', run_script)

    def test_observer_is_a_minimal_read_only_workflow_call(self):
        self.assertEqual(self.observer["permissions"], {})
        call = self.observer["on"]["workflow_call"]
        self.assertIn("caller_event_name", call["outputs"])
        self.assertIn("caller_workflow_ref", call["outputs"])
        self.assertIn("caller_trusted_controller", call["outputs"])
        job = self.observer["jobs"]["observe"]
        self.assertEqual(job["permissions"], {})
        self.assertIsNone(job["steps"][0].get("uses"))
        script = job["steps"][0]["run"]
        self.assertIn("$GITHUB_EVENT_NAME", script)
        self.assertIn("$GITHUB_WORKFLOW_REF", script)
        self.assertIn(TRUSTED_CONTROLLER_REF, self.observer_source)
        self.assertNotIn("GEMINI_API_KEY", self.observer_source)
        self.assertNotIn("run-gemini-cli", self.observer_source)

    def test_every_gemini_child_is_a_fixed_dispatch_target(self):
        for name, child, secret in self.children:
            with self.subTest(child=name):
                dispatch = child["on"]["workflow_dispatch"]
                self.assertIn("task", dispatch["inputs"])
                self.assertEqual(dispatch["inputs"]["base_ref"]["type"], "string")
                self.assertIn("scope", dispatch["inputs"])
                source = (ROOT / ".github" / "workflows" / name).read_text(encoding="utf-8")
                self.assertIn("secrets." + secret, source)
                self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
                self.assertNotIn("secrets: inherit", source)
                self.assertEqual(child["permissions"]["contents"], "read")
                self.assertIn("ghcr.io/github/github-mcp-server@sha256:", source)

    def test_probe_uses_distinct_observer_path_and_pull_request_trigger(self):
        self.assertEqual(
            self.probe["jobs"]["probe"]["uses"],
            "./.github/workflows/gemini-reusable-context-probe-wave284.yml",
        )
        self.assertIn("pull_request", self.probe["on"])
        paths = self.probe["on"]["pull_request"]["paths"]
        self.assertIn(".github/workflows/gemini-controller-context-probe-wave284.yml", paths)
        self.assertIn(".github/workflows/gemini-reusable-context-probe-wave284.yml", paths)


if __name__ == "__main__":
    unittest.main()
