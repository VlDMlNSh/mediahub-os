import hashlib
import hmac
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

if __name__ == "__main__":
    unittest.main()
