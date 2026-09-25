import multiprocessing
import sqlite3

import pytest

from runtime.mediahub_control_plane.model import AuditRecord, Event, Execution, LeaseStatus, Task, TaskStatus
from runtime.mediahub_control_plane.service import ControlPlaneService
from runtime.mediahub_control_plane.sqlite_repository import SQLiteControlPlaneRepository


def ready(repo):
    repo.create_task(Task("t", "build", status=TaskStatus.READY, idempotency_key="k", payload={"x": 1}))


def test_state_survives_repository_restart(tmp_path):
    path = tmp_path / "control-plane.db"
    first = SQLiteControlPlaneRepository(path)
    ready(first)
    lease = first.claim_task("t", "agent-a", 7)
    first.append_event(Event("e", "Claimed", 1.0, "task", "t", {"secret": "must-not-be-logged"}))
    first.append_audit(AuditRecord("e", 1.0, "agent-a", "claim", "task", "t", "READY", "CLAIMED", "RECORDED"))
    first = None

    second = SQLiteControlPlaneRepository(path)
    assert second.get_task("t").status is TaskStatus.CLAIMED
    assert second.get_lease_for_task("t").lease_id == lease.lease_id
    assert second.list_tasks()[0].payload == {"x": 1}


def test_claim_is_single_owner_and_idempotency_is_durable(tmp_path):
    path = tmp_path / "control-plane.db"
    repo = SQLiteControlPlaneRepository(path)
    ready(repo)
    repo2 = SQLiteControlPlaneRepository(path)
    with pytest.raises(ValueError):
        repo2.create_task(Task("other", "build", idempotency_key="k"))
    repo.claim_task("t", "agent-a", 1)
    with pytest.raises(ValueError):
        repo2.claim_task("t", "agent-b", 1)


def test_stale_generation_is_fenced_after_restart(tmp_path):
    path = tmp_path / "control-plane.db"
    repo = SQLiteControlPlaneRepository(path)
    ready(repo)
    repo.claim_task("t", "agent-a", 9)
    repo = SQLiteControlPlaneRepository(path)
    with pytest.raises(PermissionError):
        repo.record_execution(Execution("e", "t", "agent-a", 8, "SUCCEEDED"))


def test_event_and_audit_append_are_idempotent(tmp_path):
    repo = SQLiteControlPlaneRepository(tmp_path / "control-plane.db")
    event = Event("e", "X", 1.0, "task", "t")
    audit = AuditRecord("e", 1.0, "x", "claim", "task", "t", "READY", "CLAIMED", "ok")
    assert repo.append_event(event) == event
    assert repo.append_event(event) == event
    assert repo.append_audit(audit) == audit
    assert repo.append_audit(audit) == audit


def _claim_worker(path, agent_id, output):
    repo = SQLiteControlPlaneRepository(path)
    try:
        lease = repo.claim_and_start("t", agent_id, 1)
        output.put((agent_id, "ok", lease.lease_id))
    except ValueError:
        output.put((agent_id, "conflict", None))


def test_claim_and_start_has_single_winner_across_processes(tmp_path):
    path = str(tmp_path / "control-plane.db")
    repo = SQLiteControlPlaneRepository(path)
    ready(repo)
    ctx = multiprocessing.get_context("fork")
    output = ctx.Queue()
    workers = [ctx.Process(target=_claim_worker, args=(path, agent, output)) for agent in ("agent-a", "agent-b")]
    for worker in workers:
        worker.start()
    results = [output.get(timeout=5) for _ in workers]
    for worker in workers:
        worker.join(timeout=5)
    assert sorted(result[1] for result in results) == ["conflict", "ok"]
    assert repo.get_task("t").status is TaskStatus.RUNNING
    assert len(repo.list_leases()) == 1


def test_expire_and_reconcile_is_idempotent_after_restart(tmp_path):
    path = tmp_path / "control-plane.db"
    now = [100.0]
    repo = SQLiteControlPlaneRepository(path, clock=lambda: now[0])
    ready(repo)
    lease = repo.claim_task("t", "agent-a", 1)
    now[0] = lease.expires_at + 1
    event = Event("expiry", "LeaseExpired", now[0], "task", "t", {"agent_id": "agent-a"})
    audit = AuditRecord("expiry", now[0], "reconciler", "LeaseExpired", "task", "t", "RUNNING", "EXPIRED", "RECORDED")
    repo.expire_and_reconcile(lease.lease_id, now[0], event, audit)
    repo = SQLiteControlPlaneRepository(path, clock=lambda: now[0])
    assert repo.get_lease_for_task("t").status is LeaseStatus.EXPIRED
    assert repo.get_task("t").status is TaskStatus.EXPIRED
    repo.expire_and_reconcile(lease.lease_id, now[0], event, audit)
    assert repo.get_task("t").attempt == 1


