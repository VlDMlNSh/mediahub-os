import unittest
from datetime import datetime, timezone, timedelta

from ops.mesh.registry import register_node, record_heartbeat


def node_record(status="DISCOVERED"):
    return {
        "schema_version": "mediahub.mesh.node.v1",
        "node_id": "mh-test-01",
        "role": "worker",
        "status": status,
        "capabilities": [],
        "executors": [],
        "artifact_transports": [],
        "resources": {"ram_gib": 16, "disk_free_gib": 10},
        "last_heartbeat": "2026-10-03T12:00:00+00:00" if status == "ACTIVE" else None,
    }


def heartbeat(node_id="mh-test-01", sequence=1, issued_at=None):
    return {
        "schema_version": "mediahub.mesh.heartbeat.v1",
        "node_id": node_id,
        "issued_at": issued_at or datetime.now(timezone.utc).isoformat(),
        "sequence": sequence,
        "runtime_state": "READY",
        "capability_digest": "a" * 64,
        "resource_summary": {"ram_gib": 16},
    }


class MeshRegistryContractTests(unittest.TestCase):
    def test_register_rejects_duplicate_identity(self):
        result = register_node(node_record(), {"mh-test-01"})
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "duplicate node identity")

    def test_register_rejects_active_node_without_heartbeat(self):
        record = node_record("ACTIVE")
        record["last_heartbeat"] = None
        result = register_node(record)
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "active node requires heartbeat")

    def test_register_accepts_discovered_node_without_heartbeat(self):
        result = register_node(node_record("DISCOVERED"))
        self.assertTrue(result.accepted)

    def test_record_heartbeat_rejects_retired_node(self):
        result = record_heartbeat(
            heartbeat(),
            datetime.now(timezone.utc),
            current_status="RETIRED",
        )
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "retired node cannot reactivate")

    def test_record_heartbeat_rejects_stale_record(self):
        now = datetime.now(timezone.utc)
        result = record_heartbeat(
            heartbeat(issued_at=(now - timedelta(seconds=121)).isoformat()),
            now,
        )
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "heartbeat is stale")

    def test_record_heartbeat_accepts_fresh_record(self):
        now = datetime.now(timezone.utc)
        result = record_heartbeat(heartbeat(issued_at=now.isoformat()), now)
        self.assertTrue(result.accepted)


if __name__ == "__main__":
    unittest.main()
