from ops.astra_scheduler import Scheduler

SHA = "a" * 40


def test_claim_complete_and_next_task(tmp_path):
    s = Scheduler(tmp_path / "astra.db", lease_seconds=60)
    first = s.enqueue("coding", "do-one", SHA)
    task = s.select()
    lease = s.claim(task, "worker-1")
    next_id = s.generate_next(lease, "reconcile", "next", SHA)
    s.complete(lease, True, "verified")
    assert next_id != first
    assert s.select().task_id == next_id


def test_expired_lease_requeues_with_new_generation(tmp_path):
    s = Scheduler(tmp_path / "astra.db", lease_seconds=1)
    s.enqueue("coding", "do-one", SHA)
    task = s.select()
    lease = s.claim(task, "worker-1", now=100.0)
    assert s.reconcile(now=102.0) == 1
    assert s.select().generation == task.generation + 1
    try:
        s.complete(lease, True, "stale")
    except RuntimeError:
        pass
    else:
        raise AssertionError("stale lease was accepted")


def test_two_consecutive_cycles_without_manual_input(tmp_path):
    s = Scheduler(tmp_path / "astra.db", lease_seconds=60)
    s.enqueue("coding", "cycle-1", SHA)

    def worker(task, lease):
        return True, task.payload

    assert s.run_once("worker-1", worker) == "SUCCEEDED"
    assert s.run_once("worker-1", worker) == "SUCCEEDED"
    rows = s.db.execute(
        "SELECT event FROM events WHERE event IN ('CLAIMED','COMPLETED','ENQUEUED') ORDER BY id"
    ).fetchall()
    assert [r["event"] for r in rows] == [
        "ENQUEUED", "CLAIMED", "ENQUEUED", "COMPLETED",
        "CLAIMED", "ENQUEUED", "COMPLETED",
    ]
