import tempfile
import unittest
from pathlib import Path
from unittest import mock

from mediahub_runtime.agent_fabric import AgentClaim, AgentFabricError, ClaimStore


def mk(task_id, paths, now=100.0):
    return AgentClaim("builder", task_id, "test", tuple(paths), (), (), "ACTIVE", now, now, now + 900, "base")


class AgentFabricTests(unittest.TestCase):
    def test_exact_collision(self):
        with tempfile.TemporaryDirectory() as td, mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
            s = ClaimStore(Path(td))
            s.acquire(mk("A", ["src/a.py"]))
            with self.assertRaisesRegex(AgentFabricError, "claim_collision"):
                s.acquire(mk("B", ["src/a.py"]))

    def test_parent_child_collision(self):
        with tempfile.TemporaryDirectory() as td, mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
            s = ClaimStore(Path(td))
            s.acquire(mk("A", ["src"]))
            with self.assertRaisesRegex(AgentFabricError, "claim_collision"):
                s.acquire(mk("B", ["src/a.py"]))

    def test_max_two_active_claims(self):
        with tempfile.TemporaryDirectory() as td, mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
            s = ClaimStore(Path(td))
            s.acquire(mk("A", ["src/a.py"]))
            s.acquire(mk("B", ["src/b.py"]))
            with self.assertRaisesRegex(AgentFabricError, "claim_capacity_exceeded"):
                s.acquire(mk("C", ["src/c.py"]))

    def test_heartbeat(self):
        with tempfile.TemporaryDirectory() as td, mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
            s = ClaimStore(Path(td))
            s.acquire(mk("A", ["src/a.py"]))
            c = s.heartbeat("A", now=200.0, lease_seconds=300)
            self.assertEqual((c.status, c.expiry), ("ACTIVE", 500.0))

    def test_release(self):
        with tempfile.TemporaryDirectory() as td, mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
            s = ClaimStore(Path(td))
            s.acquire(mk("A", ["src/a.py"]))
            s.release("A")
            self.assertEqual(s.list_claims()[0].status, "CLOSED")

    def test_lease_expiry_allows_reacquire(self):
        with tempfile.TemporaryDirectory() as td:
            s = ClaimStore(Path(td))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
                s.acquire(mk("A", ["src/a.py"], now=100.0))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=1000.0):
                s.acquire(mk("B", ["src/a.py"], now=1000.0))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=1000.0):
                claims = {c.task_id: c for c in s.list_claims()}
            self.assertEqual(claims["A"].status, "EXPIRED")
            self.assertEqual(claims["B"].status, "ACTIVE")

    def test_expired_same_task_claim_can_be_reclaimed(self):
        with tempfile.TemporaryDirectory() as td:
            s = ClaimStore(Path(td))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
                s.acquire(mk("A", ["src/a.py"], now=100.0))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=1000.0):
                s.acquire(mk("A", ["src/a.py"], now=1000.0))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=1000.0):
                c = {claim.task_id: claim for claim in s.list_claims()}
            self.assertEqual(c["A"].status, "ACTIVE")
            self.assertEqual(c["A"].expiry, 1900.0)


if __name__ == "__main__":
    unittest.main()
