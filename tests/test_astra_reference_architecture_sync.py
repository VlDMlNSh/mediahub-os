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


if __name__ == "__main__":
    unittest.main()
