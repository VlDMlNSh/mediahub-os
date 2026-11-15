"""Contract tests for the fixed, single-agent read-only PR 649 review route."""
from pathlib import Path
import hashlib
import hmac
import json
import os
import re
import unittest
from unittest.mock import patch

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
REVIEW_PATH = ROOT / ".github/workflows/gemini-pr649-independent-review.yml"
BASE_SHA = "41c13e1c2b17ac48dc51c9963a9cda140f79ddb0"
HEAD_SHA = "38aafbe40c6a6d55913f13ae9bf1691fa6b2221e"
REVIEW_WORKFLOW = "gemini-pr649-independent-review.yml"


class GeminiPR649ReviewContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.controller_source = CONTROLLER_PATH.read_text(encoding="utf-8")
        cls.controller = yaml.load(cls.controller_source, Loader=yaml.BaseLoader)
        cls.review_source = REVIEW_PATH.read_text(encoding="utf-8")
        cls.review = yaml.load(cls.review_source, Loader=yaml.BaseLoader)

    def test_controller_exposes_separately_confirmed_fixed_mode(self):
        dispatch = self.controller["on"]["workflow_dispatch"]
        self.assertIn("review-pr649", dispatch["inputs"]["mode"]["options"])
        self.assertEqual(dispatch["inputs"]["confirm"]["default"], "false")
        self.assertIn("inputs.mode == 'review-pr649' && inputs.confirm == true",
                      self.controller["jobs"]["readiness_gate"]["if"])
        self.assertIn("inputs.mode == 'review-pr649' && inputs.confirm == true",
                      self.controller["jobs"]["dispatch_and_monitor"]["if"])
        self.assertIn(f'target!="{HEAD_SHA}"', self.controller_source)
        self.assertIn("PR 649 review is pinned to head", self.controller_source)
        self.assertIn(f'("{REVIEW_WORKFLOW}","PR #649 independent static review', self.controller_source)
        self.assertIn("expected_count=len(tasks)", self.controller_source)
        self.assertEqual(set(dispatch["inputs"]), {"mode", "confirm", "target_sha"})
        review_block = self.controller_source.split('elif requested_mode=="review-pr649":', 1)[1].split('elif requested_mode!="agents":', 1)[0]
        self.assertEqual(review_block.count('("gemini-pr649-independent-review.yml"'), 1)
        self.assertEqual(review_block.count('("gemini-'), 1)

    def test_child_is_one_fixed_review_workflow_with_read_only_permissions(self):
        self.assertEqual(set(self.review["on"]), {"workflow_dispatch"})
        self.assertEqual(self.review["permissions"], {"contents": "read"})
        self.assertEqual(self.review["jobs"]["authorize_dispatch"]["permissions"], {})
        self.assertEqual(self.review["jobs"]["review"]["permissions"], {"contents": "read"})
        source = self.review_source
        self.assertIn(f"WORKFLOW_FILE: {REVIEW_WORKFLOW}", source)
        self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", source)
        self.assertIn("secrets.GEMINI_API_KEY_2", source)
        self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
        self.assertNotIn("GITHUB_TOKEN", source)
        self.assertNotIn("create_branch", source)
        self.assertNotIn("create_pull_request", source)
        self.assertIn("persist-credentials: false", source)
        self.assertIn("contents: read", source)

    def test_exact_pr_patch_and_target_are_pinned(self):
        source = self.review_source
        self.assertIn(f"BASE_SHA: {BASE_SHA}", source)
        self.assertIn(f"EXPECTED_HEAD: {HEAD_SHA}", source)
        self.assertIn('[[ "$TARGET_SHA" == "$EXPECTED_HEAD" ]]', source)
        self.assertIn("git diff --no-ext-diff --unified=100", source)
        for path in (
            ".github/workflows/gemini-autonomous-engineering.yml",
            ".github/workflows/gemini-agent-2.yml",
            ".github/workflows/gemini-agent-3.yml",
        ):
            self.assertIn(path, source)
        self.assertIn("review-input/pr-649.patch", source)
        self.assertIn("sha256sum review-input/pr-649.patch", source)

    def test_gemini_has_only_read_only_file_tools_and_no_runtime_authority(self):
        tools = self.review["jobs"]["review"]["steps"][2]["with"]["settings"]
        settings = json.loads(tools)
        self.assertEqual(settings["tools"]["core"],
                         ["read_file", "grep_search", "glob", "list_directory"])
        source = self.review_source
        for forbidden in ("pull-requests: write", "contents: write", "workflow_dispatch:",
                          "secrets: inherit", "gh api", "curl ", "wget "):
            if forbidden == "workflow_dispatch:":
                continue  # The child has exactly one controller-authenticated dispatch trigger.
            self.assertNotIn(forbidden, source)
        prompt = self.review["jobs"]["review"]["steps"][2]["with"]["prompt"]
        for required in ("dispatch_id uniqueness", "HMAC binding", "NOT VERIFIED",
                         "no runtime dispatch was performed", "Do not use shell"):
            self.assertIn(required, prompt)

    @staticmethod
    def _python_heredoc(run_text):
        lines = run_text.splitlines()
        start = next(i for i, line in enumerate(lines) if line.strip() == "python3 - <<'PY'")
        end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "PY")
        return [line.strip() for line in lines[start + 1:end] if line.strip()]

    def test_controller_signature_interoperates_with_review_child_and_rejects_tampering(self):
        run = self.controller["jobs"]["dispatch_and_monitor"]["steps"][0]["run"]
        lines = self._python_heredoc(run)
        payload_line = next(line for line in lines if "; payload={" in line)
        signature_line = next(line for line in lines if line.startswith("sig=hmac.new("))
        auth = self.review["jobs"]["authorize_dispatch"]["steps"][0]
        child_lines = self._python_heredoc(auth["run"])
        child_key = next(line for line in child_lines if line.startswith("key=os.environ.get("))
        child_payload = next(line for line in child_lines if line.startswith("payload={"))
        child_expected = next(line for line in child_lines if line.startswith("expected=hmac.new("))
        fake_key = "unit-test-only-not-a-secret"
        dispatch_id = "123e4567-e89b-42d3-a456-426614174000"
        task = "fixed PR 649 read-only review fixture"
        ns = {
            "hashlib": hashlib, "hmac": hmac, "json": json,
            "wf": REVIEW_WORKFLOW, "did": dispatch_id, "target": HEAD_SHA,
            "task": task, "scope": "contour-a", "key": fake_key,
        }
        exec("payload=" + payload_line.split("; payload=", 1)[1], ns)
        exec(signature_line, ns)
        env = {
            "HMAC_KEY": fake_key, "WORKFLOW_FILE": REVIEW_WORKFLOW,
            "DISPATCH_ID": dispatch_id, "TARGET_SHA": HEAD_SHA, "TASK": task,
            "BASE_REF": "main", "SCOPE": "contour-a", "SIGNATURE": ns["sig"],
            "EVENT_NAME": "workflow_dispatch", "REPOSITORY": "VlDMlNSh/mediahub-os",
            "REF_NAME": "refs/heads/main",
        }
        child_ns = {"hashlib": hashlib, "hmac": hmac, "json": json, "os": os}
        with patch.dict(os.environ, env, clear=False):
            exec(child_key, child_ns)
            exec(child_payload, child_ns)
            exec(child_expected, child_ns)
        self.assertEqual(child_ns["payload"], ns["payload"])
        self.assertTrue(hmac.compare_digest(child_ns["expected"], env["SIGNATURE"]))
        tampered = dict(env, TARGET_SHA=BASE_SHA)
        bad_ns = {"hashlib": hashlib, "hmac": hmac, "json": json, "os": os}
        with patch.dict(os.environ, tampered, clear=False):
            exec(child_key, bad_ns)
            exec(child_payload, bad_ns)
            exec(child_expected, bad_ns)
        self.assertFalse(hmac.compare_digest(bad_ns["expected"], env["SIGNATURE"]))


if __name__ == "__main__":
    unittest.main()
