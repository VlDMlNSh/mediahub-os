"""Contracts for signed provenance of the three bounded Gemini output artifacts."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/create_gemini_artifact_provenance_manifest.py"
WORKFLOWS = (
    ".github/workflows/gemini-autonomous-engineering.yml",
    ".github/workflows/gemini-agent-2.yml",
    ".github/workflows/gemini-agent-3.yml",
)
CHECKOUT_PIN = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
DOWNLOAD_PIN = "actions/download-artifact@9000827ccba6bdab643e8b6fd33ac0654aef8333"
ATTEST_PIN = "actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6"
UPLOAD_PIN = "actions/upload-artifact@b7c566a772e6b6bfb58ed0dc250532a479d7789f"
VALID_ENV = {
    "GITHUB_REPOSITORY": "VlDMlNSh/mediahub-os",
    "GITHUB_RUN_ID": "123456789",
    "GITHUB_RUN_ATTEMPT": "1",
    "MEDIAHUB_WORKFLOW_FILE": WORKFLOWS[0],
    "MEDIAHUB_DISPATCH_ID": "123e4567-e89b-42d3-a456-426614174000",
    "MEDIAHUB_TARGET_SHA": "a" * 40,
    "MEDIAHUB_TASK_JOB_RESULT": "success",
}


class GeminiArtifactAttestationWorkflowContractTests(unittest.TestCase):
    def load_workflow(self, relative_path: str) -> dict:
        return yaml.load(
            (ROOT / relative_path).read_text(encoding="utf-8"),
            Loader=yaml.BaseLoader,
        )

    def test_each_bounded_child_has_isolated_least_privilege_attestation_job(self):
        expected_permissions = {
            "actions": "read",
            "contents": "read",
            "id-token": "write",
            "attestations": "write",
            "artifact-metadata": "write",
        }
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                workflow = self.load_workflow(relative_path)
                jobs = workflow["jobs"]
                attestation = jobs["attest_evidence"]
                self.assertEqual(attestation["needs"], "engineer")
                self.assertIn("always()", attestation["if"])
                self.assertIn("needs.engineer.result != 'skipped'", attestation["if"])
                self.assertIn("needs.engineer.result != 'cancelled'", attestation["if"])
                self.assertEqual(attestation["permissions"], expected_permissions)
                self.assertNotIn("id-token", jobs["engineer"]["permissions"])
                self.assertNotIn("attestations", jobs["engineer"]["permissions"])
                self.assertNotIn("artifact-metadata", jobs["engineer"]["permissions"])

    def test_upstream_actions_are_immutable_pins_and_artifact_digest_is_signed(self):
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                workflow = self.load_workflow(relative_path)
                steps = workflow["jobs"]["attest_evidence"]["steps"]
                actions = {step.get("name"): step.get("uses") for step in steps}
                self.assertEqual(actions["Checkout trusted workflow source"], CHECKOUT_PIN)
                self.assertEqual(actions["Download bounded Gemini output artifact"], DOWNLOAD_PIN)
                self.assertEqual(
                    actions["Create GitHub/Sigstore artifact provenance attestation"],
                    ATTEST_PIN,
                )
                self.assertEqual(
                    actions["Upload manifest and signed attestation bundle"], UPLOAD_PIN
                )
                download = next(s for s in steps if s.get("uses") == DOWNLOAD_PIN)
                self.assertEqual(download["with"]["name"], "gemini-output")
                attest = next(s for s in steps if s.get("uses") == ATTEST_PIN)
                self.assertEqual(attest["with"]["subject-path"], "evidence/gemini-output-manifest.json")
                manifest = next(
                    s for s in steps
                    if s.get("name") == "Create deterministic secret-free provenance manifest"
                )
                self.assertEqual(
                    manifest["env"]["MEDIAHUB_TARGET_SHA"], "${{ inputs.target_sha }}"
                )
                self.assertEqual(
                    manifest["env"]["MEDIAHUB_TASK_JOB_RESULT"], "${{ needs.engineer.result }}"
                )

    def test_attestation_job_has_no_model_credentials_or_write_access_to_repository(self):
        forbidden_names = (
            "GEMINI_API_KEY",
            "OPENROUTER_API_KEY",
            "ANTHROPIC_API_KEY",
            "ANTHROPIC_AUTH_TOKEN",
        )
        for relative_path in WORKFLOWS:
            with self.subTest(workflow=relative_path):
                attestation = self.load_workflow(relative_path)["jobs"]["attest_evidence"]
                serialized = json.dumps(attestation)
                for name in forbidden_names:
                    self.assertNotIn(name, serialized)
                self.assertNotIn("pull-requests", attestation["permissions"])
                self.assertNotIn("issues", attestation["permissions"])
                self.assertIn("persist-credentials", json.dumps(attestation))
                self.assertIn("false", json.dumps(attestation))

    def run_manifest(self, root: Path, output: Path, env_updates: dict[str, str] | None = None):
        env = {**os.environ, **VALID_ENV, **(env_updates or {})}
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--artifact-root", str(root), "--output", str(output)],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            timeout=10,
            check=False,
        )

    def test_manifest_records_exact_target_run_dispatch_and_file_digest(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "artifact"
            root.mkdir()
            payload = b'{"response":"bounded result"}\n'
            (root / "stdout.log").write_bytes(payload)
            (root / "nested").mkdir()
            (root / "nested" / "stderr.log").write_bytes(b"no error\n")
            output = base / "manifest.json"

            result = self.run_manifest(root, output)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            manifest = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema"], "mediahub-gemini-output-provenance/v1")
            self.assertEqual(manifest["source"]["target_sha"], "a" * 40)
            self.assertEqual(manifest["source"]["workflow_run_id"], "123456789")
            self.assertEqual(
                manifest["source"]["dispatch_id"], "123e4567-e89b-42d3-a456-426614174000"
            )
            self.assertEqual(manifest["task_job_result"], "success")
            entries = {item["path"]: item for item in manifest["artifact"]["files"]}
            self.assertEqual(entries["stdout.log"]["sha256"], hashlib.sha256(payload).hexdigest())
            self.assertEqual(entries["nested/stderr.log"]["sha256"], hashlib.sha256(b"no error\n").hexdigest())
            self.assertEqual(manifest["artifact"]["file_count"], 2)

            second = base / "manifest-second.json"
            result2 = self.run_manifest(root, second)
            self.assertEqual(result2.returncode, 0, result2.stdout + result2.stderr)
            self.assertEqual(output.read_bytes(), second.read_bytes())

    def test_manifest_fails_closed_on_invalid_target_empty_artifact_and_symlink(self):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root = base / "artifact"
            root.mkdir()
            output = base / "manifest.json"

            invalid_sha = self.run_manifest(root, output, {"MEDIAHUB_TARGET_SHA": "not-a-sha"})
            self.assertNotEqual(invalid_sha.returncode, 0)
            self.assertIn("target SHA", invalid_sha.stderr)

            (root / "stdout.log").write_text("one result", encoding="utf-8")
            try:
                (root / "link").symlink_to(root / "stdout.log")
            except (OSError, NotImplementedError):
                self.skipTest("symlink creation is unavailable on this test runner")
            linked = self.run_manifest(root, output)
            self.assertNotEqual(linked.returncode, 0)
            self.assertIn("symlink", linked.stderr)

            (root / "link").unlink()
            (root / "stdout.log").unlink()
            empty = self.run_manifest(root, output)
            self.assertNotEqual(empty.returncode, 0)
            self.assertIn("no regular files", empty.stderr)


if __name__ == "__main__":
    unittest.main()
