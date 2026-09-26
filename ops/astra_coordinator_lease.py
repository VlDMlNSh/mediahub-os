from __future__ import annotations

import fcntl
import sqlite3
from dataclasses import dataclass
from pathlib import Path


class CoordinatorLeaseError(RuntimeError):
    pass


@dataclass(frozen=True)
class CoordinatorLeaseRecord:
    coordinator_id: str
    epoch: int
    branch: str


class CoordinatorLease:
    """Single-writer coordinator lease backed by OS locking plus durable SQLite metadata."""

    def __init__(self, database: str | Path, lock_path: str | Path, *, branch: str) -> None:
        self.database = Path(database)
        self.lock_path = Path(lock_path)
        self.branch = branch
        self._handle = None
        self.record: CoordinatorLeaseRecord | None = None
        self.database.parent.mkdir(parents=True, exist_ok=True)
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.database) as db:
            db.execute("CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL)")
            db.commit()

    def acquire(self, coordinator_id: str, *, now: float) -> CoordinatorLeaseRecord:
        if self.record is not None:
            raise CoordinatorLeaseError("coordinator lease already held by this instance")
        handle = self.lock_path.open("a+")
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            handle.close()
            raise CoordinatorLeaseError("another coordinator owns the branch lease") from exc
        try:
            with sqlite3.connect(self.database) as db:
                db.execute("BEGIN IMMEDIATE")
                row = db.execute("SELECT key, value FROM meta WHERE key IN ('coordinator_id','coordinator_epoch','branch_lease')").fetchall()
                meta = dict(row)
                current = meta.get("coordinator_id", "")
                if current:
                    db.rollback()
                    raise CoordinatorLeaseError(f"durable coordinator already active: {current}")
                epoch = int(meta.get("coordinator_epoch", "0")) + 1
                db.execute("INSERT INTO meta(key,value) VALUES('coordinator_id',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (coordinator_id,))
                db.execute("INSERT INTO meta(key,value) VALUES('coordinator_epoch',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(epoch),))
                db.execute("INSERT INTO meta(key,value) VALUES('branch_lease',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (self.branch,))
                db.execute("INSERT INTO meta(key,value) VALUES('coordinator_heartbeat',?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (str(now),))
                db.commit()
            self._handle = handle
            self.record = CoordinatorLeaseRecord(coordinator_id, epoch, self.branch)
            return self.record
        except Exception:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            handle.close()
            raise

    def heartbeat(self, *, now: float) -> None:
        if self.record is None:
            raise CoordinatorLeaseError("coordinator lease not held")
        with sqlite3.connect(self.database) as db:
            row = db.execute("SELECT value FROM meta WHERE key='coordinator_id'").fetchone()
            if not row or row[0] != self.record.coordinator_id:
                raise CoordinatorLeaseError("coordinator lease was fenced")
            db.execute("UPDATE meta SET value=? WHERE key='coordinator_heartbeat'", (str(now),))
            db.commit()

    def release(self, *, now: float) -> None:
        if self.record is None:
            return
        try:
            with sqlite3.connect(self.database) as db:
                db.execute("BEGIN IMMEDIATE")
                row = db.execute("SELECT value FROM meta WHERE key='coordinator_id'").fetchone()
                if row and row[0] == self.record.coordinator_id:
                    db.execute("UPDATE meta SET value='' WHERE key='coordinator_id'")
                    db.execute("UPDATE meta SET value=? WHERE key='coordinator_released_at'", (str(now),))
                    db.commit()
                else:
                    db.rollback()
        finally:
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
            self._handle.close()
            self._handle = None
            self.record = None
