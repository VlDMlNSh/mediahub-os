"""Durable bounded scheduler for Astra autonomous development."""
from __future__ import annotations

import sqlite3
import time
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from ops.astra_github_coding_protocol import ExecutionIdentity, validate_fence


@dataclass(frozen=True)
class Task:
    task_id: str
    kind: str
    payload: str
    state: str
    generation: int
    target_sha: str


@dataclass(frozen=True)
class Lease:
    task_id: str
    execution_id: str
    generation: int
    lease_id: str
    owner_id: str
    target_sha: str
    expires_at: float


class Scheduler:
    """SQLite-backed single-writer control plane with generation fencing."""

    def __init__(self, db_path: str | Path, lease_seconds: int = 300) -> None:
        self.db = sqlite3.connect(str(db_path), timeout=30)
        self.db.row_factory = sqlite3.Row
        self.lease_seconds = lease_seconds
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS tasks(
              task_id TEXT PRIMARY KEY, kind TEXT NOT NULL, payload TEXT NOT NULL,
              state TEXT NOT NULL, generation INTEGER NOT NULL, target_sha TEXT NOT NULL,
              created_at REAL NOT NULL, updated_at REAL NOT NULL);
            CREATE TABLE IF NOT EXISTS leases(
              lease_id TEXT PRIMARY KEY, task_id TEXT NOT NULL REFERENCES tasks(task_id),
              execution_id TEXT NOT NULL UNIQUE, generation INTEGER NOT NULL,
              owner_id TEXT NOT NULL, target_sha TEXT NOT NULL, expires_at REAL NOT NULL,
              status TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS events(
              id INTEGER PRIMARY KEY AUTOINCREMENT, task_id TEXT NOT NULL,
              execution_id TEXT, event TEXT NOT NULL, detail TEXT NOT NULL,
              created_at REAL NOT NULL);
            """
        )
        self.db.commit()

    def close(self) -> None:
        self.db.close()

    def _event(self, task_id: str, execution_id: str | None, event: str, detail: str) -> None:
        self.db.execute(
            "INSERT INTO events(task_id,execution_id,event,detail,created_at) VALUES(?,?,?,?,?)",
            (task_id, execution_id, event, detail, time.time()),
        )

    def enqueue(self, kind: str, payload: str, target_sha: str, task_id: str | None = None) -> str:
        task_id = task_id or f"ASTRA-{uuid.uuid4().hex[:16]}"
        now = time.time()
        self.db.execute(
            "INSERT INTO tasks VALUES(?,?,?,?,?,?,?,?)",
            (task_id, kind, payload, "READY", 1, target_sha, now, now),
        )
        self._event(task_id, None, "ENQUEUED", kind)
        self.db.commit()
        return task_id

    def reconcile(self, now: float | None = None) -> int:
        now = time.time() if now is None else now
        rows = self.db.execute(
            "SELECT lease_id,task_id FROM leases WHERE status='ACTIVE' AND expires_at<=?",
            (now,),
        ).fetchall()
        for row in rows:
            self.db.execute("UPDATE leases SET status='EXPIRED' WHERE lease_id=?", (row["lease_id"],))
            self.db.execute(
                "UPDATE tasks SET state='READY',generation=generation+1,updated_at=? "
                "WHERE task_id=? AND state='CLAIMED'",
                (now, row["task_id"]),
            )
            self._event(row["task_id"], None, "LEASE_EXPIRED", row["lease_id"])
        self.db.commit()
        return len(rows)

    def select(self) -> Task | None:
        row = self.db.execute(
            "SELECT * FROM tasks WHERE state='READY' ORDER BY created_at,task_id LIMIT 1"
        ).fetchone()
        if row is None:
            return None
        return Task(*(row[k] for k in ("task_id","kind","payload","state","generation","target_sha")))

    def claim(self, task: Task, owner_id: str, now: float | None = None) -> Lease:
        now = time.time() if now is None else now
        execution_id, lease_id = f"exec-{uuid.uuid4().hex}", f"lease-{uuid.uuid4().hex}"
        expires_at = now + self.lease_seconds
        cur = self.db.execute(
            "UPDATE tasks SET state='CLAIMED',updated_at=? WHERE task_id=? AND state='READY' AND generation=?",
            (now, task.task_id, task.generation),
        )
        if cur.rowcount != 1:
            raise RuntimeError("task claim lost race")
        self.db.execute(
            "INSERT INTO leases VALUES(?,?,?,?,?,?,?,'ACTIVE')",
            (lease_id, task.task_id, execution_id, task.generation, owner_id, task.target_sha, expires_at),
        )
        self._event(task.task_id, execution_id, "CLAIMED", owner_id)
        self.db.commit()
        return Lease(task.task_id, execution_id, task.generation, lease_id, owner_id, task.target_sha, expires_at)

    def identity(self, lease: Lease) -> ExecutionIdentity:
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        return ExecutionIdentity.from_mapping({
            "schema_version": 1, "task_id": lease.task_id, "execution_id": lease.execution_id,
            "generation": lease.generation, "lease_id": lease.lease_id, "owner_id": lease.owner_id,
            "operation_key": "coding.execute", "target_sha": lease.target_sha,
            "created_at": now.isoformat().replace("+00:00", "Z"),
            "expires_at": now.isoformat().replace("+00:00", "Z"),
        })

    def verify_lease(self, lease: Lease) -> None:
        row = self.db.execute(
            "SELECT * FROM leases WHERE lease_id=? AND status='ACTIVE'", (lease.lease_id,)
        ).fetchone()
        if row is None or row["expires_at"] <= time.time():
            raise RuntimeError("lease is stale or missing")
        validate_fence(
            self.identity(lease), task_id=row["task_id"], execution_id=row["execution_id"],
            generation=row["generation"], lease_id=row["lease_id"], owner_id=row["owner_id"],
            target_sha=row["target_sha"],
        )

    def generate_next(self, lease: Lease, kind: str, payload: str, target_sha: str) -> str:
        self.verify_lease(lease)
        return self.enqueue(kind, payload, target_sha)

    def complete(self, lease: Lease, succeeded: bool, detail: str) -> None:
        self.verify_lease(lease)
        state = "SUCCEEDED" if succeeded else "READY"
        self.db.execute("UPDATE leases SET status='COMPLETED' WHERE lease_id=?", (lease.lease_id,))
        self.db.execute(
            "UPDATE tasks SET state=?,generation=generation+?,updated_at=? WHERE task_id=?",
            (state, 0 if succeeded else 1, time.time(), lease.task_id),
        )
        self._event(lease.task_id, lease.execution_id, "COMPLETED" if succeeded else "REQUEUED", detail)
        self.db.commit()

    def run_once(self, owner_id: str, worker: Callable[[Task, Lease], tuple[bool, str]]) -> str:
        self.reconcile()
        task = self.select()
        if task is None:
            return "IDLE"
        lease = self.claim(task, owner_id)
        try:
            succeeded, detail = worker(task, lease)
            if succeeded:
                self.generate_next(lease, "reconcile", f"after:{task.task_id}", lease.target_sha)
            self.complete(lease, succeeded, detail)
            return "SUCCEEDED" if succeeded else "REQUEUED"
        except Exception as exc:
            try:
                self.complete(lease, False, f"worker-error:{type(exc).__name__}:{exc}")
            except Exception:
                self.db.rollback()
            raise
