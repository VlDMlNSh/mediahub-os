from __future__ import annotations

import json
import sqlite3
import time
from dataclasses import asdict, replace
from pathlib import Path
from threading import RLock
from typing import Any

from .model import AuditRecord, Execution, Event, Lease, LeaseStatus, Task, TaskStatus, validate_task_transition
from .repository import ControlPlaneRepository

_SCHEMA = """
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS tasks (task_id TEXT PRIMARY KEY, idempotency_key TEXT UNIQUE,
  type TEXT NOT NULL, payload TEXT, priority INTEGER NOT NULL, status TEXT NOT NULL,
  dependencies TEXT NOT NULL, attempt INTEGER NOT NULL, max_attempts INTEGER NOT NULL,
  required_capabilities TEXT NOT NULL, architecture TEXT, retry_not_before REAL);
CREATE TABLE IF NOT EXISTS leases (lease_id TEXT PRIMARY KEY, task_id TEXT NOT NULL,
  agent_id TEXT NOT NULL, created_at REAL NOT NULL, expires_at REAL NOT NULL,
  last_renewed_at REAL NOT NULL, generation INTEGER NOT NULL, status TEXT NOT NULL);
CREATE UNIQUE INDEX IF NOT EXISTS ux_active_task_lease ON leases(task_id)
  WHERE status IN ('ACTIVE','RENEWED','EXPIRING');
CREATE TABLE IF NOT EXISTS executions (execution_id TEXT PRIMARY KEY, task_id TEXT NOT NULL,
  agent_id TEXT NOT NULL, lease_generation INTEGER NOT NULL, status TEXT NOT NULL,
  result TEXT, failure_class TEXT);
CREATE TABLE IF NOT EXISTS events (event_id TEXT PRIMARY KEY, event_type TEXT NOT NULL,
  timestamp REAL NOT NULL, entity_type TEXT NOT NULL, entity_id TEXT NOT NULL,
  payload TEXT, correlation_id TEXT);
CREATE TABLE IF NOT EXISTS audit (event_id TEXT PRIMARY KEY, timestamp REAL NOT NULL,
  actor TEXT NOT NULL, action TEXT NOT NULL, resource TEXT NOT NULL, resource_id TEXT NOT NULL,
  previous_state TEXT, new_state TEXT, result TEXT NOT NULL, correlation_id TEXT);
"""


def _json(value: Any) -> str | None:
    return None if value is None else json.dumps(value, sort_keys=True, separators=(",", ":"))


def _unjson(value: str | None) -> Any:
    return None if value is None else json.loads(value)
