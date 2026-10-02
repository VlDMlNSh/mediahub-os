import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]


class TestAstraGithubAgentReplayFence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("astra_github_agent", ROOT / "astra_github_agent.py")
        cls.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.mod)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.mod.STATE = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_remote_result_does_not_become_local_last_command_state(self):
        original_run = self.mod.run
        self.addCleanup(lambda: setattr(self.mod, "run", original_run))
        self.assertEqual(self.mod.published_command_id(), "")
        self.mod.mark_processed("remote-only-command")
        self.assertEqual(self.mod.published_command_id(), "")

    def test_published_command_remains_blocked_after_last_command_changes(self):
        self.mod.mark_processed("command-A")
        self.mod.mark_published("command-B")
        self.assertTrue(self.mod.is_processed("command-A"))
        self.assertTrue(self.mod.is_processed("command-B") is False)

    def test_remote_publication_is_reconciled_without_reexecution(self):
        import json
        original_run = self.mod.run
        self.addCleanup(lambda: setattr(self.mod, "run", original_run))
        result = {"command_id": "command-A", "target_sha": "abc123", "execution_head": "0123456789abcdef0123456789abcdef01234567", "returncode": 0}
        class Fake:
            def __init__(self, code, stdout=""):
                self.returncode = code
                self.stdout = stdout
                self.stderr = ""
        def fake_run(argv, timeout=30):
            if argv[:3] == ["git", "rev-parse", "--verify"]:
                return Fake(0, "remote-tip\\n")
            if argv[:2] == ["git", "show"]:
                return Fake(0, json.dumps(result))
            raise AssertionError(argv)
        self.mod.run = fake_run
        command = {"command_id": "command-A", "target_sha": "abc123"}
        self.assertTrue(self.mod.reconcile_published_state("command-A", command))
        self.assertTrue(self.mod.is_processed("command-A"))
        self.assertEqual(self.mod.published_command_id(), "command-A")
        self.assertFalse((self.mod.STATE / "inflight_command_id").exists())

    def test_remote_publication_identity_mismatch_fails_closed(self):
        import json
        original_run = self.mod.run
        self.addCleanup(lambda: setattr(self.mod, "run", original_run))
        class Fake:
            def __init__(self, code, stdout=""):
                self.returncode = code
                self.stdout = stdout
                self.stderr = ""
        def fake_run(argv, timeout=30):
            if argv[:3] == ["git", "rev-parse", "--verify"]:
                return Fake(0, "remote-tip\\n")
            if argv[:2] == ["git", "show"]:
                return Fake(0, json.dumps({"command_id":"command-A","target_sha":"wrong","execution_head":"wrong"}))
            raise AssertionError(argv)
        self.mod.run = fake_run
        with self.assertRaisesRegex(RuntimeError, "published_result_target_mismatch"):
            self.mod.reconcile_published_state("command-A", {"command_id":"command-A","target_sha":"abc123"})
        self.assertFalse(self.mod.is_processed("command-A"))

    def test_marker_is_hashed_and_validated(self):
        self.mod.mark_processed("command-A")
        marker = self.mod.processed_marker("command-A")
        self.assertTrue(marker.is_file())
        self.assertTrue(self.mod.is_processed("command-A"))
        marker.write_text('{"command_id":"other","status":"PUBLISHED"}\n', encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "processed_command_marker_invalid"):
            self.mod.is_processed("command-A")


if __name__ == "__main__":
    unittest.main()
