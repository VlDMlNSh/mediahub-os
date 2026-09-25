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
    """Bounded control-loop runtime; scheduling/execution remain injected policies."""
    def __init__(self, reconciler, scheduler, service, generation: int = 1, interval_seconds: float = 1.0):
        if interval_seconds <= 0:
            raise ValueError('interval_seconds must be positive')
        self.reconciler = reconciler
        self.scheduler = scheduler
        self.service = service
        self.generation = generation
        self.interval_seconds = interval_seconds
        self._stop = False
        self.stats = ControlLoopStats()

    def stop(self) -> None:
        self._stop = True

    def tick(self) -> ControlLoopStats:
        stats = self.stats
        try:
            changed = self.reconciler.reconcile_once()
            dispatched = 0
            for task in self.service.repository.list_tasks():
                if task.status.name == 'READY':
                    result = self.service.dispatch_once(task.task_id, self.scheduler, self.generation)
                    if getattr(result, 'agent_id', None):
                        dispatched += 1
            self.stats = ControlLoopStats(stats.ticks + 1, stats.reconciled + len(changed), stats.dispatched + dispatched, stats.errors)
        except Exception:
            self.stats = ControlLoopStats(stats.ticks + 1, stats.reconciled, stats.dispatched, stats.errors + 1)
        return self.stats

    def run(self, max_ticks: int | None = None) -> ControlLoopStats:
        ticks = 0
        while not self._stop and (max_ticks is None or ticks < max_ticks):
            started = monotonic()
            self.tick()
            ticks += 1
            if self._stop or (max_ticks is not None and ticks >= max_ticks):
                break
            sleep(max(0.0, self.interval_seconds - (monotonic() - started)))
        return self.stats
