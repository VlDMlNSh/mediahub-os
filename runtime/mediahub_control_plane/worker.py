from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Any, Callable

from .model import FailureClass, Lease, TaskStatus
from .service import ControlPlaneService


class LeaseLost(RuntimeError):
    """Execution lost authoritative ownership and must not be recorded as success."""


@dataclass(frozen=True, slots=True)
class ExecutionContext:
    task_id: str
    agent_id: str
    generation: int
    renew: Callable[[], Lease]


class WorkerRuntime:
    """Bounded worker execution boundary; the worker remains reusable after each task."""

    def __init__(self, service: ControlPlaneService, clock: Callable[[], float] = monotonic):
        self.service = service
        self.clock = clock
        self.completed_tasks = 0

    def _best_effort_fail(self, task_id: str, agent_id: str, generation: int, reason: str, lease_id: str) -> None:
        try:
            self.service.fail(task_id, agent_id, generation, reason, FailureClass.INFRASTRUCTURE if reason == "LEASE_LOST" else FailureClass.TASK, lease_id=lease_id)
        except PermissionError:
            pass

    def execute(self, task_id: str, agent_id: str, generation: int,
                executor: Callable[[Any, ExecutionContext], Any], verifier: Callable[[Any], bool]):
        lease = self.service.repository.get_lease_for_task(task_id)
        if lease is None:
            raise LeaseLost("task has no lease")
        try:
            self.service.repository.assert_lease_owner(lease.lease_id, agent_id, generation)
        except PermissionError as exc:
            raise LeaseLost("lease ownership rejected before execution") from exc
        task = self.service.repository.get_task(task_id)
        if task is None:
            raise KeyError(task_id)
        if task.status is not TaskStatus.RUNNING:
            raise ValueError("task is not running")

        def renew() -> Lease:
            current = self.service.repository.get_lease_for_task(task_id)
            if current is None or current.lease_id != lease.lease_id:
                raise LeaseLost("lease identity changed")
            try:
                self.service.repository.assert_lease_owner(lease.lease_id, agent_id, generation)
                duration = max(current.expires_at - current.last_renewed_at, 1.0)
                now = (self.service.repository.now() if hasattr(self.service.repository, "now") else self.clock())
                return self.service.repository.renew_lease(current.lease_id, agent_id, generation, now + duration)
            except (PermissionError, ValueError, KeyError) as exc:
                raise LeaseLost("lease renewal failed") from exc

        context = ExecutionContext(task_id, agent_id, generation, renew)
        try:
            result = executor(task.payload, context)
            self.service.repository.assert_lease_owner(lease.lease_id, agent_id, generation)
        except LeaseLost:
            self._best_effort_fail(task_id, agent_id, generation, "LEASE_LOST", lease.lease_id)
            raise
        except PermissionError as exc:
            self._best_effort_fail(task_id, agent_id, generation, "LEASE_LOST", lease.lease_id)
            raise LeaseLost("lease ownership lost during execution") from exc
        except Exception:
            self._best_effort_fail(task_id, agent_id, generation, "EXECUTION_FAILED", lease.lease_id)
            raise

        try:
            verified = bool(verifier(result))
        except Exception:
            self._best_effort_fail(task_id, agent_id, generation, "VERIFICATION_FAILED", lease.lease_id)
            raise
        if not verified:
            self._best_effort_fail(task_id, agent_id, generation, "VERIFICATION_FAILED", lease.lease_id)
            raise ValueError("execution verification failed")

        execution = self.service.complete(task_id, agent_id, generation, result, lease_id=lease.lease_id)
        self.completed_tasks += 1
        return execution

    def run_once(self, task_id: str, agent_id: str, generation: int, executor, verifier):
        return self.execute(task_id, agent_id, generation, executor, verifier)
