import unittest
from pathlib import Path
import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/astra-distributed-node-attestations.yml"
SUPERVISOR = ROOT / ".github/workflows/astra-autonomous-supervisor.yml"


class DistributedWorkflowContractTests(unittest.TestCase):
    def test_reusable_workflow_exists_and_targets_exact_nodes(self):
        document = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        self.assertTrue(document.get("jobs"))
        jobs = document["jobs"]
        self.assertIn("mh-dev-02", jobs)
        self.assertIn("mac", jobs)
        linux = str(jobs["mh-dev-02"]["runs-on"])
        mac = str(jobs["mac"]["runs-on"])
        self.assertIn("mh-dev-02-canonical", linux)
        self.assertIn("Voktors-Mac-mini-canonical", mac)

    def test_reusable_workflow_is_bound_to_command_and_target_sha(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("workflow_call", text)
        self.assertIn("command_id", text)
        self.assertIn("target_sha", text)
        self.assertIn("ASTRA_COMMAND_HMAC_KEY", text)
        self.assertIn("produce_distributed_node_attestation.py", text)

    def test_supervisor_waits_for_fresh_distributed_attestations(self):
        text = SUPERVISOR.read_text(encoding="utf-8")
        self.assertIn("astra-distributed-node-attestations.yml", text)
        self.assertIn("distributed-attestation", text)
        self.assertIn("download-artifact@v4", text)
        self.assertIn("distributed-verification", text)
        self.assertNotIn("distributed_candidates", text)


if __name__ == "__main__":
    unittest.main()
