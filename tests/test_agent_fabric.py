import multiprocessing
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from mediahub_runtime.agent_fabric import AgentClaim, AgentFabricError, ClaimStore


def mk(task_id, paths, now=100.0):
    return AgentClaim("builder", task_id, "test", tuple(paths), (), (), "ACTIVE", now, now, now + 900, "base")


def _concurrent_acquire_worker(root, task_id, barrier, results):
    try:
        store = ClaimStore(Path(root))
        barrier.wait(timeout=10)
        now = time.time()
        store.acquire(mk(task_id, ["src/shared.py"], now=now))
    except AgentFabricError as exc:
        results.put((task_id, "collision", str(exc)))
    except Exception as exc:
        results.put((task_id, "error", repr(exc)))
    else:
        results.put((task_id, "acquired", ""))


def _concurrent_heartbeat_worker(root, barrier, results):
    try:
        barrier.wait(timeout=10)
        ClaimStore(Path(root)).heartbeat("A", lease_seconds=300)
    except AgentFabricError as exc:
        results.put(("heartbeat", "rejected", str(exc)))
    except Exception as exc:
        results.put(("heartbeat", "error", repr(exc)))
    else:
        results.put(("heartbeat", "updated", ""))


def _concurrent_recovery_release_worker(root, barrier, results):
    try:
        store = ClaimStore(Path(root))
        barrier.wait(timeout=10)
        store.release_quarantined_if_matches(
            "A", expected_run_id="123456",
            expected_identity={"command_id": "CMD-1", "node_id": "node-1", "executor": "claude"},
        )
    except AgentFabricError as exc:
        results.put(("recovery", "rejected", str(exc)))
    except Exception as exc:
        results.put(("recovery", "error", repr(exc)))
    else:
        results.put(("recovery", "released", ""))


