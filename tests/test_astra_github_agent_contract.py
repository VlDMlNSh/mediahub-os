import unittest
from unittest.mock import patch

import astra_github_agent as agent
from ops.control import sign_command

class AstraTransportContractTests(unittest.TestCase):
    def test_default_repository_transport_uses_https_not_unprovisioned_ssh_key(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertIn('REMOTE=os.environ.get("ASTRA_GITHUB_REMOTE",f"https://github.com/{REPO}.git")', source)
        self.assertNotIn('REMOTE=os.environ.get("ASTRA_GITHUB_REMOTE",f"git@github.com:{REPO}.git")', source)

    def test_g4_model_capability_routing(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertIn("model_reasoning_effort=none", source)
        self.assertIn('model_provider = "omniroute"', source)
        self.assertIn('base_url = "http://127.0.0.1:20128/v1"', source)
        self.assertIn('wire_api = "responses"', source)
        self.assertIn("requires_openai_auth = false", source)
        self.assertIn('fcc_env["ENABLE_MODEL_THINKING"] = "false"', source)
        self.assertIn('codex_env["OMNIROUTE_API_KEY"] = "local"', source)
    def test_g4_has_no_inner_tempfile_import_that_shadows_module_scope(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertNotIn("        import tempfile", source)
        self.assertRegex(source[:1200], r"import .*tempfile")
    def test_g4_fcc_environment_is_initialized_before_use(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertLess(source.index("fcc_env = base_env.copy()"), source.index("fcc_host = fcc_env.get"))
    def test_g4_direct_claude_uses_isolated_fcc_transport(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertIn("direct_claude_env", source)
        self.assertIn("ANTHROPIC_BASE_URL", source)
        self.assertIn("ANTHROPIC_AUTH_TOKEN", source)
        self.assertIn("native-claude-cli-over-fcc-http", source)
        self.assertNotIn('"--bare"', source)
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

    def test_autonomous_controller_consumes_a2_artifact_without_hmac_fan_in(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertIn('source": "fresh_downloaded_a2_aggregate"', source)
        self.assertIn("distributed-verification-result.json", source)
        self.assertNotIn('subprocess.run([sys.executable,str(distributed_script)]', source)

    def test_autonomous_queue_binds_runtime_pythonpath(self):
        source = agent.Path("astra_github_agent.py").read_text(encoding="utf-8")
        self.assertIn('queue_env["PYTHONPATH"]=runtime_path', source)
        self.assertIn('mediahub_runtime.autonomous_queue', source)

if __name__ == "__main__":
    unittest.main()


class PrecomputedQueuePayloadTests(unittest.TestCase):
    def payload(self):
        sha = "a" * 40
        return {
            "schema": "mediahub.astra.autonomous-queue-summary.v1",
            "status": "PASS",
            "queue_returncode": 0,
            "command_id": "CMD-1",
            "base_sha": sha,
            "mode": "github_remote_claude_only",
            "workers": 1,
            "max_parallel_claims": 3,
            "executor_pool": {"mh-dev-01": "claude", "mh-dev-02": "claude", "Voktors-Mac-mini.local": "claude"},
            "selected_tasks": ["T1"],
            "results": [{
                "task_id": "T1", "command_id": "CMD-1", "base_sha": sha, "target_sha": sha,
                "node_id": "mh-dev-01", "executor": "claude", "verifier_identity": "claude",
                "status": "VERIFIED", "worker_run_id": "123", "worker_run_status": "completed",
                "worker_conclusion": "success", "branch": "astra-T1", "head_sha": sha,
                "remote_head": sha, "push_verification": {"status": "PASS", "branch": "astra-T1", "remote_sha": sha},
                "evidence_digest": "sha256:" + "b" * 64,
                "independent_verifier": {"status": "PASS", "returncode": 0},
            }],
        }

    def test_precomputed_queue_payload_is_bound_to_command_sha_and_verified_results(self):
        payload = self.payload()
        self.assertEqual(agent.validate_precomputed_queue_payload(payload, "CMD-1", "a" * 40), payload)

    def test_precomputed_queue_payload_rejects_wrong_command_or_sha(self):
        payload = self.payload()
        with self.assertRaisesRegex(ValueError, "command_binding"):
            agent.validate_precomputed_queue_payload(payload, "CMD-2", "a" * 40)
        with self.assertRaisesRegex(ValueError, "target_sha"):
            agent.validate_precomputed_queue_payload(payload, "CMD-1", "c" * 40)

    def test_precomputed_queue_payload_rejects_nonzero_dispatcher_exit(self):
        payload = self.payload()
        payload["queue_returncode"] = 2
        with self.assertRaisesRegex(ValueError, "queue_returncode"):
            agent.validate_precomputed_queue_payload(payload, "CMD-1", "a" * 40)

    def test_precomputed_queue_payload_rejects_nonverified_and_worker_failures(self):
        payload = self.payload()
        payload["results"][0]["status"] = "BLOCKED"
        with self.assertRaisesRegex(ValueError, "result_status"):
            agent.validate_precomputed_queue_payload(payload, "CMD-1", "a" * 40)
        payload = self.payload()
        payload["results"][0]["worker_conclusion"] = "failure"
        with self.assertRaisesRegex(ValueError, "worker_conclusion"):
            agent.validate_precomputed_queue_payload(payload, "CMD-1", "a" * 40)
