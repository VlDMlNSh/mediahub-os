import multiprocessing

import pytest

from ops.ai.task_lease import LeaseDenied, TaskLease


def test_lease_is_exclusive(tmp_path):
    path = tmp_path / "leases" / "task.lock"
    first = TaskLease(path, "task-1", "worker-a", ttl_seconds=60)
    first.acquire()
    second = TaskLease(path, "task-1", "worker-b", ttl_seconds=60)
    with pytest.raises(LeaseDenied):
        second.acquire()
    first.release()
    second.acquire()
    second.release()


def test_lease_persists_identity_while_held(tmp_path):
    path = tmp_path / "leases" / "task.lock"
    lease = TaskLease(path, "task-7", "worker-7", ttl_seconds=60)
    lease.acquire()
    data = path.read_text(encoding="utf-8")
    assert '"task_id": "task-7"' in data
    assert '"worker_id": "worker-7"' in data
    lease.release()


def _hold_lease(path: str, ready: multiprocessing.Queue, release: multiprocessing.Event) -> None:
    lease = TaskLease(__import__("pathlib").Path(path), "task-x", "worker-child", ttl_seconds=60)
    lease.acquire()
    ready.put(True)
    release.wait(5)
    lease.release()


def test_lease_is_exclusive_across_processes(tmp_path):
    path = tmp_path / "leases" / "process.lock"
    ready: multiprocessing.Queue = multiprocessing.Queue()
    release = multiprocessing.Event()
    process = multiprocessing.Process(target=_hold_lease, args=(str(path), ready, release))
    process.start()
    assert ready.get(timeout=5) is True
    try:
        with pytest.raises(LeaseDenied):
            TaskLease(path, "task-x", "worker-parent", ttl_seconds=60).acquire()
    finally:
        release.set()
        process.join(timeout=5)
    assert process.exitcode == 0
