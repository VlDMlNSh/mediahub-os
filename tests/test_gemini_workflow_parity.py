"""Static parity checks for the three manually dispatched Gemini engineering workflows.

These tests validate repository-visible guardrails only; they do not prove that
Gemini credentials work, that a workflow was dispatched, or that a run is safe.
"""
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = {
    ".github/workflows/gemini-autonomous-engineering.yml": "GEMINI_API_KEY",
    ".github/workflows/gemini-agent-2.yml": "GEMINI_API_KEY_2",
    ".github/workflows/gemini-agent-3.yml": "GEMINI_API_KEY_3",
}
EXPECTED_MCP_TOOLS = (
    "create_branch",
    "create_or_update_file",
    "create_pull_request",
    "get_file_contents",
)


class GeminiWorkflowParityTests(unittest.TestCase):
    def _source(self, relative_path):
        path = ROOT / relative_path
        self.assertTrue(path.is_file(), f"missing workflow: {relative_path}")
        return path.read_text(encoding="utf-8")

    def test_all_three_workflows_exist_and_use_distinct_credentials(self):
        credential_refs = []
        for relative_path, credential in WORKFLOWS.items():
            with self.subTest(workflow=relative_path):
                source = self._source(relative_path)
                self.assertIn(f"secrets.{credential}", source)
                credential_refs.append(credential)
        self.assertEqual(len(credential_refs), len(set(credential_refs)))

    def test_dispatch_scope_and_execution_host_are_bounded(self):
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                source = self._source(relative_path)
                self.assertIn("workflow_dispatch:", source)
                self.assertIn("required: true", source)
                self.assertIn("default: main", source)
                self.assertIn("default: contour-a", source)
                self.assertIn("runs-on: ubuntu-latest", source)
                self.assertRegex(source, r"timeout-minutes:\s*30")
                self.assertNotRegex(source, r"runs-on:\s*\[?self-hosted")
                self.assertIn("persist-credentials: false", source)

    def test_github_mcp_tool_allowlist_matches_exact_expected_order(self):
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                source = self._source(relative_path)
                match = re.search(
                    r'"includeTools"\s*:\s*\[(.*?)\]',
                    source,
                    flags=re.DOTALL,
                )
                self.assertIsNotNone(match, "GitHub MCP tool allowlist is missing")
                actual = tuple(re.findall(r'"([^"]+)"', match.group(1)))
                self.assertEqual(actual, EXPECTED_MCP_TOOLS)

    def test_all_workflows_restrict_checkout_credentials_and_forbid_implicit_promotion(self):
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                source = self._source(relative_path)
                self.assertIn("pull-requests: write", source)
                self.assertIn("contents: write", source)
                self.assertIn("Never merge or deploy.", source)
                self.assertIn("Do not install software", source)
                self.assertIn("upload_artifacts: 'true'", source)

    def test_action_and_container_pin_gaps_are_explicitly_detectable(self):
        # This is a finding detector, not an assertion that current refs are safe.
        mutable_refs = []
        for relative_path in WORKFLOWS:
            source = self._source(relative_path)
            if re.search(r"uses:\s*actions/checkout@v\d+", source):
                mutable_refs.append((relative_path, "actions/checkout"))
            if re.search(r"uses:\s*google-github-actions/run-gemini-cli@v\d+", source):
                mutable_refs.append((relative_path, "run-gemini-cli"))
            if "ghcr.io/github/github-mcp-server:v0.27.0" in source:
                mutable_refs.append((relative_path, "github-mcp-server"))
        self.assertEqual(
            len(mutable_refs),
            9,
            "Expected three mutable reference findings per workflow; revisit this "
            "detector when immutable, provenance-verified pins are introduced.",
        )


if __name__ == "__main__":
    unittest.main()
