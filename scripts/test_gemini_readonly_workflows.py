#!/usr/bin/env python3
"""Fast regression tests for the read-only Gemini workflow security contract.

These checks never load credentials, call a provider, or execute model output.
YAML syntax and GitHub Actions expression validation is delegated to actionlint.
"""
from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"
AUDIT = WORKFLOW_DIR / "gemini-readonly-audit.yml"
RETRY = WORKFLOW_DIR / "gemini-readonly-audit-retry.yml"
HTTP_HELPER = ROOT / "scripts" / "gemini_http_response.js"
HTTP_HARNESS = ROOT / "scripts" / "test_gemini_http_response.js"
MODEL = "gemini-3.5-flash-lite"
PINNED_ACTION = re.compile(r"^\s*uses:\s*[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+@([0-9a-f]{40})\s*$")


class GeminiReadOnlyWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = AUDIT.read_text(encoding="utf-8")
        cls.retry = RETRY.read_text(encoding="utf-8")

    def test_all_external_actions_are_pinned_to_full_sha(self) -> None:
        for path, source in ((AUDIT, self.audit), (RETRY, self.retry)):
            with self.subTest(workflow=path.name):
                uses = [line for line in source.splitlines() if re.match(r"^\s*uses:", line)]
                self.assertGreaterEqual(len(uses), 2)
                for line in uses:
                    self.assertRegex(line, PINNED_ACTION)

    def test_workflows_are_read_only_and_never_request_oidc(self) -> None:
        for path, source in ((AUDIT, self.audit), (RETRY, self.retry)):
            with self.subTest(workflow=path.name):
                self.assertRegex(source, r"(?m)^permissions:\n  contents: read\s*$")
                self.assertRegex(source, r"(?m)^    permissions:\n      contents: read\s*$")
                self.assertNotRegex(source, r"(?m)^\s*(?:contents|pull-requests|actions|id-token):\s*write\s*$")
                self.assertNotIn("create_or_update_file", source)
                self.assertNotIn("create_pull_request", source)

    def test_context_is_fixed_bounded_and_checkout_is_immutable(self) -> None:
        for path, source in ((AUDIT, self.audit), (RETRY, self.retry)):
            with self.subTest(workflow=path.name):
                self.assertIn("ref: ${{ github.sha }}", source)
                self.assertIn("persist-credentials: false", source)
                self.assertIn('[[ "$GITHUB_REF" == "refs/heads/main" ]]', source)
                self.assertIn("context_profile", source)
                self.assertNotIn("inputs.context_paths", source)
                self.assertNotIn("inputs.context_ref", source)
                self.assertIn("task_bytes <= 2000", source)
                self.assertIn("total_bytes <= 200000", source)
                self.assertIn("! -L", source)

    def test_provider_model_is_fixed_and_output_is_quarantined(self) -> None:
        for path, source in ((AUDIT, self.audit), (RETRY, self.retry)):
            with self.subTest(workflow=path.name):
                self.assertIn(MODEL, source)
                self.assertNotIn("inputs.model", source)
                self.assertIn("maxOutputTokens:4096", source)
                self.assertIn("bytes > 100000", source)
                self.assertIn("Untrusted model-generated advisory output", source)
                self.assertIn("evidence-manifest.json", source)
                self.assertIn("output_sha256", source)
                self.assertNotRegex(source, r"(?i)echo\s+.*(?:GEMINI_API_KEY|GOOGLE_API_KEY)")
                self.assertNotIn("text.slice(0,45000)", source)

    def test_non_idempotent_generation_post_is_never_retried_automatically(self) -> None:
        self.assertIn("non-idempotent-generation-post-no-automatic-retry", self.retry)
        self.assertIn("manifest.attempts = 1", self.retry)
        self.assertNotIn("for (let attempt=", self.retry)
        self.assertNotIn("new Set([500, 502, 503, 504])", self.retry)
        self.assertNotIn("retryableServerStatuses", self.retry)
        self.assertNotIn("retryDelay(", self.retry)
        self.assertNotIn("await sleep(", self.retry)
        self.assertNotIn("GEMINI_MODEL", self.audit + self.retry)
        self.assertNotIn("OPENROUTER_API_KEY", self.audit + self.retry)

    def test_response_body_is_streamed_with_a_hard_byte_cap(self) -> None:
        self.assertIn("require('./scripts/gemini_http_response')", self.retry)
        self.assertIn("await readBoundedResponse(res, req, 2*1024*1024)", self.retry)
        self.assertNotIn("responseBytes > maxResponseBytes", self.retry)
        self.assertNotIn("res.on('end',() => resolve({", self.retry)
        self.assertIn("require('./scripts/gemini_http_response')", self.audit)
        self.assertIn("await readBoundedResponse(res, req, 2*1024*1024)", self.audit)
        self.assertIn("DEFAULT_MAX_RESPONSE_BYTES = 2 * 1024 * 1024", HTTP_HELPER.read_text(encoding="utf-8"))
        self.assertIn("response byte limit exceeded", HTTP_HELPER.read_text(encoding="utf-8"))
        self.assertLess(self.audit.index("await readBoundedResponse"), self.audit.index("fs.writeFileSync(outputPath"))
        self.assertLess(HTTP_HELPER.read_text(encoding="utf-8").index("res.on('end'"), HTTP_HELPER.read_text(encoding="utf-8").index("resolve({"))

    def test_primary_workflow_handles_abort_and_transport_errors_without_undefined_reject(self) -> None:
        reject_definition = self.audit.index("const reject = err =>")
        helper = HTTP_HELPER.read_text(encoding="utf-8")
        abort_handler = helper.index("res.on('aborted'")
        response_end = helper.index("res.on('end'")
        output_write = self.audit.index("fs.writeFileSync(outputPath")
        self.assertLess(reject_definition, self.audit.index("await readBoundedResponse"))
        self.assertIn("req.on('error',reject)", self.audit)
        self.assertIn("if (settled) return;", self.audit)
        self.assertLess(response_end, helper.index("resolve({"))
        self.assertLess(self.audit.index("await readBoundedResponse"), output_write)
        self.assertNotIn("req.on('error',err=>{", self.audit)

    def test_local_http_regression_harness(self) -> None:
        result = subprocess.run(
            ["node", str(HTTP_HARNESS)],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, msg=result.stdout + result.stderr)
        self.assertIn("complete valid response writes output", result.stdout)

    def test_both_workflows_emit_real_newlines_in_advisory_artifacts(self) -> None:
        for path, source in ((AUDIT, self.audit), (RETRY, self.retry)):
            with self.subTest(workflow=path.name):
                self.assertIn(r"join('\\n').trim()", source)
                self.assertIn("fs.writeFileSync(outputPath", source)
                self.assertIn("Untrusted model-generated advisory output", source)

    def test_artifact_retention_is_bounded(self) -> None:
        for path, source in ((AUDIT, self.audit), (RETRY, self.retry)):
            with self.subTest(workflow=path.name):
                self.assertIn("retention-days: 14", source)


if __name__ == "__main__":
    unittest.main(verbosity=2)
