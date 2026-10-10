import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "astra-autonomous-supervisor.yml"


class AstraSupervisorWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = WORKFLOW.read_text(encoding="utf-8")
        start = cls.text.index("      - name: Validate fresh controller result")
        end = cls.text.index("      - name: Stage sanitized controller result", start)
        cls.validator = cls.text[start:end]

    def test_queue_result_supports_nested_autonomous_queue_payload(self):
        self.assertIn('queue=result.get("queue")', self.validator)
        self.assertIn('if not isinstance(queue, dict) or not queue:', self.validator)
        self.assertIn('step.get("autonomous_queue",{}).get("payload")', self.validator)
        self.assertIn('isinstance(step.get("autonomous_queue",{}).get("payload"),dict)', self.validator)

    def test_queue_controller_excludes_its_own_worker_lane_before_finalization(self):
        queue_start = self.text.index("  autonomous-queue:")
        queue_end = self.text.index("  distributed-verification-postqueue:", queue_start)
        queue_job = self.text[queue_start:queue_end]
        self.assertIn("runs-on: [self-hosted, linux, x64, mediahub-control]", queue_job)
        self.assertIn('ASTRA_CONTROLLER_NODE_ID: "mh-dev-01"', queue_job)
        self.assertIn('ASTRA_SINGLE_CONTROLLER_RUN: "0"', queue_job)
        self.assertIn("queue excludes mh-dev-01", queue_job)
        self.assertIn("mediahub_runtime.autonomous_queue", queue_job)
        self.assertIn("validate_autonomous_queue_summary.py", queue_job)
        self.assertIn("astra-autonomous-queue-result-${{ github.run_id }}-${{ github.run_attempt }}", queue_job)
        self.assertIn("  distributed-verification-postqueue:", self.text)
        supervisor = self.text[self.text.index("  supervise:"): ]
        self.assertIn("- autonomous-queue", supervisor)
        self.assertIn("- distributed-verification-postqueue", supervisor)
        self.assertIn("ASTRA_PRECOMPUTED_QUEUE_RESULT_PATH:", supervisor)
        queue_job = self.text[self.text.index("  autonomous-queue:"):self.text.index("  distributed-verification-postqueue:")]
        self.assertIn('ASTRA_SINGLE_CONTROLLER_RUN: "0"', queue_job)
        self.assertNotIn("ASTRA_CONTROLLER_CONCURRENCY_WAIT_SECONDS", queue_job)
        self.assertIn("timeout-minutes: 180", queue_job)

    def test_distributed_evidence_artifacts_are_phase_scoped(self):
        verification = (ROOT / ".github" / "workflows" / "astra-distributed-verification.yml").read_text(encoding="utf-8")
        self.assertIn("evidence_suffix:", verification)
        self.assertIn("astra-distributed-evidence-${{ inputs.evidence_suffix }}-${{ github.run_id }}-${{ github.run_attempt }}", verification)
        self.assertIn("evidence_suffix: prequeue", self.text)
        self.assertIn("evidence_suffix: postqueue", self.text)

    def test_nested_payload_does_not_weaken_fail_closed_admission(self):
        self.assertIn('assert result.get("status") == "PASS"', self.validator)
        self.assertIn('assert queue.get("status") == "PASS"', self.validator)
        self.assertIn('queue_results=queue.get("results")', self.validator)
        self.assertIn('assert isinstance(queue_results, list) and queue_results', self.validator)
        self.assertIn('assert all(isinstance(item, dict) and item.get("status") == "VERIFIED" for item in queue_results)', self.validator)
        self.assertIn('assert d.get("target_sha") == os.environ["GITHUB_SHA"]', self.validator)
        self.assertIn('assert d.get("execution_head") == d.get("target_sha")', self.validator)


    def test_mh_dev_01_worker_installs_pinned_claude_cli_for_runner_account(self):
        worker = (ROOT / ".github" / "workflows" / "astra-distributed-local-worker.yml").read_text(encoding="utf-8")
        job_start = worker.index("  mh-dev-01-claude:")
        job_end = worker.index("  mh-dev-02:", job_start)
        job = worker[job_start:job_end]
        node_pos = job.index("Set up Node.js for Claude Code installation")
        install_pos = job.index("Install pinned Claude Code CLI for the runner account")
        admission_pos = job.index("- name: Canonical admission")
        self.assertLess(node_pos, install_pos)
        self.assertLess(install_pos, admission_pos)
        self.assertIn("uses: actions/setup-node@v7", job)
        self.assertIn('node-version: "24"', job)
        self.assertIn("package-manager-cache: false", job)
        self.assertIn('CLAUDE_CODE_VERSION: "2.1.296"', job)
        self.assertIn('echo "$install_dir" >> "$GITHUB_PATH"', job)
        self.assertIn('npm install --global --prefix "$install_prefix"', job)
        self.assertIn('"@anthropic-ai/claude-code@$CLAUDE_CODE_VERSION"', job)
        self.assertIn('test -x "$install_dir/claude"', job)
        self.assertIn('"$install_dir/claude" --version | grep -F "$CLAUDE_CODE_VERSION"', job)
        self.assertNotIn("claude.ai/install.sh", job)



    def test_mh_dev_01_worker_fails_fast_when_fcc_file_is_unreadable_without_reading_it(self):
        worker = (ROOT / ".github" / "workflows" / "astra-distributed-local-worker.yml").read_text(encoding="utf-8")
        job_start = worker.index("  mh-dev-01-claude:")
        job_end = worker.index("  mh-dev-02:", job_start)
        job = worker[job_start:job_end]
        access_pos = job.index("Verify runner-scoped FCC credential access")
        install_pos = job.index("Install pinned Claude Code CLI for the runner account")
        self.assertLess(access_pos, install_pos)
        self.assertIn('[[ ! -f "$ASTRA_FCC_ENV_FILE" || ! -r "$ASTRA_FCC_ENV_FILE" ]]', job)
        self.assertIn('"fcc_env_file_readable": readable', job)
        self.assertIn('"fcc_env_file_readable": bool(os.environ.get("ASTRA_FCC_ENV_FILE"))', job)
        self.assertNotIn('cat "$ASTRA_FCC_ENV_FILE"', job)
        self.assertNotIn('read_text(encoding="utf-8")', job)



if __name__ == "__main__":
    unittest.main()
