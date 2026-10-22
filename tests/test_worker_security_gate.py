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
                {"MEDIAHUB_TEST_EXPLICIT_SENTINEL": "explicit-value"},
                explicit_allowlist={"PATH"},
            )
        self.assertEqual(env["PATH"], "/safe/bin")
        self.assertEqual(env["HOME"], "/tmp/test-home")
        self.assertNotIn("MEDIAHUB_TEST_AMBIENT_SENTINEL", env)
        self.assertNotIn("MEDIAHUB_TEST_EXPLICIT_SENTINEL", env)

    def test_fcc_env_file_cannot_inject_unapproved_credentials(self) -> None:
        with patch.dict(
            worker.os.environ,
            {"PATH": "/safe/bin", "GH_TOKEN": "ambient-token", "PYTHONPATH": "/untrusted"},
            clear=True,
        ):
            env = worker.child_environment(
                {
                    "MODEL": "ollama/qwen2.5-coder:1.5b",
                    "HOST": "127.0.0.1",
                    "PORT": "8093",
                    "ANTHROPIC_AUTH_TOKEN": "local-proxy-token",
                    "GH_TOKEN": "injected-token",
                    "ASTRA_PUBLISHER_TOKEN": "injected-token",
                    "SUPABASE_SERVICE_ROLE_KEY": "injected-key",
                    "MEDIAHUB_TEST_EXPLICIT_SENTINEL": "unapproved",
                    "PYTHONPATH": "/untrusted-explicit",
                },
                explicit_allowlist=worker.FCC_ENV_ALLOWLIST,
            )
        self.assertEqual(env["MODEL"], "ollama/qwen2.5-coder:1.5b")
        self.assertEqual(env["HOST"], "127.0.0.1")
        self.assertEqual(env["PORT"], "8093")
        self.assertEqual(env["ANTHROPIC_AUTH_TOKEN"], "local-proxy-token")
        for key in ("GH_TOKEN", "ASTRA_PUBLISHER_TOKEN", "SUPABASE_SERVICE_ROLE_KEY",
                    "MEDIAHUB_TEST_EXPLICIT_SENTINEL", "PYTHONPATH"):
            self.assertNotIn(key, env)


if __name__ == "__main__":
    unittest.main()
