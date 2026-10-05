import hashlib
import hmac
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from ops.qualification import produce_distributed_node_attestation as producer


class DistributedNodeAttestationTests(unittest.TestCase):
    def test_validate_context_accepts_matching_identity_and_head(self):
        result = producer.validate_context(
            node_id="mh-dev-01",
            hostname="mh-dev-01",
            current_user="mediahub-runner",
            target_sha="a"*40,
            current_head="a"*40,
            command_id="CMD-1",
            hmac_key="test-secret",
        )
        self.assertEqual(result, [])

    def test_wrong_node_identity_blocks(self):
        result = producer.validate_context(
            node_id="mh-dev-02",
            hostname="mh-dev-01",
            current_user="mediahub-runner",
            target_sha="a"*40,
            current_head="a"*40,
            command_id="CMD-1",
            hmac_key="test-secret",
        )
        self.assertIn("hostname_node_binding_mismatch", result)

    def test_target_head_mismatch_blocks(self):
        result = producer.validate_context(
            node_id="mh-dev-01",
            hostname="mh-dev-01",
            current_user="mediahub-runner",
            target_sha="a"*40,
            current_head="b"*40,
            command_id="CMD-1",
            hmac_key="test-secret",
        )
        self.assertIn("target_sha_mismatch", result)

    def test_missing_hmac_key_blocks(self):
        result = producer.validate_context(
            node_id="mh-dev-01",
            hostname="mh-dev-01",
            target_sha="a"*40,
            current_head="a"*40,
            command_id="CMD-1",
            hmac_key="",
        )
        self.assertIn("missing_hmac_key", result)

    def test_collect_attestation_signs_fresh_pass_payload(self):
        pass_result = {
            "returncode": 0,
            "status": "PASS",
            "duration_seconds": 0.1,
            "stdout": "",
            "stderr": "",
        }
        with patch.object(producer, "run_check", return_value=pass_result):
            result = producer.collect_attestation(
                root=Path("."),
                node_id="mh-dev-01",
                hostname="mh-dev-01",
                command_id="CMD-1",
                target_sha="a"*40,
                hmac_key="test-secret",
                current_head="a"*40,
            )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["producer_identity"], "node-agent:mh-dev-01")
        self.assertTrue(result["signature"])
        body = json.dumps(
            {k: v for k, v in result.items() if k != "signature"},
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode()
        expected = hmac.new(b"test-secret", body, hashlib.sha256).hexdigest()
        self.assertEqual(result["signature"], expected)

    def test_failed_check_cannot_emit_pass(self):
        fail_result = {
            "returncode": 1,
            "status": "BLOCKED",
            "duration_seconds": 0.1,
            "stdout": "",
            "stderr": "failed",
        }
        with patch.object(producer, "run_check", return_value=fail_result):
            result = producer.collect_attestation(
                root=Path("."),
                node_id="mh-dev-01",
                hostname="mh-dev-01",
                command_id="CMD-1",
                target_sha="a"*40,
                hmac_key="test-secret",
                current_head="a"*40,
            )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertEqual(result["returncode"], 2)

    def test_wrong_user_identity_blocks(self):
        result = producer.validate_context(
            node_id="mh-dev-01",
            hostname="mh-dev-01",
            current_user="mediahub",
            target_sha="a"*40,
            current_head="a"*40,
            command_id="CMD-1",
            hmac_key="test-secret",
        )
        self.assertIn("user_identity_mismatch", result)



if __name__ == "__main__":
    unittest.main()
