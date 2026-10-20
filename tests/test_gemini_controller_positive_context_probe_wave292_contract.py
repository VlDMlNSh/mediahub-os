"""Static security contracts for the no-secret trusted-controller probe (Wave 292)."""
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
TRUSTED_CONTROLLER_REF = (
    "VlDMlNSh/mediahub-os/.github/workflows/"
    "gemini-batch-dispatch-controller.yml@refs/heads/main"
)


class GeminiPositiveContextProbeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = CONTROLLER_PATH.read_text(encoding="utf-8")
        cls.controller = yaml.load(cls.source, Loader=yaml.BaseLoader)
        cls.children = [
            yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
            for path in CHILD_PATHS
        ]

    def test_probe_is_default_and_has_no_secret_or_write_authority(self):
        inputs = self.controller["on"]["workflow_dispatch"]["inputs"]
        self.assertEqual(inputs["mode"]["default"], "probe")
        self.assertEqual(inputs["mode"]["options"], ["probe", "agents"])
        self.assertEqual(self.controller["permissions"], {})
        probe = self.controller["jobs"]["probe"]
        self.assertEqual(probe["permissions"], {})
        self.assertNotIn("secrets", probe)
        self.assertEqual(probe["uses"], "./.github/workflows/gemini-reusable-context-probe-wave284.yml")
        self.assertNotIn("secrets", probe)
        self.assertNotIn("GEMINI_API_KEY", str(probe))
        self.assertNotIn("run-gemini-cli", str(probe))
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", str(probe))
        observer_path = ROOT / ".github/workflows/gemini-reusable-context-probe-wave284.yml"
        observer_source = observer_path.read_text(encoding="utf-8")
        observer = yaml.load(observer_source, Loader=yaml.BaseLoader)
        self.assertEqual(observer["permissions"], {})
        self.assertEqual(observer["jobs"]["observe"]["permissions"], {})
        self.assertNotIn("GEMINI_API_KEY", observer_source)
        self.assertNotIn("run-gemini-cli", observer_source)

    def test_model_jobs_require_explicit_agents_mode_and_confirmation(self):
        for name in ("agent1", "agent2", "agent3"):
            condition = self.controller["jobs"][name]["if"]
            self.assertIn("github.event_name == 'workflow_dispatch'", condition)
            self.assertIn("inputs.mode == 'agents'", condition)
            self.assertIn("inputs.confirm == 'yes'", condition)
        self.assertIn("inputs.mode == 'agents'", self.controller["jobs"]["summarize"]["if"])

    def test_probe_asserts_both_trusted_dispatch_and_untrusted_pr_paths(self):
        verify = self.controller["jobs"]["assert_probe_context"]
        self.assertEqual(verify["permissions"], {})
        self.assertEqual(verify["needs"], ["probe"])
        script = verify["steps"][0]["run"]
        self.assertIn('[[ "$OBSERVED_WORKFLOW_REF" == "$TRUSTED_CONTROLLER_REF" ]]', script)
        self.assertIn('[[ "$OBSERVED_TRUSTED_CONTROLLER" == "true" ]]', script)
        self.assertIn('[[ "$OBSERVED_WORKFLOW_REF" == *"/.github/workflows/gemini-batch-dispatch-controller.yml@refs/pull/"* ]]', script)
        self.assertIn('[[ "$OBSERVED_TRUSTED_CONTROLLER" == "false" ]]', script)
        self.assertIn(TRUSTED_CONTROLLER_REF, self.source)

    def test_agent_children_keep_default_denied_probe_gate(self):
        for child in self.children:
            with self.subTest(workflow=child["name"]):
                engineer = child["jobs"]["engineer"]
                self.assertIn("inputs.probe_only != true", engineer["if"])
                self.assertIn("needs.caller_context.outputs.trusted_controller == 'true'", engineer["if"])
                self.assertEqual(child["jobs"]["caller_context"]["permissions"], {})

    def test_pr_trigger_is_non_launching_and_covers_contract_paths(self):
        pr = self.controller["on"]["pull_request"]
        self.assertIn(".github/workflows/gemini-batch-dispatch-controller.yml", pr["paths"])
        self.assertIn("tests/test_gemini_controller_positive_context_probe_wave292_contract.py", pr["paths"])
        self.assertIn("github.event_name == 'pull_request'", self.controller["jobs"]["probe"]["if"])


if __name__ == "__main__":
    unittest.main()
