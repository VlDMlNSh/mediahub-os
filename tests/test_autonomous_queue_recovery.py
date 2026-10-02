import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from mediahub_runtime import autonomous_queue as queue


class AutonomousQueueRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        root = Path(self.tmp.name)
        queue.STATE = root / "queue"
        queue.CLAIMS = queue.STATE / "claims"
        queue.STATE.mkdir(parents=True)
        queue.CLAIMS.mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def _claim(self, status="ACTIVE", expiry=200.0):
        (queue.CLAIMS / "T.json").write_text(json.dumps({
            "agent":"builder","task_id":"T","goal":"test","paths":["src"],
            "exclusive_actions":[],"dependencies":[],"status":status,
            "started":100.0,"updated":100.0,"expiry":expiry,"base_sha":"abc"
        }) + "\\n", encoding="utf-8")

    def _evidence(self):
        d = queue.STATE / "evidence"
        d.mkdir(parents=True)
        (d / "T.json").write_text(json.dumps({"task_id":"T","status":"VERIFIED","head_sha":"def"}) + "\\n", encoding="utf-8")

    def test_verified_evidence_completes_after_claim_release(self):
        self._claim(status="VERIFIED", expiry=200.0)
        self._evidence()
        with mock.patch("mediahub_runtime.autonomous_queue.time.time", return_value=150.0):
            self.assertTrue(queue.completed("T"))

    def test_verified_evidence_completes_after_worker_dies_and_lease_expires(self):
        self._claim(status="ACTIVE", expiry=200.0)
        self._evidence()
        with mock.patch("mediahub_runtime.autonomous_queue.time.time", return_value=201.0):
            self.assertTrue(queue.completed("T"))

    def test_unexpired_active_claim_is_not_complete(self):
        self._claim(status="ACTIVE", expiry=200.0)
        self._evidence()
        with mock.patch("mediahub_runtime.autonomous_queue.time.time", return_value=150.0):
            self.assertFalse(queue.completed("T"))

    def test_corrupt_completed_marker_fails_closed(self):
        d = queue.STATE / "completed"
        d.mkdir(parents=True)
        (d / "T.json").write_text('{"task_id":"T","status":"VERIFIED"}\\n', encoding="utf-8")
        self._claim(status="VERIFIED", expiry=200.0)
        with mock.patch("mediahub_runtime.autonomous_queue.time.time", return_value=150.0):
            self.assertFalse(queue.completed("T"))


if __name__ == "__main__":
    unittest.main()
