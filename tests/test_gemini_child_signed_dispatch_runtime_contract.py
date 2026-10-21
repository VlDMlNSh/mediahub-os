"""Execute the exact child HMAC authorization scripts with a synthetic test key.

These tests perform no network requests and never use repository or provider secrets.
"""
from pathlib import Path
import hashlib
import hmac
import json
import os
import subprocess
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILD_WORKFLOWS = (
    ".github/workflows/gemini-autonomous-engineering.yml",
    ".github/workflows/gemini-agent-2.yml",
    ".github/workflows/gemini-agent-3.yml",
)
TEST_KEY = "unit-test-only-not-a-secret"
VALID_UUID4 = "123e4567-e89b-42d3-a456-426614174000"
VALID_SHA = "a" * 40
SIGNED_FIELDS = ("workflow_file", "dispatch_id", "target_sha", "task", "base_ref", "scope")


def load_authorizer(path):
    workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    step = workflow["jobs"]["authorize_dispatch"]["steps"][0]
    return step["run"]


def make_environment(workflow_file, signed_overrides=None, runtime_overrides=None):
    values = {
        "HMAC_KEY": TEST_KEY,
        "WORKFLOW_FILE": workflow_file,
        "DISPATCH_ID": VALID_UUID4,
        "TARGET_SHA": VALID_SHA,
        "TASK": "Wave 319 bounded contract and test review",
        "BASE_REF": "main",
        "SCOPE": "contour-a",
        "EVENT_NAME": "workflow_dispatch",
        "REPOSITORY": "VlDMlNSh/mediahub-os",
        "REF_NAME": "refs/heads/main",
    }
    if signed_overrides:
        env_names = {
            "workflow_file": "WORKFLOW_FILE",
            "dispatch_id": "DISPATCH_ID",
            "target_sha": "TARGET_SHA",
            "task": "TASK",
            "base_ref": "BASE_REF",
            "scope": "SCOPE",
        }
        for field, value in signed_overrides.items():
            values[env_names[field]] = value
    payload = {
        "workflow_file": values["WORKFLOW_FILE"],
        "dispatch_id": values["DISPATCH_ID"],
        "target_sha": values["TARGET_SHA"],
        "task": values["TASK"],
        "base_ref": values["BASE_REF"],
        "scope": values["SCOPE"],
    }
    values["SIGNATURE"] = hmac.new(
        values["HMAC_KEY"].encode(),
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(),
        hashlib.sha256,
    ).hexdigest()
    if runtime_overrides:
        values.update(runtime_overrides)
    return values


def run_authorizer(script, environment):
    return subprocess.run(
        ["bash", "-euo", "pipefail", "-c", script],
        env={**os.environ, **environment},
        text=True,
        capture_output=True,
        timeout=5,
        check=False,
    )


class GeminiChildSignedDispatchRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.children = []
        for relative_path in CHILD_WORKFLOWS:
            path = ROOT / relative_path
            cls.children.append((path.name, load_authorizer(path)))

    def test_valid_canonical_signature_succeeds_for_all_three_children(self):
        for workflow_file, script in self.children:
            with self.subTest(workflow=workflow_file):
                result = run_authorizer(script, make_environment(workflow_file))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Signed controller dispatch verified", result.stdout)

    def test_task_tampering_after_signing_is_rejected(self):
        for workflow_file, script in self.children:
            with self.subTest(workflow=workflow_file):
                env = make_environment(
                    workflow_file,
                    runtime_overrides={"TASK": "tampered task"},
                )
                result = run_authorizer(script, env)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Invalid controller signature", result.stdout)

    def test_signature_from_another_child_workflow_is_rejected(self):
        signer_name, signer_script = self.children[0]
        signer_env = make_environment(signer_name)
        for verifier_name, verifier_script in self.children[1:]:
            with self.subTest(signer=signer_name, verifier=verifier_name):
                env = dict(signer_env)
                env["WORKFLOW_FILE"] = verifier_name
                result = run_authorizer(verifier_script, env)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Invalid controller signature", result.stdout)

    def test_invalid_uuid_shapes_are_rejected_even_with_valid_signature(self):
        invalid_ids = (
            "not-a-uuid",
            "123e4567-e89b-12d3-a456-426614174000",
            "123e4567-e89b-42d3-7456-426614174000",
            "123e4567e89b42d3a456426614174000",
            "123e4567-e89b-42d3-a456-426614174000-extra",
        )
        for workflow_file, script in self.children:
            for dispatch_id in invalid_ids:
                with self.subTest(workflow=workflow_file, dispatch_id=dispatch_id):
                    env = make_environment(
                        workflow_file,
                        signed_overrides={"dispatch_id": dispatch_id},
                    )
                    result = run_authorizer(script, env)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Malformed target SHA or dispatch ID", result.stdout)

    def test_invalid_target_sha_is_rejected_before_signature_check(self):
        for workflow_file, script in self.children:
            with self.subTest(workflow=workflow_file):
                env = make_environment(
                    workflow_file,
                    signed_overrides={"target_sha": "short-sha"},
                )
                result = run_authorizer(script, env)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Malformed target SHA or dispatch ID", result.stdout)

    def test_non_allowlisted_base_and_scope_are_rejected_even_when_signed(self):
        cases = (
            {"base_ref": "feature/unsafe"},
            {"scope": "contour-b"},
        )
        for workflow_file, script in self.children:
            for signed_override in cases:
                with self.subTest(workflow=workflow_file, override=signed_override):
                    env = make_environment(
                        workflow_file,
                        signed_overrides=signed_override,
                    )
                    result = run_authorizer(script, env)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Input outside allowlist", result.stdout)

    def test_wrong_event_repository_or_ref_is_rejected(self):
        cases = (
            {"EVENT_NAME": "pull_request"},
            {"REPOSITORY": "attacker/example"},
            {"REF_NAME": "refs/heads/feature"},
        )
        for workflow_file, script in self.children:
            for override in cases:
                with self.subTest(workflow=workflow_file, override=override):
                    env = make_environment(
                        workflow_file,
                        runtime_overrides=override,
                    )
                    result = run_authorizer(script, env)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Child must run from trusted main workflow_dispatch", result.stdout)

    def test_missing_key_and_invalid_signature_fail_closed(self):
        for workflow_file, script in self.children:
            with self.subTest(workflow=workflow_file, case="missing-key"):
                env = make_environment(workflow_file, runtime_overrides={"HMAC_KEY": ""})
                result = run_authorizer(script, env)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Dispatch HMAC secret missing", result.stdout)
            with self.subTest(workflow=workflow_file, case="invalid-signature"):
                env = make_environment(workflow_file, runtime_overrides={"SIGNATURE": "0" * 64})
                result = run_authorizer(script, env)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("Invalid controller signature", result.stdout)

    def test_controller_and_all_children_use_the_same_canonical_signature_contract(self):
        controller = CONTROLLER_PATH.read_text(encoding="utf-8")
        self.assertIn(
            'json.dumps(payload,sort_keys=True,separators=(",",":")).encode()',
            controller,
        )
        for workflow_file, script in self.children:
            with self.subTest(workflow=workflow_file):
                self.assertIn('json.dumps(payload,sort_keys=True,separators=(",",":")).encode()', script)
                self.assertIn("hmac.compare_digest", script)
                self.assertIn(
                    'r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"',
                    script,
                )


if __name__ == "__main__":
    unittest.main()
