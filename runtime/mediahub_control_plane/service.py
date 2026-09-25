from __future__ import annotations
from dataclasses import replace
from time import monotonic
from uuid import uuid4
from .model import AuditRecord, Execution, Event, FailureClass, TaskStatus, validate_task_transition
from .repository import ControlPlaneRepository
from .retry_policy import RetryPolicy
from .metrics import ControlPlaneMetrics

class ControlPlaneService:
    """Small deterministic coordinator for the first orchestration vertical slice."""
    def __init__(self, repository: ControlPlaneRepository, agent_registry=None, retry_backoff_seconds: float = 5.0, retry_policy: RetryPolicy | None = None, metrics: ControlPlaneMetrics | None = None):
        if retry_backoff_seconds < 0: raise ValueError("retry_backoff_seconds must be non-negative")
        self.repository=repository; self.agent_registry=agent_registry; self.retry_policy=retry_policy or RetryPolicy(retry_backoff_seconds); self.metrics=metrics or ControlPlaneMetrics()
        if self.agent_registry is not None:
            self.agent_registry.attach_metrics(self.metrics)
    def mark_ready(self, task_id: str) -> None:
        task=self.repository.get_task(task_id)
        if task is None: raise KeyError(task_id)
        validate_task_transition(task.status,TaskStatus.READY); self.repository.update_task(replace(task,status=TaskStatus.READY))
    def claim(self, task_id, agent_id, generation):
        try:
            lease=self.repository.claim_task(task_id,agent_id,generation)
        except (ValueError,PermissionError):
            self.metrics.inc('claim_conflicts'); raise
        self.metrics.inc('claims'); self._transition(task_id,TaskStatus.RUNNING); return lease
    def complete(self, task_id, agent_id, generation, result=None, lease_id=None):
        lease=self.repository.get_lease_for_task(task_id)
        if lease is None: raise KeyError(task_id)
        if lease_id is not None and lease.lease_id != lease_id:
            self.metrics.inc('fencing_failures'); raise PermissionError('stale lease identity')
        try:
            self.repository.assert_lease_owner(lease.lease_id,agent_id,generation)
        except PermissionError:
            self.metrics.inc('fencing_failures'); raise
        execution=Execution(str(uuid4()),task_id,agent_id,generation,'SUCCEEDED',result); self.repository.record_execution(execution)
        self._transition(task_id,TaskStatus.VERIFYING); self._transition(task_id,TaskStatus.SUCCEEDED); self.repository.release_lease(lease.lease_id,agent_id,generation); self._record('TaskSucceeded',task_id,agent_id,'SUCCEEDED'); return execution
    def fail(self, task_id, agent_id, generation, reason='EXECUTION_FAILED', failure_class: FailureClass = FailureClass.TASK, lease_id=None):
        lease=self.repository.get_lease_for_task(task_id)
        if lease is None: raise PermissionError('no authoritative lease')
        if lease_id is not None and lease.lease_id != lease_id:
            self.metrics.inc('fencing_failures'); raise PermissionError('stale lease identity')
        try:
            self.repository.assert_lease_owner(lease.lease_id,agent_id,generation)
        except PermissionError:
            self.metrics.inc('fencing_failures'); raise
        task=self.repository.get_task(task_id)
        if task is None: raise KeyError(task_id)
        attempt=task.attempt+1; self.repository.record_execution(Execution(str(uuid4()),task_id,agent_id,generation,'FAILED',reason,failure_class)); self.repository.update_task(replace(task,attempt=attempt,status=TaskStatus.FAILED))
        if attempt < task.max_attempts:
            decision = self.retry_policy.decide(failure_class, attempt, task.max_attempts)
            retry_at = monotonic() + decision.delay_seconds
            self.repository.update_task(replace(self.repository.get_task(task_id),status=TaskStatus.RETRY_WAIT,retry_not_before=retry_at)); self.metrics.inc('task_retries')
        self.repository.release_lease(lease.lease_id,agent_id,generation)
        if self.agent_registry is not None and failure_class in {FailureClass.WORKER, FailureClass.INFRASTRUCTURE}: self.agent_registry.record_failure(agent_id)
        self._record('TaskFailed',task_id,agent_id,reason); return self.repository.get_task(task_id)
    def recover_expired(self, task_id, now=None):
        lease=self.repository.get_lease_for_task(task_id)
        if lease is None: return False
        now=monotonic() if now is None else now
        if now < lease.expires_at: return False
        self.repository.expire_lease(lease.lease_id,now); task=self.repository.get_task(task_id)
        if task is None: raise KeyError(task_id)
        if task.status in (TaskStatus.CLAIMED,TaskStatus.RUNNING): self._transition(task_id,TaskStatus.EXPIRED)
        self._record('LeaseExpired',task_id,lease.agent_id,'RECOVERY_REQUIRED'); return True
    def _transition(self, task_id, target):
        task=self.repository.get_task(task_id)
        if task is None: raise KeyError(task_id)
        validate_task_transition(task.status,target); self.repository.update_task(replace(task,status=target))
    def _record(self,event_type,task_id,agent_id,result):
        event_id=str(uuid4()); self.repository.append_event(Event(event_id,event_type,monotonic(),'task',task_id,{'agent_id':agent_id})); self.repository.append_audit(AuditRecord(event_id,monotonic(),agent_id,event_type,'task',task_id,None,None,result))
    def dispatch_once(self, task_id, scheduler, generation, active_by_agent=None, failure_by_agent=None):
        task=self.repository.get_task(task_id)
        if task is None: raise KeyError(task_id)
        self.metrics.inc('dispatch_attempts')
        decision=scheduler.select(task) if active_by_agent is None and failure_by_agent is None else scheduler.select(task, active_by_agent=active_by_agent, failure_by_agent=failure_by_agent)
        if decision.agent_id is None:
            self.metrics.inc('dispatch_rejections'); return decision
        try:
            lease=self.repository.claim_task(task_id,decision.agent_id,generation,scheduler.max_concurrency_per_agent)
        except (ValueError,PermissionError) as exc:
            self.metrics.inc('claim_conflicts')
            reason='agent_capacity_exhausted' if 'capacity' in str(exc) else 'claim_lost_race'
            self.metrics.inc('dispatch_rejections'); return type(decision)(task_id,None,reason)
        self.metrics.inc('claims'); self.metrics.inc('dispatch_successes')
        self._transition(task_id,TaskStatus.RUNNING); return lease