class SQLiteControlPlaneRepository(ControlPlaneRepository):
    """Durable repository; one SQLite database is the authoritative state store."""

    SCHEMA_VERSION = "1"

    def __init__(self, path: str | Path, *, timeout: float = 5.0, clock=time.time):
        self.path = str(path)
        self.clock = clock
        self.timeout = timeout
        self._lock = RLock()
        if self.path != ":memory:":
            Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        with self._connect() as db:
            db.executescript(_SCHEMA)
            db.execute("INSERT OR IGNORE INTO meta(key,value) VALUES('schema_version',?)", (self.SCHEMA_VERSION,))
            version = db.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()[0]
            if version != self.SCHEMA_VERSION:
                raise RuntimeError(f"unsupported control-plane schema: {version}")

    def _connect(self):
        db = sqlite3.connect(self.path, timeout=self.timeout, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=5000")
        return db

    def now(self) -> float:
        return float(self.clock())

    @staticmethod
    def _task(row):
        return Task(row["task_id"], row["type"], _unjson(row["payload"]), row["priority"],
                    TaskStatus(row["status"]), tuple(_unjson(row["dependencies"])), row["idempotency_key"],
                    row["attempt"], row["max_attempts"], tuple(_unjson(row["required_capabilities"])),
                    row["architecture"], row["retry_not_before"])

    @staticmethod
    def _lease(row):
        return Lease(row["lease_id"], row["task_id"], row["agent_id"], row["created_at"],
                     row["expires_at"], row["last_renewed_at"], row["generation"], LeaseStatus(row["status"]))
    def create_task(self, task):
        with self._connect() as db:
            try:
                db.execute("INSERT INTO tasks VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                    (task.task_id, task.idempotency_key, task.type, _json(task.payload), task.priority,
                     task.status.value, _json(task.dependencies), task.attempt, task.max_attempts,
                     _json(task.required_capabilities), task.architecture, task.retry_not_before))
            except sqlite3.IntegrityError as exc:
                raise ValueError("duplicate task identity or idempotency_key") from exc
        return task

    def get_task(self, task_id):
        with self._connect() as db:
            row = db.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
        return self._task(row) if row else None

    def list_tasks(self):
        with self._connect() as db:
            rows = db.execute("SELECT * FROM tasks ORDER BY task_id").fetchall()
        return tuple(self._task(row) for row in rows)

    def list_leases(self):
        with self._connect() as db:
            rows = db.execute("SELECT * FROM leases ORDER BY lease_id").fetchall()
        return tuple(self._lease(row) for row in rows)

    def list_executions(self):
        with self._connect() as db:
            rows = db.execute("SELECT * FROM executions ORDER BY execution_id").fetchall()
        return tuple(Execution(r["execution_id"], r["task_id"], r["agent_id"], r["lease_generation"],
                               r["status"], _unjson(r["result"]), r["failure_class"])
                     for r in rows)

    def _insert_event_audit(self, db, event, audit):
        db.execute("INSERT INTO events VALUES(?,?,?,?,?,?,?)", (event.event_id,event.event_type,event.timestamp,event.entity_type,event.entity_id,_json(event.payload),event.correlation_id))
        db.execute("INSERT INTO audit VALUES(?,?,?,?,?,?,?,?,?,?)", (audit.event_id,audit.timestamp,audit.actor,audit.action,audit.resource,audit.resource_id,audit.previous_state,audit.new_state,audit.result,audit.correlation_id))

    def claim_and_start(self, task_id, agent_id, generation, max_concurrency=None, event=None, audit=None):
        import uuid
        now = self.now()
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            if not row: raise KeyError(task_id)
            if TaskStatus(row["status"]) is not TaskStatus.READY: raise ValueError("task not claimable")
            if db.execute("SELECT 1 FROM leases WHERE task_id=? AND status IN ('ACTIVE','RENEWED','EXPIRING')", (task_id,)).fetchone(): raise ValueError("task already leased")
            if max_concurrency is not None:
                if max_concurrency <= 0: raise ValueError("max_concurrency must be positive")
                count = db.execute("SELECT COUNT(*) FROM leases WHERE agent_id=? AND status IN ('ACTIVE','RENEWED','EXPIRING')", (agent_id,)).fetchone()[0]
                if count >= max_concurrency: raise ValueError("agent capacity exhausted")
            validate_task_transition(TaskStatus(row["status"]), TaskStatus.CLAIMED)
            validate_task_transition(TaskStatus.CLAIMED, TaskStatus.RUNNING)
            lease = Lease(str(uuid.uuid4()), task_id, agent_id, now, now + 60.0, now, generation, LeaseStatus.ACTIVE)
            db.execute("UPDATE tasks SET status=? WHERE task_id=?", (TaskStatus.RUNNING.value, task_id))
            db.execute("INSERT INTO leases VALUES(?,?,?,?,?,?,?,?)", (lease.lease_id,task_id,agent_id,now,lease.expires_at,now,generation,lease.status.value))
            if event is not None and audit is not None:
                self._insert_event_audit(db, event, audit)
            db.commit()
        return lease

    def complete_atomic(self, task_id, agent_id, generation, lease_id, execution, event, audit):
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            lease = db.execute("SELECT * FROM leases WHERE lease_id=?", (lease_id,)).fetchone()
            now = self.now()
            if (not lease or lease["task_id"] != task_id or lease["agent_id"] != agent_id or
                lease["generation"] != generation or lease["status"] not in ('ACTIVE','RENEWED') or now >= lease["expires_at"]):
                raise PermissionError("stale lease owner")
            task = db.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            validate_task_transition(TaskStatus(task["status"]), TaskStatus.VERIFYING)
            validate_task_transition(TaskStatus.VERIFYING, TaskStatus.SUCCEEDED)
            db.execute("INSERT OR IGNORE INTO executions VALUES(?,?,?,?,?,?,?)", (execution.execution_id,execution.task_id,execution.agent_id,execution.lease_generation,execution.status,_json(execution.result),execution.failure_class.value if execution.failure_class else None))
            db.execute("UPDATE tasks SET status=? WHERE task_id=?", (TaskStatus.SUCCEEDED.value, task_id))
            db.execute("UPDATE leases SET status=? WHERE lease_id=?", (LeaseStatus.RELEASED.value, lease_id))
            self._insert_event_audit(db, event, audit)
            db.commit()
        return execution

    def claim_task(self, task_id, agent_id, generation, max_concurrency=None):
        import uuid
        now = self.now()
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,)).fetchone()
            if not row: raise KeyError(task_id)
            if TaskStatus(row["status"]) is not TaskStatus.READY: raise ValueError("task not claimable")
            active = db.execute("SELECT lease_id FROM leases WHERE task_id=? AND status IN ('ACTIVE','RENEWED','EXPIRING')", (task_id,)).fetchone()
            if active: raise ValueError("task already leased")
            if max_concurrency is not None:
                count = db.execute("SELECT COUNT(*) FROM leases WHERE agent_id=? AND status IN ('ACTIVE','RENEWED','EXPIRING')", (agent_id,)).fetchone()[0]
                if count >= max_concurrency: raise ValueError("agent capacity exhausted")
            lease = Lease(str(uuid.uuid4()), task_id, agent_id, now, now + 60.0, now, generation, LeaseStatus.ACTIVE)
            db.execute("UPDATE tasks SET status=? WHERE task_id=?", (TaskStatus.CLAIMED.value, task_id))
            db.execute("INSERT INTO leases VALUES(?,?,?,?,?,?,?,?)", (lease.lease_id, task_id, agent_id, now, lease.expires_at, now, generation, lease.status.value))
            db.commit()
        return lease
    def renew_lease(self, lease_id, agent_id, generation, expires_at):
        now = self.now()
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM leases WHERE lease_id=?", (lease_id,)).fetchone()
            if not row: raise KeyError(lease_id)
            if row["agent_id"] != agent_id or row["generation"] != generation: raise PermissionError("stale lease owner")
            if row["status"] not in (LeaseStatus.ACTIVE.value, LeaseStatus.RENEWED.value): raise ValueError("lease not renewable")
            db.execute("UPDATE leases SET expires_at=?,last_renewed_at=?,status=? WHERE lease_id=?", (expires_at, now, LeaseStatus.RENEWED.value, lease_id))
            db.commit()
        return replace(self._lease(row), expires_at=expires_at, last_renewed_at=now, status=LeaseStatus.RENEWED)

    def record_execution(self, execution):
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            if db.execute("SELECT 1 FROM executions WHERE execution_id=?", (execution.execution_id,)).fetchone():
                db.commit(); return execution
            row = db.execute("SELECT * FROM leases WHERE task_id=? AND status IN ('ACTIVE','RENEWED','EXPIRING') ORDER BY created_at DESC LIMIT 1", (execution.task_id,)).fetchone()
            if not row or row["agent_id"] != execution.agent_id or row["generation"] != execution.lease_generation:
                raise PermissionError("stale execution")
            db.execute("INSERT INTO executions VALUES(?,?,?,?,?,?,?)", (execution.execution_id, execution.task_id, execution.agent_id, execution.lease_generation, execution.status, _json(execution.result), execution.failure_class.value if execution.failure_class else None))
            db.commit()
        return execution

    def append_event(self, event):
        with self._connect() as db:
            db.execute("INSERT OR IGNORE INTO events VALUES(?,?,?,?,?,?,?)", (event.event_id,event.event_type,event.timestamp,event.entity_type,event.entity_id,_json(event.payload),event.correlation_id))
        return event

    def append_audit(self, record):
        with self._connect() as db:
            db.execute("INSERT OR IGNORE INTO audit VALUES(?,?,?,?,?,?,?,?,?,?)", (record.event_id,record.timestamp,record.actor,record.action,record.resource,record.resource_id,record.previous_state,record.new_state,record.result,record.correlation_id))
        return record
    def update_task(self, task):
        with self._connect() as db:
            row = db.execute("SELECT * FROM tasks WHERE task_id=?", (task.task_id,)).fetchone()
            if not row: raise KeyError(task.task_id)
            current = TaskStatus(row["status"]); validate_task_transition(current, task.status)
            db.execute("UPDATE tasks SET type=?,payload=?,priority=?,status=?,dependencies=?,attempt=?,max_attempts=?,required_capabilities=?,architecture=?,retry_not_before=?,idempotency_key=? WHERE task_id=?",
                       (task.type,_json(task.payload),task.priority,task.status.value,_json(task.dependencies),task.attempt,task.max_attempts,_json(task.required_capabilities),task.architecture,task.retry_not_before,task.idempotency_key,task.task_id))
        return task

    def get_lease_for_task(self, task_id):
        with self._connect() as db:
            row = db.execute("SELECT * FROM leases WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (task_id,)).fetchone()
        return self._lease(row) if row else None

    def assert_lease_owner(self, lease_id, agent_id, generation):
        now = self.now()
        with self._connect() as db:
            row = db.execute("SELECT * FROM leases WHERE lease_id=?", (lease_id,)).fetchone()
        if (not row or row["agent_id"] != agent_id or row["generation"] != generation or
            row["status"] not in (LeaseStatus.ACTIVE.value, LeaseStatus.RENEWED.value) or now >= row["expires_at"]):
            raise PermissionError("stale lease owner")

    def release_lease(self, lease_id, agent_id, generation):
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM leases WHERE lease_id=?", (lease_id,)).fetchone()
            if not row or row["agent_id"] != agent_id or row["generation"] != generation: raise PermissionError("stale lease owner")
            if row["status"] not in (LeaseStatus.ACTIVE.value, LeaseStatus.RENEWED.value): raise ValueError("lease not releasable")
            db.execute("UPDATE leases SET status=? WHERE lease_id=?", (LeaseStatus.RELEASED.value, lease_id)); db.commit()
        return replace(self._lease(row), status=LeaseStatus.RELEASED)

    def expire_lease(self, lease_id, now):
        with self._connect() as db:
            db.execute("BEGIN IMMEDIATE")
            row = db.execute("SELECT * FROM leases WHERE lease_id=?", (lease_id,)).fetchone()
            if not row: raise KeyError(lease_id)
            if now < row["expires_at"]: raise ValueError("lease has not expired")
            if row["status"] not in (LeaseStatus.ACTIVE.value,LeaseStatus.RENEWED.value,LeaseStatus.EXPIRING.value): raise ValueError("lease not expirable")
            db.execute("UPDATE leases SET status=? WHERE lease_id=?", (LeaseStatus.EXPIRED.value, lease_id)); db.commit()
        return replace(self._lease(row), status=LeaseStatus.EXPIRED)
