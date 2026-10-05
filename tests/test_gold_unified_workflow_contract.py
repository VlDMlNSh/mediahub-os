import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/astra-gold-unified-qualification.yml"


class GoldUnifiedWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")
        cls.document = yaml.safe_load(cls.text)

    def test_human_confirmation_remains_required(self):
        on_block = self.document.get("on", self.document.get(True))
        self.assertTrue(on_block["workflow_dispatch"]["inputs"]["confirm_launch"]["required"])
        self.assertFalse(on_block["workflow_dispatch"]["inputs"]["confirm_launch"]["default"])

    def test_gold_workflow_uses_signed_command_boundary(self):
        self.assertIn("ops/control/sign_command.py", self.text)
        self.assertIn('"workflow_only":True', self.text)
        self.assertIn('ASTRA_WORKFLOW_ONLY: "1"', self.text)
        self.assertNotIn("astra_github_agent.execute(", self.text)

    def test_gold_workflow_requires_distributed_verification(self):
        self.assertIn("uses: ./.github/workflows/astra-distributed-verification.yml", self.text)
        self.assertIn("needs:", self.text)
        self.assertIn("needs.distributed-verification.outputs.status == 'PASS'", self.text)
        self.assertIn("ASTRA_DISTRIBUTED_EVIDENCE_DIR", self.text)

    def test_gold_workflow_has_fresh_queue_result_gate(self):
        self.assertIn('result.get("phase") == "autonomous_queue"', self.text)
        self.assertIn('result.get("status") == "PASS"', self.text)
        self.assertIn('queue.get("status") == "PASS"', self.text)
        self.assertIn('item.get("status") == "VERIFIED"', self.text)

if __name__ == "__main__":
    unittest.main()
