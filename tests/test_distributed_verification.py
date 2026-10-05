import json
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ops.qualification import produce_distributed_verification_evidence as producer


class DistributedVerificationProducerTests(unittest.TestCase):
    def attestation(self, node_id, command_id="CMD-1", target_sha="a"*40, status="PASS", completed_at=1000):
        return {
            "schema": "mediahub.astra.distributed-node-attestation.v1",
            "command_id": command_id,
            "node_id": node_id,
            "target_sha": target_sha,
            "producer_identity": f"node-agent:{node_id}",
            "phase": "distributed_verification",
            "status": status,
            "returncode": 0,
            "completed_at": completed_at,
            "observations": {"identity": True, "transport": True},
        }

    def write_attestation(self, root: Path, payload: dict):
        path = root / f"{payload['node_id']}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")

    def test_missing_authority_context_blocks(self):
        result = producer.validate_context(command_id="", node_id="mh-dev-01", target_sha="a"*40, current_head="a"*40)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("missing_command_id", result.blocked_reasons)

    def test_target_sha_mismatch_blocks(self):
        result = producer.validate_context(command_id="CMD-1", node_id="mh-dev-01", target_sha="a"*40, current_head="b"*40)
        self.assertEqual(result.status, "BLOCKED")
        self.assertIn("target_sha_mismatch", result.blocked_reasons)

    def test_missing_fresh_nodes_blocks(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            self.write_attestation(root, self.attestation("mh-dev-01"))
            result = producer.aggregate(
                root, command_id="CMD-1", node_id="mh-dev-01", target_sha="a"*40, now=1100, max_age_seconds=120
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("mh-dev-02_missing", result["blocked_reasons"])
        self.assertIn("Voktors-Mac-mini.local_missing", result["blocked_reasons"])

    def test_stale_historical_attestation_is_rejected(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            for node in producer.REQUIRED_NODES:
                self.write_attestation(root, self.attestation(node, completed_at=500))
            result = producer.aggregate(
                root, command_id="CMD-1", node_id="mh-dev-01", target_sha="a"*40, now=1100, max_age_seconds=120
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any(reason.endswith("_stale") for reason in result["blocked_reasons"]))

    def test_all_fresh_matching_attestations_pass(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            for node in producer.REQUIRED_NODES:
                self.write_attestation(root, self.attestation(node, completed_at=1090))
            result = producer.aggregate(
                root, command_id="CMD-1", node_id="mh-dev-01", target_sha="a"*40, now=1100, max_age_seconds=120
            )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["checked_nodes"], producer.REQUIRED_NODES)


if __name__ == "__main__":
    unittest.main()
