from __future__ import annotations
from threading import RLock
from .model import Task, Lease, Execution, Event, AuditRecord, TaskStatus, LeaseStatus

class ControlPlaneRepository:
    def create_task(self, task: Task) -> Task: raise NotImplementedError
    def get_task(self, task_id: str) -> Task|None: raise NotImplementedError
    def claim_task(self, task_id: str, agent_id: str, generation: int) -> Lease: raise NotImplementedError
    def renew_lease(self, lease_id: str, agent_id: str, generation: int, expires_at: float) -> Lease: raise NotImplementedError
    def record_execution(self, execution: Execution) -> Execution: raise NotImplementedError
    def append_event(self, event: Event) -> Event: raise NotImplementedError
    def append_audit(self, record: AuditRecord) -> AuditRecord: raise NotImplementedError
    def update_task(self, task: Task) -> Task: raise NotImplementedError
    def get_lease_for_task(self, task_id: str) -> Lease | None: raise NotImplementedError
    def assert_lease_owner(self, lease_id: str, agent_id: str, generation: int) -> None: raise NotImplementedError
    def release_lease(self, lease_id: str, agent_id: str, generation: int) -> Lease: raise NotImplementedError
    def expire_lease(self, lease_id: str, now: float) -> Lease: raise NotImplementedError

class InMemoryControlPlaneRepository(ControlPlaneRepository):
    """Deterministic reference repository; not durable production persistence."""
    def __init__(self):
        self._lock=RLock(); self.tasks={}; self.leases={}; self.executions={}; self.events={}; self.audit={}; self._task_keys={}; self._lease_by_task={}
    def create_task(self, task):
        with self._lock:
            if task.task_id in self.tasks: raise ValueError('duplicate task_id')
            if task.idempotency_key and task.idempotency_key in self._task_keys: raise ValueError('duplicate idempotency_key')
            self.tasks[task.task_id]=task
            if task.idempotency_key: self._task_keys[task.idempotency_key]=task.task_id
            return task
    def get_task(self, task_id):
        with self._lock: return self.tasks.get(task_id)
    def claim_task(self, task_id, agent_id, generation):
        import time, uuid
        with self._lock:
            task=self.tasks.get(task_id)
            if task is None: raise KeyError(task_id)
            if task.status is not TaskStatus.READY: raise ValueError('task not claimable')
            if task_id in self._lease_by_task: raise ValueError('task already leased')
            lease=Lease(str(uuid.uuid4()),task_id,agent_id,time.monotonic(),time.monotonic()+60,time.monotonic(),generation,LeaseStatus.ACTIVE)
            from dataclasses import replace
            self.tasks[task_id]=replace(task, status=TaskStatus.CLAIMED)
            self.leases[lease.lease_id]=lease; self._lease_by_task[task_id]=lease.lease_id
            return lease
    def renew_lease(self, lease_id, agent_id, generation, expires_at):
        import dataclasses
        with self._lock:
            lease=self.leases.get(lease_id)
            if not lease: raise KeyError(lease_id)
            if lease.agent_id != agent_id or lease.generation != generation: raise PermissionError('stale lease owner')
            if lease.status not in (LeaseStatus.ACTIVE,LeaseStatus.RENEWED): raise ValueError('lease not renewable')
            lease=dataclasses.replace(lease,expires_at=expires_at,last_renewed_at=__import__('time').monotonic(),status=LeaseStatus.RENEWED)
            self.leases[lease_id]=lease; return lease
    def record_execution(self, execution):
        with self._lock:
            if execution.execution_id in self.executions: return self.executions[execution.execution_id]
            lease_id=self._lease_by_task.get(execution.task_id)
            lease=self.leases.get(lease_id) if lease_id else None
            if not lease or lease.agent_id != execution.agent_id or lease.generation != execution.lease_generation: raise PermissionError('stale execution')
            self.executions[execution.execution_id]=execution; return execution
    def append_event(self,event):
        with self._lock:
            if event.event_id in self.events: return self.events[event.event_id]
            self.events[event.event_id]=event; return event
    def append_audit(self,record):
        with self._lock:
            if record.event_id in self.audit: return self.audit[record.event_id]
            self.audit[record.event_id]=record; return record
    def update_task(self, task):
        from .model import validate_task_transition
        with self._lock:
            current=self.tasks.get(task.task_id)
            if current is None: raise KeyError(task.task_id)
            validate_task_transition(current.status, task.status)
            self.tasks[task.task_id]=task; return task
    def get_lease_for_task(self, task_id):
        with self._lock:
            lid=self._lease_by_task.get(task_id)
            return self.leases.get(lid) if lid else None
    def assert_lease_owner(self, lease_id, agent_id, generation):
        import time
        with self._lock:
            lease=self.leases.get(lease_id)
            if not lease or lease.agent_id != agent_id or lease.generation != generation or lease.status not in (LeaseStatus.ACTIVE, LeaseStatus.RENEWED) or time.monotonic() >= lease.expires_at:
                raise PermissionError('stale lease owner')
    def release_lease(self, lease_id, agent_id, generation):
        from dataclasses import replace
        with self._lock:
            lease=self.leases.get(lease_id)
            if not lease or lease.agent_id != agent_id or lease.generation != generation: raise PermissionError('stale lease owner')
            if lease.status not in (LeaseStatus.ACTIVE, LeaseStatus.RENEWED): raise ValueError('lease not releasable')
            lease=replace(lease,status=LeaseStatus.RELEASED); self.leases[lease_id]=lease; self._lease_by_task.pop(lease.task_id,None); return lease
    def expire_lease(self, lease_id, now):
        from dataclasses import replace
        with self._lock:
            lease=self.leases.get(lease_id)
            if not lease: raise KeyError(lease_id)
            if now < lease.expires_at: raise ValueError('lease has not expired')
            if lease.status not in (LeaseStatus.ACTIVE, LeaseStatus.RENEWED, LeaseStatus.EXPIRING): raise ValueError('lease not expirable')
            lease=replace(lease,status=LeaseStatus.EXPIRED); self.leases[lease_id]=lease; return lease
