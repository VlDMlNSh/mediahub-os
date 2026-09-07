import unittest

from mediahub_runtime.evidence import EvidenceError, build_evidence_record
from mediahub_runtime.event_projection import project_runtime_event
from mediahub_runtime.state_authority import AuthorizationContext, Command, StateAuthority


AUTH = AuthorizationContext("evidence-test", True, frozenset({"state.write"}))


class MH05EvidenceBindingTests(unittest.TestCase):
    def _event(self):
        authority = StateAuthority({"value": 1})
        event = authority.execute(
            Command("cmd-evidence", "corr-evidence", "set", ("value",), 2, None, AUTH, "device-local")
        )
        return project_runtime_event(event), authority

    def _record(self, canonical, authority):
        return build_evidence_record(
            test_id="MH05-EVIDENCE-01",
            contract="MH-05",
            verification_target="remediation-test",
            git_sha="exact-test-sha",
            branch="remediation/mh05-r3-event-evidence",
            runtime="python-3.12",
            platform="linux",
            dependency_lock="stdlib",
            command="python -m unittest",
            started_at="2026-09-07T00:00:00+00:00",
            completed_at="2026-09-07T00:00:01+00:00",
            exit_code=0,
            canonical_event=canonical,
            pre_state={"value": 1},
            post_state=authority.read(),
            authorization_context=AUTH,
            authorization_result="authorized",
            validation_result="valid",
            mutation_result="committed",
            stdout_reference="stdout:test",
            structured_result_reference="result:test",
            reproducibility_reference="test:MH05-EVIDENCE-01",
            reviewer="automated-test",
            review_basis="runtime regression",
            unknowns=[],
            contradictions=[],
            blockers=[],
        )

    def test_record_binds_same_event_and_fingerprint(self):
        canonical, authority = self._event()
        record = self._record(canonical, authority)
        emitted = record["observation"]["emitted_events"][0]
        self.assertEqual(emitted["id"], canonical.id)
        self.assertEqual(emitted["source"], canonical.source)
        self.assertEqual(emitted["correlation_id"], canonical.correlation_id)
        self.assertEqual(emitted["causation_id"], canonical.causation_id)
        self.assertEqual(record["evidence"]["artifact_hash"], canonical.evidence_fingerprint())
        self.assertEqual(record["input"]["command_id"], canonical.metadata["command_id"])

    def test_record_preserves_real_authorization_context(self):
        canonical, authority = self._event()
        record = self._record(canonical, authority)
        self.assertEqual(
            record["input"]["authorization_context"],
            {"subject": "evidence-test", "authenticated": True, "permissions": ["state.write"]},
        )

    def test_missing_authorization_context_is_rejected(self):
        canonical, authority = self._event()
        with self.assertRaises(EvidenceError):
            self._record(canonical, authority)  # exercised through explicit None below

    def test_record_is_observational(self):
        canonical, authority = self._event()
        before = authority.read()
        self._record(canonical, authority)
        self.assertEqual(authority.read(), before)
        self.assertEqual(authority.metadata()["event_sequence"], 1)

    def test_invalid_event_is_rejected(self):
        with self.assertRaises(EvidenceError):
            build_evidence_record(
                test_id="x", contract="x", verification_target="x", git_sha="x", branch="x",
                runtime="x", platform="x", dependency_lock="x", command="x", started_at="x",
                completed_at="x", exit_code=0, canonical_event=object(), pre_state={}, post_state={},
                authorization_context=AUTH, authorization_result="x", validation_result="x", mutation_result="x",
                stdout_reference="x", structured_result_reference="x", reproducibility_reference="x", reviewer="x",
                review_basis="x", unknowns=[], contradictions=[], blockers=[],
            )


if __name__ == "__main__":
    unittest.main()
