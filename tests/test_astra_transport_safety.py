import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT = ROOT / "astra_github_agent.py"

class AstraTransportSafetyTests(unittest.TestCase):
    def test_controller_reconciliation_contains_no_process_termination(self):
        tree = ast.parse(AGENT.read_text(encoding="utf-8"))
        forbidden = {"kill", "terminate", "pkill"}
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                self.assertNotIn(node.func.attr, forbidden, f"destructive process API: {node.func.attr}")
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.assertNotIn(node.func.id, forbidden, f"destructive process API: {node.func.id}")

    def test_published_recovery_reconciliation_requires_matching_result_identity(self):
        source = AGENT.read_text(encoding="utf-8")
        start = source.index("def reconcile_published_state(")
        end = source.index("def clear_inflight(", start)
        block = source[start:end]
        self.assertIn('git","rev-parse","--verify"', block)
        self.assertIn('git","show"', block)
        self.assertIn('published_result_target_mismatch', block)
        self.assertIn('published_result_execution_head_invalid', block)
        self.assertIn('mark_processed(command_id)', block)

    def test_controller_reconciliation_is_diagnostic(self):
        source = AGENT.read_text(encoding="utf-8")
        start = source.index('if operation == "reconcile_controller_processes":')
        end = source.index('if operation == "dual_local_executor_23wave":', start)
        block = source[start:end]
        self.assertIn('"termination_performed":False', block)
        self.assertNotIn('"/bin/kill"', block)

if __name__ == "__main__":
    unittest.main()
