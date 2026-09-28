import unittest

from ops.qualification.verify_execution_backends import verify


def evidence(status="PASS"):
    return {
        "schema": "mediahub.execution-backends.v1",
        "status": status,
        "backends": {
            backend_id: {
                "node_id": "mh-dev-01",
                "verification_state": "VERIFIED",
                "checks": {
                    "node_identity": "PASS",
                    "binary_identity": "PASS",
                    "bounded_execution": "PASS",
                },
                "output_sha256": "sha256:abc",
                "secret_values": "SUPPRESSED",
            }
            for backend_id in ("codex", "cursor")
        },
        "evidence_digest": "sha256:bundle",
        "node_id": "mh-dev-01",
        "repo_revision": "abc123",
    }


class ExecutionBackendEvidenceTests(unittest.TestCase):
    def test_complete_evidence_passes(self):
        result = verify(evidence(), "abc123")
        self.assertEqual(result["status"], "PASS")

    def test_revision_mismatch_is_blocked(self):
        result = verify(evidence(), "wrong")
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("repo_revision_mismatch", result["blocked_reasons"])

    def test_missing_backend_is_blocked(self):
        payload = evidence()
        del payload["backends"]["cursor"]
        result = verify(payload)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("cursor_missing", result["blocked_reasons"])

    def test_unverified_backend_is_blocked(self):
        payload = evidence()
        payload["backends"]["codex"]["verification_state"] = "UNVERIFIED"
        result = verify(payload)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("codex_not_VERIFIED", result["blocked_reasons"])

    def test_non_pass_evidence_cannot_be_promoted(self):
        result = verify(evidence("BLOCKED"))
        self.assertEqual(result["status"], "BLOCKED")

    def test_secret_disclosure_is_blocked(self):
        payload = evidence()
        payload["backends"]["cursor"]["secret_values"] = "LEAKED"
        result = verify(payload)
        self.assertEqual(result["status"], "BLOCKED")


if __name__ == "__main__":
    unittest.main()
