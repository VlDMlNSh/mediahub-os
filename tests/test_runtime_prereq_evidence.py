import json
import tempfile
import unittest
from pathlib import Path

from ops.qualification import produce_runtime_prereq_evidence as producer

ARTIFACTS = ("scheduler-e2e.json", "fencing.json", "recovery.json", "backup-restore.json")


class RuntimePrereqEvidenceTests(unittest.TestCase):
    def test_every_module_observation_holds(self):
        for name, (_check, run) in producer.CHECKS.items():
            observations = run()
            self.assertTrue(observations, name)
            self.assertTrue(all(observations.values()), f"{name}: {observations}")

    def test_non_canonical_context_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = producer.build(Path(tmp), node="not-mh-dev-01")
            for name, item in summary.items():
                self.assertEqual(item["status"], "BLOCKED", name)
                self.assertEqual(item["reason"], "non_canonical_context", name)
                self.assertTrue(all(item["observations"].values()), name)

    def test_canonical_context_reports_pass_with_digests(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            summary = producer.build(out, node=producer.CANONICAL_NODE)
            self.assertEqual(sorted(summary), sorted(ARTIFACTS))
            for name in ARTIFACTS:
                self.assertEqual(summary[name]["status"], "PASS", name)
                payload = json.loads((out / name).read_text(encoding="utf-8"))
                self.assertEqual(payload["status"], "PASS")
                self.assertTrue(payload["evidence_digest"].startswith("sha256:"))
                self.assertEqual(payload["secret_values"], "SUPPRESSED")
                self.assertTrue(payload["canonical_node"])
                self.assertTrue(payload["requires_live_integration"])


if __name__ == "__main__":
    unittest.main()
