import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "runtime/mediahub_runtime/autonomous_queue.py"


class AutonomousQueueContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = QUEUE.read_text(encoding="utf-8")

    def test_target_sha_is_validated_before_parallel_workers(self):
        target_marker = 'target_sha = str(os.environ.get("ASTRA_TARGET_SHA", "")).strip()'
        worker_marker = 'ThreadPoolExecutor(max_workers=len(selected))'
        self.assertIn(target_marker, self.source)
        self.assertIn(worker_marker, self.source)
        self.assertLess(self.source.index(target_marker), self.source.index(worker_marker))

    def test_workers_remain_bound_to_fixed_target_sha(self):
        self.assertIn("expected_base_sha: str", self.source)
        self.assertIn('claim.base_sha != expected_base_sha', self.source)
        self.assertIn("queue_claim_base_sha_mismatch", self.source)
        self.assertIn("queue_target_sha_not_current_head", self.source)
        self.assertNotIn('remote_main.stdout.strip() != base_sha', self.source)

    def test_parallel_claim_cap_matches_g5(self):
        self.assertIn("return max(1, min(int(requested), 3))", self.source)
        self.assertNotIn("return max(1, min(int(requested), 2))", self.source)

    def test_claim_lease_default_matches_governance(self):
        self.assertIn("ASTRA_CLAIM_LEASE_SECONDS", self.source)
        self.assertIn('"600"', self.source)

    def test_builder_uses_runner_supported_codex_flags(self):
        self.assertIn('"--sandbox", "workspace-write"', self.source)
        self.assertNotIn('"--ask-for-approval", "never"', self.source)
        self.assertNotIn('"--full-auto"', self.source)

if __name__ == "__main__":
    unittest.main()
