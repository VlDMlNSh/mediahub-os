import hashlib
import hmac
import importlib.util
import json
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class TestAstraCommandAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("astra_github_agent", ROOT / "astra_github_agent.py")
        cls.agent = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.agent)

    def test_signature_is_required_and_verified(self):
        a = self.agent
        key = "unit-test-key"
        a.COMMAND_HMAC_KEY = key
        a.COMMAND_HMAC_MAX_AGE_SECONDS = 900
        command = {"schema": 1, "command_id": "cmd-1", "node_id": "mh-dev-01",
                   "operation": "health", "issued_at": int(time.time())}
        body = json.dumps(command, sort_keys=True, separators=(",", ":")).encode()
        command["signature"] = hmac.new(key.encode(), body, hashlib.sha256).hexdigest()
        self.assertTrue(a._command_auth_valid(command))
        command["operation"] = "reconcile_controller_processes"
        self.assertFalse(a._command_auth_valid(command))

    def test_stale_command_is_rejected(self):
        a = self.agent
        a.COMMAND_HMAC_KEY = "unit-test-key"
        a.COMMAND_HMAC_MAX_AGE_SECONDS = 60
        command = {"schema": 1, "command_id": "cmd-2", "node_id": "mh-dev-01",
                   "operation": "health", "issued_at": int(time.time()) - 61}
        body = json.dumps(command, sort_keys=True, separators=(",", ":")).encode()
        command["signature"] = hmac.new(a.COMMAND_HMAC_KEY.encode(), body, hashlib.sha256).hexdigest()
        self.assertFalse(a._command_auth_valid(command))

    def test_command_id_path_safety_is_enforced(self):
        a = self.agent
        self.assertTrue(a._safe_id("cmd-3", "command id"))
        self.assertFalse(a._safe_id("../escape", "command id"))
        self.assertFalse(a._safe_id("cmd/escape", "command id"))
        self.assertFalse(a._safe_id("", "command id"))

    def test_target_sha_is_strictly_git_sha_shaped(self):
        a = self.agent
        self.assertTrue(a._valid_target_sha("a" * 40))
        self.assertTrue(a._valid_target_sha("a" * 64))
        self.assertFalse(a._valid_target_sha("a" * 39))
        self.assertFalse(a._valid_target_sha("../main"))
        self.assertFalse(a._valid_target_sha(""))

    def test_command_envelope_requires_all_authority_fields(self):
        a = self.agent
        expected = {
            "schema_version", "command_id", "node_id", "operation", "target_sha",
            "workflow_only", "owned_paths", "title", "description",
            "exclusive_actions", "issued_at",
        }
        self.assertEqual(expected, a.REQUIRED_COMMAND_FIELDS)

    def test_executed_command_marker_is_idempotent(self):
        a = self.agent
        with tempfile.TemporaryDirectory() as tmp:
            a.EXECUTED_COMMANDS = Path(tmp)
            self.assertFalse(a._command_already_executed("cmd-3"))
            a._mark_command_executed("cmd-3")
            self.assertTrue(a._command_already_executed("cmd-3"))


if __name__ == "__main__":
    unittest.main()
