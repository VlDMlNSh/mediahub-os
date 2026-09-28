import unittest

from ops.qualification.verify_astra_memory_contract import verify


class AstraMemoryContractTests(unittest.TestCase):
    def _payload(self):
        return {
            "schema": "mediahub.astra-memory-contract.v1",
            "status": "PASS",
            "checks": {name: "PASS" for name in (
                "security_gate", "scope_isolation", "supersession",
                "bounded_context", "advisory_only", "provenance",
                "raw_history_retained",
            )},
            "memory_authority": "advisory_only",
            "context_budget": {"max_records": 12, "max_chars": 12000},
            "evidence_digest": "sha256:test",
        }

    def test_complete_contract_passes(self):
        self.assertEqual(verify(self._payload())["status"], "PASS")

    def test_missing_contract_check_blocks(self):
        payload = self._payload()
        payload["checks"]["scope_isolation"] = "BLOCKED"
        result = verify(payload)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("scope_isolation_not_PASS", result["blocked_reasons"])

    def test_bad_budget_and_authority_block(self):
        payload = self._payload()
        payload["memory_authority"] = "authoritative"
        payload["context_budget"]["max_chars"] = 12001
        result = verify(payload)
        self.assertEqual(result["status"], "BLOCKED")
        self.assertIn("memory_authority_not_advisory", result["blocked_reasons"])
        self.assertIn("max_chars_out_of_bounds", result["blocked_reasons"])


if __name__ == "__main__":
    unittest.main()
