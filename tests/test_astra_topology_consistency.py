import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AstraTopologyConsistencyTests(unittest.TestCase):
    def test_canonical_concurrency_is_three(self):
        governance = (ROOT / "architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml").read_text()
        qualification = (ROOT / "architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml").read_text()
        reference = (ROOT / "architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md").read_text()
        unified = (ROOT / "architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md").read_text()
        self.assertIn("max_parallel_autonomous_claims: 3", governance)
        self.assertIn("max_parallel_autonomous_claims: 3", qualification)
        self.assertIn("Maximum autonomous claims: 3", reference)
        self.assertIn("maximum three concurrent autonomous claims", unified)

    def test_permanent_pool_and_queue_contracts_are_three_claude_lanes(self):
        queue = (ROOT / "runtime/mediahub_runtime/autonomous_queue.py").read_text()
        self.assertIn('"mh-dev-01": "claude"', queue)
        self.assertIn('"mh-dev-02": "claude"', queue)
        self.assertIn('"Voktors-Mac-mini.local": "claude"', queue)
        self.assertIn("bounded_worker_count(max_workers)", queue)

        for name in ("MH25-QUEUE-002.json", "MH25-QUEUE-003.json", "MH25-QUEUE-004.json"):
            task = json.loads((ROOT / "ops/agent-fabric/tasks" / name).read_text())
            self.assertEqual(task["executor"], "claude")
            self.assertEqual(task["verifier"], "claude")
            self.assertTrue(task["independent_verifier_process"])

    def test_no_stale_codex_lane_in_permanent_contracts(self):
        for name in ("MH25-QUEUE-002.json", "MH25-QUEUE-003.json", "MH25-QUEUE-004.json"):
            text = (ROOT / "ops/agent-fabric/tasks" / name).read_text()
            self.assertNotIn("Codex as the independent A3 Verifier", text)
            self.assertNotIn("CODEX-EXECUTOR", text)

    def test_capability_matrix_preserves_single_authority(self):
        text = (ROOT / "docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md").read_text()
        self.assertIn("capability library", text)
        self.assertIn("never new authority", text)
        self.assertIn("RECONCILIATION_REQUIRED", text)


if __name__ == "__main__":
    unittest.main()
