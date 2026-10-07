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

    def test_gold_workflow_binds_to_canonical_g4_115_workflow(self):
        self.assertIn("astra-g4-115-qualification.yml", self.text)
        self.assertNotIn("mh25-dual-local-executor-23wave.yml", self.text)
        self.assertIn("g4-115-$GITHUB_SHA", self.text)

    def test_gold_workflow_requires_distributed_verification(self):
        self.assertIn("uses: ./.github/workflows/astra-distributed-verification.yml", self.text)
        self.assertIn("needs:", self.text)
        self.assertIn("needs.distributed-verification.outputs.status == 'PASS'", self.text)
        self.assertIn("ASTRA_DISTRIBUTED_EVIDENCE_DIR", self.text)

    def test_gold_execution_is_exact_sha_bound_and_clean(self):
        self.assertIn("ref: ${{ github.sha }}", self.text)
        self.assertIn('test "$(git rev-parse HEAD)" = "$GITHUB_SHA"', self.text)
        self.assertIn('test -z "$(git status --short)"', self.text)

    def test_gold_workflow_has_fresh_queue_result_gate(self):
        self.assertIn('result.get("phase") == "autonomous_queue"', self.text)
        self.assertIn('result.get("status") == "PASS"', self.text)
        self.assertIn('queue.get("status") == "PASS"', self.text)
        self.assertIn('item.get("status") == "VERIFIED"', self.text)

    def test_gold_workflow_uses_read_only_control_and_publication_boundary(self):
        self.assertIn("contents: read", self.text)
        self.assertNotIn("contents: write", self.text)
        self.assertIn("ASTRA_DEFER_RESULT_PUBLICATION", self.text)
        self.assertNotIn("astra-node-result-publication.yml", self.text)
        self.assertNotIn("MIMO_API_KEY", self.text)

    def test_result_publication_uses_separate_workflow_run_boundary(self):
        publication = ROOT / ".github/workflows/astra-node-result-publication.yml"
        text = publication.read_text(encoding="utf-8")
        self.assertIn("workflow_run:", text)
        self.assertIn("contents: write", text)
        self.assertIn("actions: read", text)
        self.assertNotIn("MIMO_API_KEY", text)

    def test_gold_uses_downloaded_distributed_evidence_root(self):
        self.assertIn('path: .astra-state', self.text)

if __name__ == "__main__":
    unittest.main()
