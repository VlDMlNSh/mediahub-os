"""Contract tests for the signed PR-scoped read-only Gemini review child."""
from pathlib import Path
import re
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/gemini-pr-readonly-review-wave471.yml"
TASK = "PR-scoped read-only security, contract, and regression review; no code changes."


class PRReadOnlyReviewWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW.read_text(encoding="utf-8")
        cls.document = yaml.load(cls.source, Loader=yaml.BaseLoader)

    def test_dispatch_inputs_bind_pr_and_both_immutable_shas(self):
        inputs = self.document["on"]["workflow_dispatch"]["inputs"]
        for name in ("dispatch_id", "pr_number", "base_sha", "target_sha",
                     "task", "dispatch_signature"):
            with self.subTest(input=name):
                self.assertIn(name, inputs)
                self.assertTrue(inputs[name]["required"])

    def test_hmac_binds_pr_number_base_sha_and_head_sha(self):
        self.assertIn('"pr_number":pr,"base_sha":base,"target_sha":head', self.source)
        self.assertIn("hmac.compare_digest(expected,os.environ.get(\"SIGNATURE\",\"\"))", self.source)
        self.assertIn('data.get("head",{}).get("sha")!=head', self.source)
        self.assertIn('data.get("base",{}).get("sha")!=base', self.source)

    def test_only_open_same_repository_pr_based_on_main_is_accepted(self):
        for required in (
            'data.get("state")!="open"',
            'data.get("base",{}).get("ref")!="main"',
            'data.get("head",{}).get("repo",{}).get("full_name")!="VlDMlNSh/mediahub-os"',
        ):
            with self.subTest(condition=required):
                self.assertIn(required, self.source)

    def test_fixed_task_and_uuid_and_numeric_pr_guards_exist(self):
        self.assertIn(TASK, self.source)
        self.assertIn('re.fullmatch(r"[1-9][0-9]{0,8}",pr)', self.source)
        self.assertIn('re.fullmatch(r"[0-9a-f]{40}",base)', self.source)
        self.assertIn('re.fullmatch(r"[0-9a-f]{40}",head)', self.source)
        self.assertIn('re.fullmatch(uuid,did)', self.source)

    def test_diff_and_manifest_are_bound_to_verified_base_and_head(self):
        self.assertIn('git diff --no-ext-diff --no-renames --unified=60 "$BASE_SHA" "$TARGET_SHA" --', self.source)
        self.assertIn('"pull_request_number":int(pr)', self.source)
        self.assertIn('"base_sha":base', self.source)
        self.assertIn('"head_sha":head', self.source)
        self.assertIn('"changed_files":files', self.source)

    def test_child_is_read_only_and_never_dispatches_or_mutates(self):
        self.assertEqual(self.document["permissions"]["contents"], "read")
        self.assertEqual(self.document["permissions"]["pull-requests"], "read")
        self.assertIn('"tools": { "core": ["read_file", "grep_search", "glob", "list_directory"] }', self.source)
        self.assertIn("Do not edit files", self.source)
        self.assertNotIn("contents: write", self.source)
        self.assertNotIn("issues: write", self.source)
        self.assertIn("permissions:\n  contents: read\n  pull-requests: read", self.source)

    def test_artifact_contains_manifest_patch_and_file_list(self):
        self.assertIn("review-input/manifest.json", self.source)
        self.assertIn("review-input/review.patch", self.source)
        self.assertIn("review-input/changed-files.txt", self.source)
        self.assertIn("actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02", self.source)


if __name__ == "__main__":
    unittest.main()
