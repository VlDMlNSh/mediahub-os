from pathlib import Path
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
READONLY_WORKFLOW = ".github/workflows/gemini-pr-readonly-review-wave471.yml"
READONLY_TEST = "tests/test_gemini_pr_readonly_review_wave471_contract.py"
COVERAGE_TEST = "tests/test_required_ci_context_alignment_wave474.py"

REQUIRED_CHECK_JOBS = {
    ".github/workflows/astra-cloud.yml": (
        "validate",
        "Astra Cloud Runtime Validation",
    ),
    ".github/workflows/mediahub-ai-factory-verification.yml": (
        "verify",
        "AI Factory verification",
    ),
    ".github/workflows/mediahub-provider-contract-verification.yml": (
        "verify",
        "provider contract verification",
    ),
    ".github/workflows/astra-verify.yml": (
        "verify",
        "Astra Verify",
    ),
    ".github/workflows/gemini-workflow-contract-validation-wave284.yml": (
        "validate",
        "Gemini workflow contract validation (Wave 284)",
    ),
}


def load_workflow(relative_path: str) -> dict:
    path = ROOT / relative_path
    return yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)


class RequiredCiContextAlignmentWave474Tests(unittest.TestCase):
    def test_required_job_names_match_repository_ruleset_contexts(self):
        for workflow_path, (job_id, expected_name) in REQUIRED_CHECK_JOBS.items():
            with self.subTest(workflow=workflow_path):
                workflow = load_workflow(workflow_path)
                self.assertEqual(
                    workflow["jobs"][job_id].get("name"),
                    expected_name,
                    f"{workflow_path}:{job_id} must emit exact required check context",
                )

    def test_pr_readonly_review_changes_trigger_all_three_scoped_validators(self):
        scoped_workflows = (
            ".github/workflows/mediahub-ai-factory-verification.yml",
            ".github/workflows/mediahub-provider-contract-verification.yml",
            ".github/workflows/gemini-workflow-contract-validation-wave284.yml",
        )
        for workflow_path in scoped_workflows:
            with self.subTest(workflow=workflow_path):
                pull_request = load_workflow(workflow_path)["on"]["pull_request"]
                paths = pull_request.get("paths", [])
                self.assertIn(READONLY_WORKFLOW, paths)
                self.assertIn(READONLY_TEST, paths)

    def test_gemini_contract_validator_lints_and_executes_readonly_child_contract(self):
        workflow = load_workflow(
            ".github/workflows/gemini-workflow-contract-validation-wave284.yml"
        )
        steps = workflow["jobs"]["validate"]["steps"]
        actionlint_commands = [
            str(step.get("run", ""))
            for step in steps
            if "actionlint" in str(step.get("run", ""))
        ]
        self.assertTrue(actionlint_commands)
        self.assertTrue(
            any(READONLY_WORKFLOW in command for command in actionlint_commands)
        )
        child_lint = [
            step for step in steps
            if READONLY_WORKFLOW in str(step.get("run", ""))
        ]
        self.assertTrue(child_lint)
        self.assertTrue(
            any(READONLY_WORKFLOW in str(step.get("if", "")) for step in child_lint)
        )
        child_test = [
            step for step in steps
            if "test_gemini_pr_readonly_review_wave471_contract.py" in str(step.get("run", ""))
        ]
        self.assertTrue(child_test)
        self.assertTrue(
            any("hashFiles" in str(step.get("if", "")) for step in child_test)
        )

    def test_this_alignment_contract_runs_in_gemini_validation_workflow(self):
        workflow = load_workflow(
            ".github/workflows/gemini-workflow-contract-validation-wave284.yml"
        )
        paths = workflow["on"]["pull_request"].get("paths", [])
        self.assertIn(COVERAGE_TEST, paths)
        steps = workflow["jobs"]["validate"]["steps"]
        self.assertTrue(
            any(COVERAGE_TEST in str(step.get("run", "")) for step in steps)
        )


if __name__ == "__main__":
    unittest.main()
