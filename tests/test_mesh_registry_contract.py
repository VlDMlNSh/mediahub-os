import unittest
from tempfile import TemporaryDirectory
from datetime import datetime, timezone, timedelta

from ops.mesh.registry import register_node, record_heartbeat
from ops.mesh.heartbeat_auth import sign_heartbeat


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
    return sign_heartbeat({
        "schema_version": "mediahub.mesh.heartbeat.v1",
        "node_id": node_id,
        "issued_at": issued_at or datetime.now(timezone.utc).isoformat(),
        "sequence": sequence,
        "runtime_state": "READY",
        "capability_digest": "a" * 64,
        "resource_summary": {"ram_gib": 16},
    }, "test-key")


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
        with TemporaryDirectory() as d:
            result = record_heartbeat(
                heartbeat(),
                datetime.now(timezone.utc),
                current_status="RETIRED", expected_node_id="mh-test-01", hmac_key="test-key", state_path=d,
            )
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "retired node cannot reactivate")

    def test_record_heartbeat_rejects_stale_record(self):
        now = datetime.now(timezone.utc)
        with TemporaryDirectory() as d:
            result = record_heartbeat(
                heartbeat(issued_at=(now - timedelta(seconds=121)).isoformat()),
                now, expected_node_id="mh-test-01", hmac_key="test-key", state_path=d,
            )
        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "heartbeat is stale")

    def test_record_heartbeat_accepts_fresh_record(self):
        now = datetime.now(timezone.utc)
        with TemporaryDirectory() as d:
            result = record_heartbeat(heartbeat(issued_at=now.isoformat()), now, expected_node_id="mh-test-01", hmac_key="test-key", state_path=d)
            self.assertTrue(result.accepted)


class AstraPublishBranchContractTests(unittest.TestCase):
    def test_publish_branch_uses_remote_tip_without_force_push(self):
        from unittest.mock import patch
        import astra_github_agent as agent

        class Proc:
            def __init__(self, returncode=0, stdout="", stderr=""):
                self.returncode=returncode; self.stdout=stdout; self.stderr=stderr
            def check_returncode(self):
                if self.returncode: raise RuntimeError(self.stderr)

        calls=[]
        def fake_run(argv, timeout=120):
            calls.append(argv)
            if argv[:2] == ["git", "ls-remote"]:
                return Proc(stdout="abc\trefs/heads/astra-node/mh-test-01\n")
            return Proc()

        with patch.object(agent, "NODE_ID", "mh-test-01"), patch.object(agent, "run", side_effect=fake_run):
            agent._prepare_publish_branch()

        self.assertIn(["git", "fetch", "origin", "astra-node/mh-test-01:refs/remotes/origin/astra-node/mh-test-01"], calls)
        self.assertIn(["git", "checkout", "--detach", "origin/astra-node/mh-test-01"], calls)
        self.assertNotIn("--force", sum(calls, []))


if __name__ == "__main__":
    unittest.main()
