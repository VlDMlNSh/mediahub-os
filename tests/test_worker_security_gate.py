from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from ops.qualification import run_distributed_local_worker as worker


class SecurityGateSecretDetectionTests(unittest.TestCase):
    def scan(self, text: str) -> list[str]:
        with tempfile.TemporaryDirectory(prefix="mediahub-security-gate-") as directory:
            root = Path(directory)
            (root / "sample.txt").write_text(text, encoding="utf-8")
            with patch.object(worker, "ROOT", root):
                return worker.security_gate({"sample.txt"}, {"forbidden": []})

    def test_detects_api_key_assignment(self) -> None:
        key = "API" + "_KEY"
        value = "".join(["fake", "-", "test", "-", "value", "-", "1234567890"])
        findings = self.scan(f"{key} = {value!r}\n")
        self.assertEqual(findings, ["possible_secret:sample.txt"])

    def test_detects_bearer_token_assignment(self) -> None:
        key = "bear" + "er"
        value = "".join(["fake", "-", "test", "-", "value", "-", "1234567890"])
        findings = self.scan(f'{key}: "{value}"\n')
        self.assertEqual(findings, ["possible_secret:sample.txt"])

    def test_detects_private_key_pem_marker(self) -> None:
        findings = self.scan("-----BEGIN PRIVATE KEY-----\n")
        self.assertEqual(findings, ["possible_secret:sample.txt"])

    def test_allows_non_secret_text(self) -> None:
        self.assertEqual(self.scan("This is ordinary task documentation.\n"), [])


    def test_child_environment_excludes_unapproved_ambient_values(self) -> None:
        with patch.dict(
            worker.os.environ,
            {
                "PATH": "/safe/bin",
                "HOME": "/tmp/test-home",
                "MEDIAHUB_TEST_AMBIENT_SENTINEL": "ambient-value",
            },
            clear=True,
        ):
            env = worker.child_environment(
                {"MEDIAHUB_TEST_EXPLICIT_SENTINEL": "explicit-value"}
            )
        self.assertEqual(env["PATH"], "/safe/bin")
        self.assertEqual(env["HOME"], "/tmp/test-home")
        self.assertNotIn("MEDIAHUB_TEST_AMBIENT_SENTINEL", env)
        self.assertEqual(env["MEDIAHUB_TEST_EXPLICIT_SENTINEL"], "explicit-value")


if __name__ == "__main__":
    unittest.main()
