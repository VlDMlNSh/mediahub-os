import os
import tempfile
import unittest
from pathlib import Path

from runtime.mediahub_runtime.local_executor import (
    ExecutorRequest,
    LocalExecutorError,
    build_argv,
    execute,
    resolve_command,
)


class LocalExecutorTests(unittest.TestCase):
    def test_allowlisted_provider_identity(self):
        self.assertEqual(resolve_command("CODEX_LOCAL"), ("codex",))
        self.assertEqual(resolve_command("CLAUDE_LOCAL"), ("claude",))

    def test_rejects_provider_identity_mismatch(self):
        old = os.environ.get("MEDIAHUB_CODEX_EXECUTOR")
        os.environ["MEDIAHUB_CODEX_EXECUTOR"] = "bash"
        try:
            with self.assertRaises(LocalExecutorError):
                resolve_command("CODEX_LOCAL")
        finally:
            if old is None:
                os.environ.pop("MEDIAHUB_CODEX_EXECUTOR", None)
            else:
                os.environ["MEDIAHUB_CODEX_EXECUTOR"] = old

    def test_builds_provider_specific_argv(self):
        codex = build_argv(ExecutorRequest("t","c","o",1,"sha","CODEX_LOCAL",Path("."),"x"))
        claude = build_argv(ExecutorRequest("t","c","o",1,"sha","CLAUDE_LOCAL",Path("."),"x"))
        self.assertEqual(codex[1:4], ("exec","--skip-git-repo-check","--sandbox"))
        self.assertEqual(claude[1], "-p")

    def test_executes_bounded_local_process(self):
        with tempfile.TemporaryDirectory() as td:
            old = os.environ.get("MEDIAHUB_CODEX_EXECUTOR")
            script = Path(td) / "codex"
            script.write_text("#!/bin/sh\nprintf '%s\\n' EXECUTOR_OK\n", encoding="utf-8")
            script.chmod(0o755)
            os.environ["MEDIAHUB_CODEX_EXECUTOR"] = str(script)
            try:
                result = execute(ExecutorRequest("t","c","o",1,"sha","CODEX_LOCAL",Path(td),"x",5))
            finally:
                if old is None:
                    os.environ.pop("MEDIAHUB_CODEX_EXECUTOR", None)
                else:
                    os.environ["MEDIAHUB_CODEX_EXECUTOR"] = old
            self.assertEqual(result.result_status, "PASS")
            self.assertIn("EXECUTOR_OK", result.stdout)


if __name__ == "__main__":
    unittest.main()
