"""Required branch-protection contexts must run for every PR targeting main."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_WORKFLOWS = (
    ".github/workflows/gemini-workflow-contract-validation-wave284.yml",
    ".github/workflows/mediahub-ai-factory-verification.yml",
    ".github/workflows/mediahub-provider-contract-verification.yml",
)


class RequiredCiWorkflowTriggerCoverageTests(unittest.TestCase):
    def test_required_context_workflows_are_not_path_filtered(self):
        for relative_path in REQUIRED_WORKFLOWS:
            with self.subTest(workflow=relative_path):
                document = yaml.load((ROOT / relative_path).read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
                pull_request = document["on"]["pull_request"]
                self.assertEqual(pull_request.get("branches"), ["main"])
                self.assertNotIn("paths", pull_request)


if __name__ == "__main__":
    unittest.main()
