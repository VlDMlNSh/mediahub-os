import concurrent.futures
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

from ops.mesh.heartbeat_auth import sign_heartbeat
from ops.mesh.registry import record_heartbeat

KEY = "test-secret"

def base(node="mh-dev-01", sequence=1):
    return {
        "schema_version": "mediahub.mesh.heartbeat.v1",
        "node_id": node,
        "issued_at": datetime.now(timezone.utc).isoformat(),
        "sequence": sequence,
        "runtime_state": "ACTIVE",
        "capability_digest": "a" * 64,
        "resource_summary": {"ram_gib": 8},
    }

class HeartbeatAuthTests(unittest.TestCase):
    def test_valid_heartbeat_and_persisted_sequence(self):
        with tempfile.TemporaryDirectory() as d:
            record = sign_heartbeat(base(), KEY)
            result = record_heartbeat(record, datetime.now(timezone.utc), expected_node_id="mh-dev-01", state_path=d, hmac_key=KEY)
            self.assertTrue(result.accepted)
            replay = record_heartbeat(record, datetime.now(timezone.utc), expected_node_id="mh-dev-01", state_path=d, hmac_key=KEY)
            self.assertFalse(replay.accepted)
            self.assertIn("replay", replay.reason)

    def test_tampering_fails(self):
        record = sign_heartbeat(base(), KEY)
        record["runtime_state"] = "BLOCKED"
        result = record_heartbeat(record, datetime.now(timezone.utc), expected_node_id="mh-dev-01", state_path=tempfile.mkdtemp(), hmac_key=KEY)
        self.assertFalse(result.accepted)
        self.assertIn("signature", result.reason)

    def test_wrong_node_fails(self):
        record = sign_heartbeat(base(node="mh-dev-01"), KEY)
        result = record_heartbeat(record, datetime.now(timezone.utc), expected_node_id="mh-dev-02", state_path=tempfile.mkdtemp(), hmac_key=KEY)
        self.assertFalse(result.accepted)
        self.assertIn("node binding", result.reason)

    def test_stale_fails(self):
        record = base()
        record["issued_at"] = (datetime.now(timezone.utc) - timedelta(seconds=121)).isoformat()
        record = sign_heartbeat(record, KEY)
        result = record_heartbeat(record, datetime.now(timezone.utc), expected_node_id="mh-dev-01", state_path=tempfile.mkdtemp(), hmac_key=KEY)
        self.assertFalse(result.accepted)
        self.assertIn("stale", result.reason)

    def test_missing_key_fails_closed(self):
        record = sign_heartbeat(base(), KEY)
        result = record_heartbeat(record, datetime.now(timezone.utc), expected_node_id="mh-dev-01", state_path=tempfile.mkdtemp(), hmac_key="")
        self.assertFalse(result.accepted)

    def test_retired_node_does_not_mutate_sequence_state(self):
        with tempfile.TemporaryDirectory() as d:
            record = sign_heartbeat(base(sequence=7), KEY)
            result = record_heartbeat(
                record,
                datetime.now(timezone.utc),
                current_status="RETIRED",
                expected_node_id="mh-dev-01",
                state_path=d,
                hmac_key=KEY,
            )
            self.assertFalse(result.accepted)
            self.assertFalse((Path(d) / "mh-dev-01.seq").exists())

    def test_duplicate_sequence_is_single_winner_under_concurrency(self):
        with tempfile.TemporaryDirectory() as d:
            record = sign_heartbeat(base(sequence=11), KEY)

            def submit():
                return record_heartbeat(
                    record,
                    datetime.now(timezone.utc),
                    expected_node_id="mh-dev-01",
                    state_path=d,
                    hmac_key=KEY,
                )

            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                results = list(pool.map(lambda _: submit(), range(8)))

            self.assertEqual(sum(result.accepted for result in results), 1)
            self.assertEqual((Path(d) / "mh-dev-01.seq").read_text(encoding="utf-8").strip(), "11")

if __name__ == "__main__":
    unittest.main()
