import unittest
from pathlib import Path

from mediahub_runtime import autonomous_queue


class AstraCanonicalQueuePolicyTests(unittest.TestCase):
    def test_permanent_pool_is_three_claude_lanes(self):
        self.assertEqual(
            autonomous_queue.PERMANENT_EXECUTOR_POOL,
            {
                "mh-dev-01": "claude",
                "mh-dev-02": "claude",
                "Voktors-Mac-mini.local": "claude",
            },
        )

    def test_bounded_worker_count_caps_at_three(self):
        self.assertEqual(autonomous_queue.bounded_worker_count(99), 3)

    def test_source_is_canonical_remote_claude_transport(self):
        source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
        self.assertIn("github_remote_claude_with_controller_worktree", source)
        self.assertIn("permanent_pool_requires_claude", source)
        self.assertNotIn("ASTRA_DISTRIBUTED_LOCAL", source)


if __name__ == "__main__":
    unittest.main()