def _concurrent_release_worker(root, barrier, results):
    try:
        barrier.wait(timeout=10)
        ClaimStore(Path(root)).release("A", "CLOSED")
    except Exception as exc:
        results.put(("release", "error", repr(exc)))
    else:
        results.put(("release", "closed", ""))


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

    def test_expired_same_task_can_reacquire(self):
        with tempfile.TemporaryDirectory() as td:
            s = ClaimStore(Path(td))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
                s.acquire(mk("A", ["src/a.py"], now=100.0))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=1000.0):
                s.acquire(mk("A", ["src/a.py"], now=1000.0))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=1000.0):
                claims = s.list_claims()
            self.assertEqual(len(claims), 1)
            self.assertEqual((claims[0].status, claims[0].base_sha), ("ACTIVE", "base"))

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

    def test_concurrent_overlapping_acquire_allows_only_one(self):
        if "fork" not in multiprocessing.get_all_start_methods():
            self.skipTest("concurrent claim regression requires fork-capable workers")
        ctx = multiprocessing.get_context("fork")
        with tempfile.TemporaryDirectory() as td:
            barrier = ctx.Barrier(2)
            results = ctx.Queue()
            workers = [
                ctx.Process(target=_concurrent_acquire_worker, args=(td, task_id, barrier, results))
                for task_id in ("A", "B")
            ]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join(15)
            self.assertTrue(all(not worker.is_alive() for worker in workers))
            outcomes = [results.get(timeout=5) for _ in workers]
            self.assertEqual(sorted(outcome[1] for outcome in outcomes), ["acquired", "collision"])
            self.assertEqual({outcome[2] for outcome in outcomes if outcome[1] == "collision"}, {"claim_collision"})

    def test_concurrent_heartbeat_and_release_cannot_resurrect_closed_claim(self):
        if "fork" not in multiprocessing.get_all_start_methods():
            self.skipTest("concurrent claim regression requires fork-capable workers")
        ctx = multiprocessing.get_context("fork")
        with tempfile.TemporaryDirectory() as td:
            store = ClaimStore(Path(td))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
                store.acquire(mk("A", ["src/a.py"]))
            barrier = ctx.Barrier(2)
            results = ctx.Queue()
            workers = [
                ctx.Process(target=_concurrent_heartbeat_worker, args=(td, barrier, results)),
                ctx.Process(target=_concurrent_release_worker, args=(td, barrier, results)),
            ]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join(15)
            self.assertTrue(all(not worker.is_alive() for worker in workers))
            outcomes = [results.get(timeout=5) for _ in workers]
            self.assertNotIn("error", [outcome[1] for outcome in outcomes])
            self.assertEqual(store.list_claims()[0].status, "CLOSED")

    def test_queue_002_uses_independent_claude_verifier(self):
        import json
        task = json.loads(Path("ops/agent-fabric/tasks/MH25-QUEUE-002.json").read_text(encoding="utf-8"))
        self.assertEqual(task["executor"], "claude")
        self.assertEqual(task["verifier"], "claude")
        self.assertEqual(task["node_id"], "Voktors-Mac-mini.local")
        self.assertTrue(task["independent_verifier_process"])

    def test_claude_executor_uses_real_cli_and_fcc_transport(self):
        source = Path("ops/qualification/run_distributed_local_worker.py").read_text(encoding="utf-8")
        self.assertIn('claude = shutil.which("claude")', source)
        self.assertIn('ANTHROPIC_BASE_URL', source)
        self.assertIn('env["ASTRA_FCC_TRANSPORT"] = "fcc"', source)
        self.assertNotIn('urllib.request.Request(', source)


    def test_quarantined_claim_never_expires_or_allows_overlap_reacquire(self):
        with tempfile.TemporaryDirectory() as td:
            store = ClaimStore(Path(td))
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=100.0):
                store.acquire(mk("A", ["src/shared.py"], now=100.0))
                store.quarantine("A", "worker status unknown")
            with mock.patch("mediahub_runtime.agent_fabric.time.time", return_value=10_000_000.0):
                claims = store.list_claims()
                self.assertEqual(claims[0].status, "QUARANTINED")
                with self.assertRaisesRegex(AgentFabricError, "claim_collision"):
                    store.acquire(mk("B", ["src/shared.py"], now=10_000_000.0))
                with self.assertRaisesRegex(AgentFabricError, "claim_exists"):
                    store.acquire(mk("A", ["src/shared.py"], now=10_000_000.0))

    def test_quarantined_claim_can_only_be_released_explicitly(self):
        with tempfile.TemporaryDirectory() as td:
            store = ClaimStore(Path(td))
            store.acquire(mk("A", ["src/a.py"], now=time.time()))
            store.quarantine("A", "cancel status unknown")
            with self.assertRaisesRegex(AgentFabricError, "quarantined_claim_requires_remote_terminal_confirmation"):
                store.release("A", "REJECTED")
            store.release("A", "REJECTED", remote_terminal_confirmed=True)
            self.assertEqual(store.list_claims()[0].status, "REJECTED")


    def test_conditional_recovery_release_rejects_stale_identity(self):
        with tempfile.TemporaryDirectory() as td:
            store = ClaimStore(Path(td))
            claim = AgentClaim("builder", "A", "test", ("src/a.py",), (), (), "ACTIVE", time.time(), time.time(), time.time() + 1000, "base", command_id="CMD-1", node_id="node-1", executor="claude")
            store.acquire(claim)
            store.set_worker_run_id("A", "123456")
            store.quarantine("A", "unknown")
            with self.assertRaisesRegex(AgentFabricError, "claim_worker_run_id_changed"):
                store.release_quarantined_if_matches("A", expected_run_id="654321", expected_identity={"command_id": "CMD-1", "node_id": "node-1", "executor": "claude"})
            with self.assertRaisesRegex(AgentFabricError, "claim_worker_identity_changed"):
                store.release_quarantined_if_matches("A", expected_run_id="123456", expected_identity={"command_id": "CMD-1", "node_id": "node-2", "executor": "claude"})
            self.assertEqual(store.get_claim("A").status, "QUARANTINED")

    def test_concurrent_recovery_release_is_compare_and_swap(self):
        if "fork" not in multiprocessing.get_all_start_methods():
            self.skipTest("concurrent claim regression requires fork-capable workers")
        ctx = multiprocessing.get_context("fork")
        with tempfile.TemporaryDirectory() as td:
            store = ClaimStore(Path(td))
            claim = AgentClaim("builder", "A", "test", ("src/a.py",), (), (), "ACTIVE", time.time(), time.time(), time.time() + 1000, "base", command_id="CMD-1", node_id="node-1", executor="claude")
            store.acquire(claim)
            store.set_worker_run_id("A", "123456")
            store.quarantine("A", "unknown")
            barrier = ctx.Barrier(2)
            results = ctx.Queue()
            workers = [ctx.Process(target=_concurrent_recovery_release_worker, args=(td, barrier, results)) for _ in range(2)]
            for worker in workers:
                worker.start()
            for worker in workers:
                worker.join(15)
            self.assertTrue(all(not worker.is_alive() for worker in workers))
            outcomes = [results.get(timeout=5) for _ in workers]
            self.assertEqual(sorted(outcome[1] for outcome in outcomes), ["rejected", "released"])
            self.assertEqual(store.get_claim("A").status, "REJECTED")

    def test_atomic_claim_json_write_cleans_temp_and_persists_valid_json(self):
        import json
        with tempfile.TemporaryDirectory() as td:
            store = ClaimStore(Path(td))
            store.acquire(mk("A", ["src/a.py"], now=time.time()))
            store.quarantine("A", "worker state unknown")
            self.assertEqual(store.get_claim("A").status, "QUARANTINED")
            self.assertEqual(list(Path(td).glob("*.tmp")), [])
            self.assertEqual(json.loads((Path(td) / "A.json").read_text(encoding="utf-8"))["status"], "QUARANTINED")

    def test_worker_run_id_is_persisted_for_recovery(self):
        with tempfile.TemporaryDirectory() as td:
            store = ClaimStore(Path(td))
            store.acquire(mk("A", ["src/a.py"], now=time.time()))
            claim = store.set_worker_run_id("A", "123456")
            self.assertEqual(claim.worker_run_id, "123456")
            with self.assertRaisesRegex(AgentFabricError, "invalid_worker_run_id"):
                store.set_worker_run_id("A", "not-a-run-id")


    def test_recovery_run_id_persistence_is_compare_and_swap_on_quarantined_identity(self):
        with tempfile.TemporaryDirectory() as td:
            store = ClaimStore(Path(td))
            claim = AgentClaim(
                "builder", "A", "test", ("src/a.py",), (), (), "ACTIVE",
                100.0, 100.0, 1000.0, "base", command_id="CMD-1",
                node_id="node-1", executor="claude",
            )
            store.acquire(claim)
            store.quarantine("A", "unknown")
            identity = {"command_id": "CMD-1", "node_id": "node-1", "executor": "claude"}
            saved = store.set_worker_run_id_if_quarantined_matches(
                "A", "123456", expected_identity=identity
            )
            self.assertEqual(saved.worker_run_id, "123456")
            with self.assertRaisesRegex(AgentFabricError, "claim_worker_run_id_changed"):
                store.set_worker_run_id_if_quarantined_matches(
                    "A", "999999", expected_identity=identity
                )
            with self.assertRaisesRegex(AgentFabricError, "claim_worker_identity_changed"):
                store.set_worker_run_id_if_quarantined_matches(
                    "A", "123456", expected_identity={
                        "command_id": "CMD-OTHER", "node_id": "node-1", "executor": "claude"
                    }
                )
            self.assertEqual(store.get_claim("A").worker_run_id, "123456")


    def test_recovery_run_id_persistence_is_compare_and_swap_on_quarantined_identity(self):
        with tempfile.TemporaryDirectory() as td:
            store = ClaimStore(Path(td))
            now = time.time()
            claim = AgentClaim(
                "builder", "A", "test", ("src/a.py",), (), (), "ACTIVE",
                now, now, now + 1000, "base", command_id="CMD-1",
                node_id="node-1", executor="claude",
            )
            store.acquire(claim)
            store.quarantine("A", "unknown")
            identity = {"command_id": "CMD-1", "node_id": "node-1", "executor": "claude"}
            saved = store.set_worker_run_id_if_quarantined_matches(
                "A", "123456", expected_identity=identity
            )
            self.assertEqual(saved.worker_run_id, "123456")
            with self.assertRaisesRegex(AgentFabricError, "claim_worker_run_id_changed"):
                store.set_worker_run_id_if_quarantined_matches(
                    "A", "999999", expected_identity=identity
                )
            with self.assertRaisesRegex(AgentFabricError, "claim_worker_identity_changed"):
                store.set_worker_run_id_if_quarantined_matches(
                    "A", "123456", expected_identity={
                        "command_id": "CMD-OTHER", "node_id": "node-1", "executor": "claude"
                    }
                )
            self.assertEqual(store.get_claim("A").worker_run_id, "123456")


if __name__ == "__main__":
    unittest.main()
