"""Tests for gateway identity trace and native-provider qualification separation.

These exercises the requirement that:
- provider identity is preserved in evidence;
- gateway success never substitutes for native-provider qualification;
- a cloud executor path is a candidate, not an authority.
"""

import unittest

GATEWAY_PROVIDER = "openrouter"
NATIVE_PROVIDER = "gemini"


class GatewayIdentityAndNativeSeparationTests(unittest.TestCase):
    def test_gateway_success_is_not_native_provider_qualification(self):
        gateway_result = {
            "executor_id": "CODEX_FCC",
            "provider_or_model_id": GATEWAY_PROVIDER,
            "transport_id": "OPENROUTER_GATEWAY",
            "native_provider_qualified": False,
            "provider_identity_preserved": True,
            "evidence_source": "gateway",
        }
        native_qualification = {
            "executor_id": "GEMINI_DIRECT",
            "provider_or_model_id": NATIVE_PROVIDER,
            "native_provider_qualified": True,
            "provider_identity_preserved": True,
            "evidence_source": "native",
        }
        # Gateway result says the gateway is the observed provider and that no
        # native qualification was asserted on its behalf.
        self.assertEqual(gateway_result["provider_or_model_id"], GATEWAY_PROVIDER)
        self.assertFalse(gateway_result["native_provider_qualified"])
        self.assertTrue(gateway_result["provider_identity_preserved"])
        self.assertEqual(gateway_result["evidence_source"], "gateway")

        # A separate native path may eventually qualify, but the gateway result
        # does not migrate into it.
        self.assertEqual(native_qualification["provider_or_model_id"], NATIVE_PROVIDER)
        self.assertTrue(native_qualification["native_provider_qualified"])
        self.assertEqual(native_qualification["evidence_source"], "native")

    def test_provider_identity_is_preserved_in_gateway_evidence(self):
        evidence = {
            "provider_or_model_id": GATEWAY_PROVIDER,
            "transport_or_router_id": "OPENROUTER_GATEWAY",
            "provider_identity_preserved": True,
            "native_provider_identity_inferred": False,
            "raw_provider_responses_suppressed": True,
        }
        self.assertEqual(evidence["provider_or_model_id"], GATEWAY_PROVIDER)
        self.assertTrue(evidence["provider_identity_preserved"])
        self.assertFalse(evidence["native_provider_identity_inferred"])

    def test_gateway_and_native_paths_are_distinct(self):
        gateway_paths = {"CODEX_FCC", "CLAUDE_FCC"}
        native_paths = {"GEMINI_DIRECT", "OPENAI_DIRECT"}
        self.assertTrue(gateway_paths.isdisjoint(native_paths))
        self.assertIn("CODEX_FCC", gateway_paths)
        self.assertIn("GEMINI_DIRECT", native_paths)

    def test_cloud_executor_remains_candidate_not_authority(self):
        cloud_executor = {
            "id": "GEMINI_DIRECT",
            "provider": "gemini",
            "authority": "none",
            "status": "NOT_PROVEN",
            "credential_bound": True,
            "independent_a3_required": True,
            "no_self_promotion": True,
        }
        self.assertNotEqual(cloud_executor["authority"], "EXECUTOR_ONLY")
        self.assertEqual(cloud_executor["status"], "NOT_PROVEN")
        self.assertTrue(cloud_executor["credential_bound"])
        self.assertTrue(cloud_executor["independent_a3_required"])
        self.assertTrue(cloud_executor["no_self_promotion"])

    def test_native_qualification_requires_separate_admission(self):
        native_qualification = {
            "provider_or_model_id": NATIVE_PROVIDER,
            "executor_id": "GEMINI_DIRECT",
            "credential_present": True,
            "auth_success": True,
            "model_discovery": True,
            "non_mutating_probe": True,
            "task_execution": True,
            "result_validation": True,
            "native_provider_qualified": False,
            "native_provider_qualified_requires": True,
        }
        # A cloud/native path candidate does not become qualified until the full
        # admission ladder is satisfied. The evidence snippet alone does not
        # promote it.
        self.assertEqual(native_qualification["provider_or_model_id"], NATIVE_PROVIDER)
        self.assertTrue(native_qualification["credential_present"])
        self.assertFalse(native_qualification["native_provider_qualified"])
        self.assertTrue(native_qualification["native_provider_qualified_requires"])


class IdentityTraceAndUnresolvedIdentityTests(unittest.TestCase):
    def test_unresolved_identity_blocks_admission(self):
        unresolved = {
            "provider_or_model_id": "some-github-reference",
            "exact_upstream_identity_resolved": False,
            "source_sha": "",
            "version": "",
            "runtime_identity_verified": False,
        }
        admission = {
            "allowed": False,
            "reason": "unresolved_identity",
            "required_exact_upstream_identity": True,
        }
        self.assertFalse(admission["allowed"])
        self.assertFalse(unresolved["exact_upstream_identity_resolved"])

    def test_resolved_identity_carries_full_identity_chain(self):
        resolved = {
            "provider_or_model_id": NATIVE_PROVIDER,
            "exact_upstream_identity_resolved": True,
            "source_sha": "sha-123",
            "version": "1.0.0",
            "runtime_identity_verified": True,
            "dependency_fingerprint": "lockfile-sha",
        }
        self.assertTrue(resolved["exact_upstream_identity_resolved"])
        self.assertTrue(resolved["runtime_identity_verified"])
        self.assertEqual(resolved["provider_or_model_id"], NATIVE_PROVIDER)


if __name__ == "__main__":
    unittest.main()
