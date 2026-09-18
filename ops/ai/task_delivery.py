"""Durable local delivery state for hybrid engineering tasks.

This module provides exactly-once local admission and conservative handling of
unknown transport outcomes. It never claims exactly-once execution by an
external provider without provider-side idempotency evidence.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import tempfile
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import StrEnum
from pathlib import Path


class DeliveryState(StrEnum):
    PREPARED = "PREPARED"
    DISPATCHED = "DISPATCHED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    RECONCILIATION_REQUIRED = "RECONCILIATION_REQUIRED"
    SAFE_STOP = "SAFE_STOP"


class DeliveryDenied(RuntimeError):
    """Raised when a task transition cannot be proven safe."""


@dataclass(frozen=True)
class TaskDelivery:
    task_id: str
    request_fingerprint: str
    conversation_id: str
    session_id: str
    generation: int
    state: DeliveryState
    attempt: int = 0
    response_fingerprint: str = ""
    reason: str = "prepared"


@dataclass
class TaskDeliveryJournal:
    path: Path
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)
    delivery: TaskDelivery | None = None
    _lock_handle: object | None = None

    def __post_init__(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.path.with_name(self.path.name + ".lock")
        try:
            handle = open(lock_path, "a+")  # noqa: SIM115 — handle lifetime owns the inter-process lock
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            try:
                handle.close()
            except UnboundLocalError:
                pass
            raise DeliveryDenied("task delivery ownership is already held") from exc
        self._lock_handle = handle

    def release(self) -> None:
        if self._lock_handle is None:
            return
        fcntl.flock(self._lock_handle.fileno(), fcntl.LOCK_UN)
        self._lock_handle.close()
        self._lock_handle = None

    @staticmethod
    def fingerprint(payload: str) -> str:
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def prepare(self, task_id: str, envelope: str, conversation_id: str,
                session_id: str, generation: int) -> TaskDelivery:
        if not task_id or not conversation_id or not session_id or generation < 1:
            raise DeliveryDenied("invalid task identity")
        fp = self.fingerprint(envelope)
        if self.delivery is not None:
            if self.delivery.task_id == task_id and self.delivery.request_fingerprint == fp:
                return self.delivery
            raise DeliveryDenied("another task is already active")
        self.delivery = TaskDelivery(task_id, fp, conversation_id, session_id,
                                     generation, DeliveryState.PREPARED)
        self.persist()
        return self.delivery

    def mark_dispatched(self) -> TaskDelivery:
        d = self._require()
        if d.state is DeliveryState.DISPATCHED:
            return d
        if d.state is not DeliveryState.PREPARED:
            raise DeliveryDenied("dispatch is not permitted from current state")
        self.delivery = TaskDelivery(**{**d.__dict__, "state": DeliveryState.DISPATCHED,
                                       "attempt": d.attempt + 1, "reason": "transport sent"})
        self.persist()
        return self.delivery

    def mark_acknowledged(self, response: str) -> TaskDelivery:
        d = self._require()
        fp = self.fingerprint(response)
        if d.state is DeliveryState.ACKNOWLEDGED and d.response_fingerprint == fp:
            return d
        if d.state is not DeliveryState.DISPATCHED:
            raise DeliveryDenied("acknowledgment requires dispatched state")
        self.delivery = TaskDelivery(**{**d.__dict__, "state": DeliveryState.ACKNOWLEDGED,
                                       "response_fingerprint": fp, "reason": "response accepted"})
        self.persist()
        return self.delivery

    def mark_transport_unknown(self, reason: str = "transport outcome unknown") -> TaskDelivery:
        d = self._require()
        if d.state is not DeliveryState.DISPATCHED:
            raise DeliveryDenied("unknown transport outcome requires dispatched state")
        self.delivery = TaskDelivery(**{**d.__dict__, "state": DeliveryState.RECONCILIATION_REQUIRED,
                                       "reason": reason})
        self.persist()
        return self.delivery

    def mark_safe_stop(self, reason: str) -> TaskDelivery:
        d = self._require()
        self.delivery = TaskDelivery(**{**d.__dict__, "state": DeliveryState.SAFE_STOP,
                                       "reason": reason})
        self.persist()
        return self.delivery

    def restore(self) -> TaskDelivery:
        if not self.path.exists():
            raise DeliveryDenied("task delivery checkpoint is unavailable")
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            if data.get("version") != 1:
                raise DeliveryDenied("unsupported task delivery checkpoint version")
            self.delivery = TaskDelivery(
                data["task_id"], data["request_fingerprint"], data["conversation_id"],
                data["session_id"], int(data["generation"]), DeliveryState(data["state"]),
                int(data["attempt"]), data.get("response_fingerprint", ""),
                data.get("reason", "restored"),
            )
        except DeliveryDenied:
            raise
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise DeliveryDenied("task delivery checkpoint is invalid") from exc
        return self.delivery

    def restore_for_identity(self, *, session_id: str, conversation_id: str,
                             generation: int) -> TaskDelivery:
        """Restore only when checkpoint identity exactly matches the active context."""
        delivery = self.restore()
        if (delivery.session_id != session_id or delivery.conversation_id != conversation_id
                or delivery.generation != generation):
            self.delivery = None
            raise DeliveryDenied("restored delivery identity does not match current session")
        if delivery.state is DeliveryState.SAFE_STOP:
            raise DeliveryDenied("restored delivery is in SAFE_STOP")
        return delivery

    def persist(self) -> None:
        if self.delivery is None:
            raise DeliveryDenied("no task delivery to persist")
        record = {"version": 1, **self.delivery.__dict__}
        record["state"] = self.delivery.state.value
        payload = json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
        fd, temp_name = tempfile.mkstemp(prefix=self.path.name + ".", dir=self.path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                tmp.write(payload)
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(temp_name, self.path)
            dir_fd = os.open(self.path.parent, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError as exc:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass
            raise DeliveryDenied("task delivery checkpoint durability failed") from exc

    def _require(self) -> TaskDelivery:
        if self.delivery is None:
            raise DeliveryDenied("no task delivery is active")
        if self.delivery.state is DeliveryState.SAFE_STOP:
            raise DeliveryDenied("task delivery is in SAFE_STOP")
        return self.delivery
