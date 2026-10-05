import json
import hashlib
import hmac
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ops.qualification import produce_distributed_verification_evidence as producer


class DistributedVerificationProducerTests(unittest.TestCase):
    def attestation(self, node_id, command_id="CMD-1", target_sha="a"*40, status="PASS", completed_at=1000, key=None):
        key = key or {
            "mh-dev-01": b"test-secret",
            "mh-dev-02": b"test-secret-2",
            "Voktors-Mac-mini.local": b"test-secret-3",
        }[node_id]
        payload = {
            "schema": "mediahub.astra.distributed-node-attestation.v1",
            "command_id": command_id,
            "node_id": node_id,
            "target_sha": target_sha,
            "producer_identity": f"node-agent:{node_id}",
            "auth_key_id": f"{node_id}-distributed-attestation-v1",
            "phase": "distributed_verification",
            "status": status,
            "returncode": 0,
            "completed_at": completed_at,
            "current_head": target_sha,
            "observations": {"identity": True, "transport": True},
            "auth_schema_version": "mediahub.astra.distributed.auth.v1",
        }
        payload["signature"] = hmac.new(
            key,
            json.dumps({k: v for k, v in payload.items() if k != "signature"}, sort_keys=True, separators=(",", ":")).encode(),
            hashlib.sha256,
        ).hexdigest()
        return payload

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
                root, command_id="CMD-1", node_id="mh-dev-01", target_sha="a"*40, current_head="a"*40, now=1100, max_age_seconds=120, hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "test-secret-2", "Voktors-Mac-mini.local": "test-secret-3"}
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
                root, command_id="CMD-1", node_id="mh-dev-01", target_sha="a"*40, current_head="a"*40, now=1100, max_age_seconds=120, hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "test-secret-2", "Voktors-Mac-mini.local": "test-secret-3"}
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertTrue(any(reason.endswith("_stale") for reason in result["blocked_reasons"]))

    def test_all_fresh_matching_attestations_pass(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            for node in producer.REQUIRED_NODES:
                self.write_attestation(root, self.attestation(node, completed_at=1090))
            result = producer.aggregate(
                root, command_id="CMD-1", node_id="mh-dev-01", target_sha="a"*40, current_head="a"*40, now=1100, max_age_seconds=120, hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "test-secret-2", "Voktors-Mac-mini.local": "test-secret-3"}
            )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["checked_nodes"], producer.REQUIRED_NODES)

    def test_unsigned_attestation_is_rejected(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            payload = self.attestation("mh-dev-01")
            payload.pop("signature")
            self.write_attestation(root, payload)
            result = producer.aggregate(
                root, command_id="CMD-1", node_id="mh-dev-01", target_sha="a"*40, current_head="a"*40, now=1000, max_age_seconds=120, hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "test-secret-2", "Voktors-Mac-mini.local": "test-secret-3"}
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("mh-dev-01_signature_missing", result["blocked_reasons"])

    def test_tampered_attestation_signature_is_rejected(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            payload = self.attestation("mh-dev-01")
            payload["observations"]["transport"] = False
            self.write_attestation(root, payload)
            result = producer.aggregate(
                root, command_id="CMD-1", node_id="mh-dev-01", target_sha="a"*40, current_head="a"*40, now=1000, max_age_seconds=120, hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "test-secret-2", "Voktors-Mac-mini.local": "test-secret-3"}
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("mh-dev-01_signature_invalid", result["blocked_reasons"])

    def test_aggregate_rejects_current_head_mismatch(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            result = producer.aggregate(
                root,
                command_id="CMD-1",
                node_id="mh-dev-01",
                target_sha="a"*40,
                current_head="b"*40,
                now=1000,
                max_age_seconds=120,
                hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "test-secret-2", "Voktors-Mac-mini.local": "test-secret-3"},
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("target_sha_mismatch", result["blocked_reasons"])

    def test_wrong_producer_identity_is_rejected(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            payload = self.attestation("mh-dev-01")
            payload["producer_identity"] = "node-agent:mh-dev-02"
            self.write_attestation(root, payload)
            result = producer.aggregate(
                root,
                command_id="CMD-1",
                node_id="mh-dev-01",
                target_sha="a"*40,
                current_head="a"*40,
                now=1000,
                max_age_seconds=120,
                hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "test-secret-2", "Voktors-Mac-mini.local": "test-secret-3"},
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("mh-dev-01_producer_identity_mismatch", result["blocked_reasons"])

    def test_attestation_current_head_mismatch_is_rejected(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            payload = self.attestation("mh-dev-01")
            payload["current_head"] = "b"*40
            payload["signature"] = hmac.new(
                b"test-secret",
                json.dumps({k: v for k, v in payload.items() if k != "signature"},
                           sort_keys=True, separators=(",", ":")).encode(),
                hashlib.sha256,
            ).hexdigest()
            self.write_attestation(root, payload)
            result = producer.aggregate(
                root,
                command_id="CMD-1",
                node_id="mh-dev-01",
                target_sha="a"*40,
                current_head="a"*40,
                now=1000,
                max_age_seconds=120,
                hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "test-secret-2", "Voktors-Mac-mini.local": "test-secret-3"},
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("mh-dev-01_current_head_mismatch", result["blocked_reasons"])

    def test_wrong_node_key_cannot_validate_attestation(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            payload = self.attestation("mh-dev-01", key=b"other-secret")
            self.write_attestation(root, payload)
            result = producer.aggregate(
                root,
                command_id="CMD-1",
                node_id="mh-dev-01",
                target_sha="a"*40,
                current_head="a"*40,
                now=1000,
                max_age_seconds=120,
                hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "x", "Voktors-Mac-mini.local": "y"},
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("mh-dev-01_signature_invalid", result["blocked_reasons"])

    def test_auth_key_id_mismatch_is_rejected(self):
        with TemporaryDirectory() as td:
            root = Path(td)
            payload = self.attestation("mh-dev-01")
            payload["auth_key_id"] = "mh-dev-02-distributed-attestation-v1"
            payload["signature"] = hmac.new(
                b"test-secret",
                json.dumps({k: v for k, v in payload.items() if k != "signature"},
                           sort_keys=True, separators=(",", ":")).encode(),
                hashlib.sha256,
            ).hexdigest()
            self.write_attestation(root, payload)
            result = producer.aggregate(
                root,
                command_id="CMD-1",
                node_id="mh-dev-01",
                target_sha="a"*40,
                current_head="a"*40,
                now=1000,
                max_age_seconds=120,
                hmac_keys={"mh-dev-01": "test-secret", "mh-dev-02": "x", "Voktors-Mac-mini.local": "y"},
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("mh-dev-01_auth_key_id_mismatch", result["blocked_reasons"])



if __name__ == "__main__":
    unittest.main()