def test_crash_before_commit_leaves_no_partial_state(tmp_path):
    path = str(tmp_path / "control-plane.db")
    repo = SQLiteControlPlaneRepository(path)
    ready(repo)
    script = "import sqlite3, os; path=os.environ['CP_DB']; db=sqlite3.connect(path,isolation_level=None); db.execute('BEGIN IMMEDIATE'); db.execute(\"UPDATE tasks SET status='RUNNING' WHERE task_id='t'\"); db.execute(\"INSERT INTO leases VALUES('crash-lease','t','agent-a',1,61,1,1,'ACTIVE')\"); os._exit(0)"
    import os, subprocess, sys
    env = dict(os.environ, CP_DB=str(path))
    subprocess.run([sys.executable, "-c", script], env=env, check=True)
    reopened = SQLiteControlPlaneRepository(path)
    assert reopened.get_task("t").status is TaskStatus.READY
    assert reopened.list_leases() == ()


def test_complete_atomic_rolls_back_all_state_on_audit_constraint_failure(tmp_path):
    path = tmp_path / "control-plane.db"
    repo = SQLiteControlPlaneRepository(path)
    ready(repo)
    service = ControlPlaneService(repo)
    lease = service.claim("t", "agent-a", 1)
    execution = Execution("exec", "t", "agent-a", 1, "SUCCEEDED", {"ok": True})
    bad_event = Event("event", None, 1.0, "task", "t")
    bad_audit = AuditRecord("event", 1.0, "agent-a", "complete", "task", "t", "RUNNING", "SUCCEEDED", "RECORDED")
    with pytest.raises(sqlite3.IntegrityError):
        repo.complete_atomic("t", "agent-a", 1, lease.lease_id, execution, bad_event, bad_audit)
    assert repo.get_task("t").status is TaskStatus.RUNNING
    assert repo.get_lease_for_task("t").status.value == "ACTIVE"
    assert repo.list_executions() == ()


def test_reconciler_uses_atomic_expiry_and_schedules_retry(tmp_path):
    from runtime.mediahub_control_plane.reconciler import ControlPlaneReconciler

    now = [100.0]
    repo = SQLiteControlPlaneRepository(tmp_path / "control-plane.db", clock=lambda: now[0])
    repo.create_task(Task("t", "build", status=TaskStatus.READY, max_attempts=2, idempotency_key="k", payload={"x": 1}))
    service = ControlPlaneService(repo)
    lease = service.claim("t", "agent-a", 1)
    expired_at = lease.expires_at + 1
    changed = ControlPlaneReconciler(repo).reconcile_once(now=expired_at)

    task = repo.get_task("t")
    persisted_lease = repo.get_lease_for_task("t")
    assert changed == ("t",)
    assert persisted_lease.status is LeaseStatus.EXPIRED
    assert task.status is TaskStatus.RETRY_WAIT
    assert task.attempt == 1
    assert task.retry_not_before == expired_at + 15.0
    assert len(repo.list_executions()) == 0

    # A second reconciliation cannot re-expire the same lease or increment the attempt.
    changed_again = ControlPlaneReconciler(repo).reconcile_once(now=expired_at + 1)
    assert changed_again == ()
    assert repo.get_task("t").attempt == 1
    assert len(repo.list_executions()) == 0


def test_reconciler_expiry_exhausts_attempts_without_duplicate_execution(tmp_path):
    from runtime.mediahub_control_plane.reconciler import ControlPlaneReconciler

    now = [100.0]
    repo = SQLiteControlPlaneRepository(tmp_path / "control-plane.db", clock=lambda: now[0])
    repo.create_task(Task("t", "build", status=TaskStatus.READY, max_attempts=1, idempotency_key="k", payload={"x": 1}))
    lease = ControlPlaneService(repo).claim("t", "agent-a", 1)
    reconciler = ControlPlaneReconciler(repo)
    reconciler.reconcile_once(now=lease.expires_at + 1)

    assert repo.get_task("t").status is TaskStatus.EXPIRED
    assert repo.get_task("t").attempt == 1
    assert repo.get_lease_for_task("t").status is LeaseStatus.EXPIRED
    assert len(repo.list_executions()) == 0


