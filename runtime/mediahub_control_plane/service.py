from __future__ import annotations

from dataclasses import replace
from time import monotonic
from uuid import uuid4

from .model import AuditRecord, Execution, Event, LeaseStatus, TaskStatus, validate_task_transition
from .repository import ControlPlaneRepository


class ControlPlaneService:
    """Small deterministic coordinator for the first orchestration vertical slice."""

    def __init__(self, repository: ControlPlaneRepository):
        self.repository = repository

    def mark_ready(self, task_id: str) -> None:
        task = self.repository.get_task(task_id)
        if task is None:
            raise KeyError(task_id)
        validate_task_transition(task.status, TaskStatus.READY)
        self.repository.update_task(replace(task, status=TaskStatus.READY))

    def claim(self, task_id: str, agent_id: str, generation: int):
        lease = self.repository.claim_task(task_id, agent_id, generation)
        self._transition(task_id, TaskStatus.RUNNING)
        return lease

    def complete(self, task_id: str, agent_id: str, generation: int, result=None):
        lease = self.repository.get_lease_for_task(task_id)
        if lease is None:
            raise KeyError(task_id)
        self.repository.assert_lease_owner(lease.lease_id, agent_id, generation)
        execution = Execution(str(uuid4()), task_id, agent_id, generation, "SUCCEEDED", result)
        self.repository.record_execution(execution)
        self._transition(task_id, TaskStatus.VERIFYING)
        self._transition(task_id, TaskStatus.SUCCEEDED)
        self.repository.release_lease(lease.lease_id, agent_id, generation)
        self._record("TaskSucceeded", task_id, agent_id, "SUCCEEDED")
        return execution

    def recover_expired(self, task_id: str, now: float | None = None) -> bool:
        lease = self.repository.get_lease_for_task(task_id)
        if lease is None:
            return False
        if now is None:
            now = monotonic()
        if now < lease.expires_at:
            return False
        self.repository.expire_lease(lease.lease_id, now)
        task = self.repository.get_task(task_id)
        if task is None:
            raise KeyError(task_id)
        if task.status in (TaskStatus.CLAIMED, TaskStatus.RUNNING):
            self._transition(task_id, TaskStatus.EXPIRED)
        self._record("LeaseExpired", task_id, lease.agent_id, "RECOVERY_REQUIRED")
        return True

    def _transition(self, task_id: str, target: TaskStatus) -> None:
        task = self.repository.get_task(task_id)
        if task is None:
            raise KeyError(task_id)
        validate_task_transition(task.status, target)
        self.repository.update_task(replace(task, status=target))

    def _record(self, event_type: str, task_id: str, agent_id: str, result: str) -> None:
        event_id = str(uuid4())
        self.repository.append_event(Event(event_id, event_type, monotonic(), "task", task_id, {"agent_id": agent_id}))
        self.repository.append_audit(AuditRecord(event_id, monotonic(), agent_id, event_type, "task", task_id, None, None, result))

    def dispatch_once(self, task_id: str, scheduler, generation: int):
        """Select then atomically claim; a concurrent winner causes a clean retry signal."""
        task = self.repository.get_task(task_id)
        if task is None:
            raise KeyError(task_id)
        decision = scheduler.select(task)
        if decision.agent_id is None:
            return decision
        try:
            lease = self.repository.claim_task(task_id, decision.agent_id, generation)
        except (ValueError, PermissionError):
            return type(decision)(task_id, None, 'claim_lost_race')
        self._transition(task_id, TaskStatus.RUNNING)
        return lease
