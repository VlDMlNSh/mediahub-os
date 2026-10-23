"""Execute the exact child HMAC authorization scripts with a synthetic test key.

These tests perform no network requests and never use repository or provider secrets.
"""
from pathlib import Path
import hashlib
import hmac
import json
import os
import subprocess
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTROLLER_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILD_WORKFLOWS = (
    ".github/workflows/gemini-autonomous-engineering.yml",
    ".github/workflows/gemini-agent-2.yml",
    ".github/workflows/gemini-agent-3.yml",
    ".github/workflows/gemini-fcc-independent-review-wave409.yml",
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
    # Test overrides use the canonical signed-field names; translate them to
    # the child's uppercase environment-variable names before signing.
    env_names = {
        "workflow_file": "WORKFLOW_FILE",
        "dispatch_id": "DISPATCH_ID",
        "target_sha": "TARGET_SHA",
        "task": "TASK",
        "base_ref": "BASE_REF",
        "scope": "SCOPE",
    }
    for field, value in (signed_overrides or {}).items():
        if field not in env_names:
            raise ValueError(f"Unsupported signed field: {field}")
        values[env_names[field]] = value
    payload = {
        field: values[env_names[field]]
        for field in SIGNED_FIELDS
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

    def test_valid_canonical_signature_succeeds_for_all_authorized_children(self):
        for workflow_file, script in self.children:
            with self.subTest(workflow=workflow_file):
                result = run_authorizer(script, make_environment(workflow_file))
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertIn("Signed", result.stdout)
                self.assertIn("dispatch verified", result.stdout)

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

    def test_unsupported_signed_fixture_override_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unsupported signed field: attacker_controlled"):
            make_environment(
                CHILD_WORKFLOWS[0].split("/")[-1],
                signed_overrides={"attacker_controlled": "value"},
            )

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



    def test_review_child_is_read_only_and_uploads_review_artifact(self):
        path = ROOT / ".github/workflows/gemini-fcc-independent-review-wave409.yml"
        workflow = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
        self.assertEqual(workflow["permissions"]["contents"], "read")
        self.assertEqual(workflow["jobs"]["review"]["permissions"]["contents"], "read")
        self.assertNotIn("pull-requests", workflow["jobs"]["review"]["permissions"])
        source = path.read_text(encoding="utf-8")
        self.assertIn('"tools": { "core": ["read_file", "grep_search", "glob", "list_directory"] }', source)
        self.assertIn("persist-credentials: false", source)
        self.assertIn("actions/upload-artifact@", source)
        self.assertIn("Validate non-empty structured review output", source)
        self.assertNotIn("GITHUB_PERSONAL_ACCESS_TOKEN", source)
        self.assertNotIn("create_pull_request", source)
        self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", source)
        self.assertIn("secrets.GEMINI_API_KEY_2", source)
        self.assertIn("git diff --no-ext-diff --unified=80 85e74ec24b862a5f6427ad5dca7d050df89c224c 3a0cda63a6e39b844c3d78bede4b777e3a0004bf", source)
        self.assertIn("git diff --no-ext-diff --unified=80 3a0cda63a6e39b844c3d78bede4b777e3a0004bf 074f20eb495666946a14410ab88d566aaa754f24", source)
        self.assertNotIn("git diff --no-ext-diff --unified=80 85e74ec24b862a5f6427ad5dca7d050df89c224c a8cef5fbad56c93573e309c6048ffd8a0f675053", source)

    def test_child_output_validator_accepts_only_actionable_pr_results(self):
        valid_output = {
            "response": "bounded result",
            "stats": {
                "tools": {
                    "byName": {
                        "mcp_github_get_file_contents": {"success": 1},
                        "mcp_github_create_pull_request": {"success": 1},
                    }
                }
            },
        }
        invalid_outputs = (
            ("malformed-json", "{", "not valid JSON"),
            (
                "empty-response",
                json.dumps({**valid_output, "response": "  \n"}),
                "empty response",
            ),
            (
                "no-successful-tools",
                json.dumps({
                    "response": "result",
                    "stats": {"tools": {"byName": {
                        "mcp_github_get_file_contents": {"success": 0},
                        "mcp_github_create_pull_request": {"success": 0},
                    }}},
                }),
                "without a successful tool call",
            ),
            (
                "no-pr-creation",
                json.dumps({
                    "response": "result",
                    "stats": {"tools": {"byName": {
                        "mcp_github_get_file_contents": {"success": 1},
                    }}},
                }),
                "did not successfully create a Pull Request",
            ),
        )
        for relative_path in CHILD_WORKFLOWS[:3]:
            workflow_path = ROOT / relative_path
            workflow = yaml.load(
                workflow_path.read_text(encoding="utf-8"),
                Loader=yaml.BaseLoader,
            )
            validator = next(
                step["run"]
                for step in workflow["jobs"]["engineer"]["steps"]
                if step.get("name") == "Validate Gemini produced an actionable PR result"
            )
            with self.subTest(workflow=workflow_path.name, case="valid"):
                with tempfile.TemporaryDirectory() as temporary:
                    output_path = Path(temporary) / "gemini-artifacts" / "stdout.log"
                    output_path.parent.mkdir()
                    output_path.write_text(json.dumps(valid_output), encoding="utf-8")
                    result = subprocess.run(
                        ["bash", "-euo", "pipefail", "-c", validator],
                        cwd=temporary,
                        text=True,
                        capture_output=True,
                        timeout=5,
                        check=False,
                    )
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertIn("recorded a successful Pull Request", result.stdout)
            failure_cases = (
                ("missing-output", None, "missing or empty"),
                *invalid_outputs,
            )
            for case, output, expected_message in failure_cases:
                with self.subTest(workflow=workflow_path.name, case=case):
                    with tempfile.TemporaryDirectory() as temporary:
                        output_path = Path(temporary) / "gemini-artifacts" / "stdout.log"
                        if output is not None:
                            output_path.parent.mkdir()
                            output_path.write_text(output, encoding="utf-8")
                        result = subprocess.run(
                            ["bash", "-euo", "pipefail", "-c", validator],
                            cwd=temporary,
                            text=True,
                            capture_output=True,
                            timeout=5,
                            check=False,
                        )
                        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
                        self.assertIn(expected_message, result.stdout + result.stderr)


    def test_review_child_fails_closed_when_gemini_execution_fails(self):
        relative_path = ".github/workflows/gemini-fcc-independent-review-wave409.yml"
        workflow = yaml.load(
            (ROOT / relative_path).read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )
        steps = workflow["jobs"]["review"]["steps"]
        gemini_step = next(step for step in steps if step.get("id") == "gemini")
        validator_step = next(
            step for step in steps
            if step.get("name") == "Validate non-empty structured review output"
        )
        self.assertNotIn("continue-on-error", gemini_step)
        self.assertEqual(validator_step.get("if"), "always()")
        self.assertEqual(
            validator_step.get("env", {}).get("GEMINI_OUTCOME"),
            "${{ steps.gemini.outcome }}",
        )
        self.assertIn('if [[ "$GEMINI_OUTCOME" != "success" ]]', validator_step["run"])
        self.assertNotIn("continue-on-error", workflow["jobs"]["review"])
        upload_step = next(
            step for step in steps if step.get("name") == "Upload review evidence"
        )
        self.assertEqual(upload_step.get("if"), "always()")
        self.assertNotIn("continue-on-error", upload_step)

        valid_output = json.dumps({
            "response": "Review completed with evidence.",
            "stats": {"tools": {"byName": {"read_file": {"success": 1}}}},
        })
        with tempfile.TemporaryDirectory() as temporary:
            output_path = Path(temporary) / "gemini-artifacts" / "stdout.log"
            output_path.parent.mkdir()
            output_path.write_text(valid_output, encoding="utf-8")

            for outcome in ("failure", "cancelled", "skipped", ""):
                with self.subTest(gemini_outcome=outcome or "empty"):
                    failed_model = subprocess.run(
                        ["bash", "-euo", "pipefail", "-c", validator_step["run"]],
                        cwd=temporary,
                        env={**os.environ, "GEMINI_OUTCOME": outcome},
                        text=True,
                        capture_output=True,
                        timeout=5,
                        check=False,
                    )
                    self.assertNotEqual(failed_model.returncode, 0)
                    self.assertIn(
                        "Gemini review execution did not succeed",
                        failed_model.stdout + failed_model.stderr,
                    )

            successful_model = subprocess.run(
                ["bash", "-euo", "pipefail", "-c", validator_step["run"]],
                cwd=temporary,
                env={**os.environ, "GEMINI_OUTCOME": "success"},
                text=True,
                capture_output=True,
                timeout=5,
                check=False,
            )
            self.assertEqual(
                successful_model.returncode, 0,
                successful_model.stdout + successful_model.stderr,
            )


if __name__ == "__main__":
    unittest.main()
