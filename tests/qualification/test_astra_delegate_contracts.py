"""Delegation-style runtime tests for ASTRA GOLD category and replay contracts.

These are intentional "delegation" tests: they exercise the shared
contract helpers behind the schema categories and the replay contract
without pretending that any real provider or executor is qualified.
They fail closed by design.
"""

import unittest

from tests.common_delegates import (
    CategoryEvidence,
    category_acceptance_requires,
    replay_accepts_only_original_status,
    replay_idempotency_check,
)


class CategoryAcceptanceDelegateTests(unittest.TestCase):
    def test_accepted_payload_matches_required_shape(self):
        evidence = {
            "issuer": "example-source",
            "source_sha": "abc123",
            "version": "1.0.0",
            "dependency_fingerprint": "lockfile-sha",
            "non_mutating_probe": True,
            "sandbox_boundary": True,
            "result_validation": True,
            "recovery": True,
            "a3_binding": True,
        }
        result = category_acceptance_requires(
            evidence,
            issuer="example-source",
            version="1.0.0",
            dependency_fingerprint="lockfile-sha",
            non_mutating_probe=True,
            sandbox_boundary=True,
            result_validation=True,
            recovery=True,
            a3_binding=True,
        )
        self.assertTrue(result["accepted"])
        self.assertEqual(result["missing"], [])
        self.assertFalse(result["blocked"])

    def test_missing_fields_are_reported(self):
        evidence = {
            "issuer": "example-source",
            "source_sha": "abc123",
            "non_mutating_probe": True,
        }
        result = category_acceptance_requires(
            evidence,
            issuer="example-source",
            version="1.0.0",
            dependency_fingerprint="lockfile-sha",
            non_mutating_probe=True,
            sandbox_boundary=True,
            result_validation=True,
            recovery=True,
            a3_binding=True,
        )
        self.assertFalse(result["accepted"])
        self.assertIn("version", result["missing"])
        self.assertIn("dependency_fingerprint", result["missing"])

    def test_authority_boundary_is_explicit_not_implied(self):
        evidence = {
            "issuer": "candidate",
            "source_sha": "abc123",
            "version": "1.0.0",
            "dependency_fingerprint": "lockfile-sha",
            "non_mutating_probe": True,
            "sandbox_boundary": True,
            "result_validation": True,
            "recovery": True,
        }
        result = category_acceptance_requires(
            evidence,
            issuer="example-source",
            version="1.0.0",
            dependency_fingerprint="lockfile-sha",
            non_mutating_probe=True,
            sandbox_boundary=True,
            result_validation=True,
            recovery=True,
            a3_binding=True,
        )
        self.assertFalse(result["accepted"])
        self.assertIn("a3_binding", result["missing"])

    def test_weak_probe_blocks_acceptance(self):
        evidence = {
            "issuer": "example-source",
            "source_sha": "abc123",
            "version": "1.0.0",
            "dependency_fingerprint": "lockfile-sha",
            "non_mutating_probe": False,
            "sandbox_boundary": True,
            "result_validation": True,
            "recovery": True,
            "a3_binding": True,
        }
        result = category_acceptance_requires(
            evidence,
            issuer="example-source",
            version="1.0.0",
            dependency_fingerprint="lockfile-sha",
            non_mutating_probe=True,
            sandbox_boundary=True,
            result_validation=True,
            recovery=True,
            a3_binding=True,
        )
        self.assertFalse(result["accepted"])
        self.assertIn("non_mutating_probe", result["missing"])


class ReplayIdempotencyDelegateTests(unittest.TestCase):
    def test_valid_replay_matches_original_status(self):
        replay = replay_idempotency_check(
            event_id="r1",
            original_event_id="r1",
            timestamp=1.0,
            expected_original_status="PASS",
        )
        self.assertEqual(replay.status, "PASS")
        result = replay_accepts_only_original_status(replay, "PASS")
        self.assertTrue(result["replay_acceptable"])
        self.assertFalse(result["blocked"])

    def test_mismatched_event_id_is_replay_anomaly(self):
        replay = replay_idempotency_check(
            event_id="r1",
            original_event_id="r2",
            timestamp=1.0,
            expected_original_status="PASS",
        )
        result = replay_accepts_only_original_status(replay, "PASS")
        self.assertFalse(result["replay_acceptable"])
        self.assertEqual(result["blocked"], replay.status != result["original_status"])
        self.assertIn("replay_status", result)

    def test_mismatched_status_is_replay_anomaly(self):
        replay = replay_idempotency_check(
            event_id="r1",
            original_event_id="r1",
            timestamp=1.0,
            expected_original_status="PASS",
        )
        result = replay_accepts_only_original_status(replay, "BLOCKED")
        self.assertFalse(result["replay_acceptable"])
        self.assertTrue(result["blocked"])

    def test_invalid_payload_is_blocked(self):
        replay = replay_idempotency_check(
            event_id="",
            original_event_id="r1",
            timestamp=-1.0,
            expected_original_status="PASS",
        )
        self.assertEqual(replay.status, "BLOCKED")
        result = replay_accepts_only_original_status(replay, "PASS")
        self.assertFalse(result["replay_acceptable"])
        self.assertTrue(result["blocked"])

    def test_authority_boundary_is_not_implied_by_replay_failure(self):
        replay = replay_idempotency_check(
            event_id="r1",
            original_event_id="r1",
            timestamp=1.0,
            expected_original_status="PASS",
        )
        result = replay_accepts_only_original_status(replay, "BLOCKED")
        self.assertTrue(result["blocked"])
        self.assertEqual(result["blocked"], replay.status != result["original_status"])


if __name__ == "__main__":
    unittest.main()
