import multiprocessing

import pytest

from ops.ai.task_lease import (
    ACTIVE,
    ORPHANED,
    STALE,
    UNKNOWN,
    LeaseDenied,
    TaskLease,
    classify_lease_record,
)


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


def test_lease_persists_full_provenance(tmp_path):
    path = tmp_path / "leases" / "task.lock"
    lease = TaskLease(
        path, "task-7", "worker-7", ttl_seconds=60,
        worktree="/work/tree", branch="feature/x", base_sha="abc123", checkpoint_id="cp-7",
    )
    lease.acquire()
    record = lease.read_record()
    assert record["task_id"] == "task-7"
    assert record["worker_id"] == "worker-7"
    assert isinstance(record["pid"], int)
    assert record["process_start_identity"]
    assert record["worktree"] == "/work/tree"
    assert record["branch"] == "feature/x"
    assert record["base_sha"] == "abc123"
    assert record["checkpoint_id"] == "cp-7"
    assert record["created_at"] <= record["expires_at"]
    lease.release()


def test_expired_live_owner_is_stale_not_orphaned():
    record = {
        "task_id": "task-1", "worker_id": "worker-1", "pid": 42,
        "process_start_identity": "100", "worktree": "/work", "branch": "b", "base_sha": "sha",
        "created_at": 1.0, "expires_at": 5.0,
    }
    assert classify_lease_record(record, now=10.0, owner_probe=lambda _: (True, True)) == STALE


def test_live_unexpired_owner_is_active():
    record = {
        "task_id": "task-1", "worker_id": "worker-1", "pid": 42,
        "process_start_identity": "100", "worktree": "/work", "branch": "b", "base_sha": "sha",
        "created_at": 1.0, "expires_at": 20.0,
    }
    assert classify_lease_record(record, now=10.0, owner_probe=lambda _: (True, True)) == ACTIVE

def test_dead_owner_with_complete_provenance_is_orphaned():
    record = {
        "task_id": "task-1", "worker_id": "worker-1", "pid": 42,
        "process_start_identity": "100", "worktree": "/work", "branch": "b", "base_sha": "sha",
        "created_at": 1.0, "expires_at": 5.0,
    }
    assert classify_lease_record(record, now=10.0, owner_probe=lambda _: (False, True)) == ORPHANED


def test_missing_worker_provenance_is_unknown_even_when_expired():
    record = {
        "task_id": "task-legacy", "worker_id": "worker-old",
        "created_at": 1.0, "expires_at": 5.0,
    }
    assert classify_lease_record(record, now=100.0, owner_probe=lambda _: (False, True)) == UNKNOWN


def test_pid_identity_mismatch_is_unknown():
    record = {
        "task_id": "task-1", "worker_id": "worker-1", "pid": 42,
        "process_start_identity": "100", "worktree": "/work", "branch": "b", "base_sha": "sha",
        "created_at": 1.0, "expires_at": 20.0,
    }
    assert classify_lease_record(record, now=10.0, owner_probe=lambda _: (False, False)) == UNKNOWN


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

def test_release_does_not_delete_lease_record(tmp_path):
    path = tmp_path / "leases" / "task.lock"
    lease = TaskLease(path, "task-keep", "worker-keep", ttl_seconds=60)
    lease.acquire()
    before = lease.read_record()
    lease.release()
    assert path.exists()
    assert lease.read_record()["task_id"] == before["task_id"]


def test_ttl_expiry_does_not_claim_worker_death():
    record = {
        "task_id": "task-1", "worker_id": "worker-1", "pid": 42,
        "process_start_identity": "100", "worktree": "/work", "branch": "b", "base_sha": "sha",
        "created_at": 1.0, "expires_at": 2.0,
    }
    assert classify_lease_record(record, now=3.0, owner_probe=lambda _: (True, True)) == STALE
