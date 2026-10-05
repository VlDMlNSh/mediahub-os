import unittest
import ast
from pathlib import Path


class AutonomousMissionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = Path("astra_github_agent.py").read_text(encoding="utf-8")
        cls.tree = ast.parse(cls.source)

    def test_autonomous_gold_mission_is_registered(self):
        self.assertIn('"autonomous_gold_mission"', self.source)

    def test_mission_is_stateful_and_gate_ordered(self):
        for marker in (
            "target_sha_not_ancestor_of_current_main",
            "execution_backend_qualification",
            "pre_soak_evidence",
            "strict_pre_soak_verification",
            "distributed_verification",
            "gold_qualification",
            "ASTRA_AUTONOMOUS_MAX_CYCLES",
            "ASTRA_AUTONOMOUS_RETRY_SECONDS",
        ):
            self.assertIn(marker, self.source)

    def test_main_loop_preserves_workflow_only_command_before_sync(self):
        self.assertIn('if not (os.environ.get("ASTRA_ONESHOT") == "1" and os.environ.get("ASTRA_WORKFLOW_ONLY") == "1"):', self.source)
        self.assertIn("maybe_reexec_updated_agent()", self.source)
        self.assertIn("read_command()", self.source)

    def test_controller_uses_explicit_distributed_producer_binding(self):
        self.assertIn('produce_distributed_verification_evidence.py', self.source)
        self.assertIn('ASTRA_COMMAND_ID', self.source)
        self.assertIn('ASTRA_TARGET_SHA', self.source)
        self.assertIn('canonical-distributed-verification-producer-v1', self.source)

    def test_controller_does_not_promote_pre_soak_executor_to_gold(self):
        self.assertNotIn('astra_gold_executor.py', self.source)


if __name__ == "__main__":
    unittest.main()
