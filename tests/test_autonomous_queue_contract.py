import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "runtime/mediahub_runtime/autonomous_queue.py"


class AutonomousQueueContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = QUEUE.read_text(encoding="utf-8")

    def test_origin_main_fetch_is_serialized_before_parallel_workers(self):
        fetch_marker = 'fetch_main = run(["git", "fetch", "--prune", "origin", "main"], 120)'
        worker_marker = 'ThreadPoolExecutor(max_workers=len(selected))'
        self.assertIn(fetch_marker, self.source)
        self.assertIn(worker_marker, self.source)
        self.assertLess(self.source.index(fetch_marker), self.source.index(worker_marker))
        process = self.source[self.source.index("def process_task"):self.source.index("def main")]
        self.assertNotIn('git", "fetch", "--prune", "origin", "main"', process)

    def test_workers_remain_bound_to_fixed_base_sha(self):
        self.assertIn("expected_base_sha: str", self.source)
        self.assertIn('claim.base_sha != expected_base_sha', self.source)
        self.assertIn("queue_claim_base_sha_mismatch", self.source)
        self.assertIn('remote_main.stdout.strip() != base_sha', self.source)

if __name__ == "__main__":
    unittest.main()
