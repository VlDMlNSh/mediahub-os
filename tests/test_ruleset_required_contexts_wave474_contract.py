"""Ensure active required status-check contexts exist as exact PR job names and triggers."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CHILD = ".github/workflows/gemini-pr-readonly-review-wave471.yml"
CHILD_TEST = "tests/test_gemini_pr_readonly_review_wave471_contract.py"
SELF = "tests/test_ruleset_required_contexts_wave474_contract.py"

REQUIRED = {
    "Astra Cloud Runtime Validation": (".github/workflows/astra-cloud.yml", "validate"),
    "AI Factory verification": (".github/workflows/mediahub-ai-factory-verification.yml", "verify"),
    "provider contract verification": (".github/workflows/mediahub-provider-contract-verification.yml", "verify"),
    "Astra Verify": (".github/workflows/astra-verify.yml", "verify"),
    "Gemini workflow contract validation (Wave 284)": (
        ".github/workflows/gemini-workflow-contract-validation-wave284.yml", "validate"
    ),
}


def load_workflow(path):
    source = (ROOT / path).read_text(encoding="utf-8")
    return yaml.load(source, Loader=yaml.BaseLoader)


class RulesetRequiredContextsWave474Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflows = {
            context: (path, job, load_workflow(path)["jobs"][job])
            for context, (path, job) in REQUIRED.items()
        }

    def test_each_required_context_is_an_exact_job_name(self):
        for context, (path, job_id, job) in self.workflows.items():
            with self.subTest(context=context):
                self.assertEqual(
                    job.get("name"), context,
                    f"{path} job {job_id} must publish exact ruleset context {context!r}",
                )

    def test_ai_factory_and_provider_workflows_cover_review_child_changes(self):
        for context in ("AI Factory verification", "provider contract verification"):
            path, _, _ = self.workflows[context]
            triggers = load_workflow(path)["on"]["pull_request"]
            paths = set(triggers["paths"])
            with self.subTest(context=context):
                self.assertIn(CHILD, paths)
                self.assertIn(CHILD_TEST, paths)

    def test_gemini_contract_validation_covers_review_child_and_runs_this_test(self):
        path, _, job = self.workflows["Gemini workflow contract validation (Wave 284)"]
        workflow = load_workflow(path)
        paths = set(workflow["on"]["pull_request"]["paths"])
        self.assertIn(CHILD, paths)
        self.assertIn(CHILD_TEST, paths)
        self.assertIn(SELF, paths)
        commands = "\n".join(step.get("run", "") for step in job["steps"])
        self.assertIn("test_ruleset_required_contexts_wave474_contract.py", commands)

    def test_astra_required_workflows_run_for_pull_requests_without_path_allowlists(self):
        for context in ("Astra Verify", "Astra Cloud Runtime Validation"):
            path, _, _ = self.workflows[context]
            pull_request = load_workflow(path)["on"]["pull_request"]
            with self.subTest(context=context):
                self.assertNotIn("paths", pull_request)


if __name__ == "__main__":
    unittest.main()
