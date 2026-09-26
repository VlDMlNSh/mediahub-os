from __future__ import annotations
from dataclasses import replace
from time import monotonic
from uuid import uuid4
from .dependencies import dependencies_satisfied
from .model import AuditRecord, CircuitState, Event, FailureClass, LeaseStatus, TaskStatus
from .retry_policy import RetryPolicy
from .metrics import ControlPlaneMetrics

class ControlPlaneReconciler:
    """Deterministic, idempotent convergence pass over observable control-plane state."""
    def __init__(self, repository, agent_registry=None, retry_policy: RetryPolicy | None = None, metrics: ControlPlaneMetrics | None = None):
        self.repository=repository; self.agent_registry=agent_registry; self.retry_policy=retry_policy or RetryPolicy(); self.metrics=metrics or ControlPlaneMetrics()
    def reconcile_once(self, now: float | None = None) -> tuple[str, ...]:
        now=monotonic() if now is None else now; changed=[]; self.metrics.inc('reconcile_ticks'); tasks=self.repository.list_tasks()
        completed={t.task_id for t in tasks if t.status is TaskStatus.SUCCEEDED}
        for task in tasks:
            retry_due = task.retry_not_before is None or now >= task.retry_not_before
            if task.status in {TaskStatus.PENDING,TaskStatus.BLOCKED} and dependencies_satisfied(task,completed):
                self.repository.update_task(replace(task,status=TaskStatus.READY,retry_not_before=None)); self._record('TaskReady',task.task_id,None,task.status.value,TaskStatus.READY.value); changed.append(task.task_id)
            elif task.status is TaskStatus.RETRY_WAIT and retry_due and dependencies_satisfied(task,completed):
                self.repository.update_task(replace(task,status=TaskStatus.READY,retry_not_before=None)); self._record('TaskReady',task.task_id,None,task.status.value,TaskStatus.READY.value); changed.append(task.task_id)
        for lease in self.repository.list_leases():
            if lease.status in {LeaseStatus.ACTIVE,LeaseStatus.RENEWED,LeaseStatus.EXPIRING} and now >= lease.expires_at:
                task=self.repository.get_task(lease.task_id)
                if task is None:
                    continue
                if task.status in {TaskStatus.CLAIMED,TaskStatus.RUNNING}:
                    attempt=task.attempt+1
                    retry_not_before=None
                    target=TaskStatus.EXPIRED
                    delay_seconds=0.0
                    if attempt < task.max_attempts:
                        decision=self.retry_policy.decide(FailureClass.INFRASTRUCTURE,attempt,task.max_attempts)
                        target=TaskStatus.RETRY_WAIT
                        delay_seconds=decision.delay_seconds
                        retry_not_before=now+delay_seconds
                    event_id=str(uuid4())
                    event=Event(event_id,'LeaseExpired',now,'task',task.task_id,{'agent_id':lease.agent_id,'previous_state':task.status.value,'new_state':TaskStatus.EXPIRED.value})
                    audit=AuditRecord(event_id,now,lease.agent_id,'LeaseExpired','task',task.task_id,task.status.value,TaskStatus.EXPIRED.value,'RECORDED')
                    if hasattr(self.repository,'expire_and_reconcile'):
                        self.repository.expire_and_reconcile(lease.lease_id,now,event=event,audit=audit,retry_not_before=retry_not_before)
                    else:
                        self.repository.expire_lease(lease.lease_id,now)
                        self.repository.update_task(replace(task,attempt=attempt,status=TaskStatus.EXPIRED,retry_not_before=None))
                        if target is TaskStatus.RETRY_WAIT:
                            self.repository.update_task(replace(self.repository.get_task(task.task_id),status=TaskStatus.RETRY_WAIT,retry_not_before=retry_not_before))
                        self.repository.append_event(event); self.repository.append_audit(audit)
                    self.metrics.inc('lease_expiries')
                    if target is TaskStatus.RETRY_WAIT:
                        self.metrics.inc('task_retries')
                        self._record('TaskRetryScheduled',task.task_id,lease.agent_id,TaskStatus.EXPIRED.value,TaskStatus.RETRY_WAIT.value,{'failure_class':FailureClass.INFRASTRUCTURE.value,'delay_seconds':delay_seconds})
                    if self.agent_registry is not None:
                        previous=self.agent_registry.circuit_state(lease.agent_id)
                        self.agent_registry.record_failure(lease.agent_id)
                        current=self.agent_registry.circuit_state(lease.agent_id)
                        if current != previous:
                            self._record('AgentCircuitChanged',lease.task_id,lease.agent_id,previous.value,current.value,{'failure_count':self.agent_registry.failure_count(lease.agent_id)})
                    changed.append(task.task_id)
        if self.agent_registry is not None:
            self.agent_registry.reconcile()
            for agent in self.agent_registry.all():
                if self.agent_registry.circuit_state(agent.agent_id) is CircuitState.OPEN:
                    previous = self.agent_registry.circuit_state(agent.agent_id)
                    probed = self.agent_registry.probe_from_heartbeat(agent.agent_id)
                    current = self.agent_registry.circuit_state(agent.agent_id)
                    if current is not previous:
                        self._record('AgentCircuitChanged', None, agent.agent_id, previous.value, current.value, {'probe': True, 'success': probed})
        return tuple(changed)

    def _record(self, event_type, task_id, agent_id, previous_state, new_state, payload=None):
        event_id=str(uuid4()); timestamp=monotonic()
        data={'agent_id':agent_id,'previous_state':previous_state,'new_state':new_state}
        if payload: data.update(payload)
        self.repository.append_event(Event(event_id,event_type,timestamp,'task',task_id,data))
        self.repository.append_audit(AuditRecord(event_id,timestamp,agent_id or 'reconciler',event_type,'task',task_id,previous_state,new_state,'RECORDED'))
