import multiprocessing
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock

from mediahub_runtime.agent_fabric import AgentClaim, AgentFabricError, ClaimStore
from mediahub_runtime import autonomous_queue
sys.path.insert(0, "ops/qualification")
import run_distributed_local_worker as local_worker


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

    def test_queue_002_uses_independent_claude_verifier(self):
        import json
        task = json.loads(Path("ops/agent-fabric/tasks/MH25-QUEUE-002.json").read_text(encoding="utf-8"))
        self.assertEqual(task["executor"], "claude")
        self.assertEqual(task["verifier"], "claude")
        self.assertEqual(task["node_id"], "Voktors-Mac-mini.local")
        self.assertTrue(task["independent_verifier_process"])

    def test_remote_worker_artifact_names_match_lane_workflows(self):
        self.assertEqual(autonomous_queue.worker_artifact_names("mh-dev-01", 123), ["astra-distributed-worker-mh-dev-01-claude-123", "astra-distributed-worker-123"])
        self.assertEqual(autonomous_queue.worker_artifact_names("mh-dev-02", 456), ["astra-distributed-worker-mh-dev-02-claude-456", "astra-distributed-worker-456"])
        self.assertEqual(autonomous_queue.worker_artifact_names("Voktors-Mac-mini.local", 789), ["astra-distributed-worker-789"])

    def test_node_runtime_identity_and_mac_fcc_model_bindings_match_workers(self):
        self.assertEqual(local_worker.NODE_CONFIG["mh-dev-01"]["user"], "mediahub-runner")
        self.assertEqual(local_worker.NODE_CONFIG["Voktors-Mac-mini.local"]["model"], "qwen2.5-coder:3b")
        self.assertEqual(local_worker.NODE_CONFIG["Voktors-Mini.Dlink"]["model"], "qwen2.5-coder:3b")

    def test_bounded_markdown_fallback_materializes_only_valid_boundary(self):
        required = ["Voktors-Mac-mini.local", "claude", "qwen2.5-coder:3b", "target-SHA", "fail-closed", "main"]
        output = "```plaintext\n# Executor Lane\nVoktors-Mac-mini.local claude qwen2.5-coder:3b target-SHA fail-closed main\n```"
        with tempfile.TemporaryDirectory() as td, mock.patch.object(local_worker, "ROOT", Path(td)):
            result = local_worker._materialize_bounded_markdown_output(output, "docs/ops/lane.md", required)
            self.assertEqual(result, "docs/ops/lane.md")
            self.assertIn("qwen2.5-coder:3b", (Path(td) / "docs/ops/lane.md").read_text(encoding="utf-8"))
            self.assertIsNone(local_worker._materialize_bounded_markdown_output(output, "../escape.md", required))
            self.assertIsNone(local_worker._materialize_bounded_markdown_output("```text\nnot the required document\n```", "docs/ops/no.md", required))

    def test_claude_executor_uses_real_cli_and_fcc_transport(self):
        source = Path("ops/qualification/run_distributed_local_worker.py").read_text(encoding="utf-8")
        self.assertIn('claude = shutil.which("claude")', source)
        self.assertIn('ANTHROPIC_BASE_URL', source)
        self.assertIn('env["ASTRA_FCC_TRANSPORT"] = "fcc"', source)
        self.assertNotIn('urllib.request.Request(', source)


if __name__ == "__main__":
    unittest.main()
