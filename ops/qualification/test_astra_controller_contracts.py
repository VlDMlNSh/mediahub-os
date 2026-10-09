"""Regression tests for Astra execution and evidence contracts."""
from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "runtime"))

WORKER_PATH = ROOT / "ops" / "qualification" / "run_distributed_local_worker.py"
SPEC = importlib.util.spec_from_file_location("astra_worker_contracts", WORKER_PATH)
assert SPEC and SPEC.loader
worker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(worker)

from mediahub_runtime.autonomous_queue import worker_artifact_name


class ExecutionBindingTests(unittest.TestCase):
    def task(self):
        return {"node_id": "mh-dev-01", "executor": "claude", "verifier": "claude"}

    def test_accepts_canonical_claude_lane(self):
        self.assertEqual(worker.validate_execution_binding(self.task(), "mh-dev-01", "claude")["platform"], "linux")

    def test_rejects_codex_environment(self):
        with self.assertRaisesRegex(RuntimeError, "permanent_executor_policy_violation"):
            worker.validate_execution_binding(self.task(), "mh-dev-01", "codex")

    def test_rejects_payload_executor_substitution(self):
        task = self.task()
        task["executor"] = "codex"
        with self.assertRaisesRegex(RuntimeError, "task_executor_binding_mismatch"):
            worker.validate_execution_binding(task, "mh-dev-01", "claude")

    def test_rejects_node_substitution(self):
        with self.assertRaisesRegex(RuntimeError, "task_node_binding_mismatch"):
            worker.validate_execution_binding(self.task(), "mh-dev-02", "claude")

    def test_rejects_non_claude_verifier(self):
        task = self.task()
        task["verifier"] = "codex"
        with self.assertRaisesRegex(RuntimeError, "permanent_verifier_policy_violation"):
            worker.validate_execution_binding(task, "mh-dev-01", "claude")


class SecretDetectionTests(unittest.TestCase):
    def test_detects_common_secret_assignments(self):
        samples = (
            "API_KEY='0123456789abcdef'",
            'API_KEY = "0123456789abcdef"',
            "access_token='abcdefghijklmnop'",
            'secret="abcdefghijklmnop"',
            "bearer='abcdefghijklmnop'",
        )
        for sample in samples:
            with self.subTest(sample=sample):
                self.assertTrue(worker.contains_secret(sample))

    def test_detects_private_key_header(self):
        self.assertTrue(worker.contains_secret("-----BEGIN PRIVATE KEY-----"))

    def test_does_not_flag_plain_text_without_assignment(self):
        self.assertFalse(worker.contains_secret("The API key is stored in a secret manager."))


class ArtifactContractTests(unittest.TestCase):
    def test_linux_artifact_names_match_workflow(self):
        self.assertEqual(worker_artifact_name(123, "mh-dev-01"), "astra-distributed-worker-mh-dev-01-claude-123")
        self.assertEqual(worker_artifact_name(123, "mh-dev-02"), "astra-distributed-worker-mh-dev-02-claude-123")

    def test_mac_artifact_name_matches_workflow(self):
        self.assertEqual(worker_artifact_name(123, "Voktors-Mac-mini.local"), "astra-distributed-worker-123")

    def test_rejects_unknown_node_and_invalid_run_id(self):
        with self.assertRaisesRegex(ValueError, "unsupported_worker_node"):
            worker_artifact_name(123, "unknown-node")
        with self.assertRaisesRegex(ValueError, "invalid_worker_run_id"):
            worker_artifact_name("12x", "mh-dev-01")


if __name__ == "__main__":
    unittest.main()
