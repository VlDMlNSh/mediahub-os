from __future__ import annotations

from dataclasses import dataclass
from time import monotonic
from typing import Any, Callable

from .model import Lease, TaskStatus
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

    def _best_effort_fail(self, task_id: str, agent_id: str, generation: int, reason: str) -> None:
        try:
            self.service.fail(task_id, agent_id, generation, reason)
        except PermissionError:
            # Once fencing rejects us, the worker is no longer authoritative.
            pass

    def execute(
        self,
        task_id: str,
        agent_id: str,
        generation: int,
        executor: Callable[[Any, ExecutionContext], Any],
        verifier: Callable[[Any], bool],
    ):
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
            if current is None:
                raise LeaseLost("lease disappeared")
            try:
                self.service.repository.assert_lease_owner(current.lease_id, agent_id, generation)
                duration = current.expires_at - current.last_renewed_at
                return self.service.repository.renew_lease(
                    current.lease_id, agent_id, generation, self.clock() + duration
                )
            except (PermissionError, ValueError, KeyError) as exc:
                raise LeaseLost("lease renewal failed") from exc

        context = ExecutionContext(task_id, agent_id, generation, renew)
        try:
            result = executor(task.payload, context)
            self.service.repository.assert_lease_owner(lease.lease_id, agent_id, generation)
        except LeaseLost:
            self._best_effort_fail(task_id, agent_id, generation, "LEASE_LOST")
            raise
        except PermissionError as exc:
            self._best_effort_fail(task_id, agent_id, generation, "LEASE_LOST")
            raise LeaseLost("lease ownership lost during execution") from exc
        except Exception:
            self._best_effort_fail(task_id, agent_id, generation, "EXECUTION_FAILED")
            raise

        try:
            verified = bool(verifier(result))
        except Exception:
            self._best_effort_fail(task_id, agent_id, generation, "VERIFICATION_FAILED")
            raise
        if not verified:
            self._best_effort_fail(task_id, agent_id, generation, "VERIFICATION_FAILED")
            raise ValueError("execution verification failed")

        execution = self.service.complete(task_id, agent_id, generation, result)
        self.completed_tasks += 1
        return execution

    def run_once(self, task_id: str, agent_id: str, generation: int, executor, verifier):
        """Alias for one task; callers may invoke repeatedly without recreating the runtime."""
        return self.execute(task_id, agent_id, generation, executor, verifier)
