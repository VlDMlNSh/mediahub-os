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

    def test_published_command_remains_blocked_after_last_command_changes(self):
        self.mod.mark_processed("command-A")
        self.mod.mark_published("command-B")
        self.assertTrue(self.mod.is_processed("command-A"))
        self.assertTrue(self.mod.is_processed("command-B") is False)

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
