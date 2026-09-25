from __future__ import annotations
from dataclasses import replace
from time import monotonic
from .dependencies import dependencies_satisfied
from .model import LeaseStatus, TaskStatus

class ControlPlaneReconciler:
    """Deterministic, idempotent convergence pass over observable control-plane state."""
    def __init__(self, repository, agent_registry=None): self.repository=repository; self.agent_registry=agent_registry
    def reconcile_once(self, now: float | None = None) -> tuple[str, ...]:
        now=monotonic() if now is None else now; changed=[]; tasks=self.repository.list_tasks()
        completed={t.task_id for t in tasks if t.status is TaskStatus.SUCCEEDED}
        for task in tasks:
            retry_due = task.retry_not_before is None or now >= task.retry_not_before
            if task.status in {TaskStatus.PENDING,TaskStatus.BLOCKED} and dependencies_satisfied(task,completed):
                self.repository.update_task(replace(task,status=TaskStatus.READY,retry_not_before=None)); changed.append(task.task_id)
            elif task.status is TaskStatus.RETRY_WAIT and retry_due and dependencies_satisfied(task,completed):
                self.repository.update_task(replace(task,status=TaskStatus.READY,retry_not_before=None)); changed.append(task.task_id)
        for lease in self.repository.list_leases():
            if lease.status in {LeaseStatus.ACTIVE,LeaseStatus.RENEWED,LeaseStatus.EXPIRING} and now >= lease.expires_at:
                self.repository.expire_lease(lease.lease_id,now); task=self.repository.get_task(lease.task_id)
                if task and task.status in {TaskStatus.CLAIMED,TaskStatus.RUNNING}:
                    attempt=task.attempt+1
                    self.repository.update_task(replace(task,attempt=attempt,status=TaskStatus.EXPIRED))
                    if attempt < task.max_attempts:
                        self.repository.update_task(replace(self.repository.get_task(task.task_id),status=TaskStatus.RETRY_WAIT))
                    changed.append(task.task_id)
        if self.agent_registry is not None: self.agent_registry.reconcile()
        return tuple(changed)
