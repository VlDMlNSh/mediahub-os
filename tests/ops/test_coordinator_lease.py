import sqlite3

import pytest

from ops.astra_coordinator_lease import CoordinatorLease, CoordinatorLeaseError


def test_acquire_records_epoch_and_branch(tmp_path):
    db = tmp_path / "control.sqlite3"
    lease = CoordinatorLease(db, tmp_path / "coord.lock", branch="engineering/test")
    acquired = lease.acquire("coord-a", now=100.0)
    assert acquired.epoch == 1
    with sqlite3.connect(db) as conn:
        rows = dict(conn.execute("SELECT key, value FROM meta"))
    assert rows["coordinator_id"] == "coord-a"
    assert rows["coordinator_epoch"] == "1"
    assert rows["branch_lease"] == "engineering/test"
    lease.release(now=101.0)


def test_second_coordinator_is_rejected_while_first_holds_lock(tmp_path):
    db = tmp_path / "control.sqlite3"
    lock = tmp_path / "coord.lock"
    first = CoordinatorLease(db, lock, branch="engineering/test")
    second = CoordinatorLease(db, lock, branch="engineering/test")
    first.acquire("coord-a", now=100.0)
    with pytest.raises(CoordinatorLeaseError):
        second.acquire("coord-b", now=101.0)
    first.release(now=102.0)


def test_epoch_increments_after_release(tmp_path):
    db = tmp_path / "control.sqlite3"
    lock = tmp_path / "coord.lock"
    first = CoordinatorLease(db, lock, branch="engineering/test")
    assert first.acquire("coord-a", now=100.0).epoch == 1
    first.release(now=101.0)
    second = CoordinatorLease(db, lock, branch="engineering/test")
    assert second.acquire("coord-b", now=102.0).epoch == 2
    second.release(now=103.0)
