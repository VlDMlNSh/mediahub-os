from __future__ import annotations
from dataclasses import dataclass
from time import monotonic, sleep
from .metrics import ControlPlaneMetrics

@dataclass(frozen=True, slots=True)
class ControlLoopStats:
    ticks: int = 0
    reconciled: int = 0
    dispatched: int = 0
    errors: int = 0

class ControlLoop:
    def __init__(self, reconciler, scheduler, service, generation=1, interval_seconds=1.0, metrics: ControlPlaneMetrics | None = None):
        if interval_seconds <= 0: raise ValueError('interval_seconds must be positive')
        self.reconciler=reconciler; self.scheduler=scheduler; self.service=service; self.generation=generation; self.interval_seconds=interval_seconds; self._stop=False; self.stats=ControlLoopStats(); self.metrics=metrics or service.metrics
    def stop(self): self._stop=True
    def tick(self):
        try:
            changed=self.reconciler.reconcile_once(); dispatched=0
            repo=self.service.repository
            active_by_agent={}
            for lease in repo.list_leases():
                if lease.status.name in {'ACTIVE','RENEWED','EXPIRING'}:
                    active_by_agent[lease.agent_id]=active_by_agent.get(lease.agent_id,0)+1
            failure_by_task_agent={}
            for execution in repo.list_executions():
                if execution.status == 'FAILED':
                    key=(execution.task_id,execution.agent_id); failure_by_task_agent[key]=failure_by_task_agent.get(key,0)+1
            tasks=self.scheduler.order_ready(repo.list_tasks())
            for task in tasks:
                failures={a.agent_id:failure_by_task_agent.get((task.task_id,a.agent_id),0) for a in self.scheduler.registry.all()}
                decision=self.scheduler.select(task, active_by_agent=active_by_agent, failure_by_agent=failures)
                if decision.agent_id is None: continue
                result=self.service.dispatch_once(task.task_id,self.scheduler,self.generation,active_by_agent,failures)
                if getattr(result,'agent_id',None):
                    dispatched += 1
                    active_by_agent[result.agent_id]=active_by_agent.get(result.agent_id,0)+1
            self.stats=ControlLoopStats(self.stats.ticks+1,self.stats.reconciled+len(changed),self.stats.dispatched+dispatched,self.stats.errors)
        except Exception:
            self.metrics.inc('reconcile_errors'); self.stats=ControlLoopStats(self.stats.ticks+1,self.stats.reconciled,self.stats.dispatched,self.stats.errors+1)
        return self.stats
    def run(self,max_ticks=None):
        while not self._stop and (max_ticks is None or self.stats.ticks < max_ticks):
            started=monotonic(); self.tick()
            if self._stop or (max_ticks is not None and self.stats.ticks >= max_ticks): break
            sleep(max(0,self.interval_seconds-(monotonic()-started)))
        return self.stats
