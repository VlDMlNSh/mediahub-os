"""Contracts for conservative adoption of mature agent-runtime patterns."""
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AstraReferenceArchitectureSyncTests(unittest.TestCase):
    def test_reference_design_records_verified_upstream_sources(self):
        doc = (ROOT / "docs/operations/ASTRA-REFERENCE-ARCHITECTURE-SYNCHRONIZATION.md").read_text(encoding="utf-8")
        for upstream in (
            "OpenHands", "SWE-agent", "LangGraph", "Temporal Python SDK",
            "Microsoft Agent Framework",
        ):
            self.assertIn(upstream, doc)
        for invariant in (
            "Astra does not record such provenance",
            "Recover before retry",
            "Fenced lease",
            "Restricted execution",
            "24-hour GOLD soak remains separate",
        ):
            self.assertIn(invariant, doc)

    def test_unqualified_reference_designs_are_not_registered_as_pass(self):
        registry = (ROOT / "docs/operations/ASTRA-AUTHORIZED-EXECUTION-SCHEMES.md").read_text(encoding="utf-8")
        self.assertIn("NONE CERTIFIED", registry)
        self.assertNotIn("AUTHORIZED / QUALIFICATION PENDING", registry)
        self.assertIn("a candidate topology", registry)

    def test_supervisor_serializes_controller_runs_across_target_shas(self):
        workflow = (ROOT / ".github/workflows/astra-autonomous-supervisor.yml").read_text(encoding="utf-8")
        self.assertIn("astra-autonomous-supervisor-v3-${{ github.repository }}", workflow)
        self.assertIn("cancel-in-progress: false", workflow)
        self.assertNotIn("astra-autonomous-supervisor-v2-${{ github.sha }}", workflow)

    def test_supervisor_requires_persistent_writable_claim_store(self):
        workflow = (ROOT / ".github/workflows/astra-autonomous-supervisor.yml").read_text(encoding="utf-8")
        self.assertIn('ASTRA_QUEUE_STATE_DIR: "/var/lib/mediahub-astra/queue"', workflow)
        self.assertIn('test -d "$ASTRA_QUEUE_STATE_DIR/claims"', workflow)
        self.assertIn('probe="$ASTRA_QUEUE_STATE_DIR/claims/.astra-write-probe-', workflow)
        self.assertIn('trap \'rm -f "$probe"\' EXIT', workflow)

    def test_agent_tools_do_not_expose_general_shell_or_python(self):
        worker = (ROOT / "ops/qualification/run_distributed_local_worker.py").read_text(encoding="utf-8")
        self.assertIn('tools_mode: str = "Read,Edit"', worker)
        self.assertIn('max_turns=2, tools_mode="Read"', worker)
        self.assertNotIn('"Bash(python *)"', worker)
        self.assertNotIn('"Bash(git *)"', worker)


if __name__ == "__main__":
    unittest.main()
