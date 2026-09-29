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

    def test_main_loop_reexecs_updated_agent_before_reading_command(self):
        main = next(n for n in self.tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
        calls = [n.func.id for n in ast.walk(main) if isinstance(n, ast.Call)
                 and isinstance(n.func, ast.Name)]
        self.assertLess(calls.index("sync"), calls.index("maybe_reexec_updated_agent"))
        self.assertLess(calls.index("maybe_reexec_updated_agent"), calls.index("read_command"))


if __name__ == "__main__":
    unittest.main()
