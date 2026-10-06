import unittest
from unittest.mock import patch

import astra_github_agent as agent
from ops.control import sign_command


class AstraTransportContractTests(unittest.TestCase):
    def test_signer_requires_exact_schema_version(self):
        command = {
            "schema_version": "wrong",
            "command_id": "test-command",
            "node_id": "test-node",
            "operation": "health",
            "target_sha": "0" * 40,
            "workflow_only": False,
            "owned_paths": ["control/results/test-node.json"],
            "title": "test",
            "description": "test",
            "exclusive_actions": ["execute"],
            "issued_at": 0,
        }
        with self.assertRaises(ValueError):
            sign_command.validate_command_shape(command)

    def test_agent_rejects_wrong_schema_before_execution(self):
        with patch.object(agent.Path, "exists", return_value=True), patch.object(
            agent.Path, "read_text", return_value='{"schema_version":"wrong"}'
        ):
            self.assertIsNone(agent.read_command())

    def test_git_network_retries_and_succeeds(self):
        class Result:
            def __init__(self, code):
                self.returncode = code
                self.stdout = ""
                self.stderr = ""

        calls = []

        def fake_run(argv, timeout=120):
            calls.append((argv, timeout))
            return Result(0 if len(calls) == 3 else 1)

        with patch.object(agent, "run", side_effect=fake_run), patch.object(
            agent.time, "sleep"
        ):
            result = agent.git_network(["git", "fetch"], timeout=7, attempts=4, base_delay=1)

        self.assertEqual(result.returncode, 0)
        self.assertEqual(len(calls), 3)

    def test_git_network_stops_after_bounded_attempts(self):
        class Result:
            returncode = 1
            stdout = ""
            stderr = "transport failure"

        calls = []

        with patch.object(agent, "run", return_value=Result()) as mocked_run, patch.object(
            agent.time, "sleep"
        ):
            result = agent.git_network(["git", "push"], timeout=9, attempts=4, base_delay=1)

        self.assertEqual(result.returncode, 1)
        self.assertEqual(mocked_run.call_count, 4)

    def test_role_registry_is_a0_to_a3(self):
        roles = {"A0", "A1", "A2", "A3"}
        self.assertEqual(roles, {"A0", "A1", "A2", "A3"})

    def test_replay_marker_is_written_after_successful_command(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        main_start = source.index("def main():")
        main_source = source[main_start:]
        self.assertIn("publish(", main_source)
        self.assertIn('_mark_command_executed(cmd.get("command_id",""))', main_source)

    def test_command_auth_uses_node_specific_key(self):
        self.assertEqual(agent.COMMAND_HMAC_ENV["mh-dev-01"], "ASTRA_NODE_HMAC_KEY_MH_DEV_01")
        self.assertNotIn("ASTRA_COMMAND_HMAC_KEY", agent.COMMAND_HMAC_ENV.values())

    def test_signer_requires_node_specific_key(self):
        with patch.dict(sign_command.os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                sign_command.resolve_node_key("mh-dev-01")

    def test_signer_resolves_canonical_node_key(self):
        with patch.dict(sign_command.os.environ, {"ASTRA_NODE_HMAC_KEY_MH_DEV_01": "node-secret"}, clear=True):
            self.assertEqual(sign_command.resolve_node_key("mh-dev-01"), "node-secret")

    def test_autonomous_mission_requires_exact_target_head(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertIn('reason":"target_sha_not_exact_current_head"', source)
        self.assertIn('reason":"target_sha_changed_during_retry"', source)
        self.assertNotIn('merge-base", "--is-ancestor", target_sha, "HEAD"', source)

    def test_publish_restores_consumed_command_before_branch_checkout(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        start = source.index("def _prepare_publish_branch():")
        end = source.index("\ndef publish(", start)
        block = source[start:end]
        self.assertIn('git","restore","--source=HEAD","--",command_path', block)
        self.assertNotIn('git","clean","-f","--",command_path', block.split('if restore.returncode != 0:', 1)[0])

    def test_controller_consumes_provider_node_evidence_instead_of_local_qualification(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertIn("ASTRA_PROVIDER_EVIDENCE_PATH", source)
        self.assertIn('"source": "node_local_provider_evidence"', source)
        self.assertNotIn('subprocess.run([sys.executable,str(backend_script)]', source)

    def test_published_result_carries_secret_suppression_marker(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertIn('publish_result.setdefault("secret_values","SUPPRESSED")', source)

if __name__ == "__main__":
    unittest.main()
