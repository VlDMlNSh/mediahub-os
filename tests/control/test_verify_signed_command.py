import hashlib
import hmac
import importlib.util
import time
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location(
    "sign_command", Path(__file__).parents[2] / "ops" / "control" / "sign_command.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class SignedCommandVerifierTests(unittest.TestCase):
    KEY = "test-key"
    PATH = "control/commands/mh-dev-01.json"
    TARGET = "bbc8475c43b2aeabc86906ebf31bb4a7afa2959a"

    def command(self):
        return {
            "schema_version": MODULE.SCHEMA_VERSION,
            "command_id": "cmd-verify-001",
            "node_id": "mh-dev-01",
            "operation": "health",
            "target_sha": self.TARGET,
            "workflow_only": True,
            "owned_paths": [self.PATH],
            "title": "health",
            "description": "bounded health check",
            "exclusive_actions": ["execute"],
            "issued_at": int(time.time()),
        }

    def signed(self, command=None):
        return MODULE.sign_command(command or self.command(), self.KEY)

    def verify(self, command=None, **overrides):
        context = {
            "expected_node_id": "mh-dev-01",
            "expected_operation": "health",
            "expected_target_sha": self.TARGET,
            "allowed_paths": {self.PATH},
        }
        context.update(overrides)
        return MODULE.verify_signed_command(self.signed(command), self.KEY, **context)

    def test_accepts_valid_command(self):
        self.assertEqual(self.verify()["command_id"], "cmd-verify-001")

    def test_rejects_payload_tampering(self):
        signed = self.signed()
        signed["operation"] = "deploy"
        with self.assertRaisesRegex(ValueError, "signature verification failed"):
            MODULE.verify_signed_command(signed, self.KEY, expected_node_id="mh-dev-01",
                expected_operation="health", expected_target_sha=self.TARGET, allowed_paths={self.PATH})

    def test_rejects_wrong_node(self):
        with self.assertRaisesRegex(ValueError, "node_id"):
            self.verify(expected_node_id="mh-dev-02")

    def test_rejects_wrong_operation(self):
        with self.assertRaisesRegex(ValueError, "operation"):
            self.verify(expected_operation="deploy")

    def test_rejects_wrong_target(self):
        with self.assertRaisesRegex(ValueError, "target_sha"):
            self.verify(expected_target_sha="0" * 40)

    def test_rejects_unapproved_path(self):
        command = self.command()
        command["owned_paths"] = ["ops/control/other.json"]
        with self.assertRaisesRegex(ValueError, "exceed trusted allowed_paths"):
            self.verify(command)

    def test_rejects_path_traversal(self):
        command = self.command()
        command["owned_paths"] = ["control/../private.txt"]
        with self.assertRaisesRegex(ValueError, "unsafe path"):
            self.verify(command, allowed_paths={"control/../private.txt"})

    def test_rejects_unknown_fields(self):
        command = self.command()
        command["unreviewed_authority"] = True
        with self.assertRaisesRegex(ValueError, "unexpected command fields"):
            self.verify(command)

    def test_rejects_missing_signature(self):
        signed = self.signed()
        del signed["signature"]
        with self.assertRaisesRegex(ValueError, "signature"):
            MODULE.verify_signed_command(signed, self.KEY, expected_node_id="mh-dev-01",
                expected_operation="health", expected_target_sha=self.TARGET, allowed_paths={self.PATH})

    def test_rejects_boolean_issued_at(self):
        command = self.command()
        command["issued_at"] = True
        signed = dict(command)
        signed["signature"] = hmac.new(
            self.KEY.encode(), MODULE.canonical_command_body(signed), hashlib.sha256
        ).hexdigest()
        with self.assertRaisesRegex(ValueError, "issued_at"):
            MODULE.verify_signed_command(
                signed,
                self.KEY,
                expected_node_id="mh-dev-01",
                expected_operation="health",
                expected_target_sha=self.TARGET,
                allowed_paths={self.PATH},
                now=1,
            )

    def test_rejects_stale_command(self):
        command = self.command()
        command["issued_at"] = int(time.time()) - MODULE.MAX_AGE_SECONDS - 5
        signed = dict(command)
        signed["signature"] = hmac.new(self.KEY.encode(), MODULE.canonical_command_body(signed), hashlib.sha256).hexdigest()
        with self.assertRaisesRegex(ValueError, "freshness window"):
            MODULE.verify_signed_command(signed, self.KEY, expected_node_id="mh-dev-01",
                expected_operation="health", expected_target_sha=self.TARGET, allowed_paths={self.PATH})


if __name__ == "__main__":
    unittest.main()
