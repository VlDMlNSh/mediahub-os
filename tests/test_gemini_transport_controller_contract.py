"""Static tests for explicit, token-backed GitHub API Gemini dispatch."""
from pathlib import Path
import hashlib
import hmac
import json
import os
import re
import unittest
from unittest.mock import patch
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILDREN = (
    ("gemini-autonomous-engineering.yml", "GEMINI_API_KEY"),
    ("gemini-agent-2.yml", "GEMINI_API_KEY_2"),
    ("gemini-agent-3.yml", "GEMINI_API_KEY_3"),
)


class GeminiTransportControllerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.workflow = yaml.load(cls.source, Loader=yaml.BaseLoader)
        cls.child_sources = [(name, (ROOT / ".github/workflows" / name).read_text(encoding="utf-8"), secret) for name, secret in CHILDREN]

    def test_explicit_confirmation_and_nonlaunching_default(self):
        dispatch = self.workflow["on"]["workflow_dispatch"]
        self.assertEqual(dispatch["inputs"]["mode"]["default"], "probe")
        self.assertEqual(dispatch["inputs"]["mode"]["options"], ["probe", "agents"])
        self.assertEqual(dispatch["inputs"]["confirm"]["type"], "boolean")
        self.assertEqual(dispatch["inputs"]["confirm"]["default"], "false")
        self.assertEqual(self.workflow["permissions"], {})
        condition = self.workflow["jobs"]["dispatch_and_monitor"]["if"].replace(" ", "")
        self.assertIn("github.event_name=='workflow_dispatch'", condition)
        self.assertIn("github.ref=='refs/heads/main'", condition)
        self.assertIn("inputs.mode=='agents'", condition)
        self.assertIn("inputs.confirm==true", condition)

    def test_controller_uses_transport_token_only_for_api_dispatch(self):
        self.assertIn("secrets.MEDIAHUB_GITHUB_TOKEN", self.source)
        self.assertIn("api.github.com", self.source)
        self.assertIn("/actions/workflows/{wf}/dispatches", self.source)
        self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", self.source)
        self.assertNotIn("secrets: inherit", self.source)
        for _, source, _ in self.child_sources:
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)

    def test_fixed_three_workflows_receive_same_target_sha(self):
        for filename, _ in CHILDREN:
            self.assertIn(filename, self.source)
        self.assertIn("target=ref[\"object\"][\"sha\"]", self.source)
        self.assertIn('"target_sha":target', self.source)
        self.assertIn("target_sha", self.source)
        self.assertIn("Shared immutable target SHA", self.source)

    def test_hmac_and_run_monitoring_fail_closed(self):
        self.assertIn("hmac.new", self.source)
        self.assertIn("hashlib.sha256", self.source)
        self.assertIn("NOT_COMPLETED_BEFORE_TIMEOUT", self.source)
        self.assertIn('results.get(j["id"],{}).get("conclusion")!="success"', self.source)
        self.assertNotIn("secrets: inherit", self.source)

    def test_child_provider_keys_are_separate_and_explicit(self):
        for _, source, secret in self.child_sources:
            self.assertIn(secret, source)
            self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", source)
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
            self.assertIn("needs.authorize_dispatch.result == 'success'", source)

    def test_partial_dispatch_is_recorded_and_accepted_children_are_reconciled(self):
        # Every attempt is recorded before POST; individual failures must not
        # abort the loop before accepted children are monitored and summarized.
        self.assertIn('job={"workflow":wf,"id":did,"dispatch_status":"PENDING"}; jobs.append(job)', self.source)
        self.assertIn('except Exception as exc:', self.source)
        self.assertIn('job["dispatch_status"]="UNKNOWN"', self.source)
        self.assertIn("code != 408", self.source)
        self.assertIn('pending={j["id"]:j for j in jobs if j["dispatch_status"] in ("ACCEPTED","UNKNOWN")}', self.source)
        self.assertIn('job["dispatch_status"]="UNKNOWN"', self.source)
        self.assertIn('job["dispatch_status"]="FAILED"', self.source)
        self.assertIn('Dispatch outcome unknown', self.source)
        self.assertIn('if code is not None and 400 <= code < 500 and code != 408:', self.source)
        self.assertIn('results[did]={"status":"DISPATCH_FAILED","conclusion":"failure"}', self.source)
        self.assertIn('Dispatch | Run ID | Conclusion', self.source)
        self.assertIn('len(jobs)!=3', self.source)
        self.assertIn('if j["dispatch_status"]=="UNKNOWN":', self.source)
        self.assertIn('j["dispatch_status"]="RECONCILED"', self.source)
        self.assertIn('j["dispatch_status"] not in ("ACCEPTED","RECONCILED")', self.source)
        self.assertIn('error_type={type(exc).__name__}', self.source)
        self.assertNotIn('print(exc)', self.source)


    def test_owner_only_next_comment_bridge_is_scoped_and_idempotent(self):
        event = self.workflow["on"]["issue_comment"]
        self.assertEqual(event["types"], ["created"])
        condition = self.workflow["jobs"]["dispatch_and_monitor"]["if"]
        self.assertIn("github.event.issue.number == 301", condition)
        self.assertIn("github.event.issue.pull_request == null", condition)
        self.assertIn("github.event.comment.body == '/next'", condition)
        self.assertIn("github.event.comment.author_association == 'OWNER'", condition)
        self.assertIn('SOURCE_COMMENT_ID: ${{ github.event.comment.id }}', self.source)
        self.assertIn('CURRENT_RUN_ID: ${{ github.run_id }}', self.source)
        self.assertIn('This /next comment already has a controller run; duplicate dispatch suppressed.', self.source)
        self.assertIn('("next-comment-"+source_comment_id)', self.source)
        self.assertIn('if source_comment_id:', self.source)

    def test_child_branch_names_are_unique_per_signed_dispatch(self):
        expected = {
            "gemini-autonomous-engineering.yml": "contour-a/agent-1-${{ inputs.dispatch_id }}",
            "gemini-agent-2.yml": "contour-a/agent-2-${{ inputs.dispatch_id }}",
            "gemini-agent-3.yml": "contour-a/agent-3-${{ inputs.dispatch_id }}",
        }
        for filename, source, _ in self.child_sources:
            with self.subTest(workflow=filename):
                self.assertIn(expected[filename], source)
                self.assertIn("Do not reuse a branch from another dispatch.", source)
                self.assertIn("Include the dispatch ID in the PR body.", source)

    def test_batch_admission_flag_defaults_closed(self):
        gate = self.workflow["jobs"]["readiness_gate"]
        self.assertEqual(gate["permissions"], {})
        self.assertIn("MEDIAHUB_GEMINI_BATCH_ENABLED", self.source)
        self.assertIn('BATCH_ENABLED: ${{ vars.MEDIAHUB_GEMINI_BATCH_ENABLED }}', self.source)
        self.assertIn('needs: readiness_gate', self.source)
        condition = self.workflow["jobs"]["dispatch_and_monitor"]["if"]
        self.assertIn("needs.readiness_gate.outputs.enabled == 'true'", condition)
        self.assertIn('no child dispatch will occur', self.source)
    def test_each_next_has_three_distinct_roadmap_driven_roles(self):
        self.assertIn("Per-/next Agent 1 — bounded implementation.", self.source)
        self.assertIn("highest-priority open, unblocked next task", self.source)
        self.assertIn("Per-/next Agent 2 — independent contract and test verification.", self.source)
        self.assertIn("Do not claim to have reviewed Agent 1 changes created concurrently from this batch.", self.source)
        self.assertIn("Per-/next Agent 3 — independent security and provenance audit.", self.source)
        self.assertIn("Never read or output secret values.", self.source)
        self.assertIn("no merge, deployment, qualification", self.source)


    @staticmethod
    def _extract_python_heredoc(run_text):
        lines = run_text.splitlines()
        start = next(i for i, line in enumerate(lines) if line.strip() == "python3 - <<'PY'")
        end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "PY")
        return [line.strip() for line in lines[start + 1:end] if line.strip()]

    def test_controller_hmac_payload_interoperates_with_all_child_authorizers(self):
        controller_run = self.workflow["jobs"]["dispatch_and_monitor"]["steps"][0]["run"]
        controller_lines = self._extract_python_heredoc(controller_run)
        payload_line = next(line for line in controller_lines if "; payload={" in line)
        controller_payload_expr = payload_line.split("; payload=", 1)[1]
        controller_signature_line = next(line for line in controller_lines if line.startswith("sig=hmac.new("))

        fake_key = "contract-test-only-key-not-a-secret"
        target_sha = "a" * 40
        dispatch_id = "123e4567-e89b-42d3-a456-426614174000"
        task = "non-secret HMAC interoperability fixture"
        signatures = {}

        for filename, child_source, _ in self.child_sources:
            with self.subTest(workflow=filename):
                child_workflow = yaml.load(child_source, Loader=yaml.BaseLoader)
                auth_run = child_workflow["jobs"]["authorize_dispatch"]["steps"][0]["run"]
                child_lines = self._extract_python_heredoc(auth_run)
                child_key_line = next(line for line in child_lines if line.startswith("key=os.environ.get("))
                child_payload_line = next(line for line in child_lines if line.startswith("payload={"))
                child_expected_line = next(line for line in child_lines if line.startswith("expected=hmac.new("))
                child_env = child_workflow["jobs"]["authorize_dispatch"]["steps"][0]["env"]
                self.assertEqual(child_env["WORKFLOW_FILE"], filename)

                controller_ns = {
                    "hashlib": hashlib, "hmac": hmac, "json": json,
                    "wf": filename, "did": dispatch_id, "target": target_sha,
                    "task": task, "scope": "contour-a",
                }
                exec("payload=" + controller_payload_expr, controller_ns)
                controller_ns["key"] = fake_key
                exec(controller_signature_line, controller_ns)
                signatures[filename] = controller_ns["sig"]

                runtime_env = {
                    "HMAC_KEY": fake_key,
                    "WORKFLOW_FILE": child_env["WORKFLOW_FILE"],
                    "DISPATCH_ID": dispatch_id,
                    "TARGET_SHA": target_sha,
                    "TASK": task,
                    "BASE_REF": "main",
                    "SCOPE": "contour-a",
                    "SIGNATURE": controller_ns["sig"],
                    "EVENT_NAME": "workflow_dispatch",
                    "REPOSITORY": "VlDMlNSh/mediahub-os",
                    "REF_NAME": "refs/heads/main",
                }
                child_ns = {"hashlib": hashlib, "hmac": hmac, "json": json, "os": os}
                with patch.dict(os.environ, runtime_env, clear=False):
                    exec(child_key_line, child_ns)
                    exec(child_payload_line, child_ns)
                    exec(child_expected_line, child_ns)
                self.assertEqual(child_ns["payload"], controller_ns["payload"])
                self.assertTrue(hmac.compare_digest(child_ns["expected"], runtime_env["SIGNATURE"]))

                tampered_env = dict(runtime_env, TASK=task + " (tampered)")
                tampered_ns = {"hashlib": hashlib, "hmac": hmac, "json": json, "os": os}
                with patch.dict(os.environ, tampered_env, clear=False):
                    exec(child_key_line, tampered_ns)
                    exec(child_payload_line, tampered_ns)
                    exec(child_expected_line, tampered_ns)
                self.assertFalse(hmac.compare_digest(tampered_ns["expected"], runtime_env["SIGNATURE"]))

        # A signature for one workflow must not authorize a different child.
        filename, child_source, _ = self.child_sources[1]
        child_workflow = yaml.load(child_source, Loader=yaml.BaseLoader)
        auth_run = child_workflow["jobs"]["authorize_dispatch"]["steps"][0]["run"]
        child_lines = self._extract_python_heredoc(auth_run)
        child_key_line = next(line for line in child_lines if line.startswith("key=os.environ.get("))
        child_payload_line = next(line for line in child_lines if line.startswith("payload={"))
        child_expected_line = next(line for line in child_lines if line.startswith("expected=hmac.new("))
        replay_env = {
            "HMAC_KEY": fake_key,
            "WORKFLOW_FILE": filename,
            "DISPATCH_ID": dispatch_id,
            "TARGET_SHA": target_sha,
            "TASK": task,
            "BASE_REF": "main",
            "SCOPE": "contour-a",
            "SIGNATURE": signatures[self.child_sources[0][0]],
            "EVENT_NAME": "workflow_dispatch",
            "REPOSITORY": "VlDMlNSh/mediahub-os",
            "REF_NAME": "refs/heads/main",
        }
        replay_ns = {"hashlib": hashlib, "hmac": hmac, "json": json, "os": os}
        with patch.dict(os.environ, replay_env, clear=False):
            exec(child_key_line, replay_ns)
            exec(child_payload_line, replay_ns)
            exec(child_expected_line, replay_ns)
        self.assertFalse(hmac.compare_digest(replay_ns["expected"], replay_env["SIGNATURE"]))

    def test_canonical_uuidv4_pattern_rejects_malformed_and_non_v4_ids(self):
        pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
        valid = "123e4567-e89b-42d3-a456-426614174000"
        malformed = ("not-a-uuid", "123e4567e89b42d3a456426614174000",
                     "123e4567-e89b-12d3-a456-426614174000",
                     "123e4567-e89b-42d3-7456-426614174000")
        for filename, source, _ in self.child_sources:
            with self.subTest(workflow=filename):
                self.assertIn(pattern, source)
        self.assertIsNotNone(re.fullmatch(pattern, valid))
        for candidate in malformed:
            with self.subTest(candidate=candidate):
                self.assertIsNone(re.fullmatch(pattern, candidate))


if __name__ == "__main__":
    unittest.main()
