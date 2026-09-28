import json
import tempfile
import unittest
from pathlib import Path

from ops.qualification.verify_astra_memory_soak import verify


class AstraMemorySoakTests(unittest.TestCase):
    def test_short_or_incomplete_soak_is_blocked(self):
        payload = {
            "schema": "mediahub.astra-memory-soak.v1",
            "status": "PASS",
            "duration_seconds": 3600,
            "checks": {
                "session_continuation": "PASS",
                "project_recall": "PASS",
                "restart_recovery": "PASS",
                "bounded_context": "PASS",
            },
            "restart_count": 1,
            "evidence_digest": "sha256:test",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "soak.json"
            path.write_text(json.dumps(payload))
            result = verify(path)
            self.assertEqual(result["status"], "BLOCKED")
            self.assertIn("duration_below_24h", result["blocked_reasons"])

    def test_complete_fresh_shape_can_be_verified(self):
        payload = {
            "schema": "mediahub.astra-memory-soak.v1",
            "status": "PASS",
            "duration_seconds": 86400,
            "checks": {name: "PASS" for name in (
                "session_continuation", "project_recall",
                "restart_recovery", "bounded_context")},
            "restart_count": 1,
            "evidence_digest": "sha256:test",
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "soak.json"
            path.write_text(json.dumps(payload))
            result = verify(path)
            self.assertEqual(result["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
