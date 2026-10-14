import json
import re
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]


class AstraTopologyConsistencyTests(unittest.TestCase):
    def test_concurrency_authority_and_mirrors_are_consistent(self):
        governance = yaml.safe_load((ROOT / "architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml").read_text())
        qualification = yaml.safe_load((ROOT / "architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml").read_text())
        unified_model = yaml.safe_load((ROOT / "architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml").read_text())
        reference = (ROOT / "architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md").read_text()
        unified = (ROOT / "architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md").read_text()
        component = (ROOT / "architecture/ASTRA-GOLD-COMPLETE-COMPONENT-SCHEME.md").read_text()

        schema_path = "architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml"
        self.assertEqual(governance["authority_source"], schema_path)
        self.assertEqual(governance["gate_registry"]["source_of_truth"], schema_path)
        canonical_limit = qualification["gates"]["G5_CONCURRENCY"]["max_parallel_autonomous_claims"]
        self.assertEqual(governance["runtime_thresholds"]["max_parallel_autonomous_claims"], canonical_limit)
        self.assertEqual(unified_model["qualification"]["concurrency"]["max_parallel"], canonical_limit)

        self.assertIn("runtime_thresholds.max_parallel_autonomous_claims", reference)
        self.assertIn("runtime_thresholds.max_parallel_autonomous_claims", unified)
        self.assertIn("runtime_thresholds.max_parallel_autonomous_claims", component)
        self.assertNotIn("Maximum autonomous claims:", reference)
        self.assertNotRegex(unified, r"maximum (?:three|[0-9]+) concurrent autonomous claims")

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

    def test_canonical_schemas_do_not_present_codex_as_production_executor(self):
        queue = (ROOT / "runtime/mediahub_runtime/autonomous_queue.py").read_text()
        unified = (ROOT / "architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md").read_text()
        task = (ROOT / "ops/agent-fabric/tasks/MH25-QUEUE-002.json").read_text()
        self.assertNotIn("codex", queue.lower())
        self.assertNotIn("Codex + FCC", unified)
        self.assertNotIn("Codex + OmniRoute", unified)
        self.assertNotIn("Codex CLI", unified)
        self.assertNotIn("Claude, Codex", task)

    def test_capability_matrix_preserves_single_authority(self):
        text = (ROOT / "docs/operations/ASTRA-EXECUTOR-CAPABILITY-MATRIX.md").read_text()
        self.assertIn("capability library", text)
        self.assertIn("never new authority", text)
        self.assertIn("RECONCILIATION_REQUIRED", text)


if __name__ == "__main__":
    unittest.main()
