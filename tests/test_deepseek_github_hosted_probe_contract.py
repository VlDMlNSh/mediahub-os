import unittest
from pathlib import Path


class DeepSeekGitHubHostedProbeContractTests(unittest.TestCase):
    def test_probe_is_github_hosted_and_single_request_only(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github" / "workflows" / "deepseek-github-hosted-one-shot-probe.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("workflow_dispatch:", workflow)
        self.assertIn("runs-on: ubuntu-latest", workflow)
        self.assertNotIn("self-hosted", workflow)
        self.assertIn("github.ref == 'refs/heads/main' && inputs.confirm_request == true", workflow)
        self.assertIn("DEEPSEEK_API_KEY: ${{ secrets.DEEPSEEK_API_KEY }}", workflow)
        self.assertIn("MEDIAHUB_DEEPSEEK_MODEL: ${{ vars.MEDIAHUB_DEEPSEEK_MODEL }}", workflow)
        self.assertIn('MODEL = "deepseek-flash"', workflow)
        self.assertIn('"max_tokens": MAX_OUTPUT_TOKENS', workflow)
        self.assertIn("MAX_OUTPUT_TOKENS = 8", workflow)
        self.assertIn("request_count\"] = 1", workflow)
        self.assertIn("NoRedirect", workflow)
        self.assertIn("no retries", workflow)
        self.assertIn("Upload sanitized evidence", workflow)
        self.assertIn("response_content\": \"SUPPRESSED\"", workflow)
        self.assertNotIn("--retry", workflow)
        self.assertNotIn("qualify_execution_backends.py", workflow)
        self.assertNotIn("secrets: inherit", workflow)


if __name__ == "__main__":
    unittest.main()
