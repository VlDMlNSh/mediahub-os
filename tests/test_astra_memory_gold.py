import unittest

from ops.qualification.verify_astra_memory_gold import verify


class AstraMemoryGoldTests(unittest.TestCase):
    def _payload(self):
        return {
            "schema": "mediahub.astra-memory-soak.v1",
            "status": "PASS",
            "duration_seconds": 86400,
            "checks": {k: "PASS" for k in (
                "session_continuation", "project_recall",
                "restart_recovery", "bounded_context")},
            "restart_count": 1,
            "evidence_digest": "sha256:evidence",
            "context_budget": {"max_records": 12, "max_chars": 12000},
            "memory_authority": "advisory_only",
        }

    def test_complete_evidence_passes_independent_gate(self):
        result = verify(self._payload())
        self.assertEqual(result["status"], "PASS")

    def test_authority_or_budget_violation_blocks(self):
        payload = self._payload()
        payload["memory_authority"] = "authoritative"
        payload["context_budget"]["max_chars"] = 12001
        result = verify(payload)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("memory_authority_not_advisory", result["blocked_reasons"])
        self.assertIn("max_chars_out_of_bounds", result["blocked_reasons"])


if __name__ == "__main__":
    unittest.main()
