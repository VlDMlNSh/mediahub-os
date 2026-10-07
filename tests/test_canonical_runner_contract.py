import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_LABEL = "mediahub-control"


class CanonicalRunnerRoutingTests(unittest.TestCase):
    def test_every_mh_dev_01_self_hosted_workflow_uses_unique_label(self):
        workflows = sorted((ROOT / ".github/workflows").glob("*.y*ml"))
        checked = []
        for workflow in workflows:
            text = workflow.read_text(encoding="utf-8")
            if 'test "$(hostname)" = "mh-dev-01"' not in text and "node=mh-dev-01" not in text:
                continue
            if "runs-on:" not in text:
                continue
            if "[self-hosted" not in text:
                continue
            checked.append(workflow.name)
            self.assertIn(CANONICAL_LABEL, text, workflow.name)
            self.assertNotIn("runs-on: [self-hosted, linux, x64]", text, workflow.name)
            self.assertNotIn("runs-on: [self-hosted, mediahub-runner]", text, workflow.name)
            self.assertNotIn("runs-on: self-hosted", text, workflow.name)
        self.assertGreaterEqual(len(checked), 1)

    def test_canonical_contract_exists(self):
        contract = ROOT / "control/qualification/canonical-runner-contract.json"
        self.assertTrue(contract.is_file())
        self.assertIn(CANONICAL_LABEL, contract.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
