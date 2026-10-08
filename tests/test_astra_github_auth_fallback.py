import os
import unittest
from unittest.mock import patch

from mediahub_runtime import autonomous_queue


class AstraGithubAuthFallbackTests(unittest.TestCase):
    @patch.dict(os.environ, {}, clear=True)
    @patch("mediahub_runtime.autonomous_queue.subprocess.run")
    def test_authenticated_gh_cli_token_is_used(self, run):
        run.return_value.returncode = 0
        run.return_value.stdout = "opaque-token\n"
        env = autonomous_queue.github_auth_env()
        self.assertIsNotNone(env)
        self.assertEqual(env["GH_TOKEN"], "opaque-token")
        run.assert_called_once()
        self.assertEqual(run.call_args.args[0], ["gh", "auth", "token"])

    @patch.dict(os.environ, {}, clear=True)
    @patch("mediahub_runtime.autonomous_queue.subprocess.run")
    def test_missing_gh_auth_blocks(self, run):
        run.return_value.returncode = 1
        run.return_value.stdout = ""
        self.assertIsNone(autonomous_queue.github_auth_env())


if __name__ == "__main__":
    unittest.main()
