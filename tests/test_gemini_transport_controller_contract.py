"""Static tests for explicit, token-backed GitHub API Gemini dispatch."""
from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".github/workflows/gemini-batch-dispatch-controller.yml"
CHILDREN = (
    ("gemini-autonomous-engineering.yml", "GEMINI_API_KEY"),
    ("gemini-agent-2.yml", "GEMINI_API_KEY_2"),
    ("gemini-agent-3.yml", "GEMINI_API_KEY_3"),
)


class GeminiTransportControllerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = WORKFLOW_PATH.read_text(encoding="utf-8")
        cls.workflow = yaml.load(cls.source, Loader=yaml.BaseLoader)
        cls.child_sources = [(name, (ROOT / ".github/workflows" / name).read_text(encoding="utf-8"), secret) for name, secret in CHILDREN]

    def test_explicit_confirmation_and_nonlaunching_default(self):
        dispatch = self.workflow["on"]["workflow_dispatch"]
        self.assertEqual(dispatch["inputs"]["mode"]["default"], "probe")
        self.assertEqual(dispatch["inputs"]["mode"]["options"], ["probe", "agents"])
        self.assertEqual(dispatch["inputs"]["confirm"]["type"], "choice")
        self.assertEqual(dispatch["inputs"]["confirm"]["options"], ["no", "yes"])
        self.assertEqual(dispatch["inputs"]["confirm"]["default"], "no")
        self.assertEqual(self.workflow["permissions"], {})
        condition = self.workflow["jobs"]["dispatch_and_monitor"]["if"].replace(" ", "")
        self.assertIn("github.event_name=='workflow_dispatch'", condition)
        self.assertIn("github.ref=='refs/heads/main'", condition)
        self.assertIn("inputs.mode=='agents'", condition)
        self.assertIn("inputs.confirm=='yes'", condition)

    def test_controller_uses_transport_token_only_for_api_dispatch(self):
        self.assertIn("secrets.MEDIAHUB_GITHUB_TOKEN", self.source)
        self.assertIn("api.github.com", self.source)
        self.assertIn("/actions/workflows/{wf}/dispatches", self.source)
        self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", self.source)
        self.assertNotIn("secrets: inherit", self.source)
        for _, source, _ in self.child_sources:
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)

    def test_fixed_three_workflows_receive_same_target_sha(self):
        for filename, _ in CHILDREN:
            self.assertIn(filename, self.source)
        self.assertIn("target=ref[\"object\"][\"sha\"]", self.source)
        self.assertIn('"target_sha":target', self.source)
        self.assertIn("target_sha", self.source)
        self.assertIn("Shared immutable target SHA", self.source)

    def test_hmac_and_run_monitoring_fail_closed(self):
        self.assertIn("hmac.new", self.source)
        self.assertIn("hashlib.sha256", self.source)
        self.assertIn("NOT_COMPLETED_BEFORE_TIMEOUT", self.source)
        self.assertIn('results.get(j["id"],{}).get("conclusion")!="success"', self.source)
        self.assertNotIn("secrets: inherit", self.source)

    def test_child_provider_keys_are_separate_and_explicit(self):
        for _, source, secret in self.child_sources:
            self.assertIn(secret, source)
            self.assertIn("secrets.MEDIAHUB_DISPATCH_HMAC_KEY", source)
            self.assertNotIn("MEDIAHUB_GITHUB_TOKEN", source)
            self.assertIn("needs.authorize_dispatch.result == 'success'", source)

    def test_partial_dispatch_is_recorded_and_accepted_children_are_reconciled(self):
        # Every attempt is recorded before POST; individual failures must not
        # abort the loop before accepted children are monitored and summarized.
        self.assertIn('job={"workflow":wf,"id":did,"dispatch_status":"PENDING"}; jobs.append(job)', self.source)
        self.assertIn('except Exception as exc:', self.source)
        self.assertIn('job["dispatch_status"]="UNKNOWN"', self.source)
        self.assertIn("code != 408", self.source)
        self.assertIn('pending={j["id"]:j for j in jobs if j["dispatch_status"] in ("ACCEPTED","UNKNOWN")}', self.source)
        self.assertIn('job["dispatch_status"]="UNKNOWN"', self.source)
        self.assertIn('job["dispatch_status"]="FAILED"', self.source)
        self.assertIn('Dispatch outcome unknown', self.source)
        self.assertIn('if code is not None and 400 <= code < 500 and code != 408:', self.source)
        self.assertIn('results[did]={"status":"DISPATCH_FAILED","conclusion":"failure"}', self.source)
        self.assertIn('Dispatch | Run ID | Conclusion', self.source)
        self.assertIn('len(jobs)!=3', self.source)
        self.assertIn('j["dispatch_status"]!="ACCEPTED"', self.source)
        self.assertIn('error_type={type(exc).__name__}', self.source)
        self.assertNotIn('print(exc)', self.source)


    def test_owner_only_next_comment_bridge_is_scoped_and_idempotent(self):
        event = self.workflow["on"]["issue_comment"]
        self.assertEqual(event["types"], ["created"])
        condition = self.workflow["jobs"]["dispatch_and_monitor"]["if"]
        self.assertIn("github.event.issue.number == 301", condition)
        self.assertIn("github.event.issue.pull_request == null", condition)
        self.assertIn("github.event.comment.body == '/next'", condition)
        self.assertIn("github.event.comment.author_association == 'OWNER'", condition)
        self.assertIn('SOURCE_COMMENT_ID: ${{ github.event.comment.id }}', self.source)
        self.assertIn('CURRENT_RUN_ID: ${{ github.run_id }}', self.source)
        self.assertIn('This /next comment already has a controller run; duplicate dispatch suppressed.', self.source)
        self.assertIn('if source_comment_id:', self.source)

    def test_batch_admission_flag_defaults_closed(self):
        gate = self.workflow["jobs"]["readiness_gate"]
        self.assertEqual(gate["permissions"], {})
        self.assertIn("MEDIAHUB_GEMINI_BATCH_ENABLED", self.source)
        self.assertIn('BATCH_ENABLED: ${{ vars.MEDIAHUB_GEMINI_BATCH_ENABLED }}', self.source)
        self.assertIn('needs: readiness_gate', self.source)
        condition = self.workflow["jobs"]["dispatch_and_monitor"]["if"]
        self.assertIn("needs.readiness_gate.outputs.enabled == 'true'", condition)
        self.assertIn('no child dispatch will occur', self.source)

if __name__ == "__main__":
    unittest.main()
