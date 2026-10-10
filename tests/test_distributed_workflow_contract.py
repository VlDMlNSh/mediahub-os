import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/astra-distributed-verification.yml"
SUPERVISOR = ROOT / ".github/workflows/astra-autonomous-supervisor.yml"


class DistributedWorkflowContractTests(unittest.TestCase):
    def test_mh25_has_single_canonical_dual_local_workflow(self):
        workflows = {p.name for p in (ROOT / ".github/workflows").glob("*.y*ml")}
        self.assertIn("mh25-dual-local-23wave.yml", workflows)
        self.assertNotIn("mh25-dual-local-executor-23wave.yml", workflows)
        canonical = (ROOT / ".github/workflows/mh25-dual-local-23wave.yml").read_text(encoding="utf-8")
        self.assertIn("name: MH-25 Dual Local Executor 23-Wave Qualification", canonical)
        self.assertIn("codex-local:", canonical)
        self.assertIn("claude-local:", canonical)
        self.assertIn("aggregate:", canonical)
        self.assertIn("verify_dual_local_23wave.py", canonical)

    def test_single_reusable_workflow_targets_all_three_nodes(self):
        document = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        self.assertTrue(document.get("jobs"))
        jobs = document["jobs"]
        self.assertIn("node-mh-dev-01", jobs)
        self.assertIn("node-mh-dev-02", jobs)
        self.assertIn("node-voktors-mac", jobs)
        self.assertIn("aggregate", jobs)
        self.assertIn("mediahub-control", str(jobs["node-mh-dev-01"]["runs-on"]))
        self.assertIn("mediahub-provider", str(jobs["node-mh-dev-02"]["runs-on"]))
        self.assertIn("astra-control", str(jobs["node-voktors-mac"]["runs-on"]))

    def test_workflow_call_declares_command_and_target_inputs(self):
        document = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        on_block = document.get("on", document.get(True))
        self.assertIsInstance(on_block, dict)
        call = on_block["workflow_call"]
        self.assertEqual(call["inputs"]["command_id"]["required"], True)
        self.assertEqual(call["inputs"]["command_id"]["type"], "string")
        self.assertEqual(call["inputs"]["target_sha"]["required"], True)
        self.assertEqual(call["inputs"]["target_sha"]["type"], "string")

    def test_workflow_uses_caller_bindings_not_its_own_run_id(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("ASTRA_COMMAND_ID: ${{ inputs.command_id }}", text)
        self.assertIn("ASTRA_TARGET_SHA: ${{ inputs.target_sha }}", text)
        self.assertNotIn("MH-AUTONOMOUS-GOLD-mh-dev-01-${{ github.run_id }}-${{ github.run_attempt }}", text)

    def test_node_jobs_require_expected_runtime_identity(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        self.assertIn('test "$(hostname)" = "mh-dev-01"', text)
        self.assertIn('test "$(id -un)" = "mediahub-runner"', text)
        self.assertIn('test "$(hostname)" = "mh-dev-02"', text)
        self.assertIn('test "$(id -un)" = "mediahub"', text)
        self.assertIn('test "$(id -un)" = "voktor"', text)
        self.assertIn('test "${RUNNER_NAME:-}" = "Voktors-Mini-Astra-Control"', text)
        self.assertIn('host="$(hostname)"', text)
        self.assertIn('test "$host" = "Voktors-Mini.Dlink" || test "$host" = "Voktors-Mac-mini"', text)

    def test_workflow_binds_command_sha_and_node_hmac(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        for marker in ("workflow_call", "ASTRA_COMMAND_ID", "ASTRA_TARGET_SHA",
                       "ASTRA_NODE_HMAC_KEY_MH_DEV_01",
                       "ASTRA_NODE_HMAC_KEY_MH_DEV_02",
                       "ASTRA_NODE_HMAC_KEY_VOKTORS_MAC",
                       "produce_distributed_node_attestation.py"):
            self.assertIn(marker, text)

    def test_distributed_runner_contract_declares_all_three_nodes(self):
        contract = ROOT / "control/qualification/distributed-runner-contract.json"
        self.assertTrue(contract.is_file())
        text = contract.read_text(encoding="utf-8")
        for label in (
            "mediahub-control",
            "mediahub-provider",
            "astra-control",
        ):
            self.assertIn(label, text)
        for node in ("mh-dev-01", "mh-dev-02", "Voktors-Mac-mini.local"):
            self.assertIn(node, text)

    def test_supervisor_does_not_inject_provider_credentials(self):
        text = SUPERVISOR.read_text(encoding="utf-8")
        forbidden = (
            "SILICONFLOW_API_KEY", "NOVITA_API_KEY", "ZAI_API_KEY", "KIMI_API_KEY",
            "MOONSHOT_API_KEY", "LLM7_API_KEY", "SAMBANOVA_API_KEY", "AIONLABS_API_KEY",
            "CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID", "NARAROUTER_API_KEY",
            "ORCAROUTER_API_KEY", "UNOROUTER_API_KEY", "ZEROUTER_API_KEY",
            "DEEPSEEK_API_KEY", "GEMINI_API_KEY", "GROQ_API_KEY", "MISTRAL_API_KEY",
            "OPENROUTER_API_KEY", "HF_TOKEN",
        )
        for marker in forbidden:
            self.assertNotIn(marker, text)

    def test_supervisor_uses_single_distributed_gate(self):
        text = SUPERVISOR.read_text(encoding="utf-8")
        self.assertIn("distributed-verification:", text)
        self.assertIn("astra-distributed-verification.yml", text)
        self.assertIn("distributed-verification:", text)
        self.assertIn("needs:", text)
        self.assertIn("download-artifact@v4", text)
        self.assertNotIn("astra-distributed-node-attestations.yml", text)
        self.assertNotIn("distributed_candidates", text)

    def test_each_node_job_declares_artifact_output_path(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        for node in ("mh-dev-01", "mh-dev-02", "Voktors-Mac-mini.local"):
            self.assertIn("ASTRA_NODE_ATTESTATION_OUTPUT", text)
        self.assertIn(".astra-state/distributed-attestation/mh-dev-01.json", text)
        self.assertIn(".astra-state/distributed-attestation/mh-dev-02.json", text)
        self.assertIn(".astra-state/distributed-attestation/Voktors-Mac-mini.local.json", text)


    def test_reusable_workflow_requires_distinct_node_secrets(self):
        text = WORKFLOW.read_text(encoding="utf-8")
        for secret in (
            "ASTRA_NODE_HMAC_KEY_MH_DEV_01",
            "ASTRA_NODE_HMAC_KEY_MH_DEV_02",
            "ASTRA_NODE_HMAC_KEY_VOKTORS_MAC",
        ):
            self.assertIn(secret, text)
        self.assertNotIn("ASTRA_COMMAND_HMAC_KEY: ${{ secrets.ASTRA_COMMAND_HMAC_KEY }}", text)

    def test_autonomous_and_gold_workflows_use_read_only_token_permissions(self):
        for workflow in (
            ROOT / ".github/workflows/astra-autonomous-supervisor.yml",
            ROOT / ".github/workflows/astra-gold-unified-qualification.yml",
        ):
            text = workflow.read_text(encoding="utf-8")
            self.assertIn("permissions:", text)
            self.assertIn("contents: read", text)
            self.assertNotIn("contents: write", text)

    def test_supervisor_and_unified_gold_bind_execution_head_to_target_sha(self):
        supervisor = (ROOT / ".github/workflows/astra-autonomous-supervisor.yml").read_text(encoding="utf-8")
        unified = (ROOT / ".github/workflows/astra-gold-unified-qualification.yml").read_text(encoding="utf-8")
        self.assertIn('assert d.get("execution_head") == d.get("target_sha")', supervisor)
        self.assertIn('assert d.get("execution_head") == d.get("target_sha")', unified)

    def test_provider_qualification_is_node_local_and_artifact_bound(self):
        provider = ROOT / ".github/workflows/astra-provider-qualification.yml"
        text = provider.read_text(encoding="utf-8")
        self.assertIn("qualify_execution_backends.py --target-sha", text)
        self.assertIn("mediahub-provider", text)
        self.assertIn("astra-provider-qualification-", text)
        self.assertIn("secrets: inherit", SUPERVISOR.read_text(encoding="utf-8"))


    def test_supervisor_defers_result_publication_to_write_boundary(self):
        text = SUPERVISOR.read_text(encoding="utf-8")
        self.assertNotIn("contents: write", text)
        self.assertNotIn("MIMO_API_KEY", text)
        self.assertIn("ASTRA_DEFER_RESULT_PUBLICATION", text)
        self.assertNotIn("astra-node-result-publication.yml", text)

    def test_result_publication_is_separate_workflow_run_boundary(self):
        publication = ROOT / ".github/workflows/astra-node-result-publication.yml"
        text = publication.read_text(encoding="utf-8")
        self.assertIn("workflow_run:", text)
        self.assertIn("Astra autonomous queue supervisor", text)
        self.assertIn("ASTRA GOLD unified autonomous development qualification", text)
        self.assertIn("contents: write", text)
        self.assertIn("actions: read", text)
        self.assertNotIn("MIMO_API_KEY", text)

    def test_supervisor_uses_downloaded_distributed_evidence_root(self):
        text = SUPERVISOR.read_text(encoding="utf-8")
        self.assertIn("ASTRA_DISTRIBUTED_EVIDENCE_DIR=", text)
        self.assertIn("path: .astra-state", text)


if __name__ == "__main__":
    unittest.main()
