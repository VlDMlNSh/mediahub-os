import copy
import json
import unittest
from pathlib import Path

from ops.qualification.source_change_bundle import BundleValidationError, validate_bundle_binding

ROOT = Path(__file__).resolve().parents[2]


class SourceChangeBundleTests(unittest.TestCase):
    def setUp(self):
        self.expected = {
            "task_id": "task-01", "command_id": "cmd-01", "node_id": "node-01",
            "base_sha": "d" * 40, "target_sha": "a" * 40, "issuer_id": "issuer-ci", "capability_id": "source-change-proposal",
            "policy_sha256": "b" * 64, "signed_command_sha256": "c" * 64,
        }
        self.owned_paths = ["docs/example.md", "tests/test_example.py"]
        self.bundle = {
            "schema_version": "mediahub.astra.source-change-bundle.v1", "bundle_id": "bundle-01",
            "task_id": "task-01", "command_id": "cmd-01", "node_id": "node-01",
            "base_sha": "d" * 40, "target_sha": "a" * 40,
            "patch_sha256": "e" * 64, "patch_size": 17,
            "changed_paths": ["docs/example.md"],
            "authorization_context": {"issuer_id": "issuer-ci", "capability_id": "source-change-proposal",
                                      "policy_sha256": "b" * 64, "signed_command_sha256": "c" * 64},
            "created_at": 1, "state": "PROPOSED_UNVERIFIED",
        }

    def assert_rejected(self, mutate, reason):
        bundle = copy.deepcopy(self.bundle)
        mutate(bundle)
        with self.assertRaisesRegex(BundleValidationError, reason):
            validate_bundle_binding(bundle, expected=self.expected, owned_paths=self.owned_paths)

    def test_valid_candidate_is_only_structurally_bound(self):
        validate_bundle_binding(self.bundle, expected=self.expected, owned_paths=self.owned_paths)

    def test_schema_is_valid_json_and_explicitly_unverified(self):
        schema = json.loads((ROOT / "architecture/mesh/source-change-bundle.schema.json").read_text())
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        self.assertEqual(schema["properties"]["state"]["const"], "PROPOSED_UNVERIFIED")
        self.assertIn("not authorization", schema["description"])

    def test_missing_authorization_context_fails_closed(self):
        self.assert_rejected(lambda b: b.pop("authorization_context"), "authorization_context_required")

    def test_unknown_fields_fail_closed(self):
        self.assert_rejected(lambda b: b.__setitem__("publisher_token", "never-allowed"), "unexpected_bundle_fields")
        self.assert_rejected(lambda b: b["authorization_context"].__setitem__("wildcard", True), "authorization_context_fields_mismatch")

    def test_wrong_task_command_node_or_revision_fails_closed(self):
        for field, value, reason in [("task_id", "other", "task_id_mismatch"), ("command_id", "other", "command_id_mismatch"),
                                     ("node_id", "other", "node_id_mismatch"), ("base_sha", "f" * 40, "base_sha_mismatch"),
                                     ("target_sha", "f" * 40, "target_sha_mismatch")]:
            with self.subTest(field=field):
                self.assert_rejected(lambda b, f=field, v=value: b.__setitem__(f, v), reason)

    def test_wrong_issuer_capability_or_policy_digest_fails_closed(self):
        cases = [("issuer_id", "other", "authorization_issuer_id_mismatch"),
                 ("capability_id", "wildcard", "authorization_capability_id_mismatch"),
                 ("policy_sha256", "f" * 64, "authorization_policy_sha256_mismatch"),
                 ("signed_command_sha256", "f" * 64, "authorization_signed_command_sha256_mismatch")]
        for field, value, reason in cases:
            with self.subTest(field=field):
                self.assert_rejected(lambda b, f=field, v=value: b["authorization_context"].__setitem__(f, v), reason)

    def test_path_escape_absolute_windows_and_git_metadata_rejected(self):
        for path in ("../secret", "/etc/passwd", "C:/temp/file", "docs\\secret", ".git/config", "docs/.git/config", "docs//file"):
            with self.subTest(path=path):
                self.assert_rejected(lambda b, p=path: b.__setitem__("changed_paths", [p]), "unsafe_changed_path")

    def test_unowned_path_rejected(self):
        self.assert_rejected(lambda b: b.__setitem__("changed_paths", ["src/unauthorized.py"]), "changed_path_outside_owned_paths")

    def test_duplicate_path_rejected(self):
        self.assert_rejected(lambda b: b.__setitem__("changed_paths", ["docs/example.md"] * 2), "duplicate_changed_path")

    def test_malformed_digest_or_size_rejected(self):
        self.assert_rejected(lambda b: b.__setitem__("patch_sha256", "not-a-digest"), "invalid_patch_sha256")
        self.assert_rejected(lambda b: b.__setitem__("patch_size", True), "invalid_patch_size")

    def test_unverified_state_cannot_be_promoted_by_manifest(self):
        self.assert_rejected(lambda b: b.__setitem__("state", "VERIFIED"), "bundle_must_remain_unverified")

    def test_expected_authorization_context_is_mandatory(self):
        with self.assertRaisesRegex(BundleValidationError, "authorization_issuer_id_mismatch"):
            validate_bundle_binding(self.bundle, expected={**self.expected, "issuer_id": ""}, owned_paths=self.owned_paths)


if __name__ == "__main__":
    unittest.main()
