import os
import unittest
from pathlib import Path

from runtime.mediahub_runtime.harness import HarnessError, MediaHubHarness
from runtime.mediahub_runtime.autonomous_queue import _validate_task_id


class SecurityBoundaryTests(unittest.TestCase):
    def test_task_id_rejects_path_traversal(self):
        for value in ("../escape", "a/../../b", "..", "a\\b"):
            with self.assertRaises(RuntimeError):
                _validate_task_id(value)

    def test_task_id_accepts_bounded_identifier(self):
        self.assertEqual(_validate_task_id("MH25-task_01"), "MH25-task_01")

    def test_harness_rejects_git_configuration_escape(self):
        harness = MediaHubHarness()
        with self.assertRaises(HarnessError) as ctx:
            harness._validate(["git", "-c", "core.pager=!cmd", "status"], Path.cwd())
        self.assertEqual(ctx.exception.code, "git_argument_not_allowed")


if __name__ == "__main__":
    unittest.main()