def test_sqlite_runtime_vertical_slice_is_durable(tmp_path):
    from runtime.mediahub_control_plane.worker import WorkerRuntime
    from runtime.mediahub_control_plane.worker_loop import WorkerLoop

    repo = SQLiteControlPlaneRepository(tmp_path / "control-plane.db")
    service = ControlPlaneService(repo)
    repo.create_task(Task("t", "build", status=TaskStatus.READY, max_attempts=2))
    class Registry:
        def all(self): return ()
        def select(self, task, **kwargs): return None
    class Scheduler:
        max_concurrency_per_agent = 1
        registry = Registry()
        def order_ready(self, tasks): return tuple(tasks)
        def select(self, task, **kwargs):
            from types import SimpleNamespace
            return SimpleNamespace(agent_id="agent-a")

    lease = service.dispatch_once("t", Scheduler(), 7)
    assert lease.agent_id == "agent-a"
    assert repo.get_task("t").status is TaskStatus.RUNNING
    reopened = SQLiteControlPlaneRepository(tmp_path / "control-plane.db")
    loop = WorkerLoop(reopened, WorkerRuntime(ControlPlaneService(reopened)), "agent-a", 7,
                      lambda _: lambda payload, ctx: "ok", lambda _: lambda result: result == "ok")
    assert loop.run(max_polls=1).executed == 1
    final = SQLiteControlPlaneRepository(tmp_path / "control-plane.db")
    assert final.get_task("t").status is TaskStatus.SUCCEEDED
    assert final.get_lease_for_task("t") is None


def test_schema_version_is_fail_closed(tmp_path):
    path = tmp_path / "future.db"
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL)")
    db.execute("INSERT INTO meta VALUES('schema_version','999')")
    db.commit(); db.close()
    with pytest.raises(RuntimeError, match="unsupported control-plane schema"):
        SQLiteControlPlaneRepository(path)


def test_partial_schema_is_fail_closed(tmp_path):
    path = tmp_path / "partial.db"
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE tasks(task_id TEXT PRIMARY KEY)")
    db.commit(); db.close()
    with pytest.raises(RuntimeError, match="schema mismatch"):
        SQLiteControlPlaneRepository(path)


def test_unmarked_but_complete_schema_is_adopted_as_version_one(tmp_path):
    path = tmp_path / "legacy.db"
    db = sqlite3.connect(path)
    db.executescript("""CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE tasks(task_id TEXT PRIMARY KEY, idempotency_key TEXT UNIQUE, type TEXT NOT NULL, payload TEXT, priority INTEGER NOT NULL, status TEXT NOT NULL, dependencies TEXT NOT NULL, attempt INTEGER NOT NULL, max_attempts INTEGER NOT NULL, required_capabilities TEXT NOT NULL, architecture TEXT, retry_not_before REAL);
CREATE TABLE leases(lease_id TEXT PRIMARY KEY, task_id TEXT NOT NULL, agent_id TEXT NOT NULL, created_at REAL NOT NULL, expires_at REAL NOT NULL, last_renewed_at REAL NOT NULL, generation INTEGER NOT NULL, status TEXT NOT NULL);
CREATE TABLE executions(execution_id TEXT PRIMARY KEY, task_id TEXT NOT NULL, agent_id TEXT NOT NULL, lease_generation INTEGER NOT NULL, status TEXT NOT NULL, result TEXT, failure_class TEXT);
CREATE TABLE events(event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL, timestamp REAL NOT NULL, entity_type TEXT NOT NULL, entity_id TEXT NOT NULL, payload TEXT, correlation_id TEXT);
CREATE TABLE audit(event_id TEXT PRIMARY KEY, timestamp REAL NOT NULL, actor TEXT NOT NULL, action TEXT NOT NULL, resource TEXT NOT NULL, resource_id TEXT NOT NULL, previous_state TEXT, new_state TEXT, result TEXT NOT NULL, correlation_id TEXT);""")
    db.commit(); db.close()
    SQLiteControlPlaneRepository(path)
    db = sqlite3.connect(path)
    assert db.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()[0] == '1'
    db.close()
