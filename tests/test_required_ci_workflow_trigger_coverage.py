"""Required branch-protection contexts must run for every PR targeting main."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CONTEXTS = {
    ".github/workflows/astra-cloud.yml": ("validate", "Astra Cloud Runtime Validation"),
    ".github/workflows/astra-verify.yml": ("verify", "Astra Verify"),
    ".github/workflows/mediahub-ai-factory-verification.yml": ("verify", "AI Factory verification"),
    ".github/workflows/mediahub-provider-contract-verification.yml": ("verify", "provider contract verification"),
    ".github/workflows/gemini-workflow-contract-validation-wave284.yml": (
        "validate",
        "Gemini workflow contract validation (Wave 284)",
    ),
}


class RequiredCiWorkflowTriggerCoverageTests(unittest.TestCase):
    def test_required_context_workflows_run_for_every_main_pull_request(self):
        for relative_path, _ in REQUIRED_CONTEXTS.items():
            with self.subTest(workflow=relative_path):
                document = yaml.load((ROOT / relative_path).read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
                pull_request = document["on"]["pull_request"]
                self.assertEqual(pull_request.get("branches"), ["main"])
                self.assertNotIn("paths", pull_request)
                self.assertNotIn("paths-ignore", pull_request)

    def test_required_job_names_match_ruleset_contexts_exactly(self):
        for relative_path, (job_id, expected_name) in REQUIRED_CONTEXTS.items():
            with self.subTest(workflow=relative_path, job=job_id):
                document = yaml.load((ROOT / relative_path).read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
                actual_name = document["jobs"][job_id].get("name")
                self.assertEqual(actual_name, expected_name)


if __name__ == "__main__":
    unittest.main()
