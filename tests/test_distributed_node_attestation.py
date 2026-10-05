import hashlib
import hmac
import json
import unittest
from pathlib import Path
from unittest.mock import patch

from ops.qualification import produce_distributed_node_attestation as producer


class DistributedNodeAttestationTests(unittest.TestCase):
    def test_context_requires_expected_identity_and_target_head(self):
        with patch.object(producer, "current_head", return_value="a"*40):
            result = producer.build_attestation(
                command_id="CMD-1",
                node_id="mh-dev-01",
                target_sha="a"*40,
                current_node="mh-dev-01",
                current_user="mediahub-runner",
                current_head="a"*40,
                observed_at=1000,
                checks={"identity": True, "head": True},
                hmac_key="test-secret",
            )
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["producer_identity"], "node-agent:mh-dev-01")
        self.assertIn("signature", result)

    def test_wrong_node_identity_blocks(self):
        result = producer.build_attestation(
            command_id="CMD-1",
            node_id="mh-dev-01",
            target_sha="a"*40,
            current_node="mh-dev-02",
            current_user="mediahub",
            current_head="a"*40,
            observed_at=1000,
            checks={"identity": True, "head": True},
            hmac_key="test-secret",
        )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("node_identity_mismatch", result["blocked_reasons"])

    def test_target_head_mismatch_blocks(self):
        result = producer.build_attestation(
            command_id="CMD-1",
            node_id="mh-dev-01",
            target_sha="a"*40,
            current_node="mh-dev-01",
            current_user="mediahub-runner",
            current_head="b"*40,
            observed_at=1000,
            checks={"identity": True, "head": True},
            hmac_key="test-secret",
        )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("target_sha_mismatch", result["blocked_reasons"])

    def test_missing_hmac_key_blocks(self):
        result = producer.build_attestation(
            command_id="CMD-1",
            node_id="mh-dev-01",
            target_sha="a"*40,
            current_node="mh-dev-01",
            current_user="mediahub-runner",
            current_head="a"*40,
            observed_at=1000,
            checks={"identity": True, "head": True},
            hmac_key="",
        )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("hmac_key_missing", result["blocked_reasons"])

    def test_failed_check_cannot_emit_pass(self):
        result = producer.build_attestation(
            command_id="CMD-1",
            node_id="mh-dev-01",
            target_sha="a"*40,
            current_node="mh-dev-01",
            current_user="mediahub-runner",
            current_head="a"*40,
            observed_at=1000,
            checks={"identity": True, "head": False},
            hmac_key="test-secret",
        )
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("check_failed:head", result["blocked_reasons"])


if __name__ == "__main__":
    unittest.main()
