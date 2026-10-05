import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/astra-distributed-verification.yml"
SUPERVISOR = ROOT / ".github/workflows/astra-autonomous-supervisor.yml"


class DistributedWorkflowContractTests(unittest.TestCase):
    def test_single_reusable_workflow_targets_all_three_nodes(self):
        document = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        self.assertTrue(document.get("jobs"))
        jobs = document["jobs"]
        self.assertIn("node-mh-dev-01", jobs)
        self.assertIn("node-mh-dev-02", jobs)
        self.assertIn("node-voktors-mac", jobs)
        self.assertIn("aggregate", jobs)
        self.assertIn("mh-dev-01-canonical", str(jobs["node-mh-dev-01"]["runs-on"]))
        self.assertIn("mh-dev-02-distributed", str(jobs["node-mh-dev-02"]["runs-on"]))
        self.assertIn("voktors-mac-mini-distributed", str(jobs["node-voktors-mac"]["runs-on"]))

    def test_node_jobs_require_expected_runtime_identity(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('test "$(hostname)" = "mh-dev-01"', text)
        self.assertIn('test "$(id -un)" = "mediahub-runner"', text)
        self.assertIn('test "$(hostname)" = "mh-dev-02"', text)
        self.assertIn('test "$(id -un)" = "mediahub"', text)
        self.assertIn('test "$(id -un)" = "voktor"', text)

    def test_workflow_binds_command_sha_and_hmac(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        for marker in ("workflow_call", "ASTRA_COMMAND_ID", "ASTRA_TARGET_SHA",
                       "ASTRA_COMMAND_HMAC_KEY", "produce_distributed_node_attestation.py"):
            self.assertIn(marker, text)

    def test_distributed_runner_contract_declares_all_three_nodes(self):
        contract = ROOT / "control/qualification/distributed-runner-contract.json"
        self.assertTrue(contract.is_file())
        text = contract.read_text(encoding="utf-8")
        for label in (
            "mh-dev-01-canonical",
            "mh-dev-02-distributed",
            "voktors-mac-mini-distributed",
        ):
            self.assertIn(label, text)
        for node in ("mh-dev-01", "mh-dev-02", "Voktors-Mac-mini.local"):
            self.assertIn(node, text)

    def test_supervisor_uses_single_distributed_gate(self):
        text = SUPERVISOR.read_text(encoding="utf-8")
        self.assertIn("distributed-verification:", text)
        self.assertIn("astra-distributed-verification.yml", text)
        self.assertIn("needs: distributed-verification", text)
        self.assertIn("download-artifact@v4", text)
        self.assertNotIn("astra-distributed-node-attestations.yml", text)
        self.assertNotIn("distributed_candidates", text)


if __name__ == "__main__":
    unittest.main()
