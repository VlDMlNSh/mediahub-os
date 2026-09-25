from __future__ import annotations
from dataclasses import dataclass
from time import monotonic, sleep

@dataclass(frozen=True, slots=True)
class ControlLoopStats:
    ticks: int = 0
    reconciled: int = 0
    dispatched: int = 0
    errors: int = 0

class ControlLoop:
    def __init__(self, reconciler, scheduler, service, generation=1, interval_seconds=1.0):
        if interval_seconds <= 0: raise ValueError('interval_seconds must be positive')
        self.reconciler=reconciler; self.scheduler=scheduler; self.service=service; self.generation=generation; self.interval_seconds=interval_seconds; self._stop=False; self.stats=ControlLoopStats()
    def stop(self): self._stop=True
    def tick(self):
        try:
            changed=self.reconciler.reconcile_once(); dispatched=0
            tasks=self.scheduler.order_ready(self.service.repository.list_tasks())
            for task in tasks:
                result=self.service.dispatch_once(task.task_id,self.scheduler,self.generation)
                if getattr(result,'agent_id',None): dispatched += 1
            self.stats=ControlLoopStats(self.stats.ticks+1,self.stats.reconciled+len(changed),self.stats.dispatched+dispatched,self.stats.errors)
        except Exception:
            self.stats=ControlLoopStats(self.stats.ticks+1,self.stats.reconciled,self.stats.dispatched,self.stats.errors+1)
        return self.stats
    def run(self,max_ticks=None):
        while not self._stop and (max_ticks is None or self.stats.ticks < max_ticks):
            started=monotonic(); self.tick()
            if self._stop or (max_ticks is not None and self.stats.ticks >= max_ticks): break
            sleep(max(0,self.interval_seconds-(monotonic()-started)))
        return self.stats
