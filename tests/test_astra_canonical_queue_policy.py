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

    def test_source_defaults_to_remote_distributed_transport(self):
        source = Path(autonomous_queue.__file__).read_text(encoding="utf-8")
        self.assertIn('os.environ.get("ASTRA_DISTRIBUTED_LOCAL", "1")', source)
        self.assertIn("permanent_pool_requires_claude", source)


if __name__ == "__main__":
    unittest.main()
