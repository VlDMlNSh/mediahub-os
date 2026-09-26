from __future__ import annotations

from dataclasses import dataclass
from threading import Event, Thread
from time import monotonic, sleep
from typing import Any, Callable

from .worker import LeaseLost, WorkerRuntime


@dataclass(frozen=True, slots=True)
class WorkerLoopStats:
    polls: int = 0
    executed: int = 0
    failures: int = 0


class WorkerLoop:
    """Persistent worker lifecycle: poll, execute assigned work, then return to idle."""

    def __init__(self, repository, worker: WorkerRuntime, agent_id: str, generation: int,
                 executor_for: Callable[[str], Callable[[Any, Any], Any]],
                 verifier_for: Callable[[str], Callable[[Any], bool]],
                 interval_seconds: float = 1.0, renewal_interval_seconds: float = 1.0):
        if interval_seconds <= 0 or renewal_interval_seconds <= 0:
            raise ValueError("interval_seconds and renewal_interval_seconds must be positive")
        self.repository = repository
        self.worker = worker
        self.agent_id = agent_id
        self.generation = generation
        self.executor_for = executor_for
        self.verifier_for = verifier_for
        self.interval_seconds = interval_seconds
        self.renewal_interval_seconds = renewal_interval_seconds
        self._stop = Event()
        self.stats = WorkerLoopStats()

    def stop(self) -> None:
        self._stop.set()

    def poll_once(self) -> WorkerLoopStats:
        executed = failures = 0
        for lease in self.repository.list_leases():
            if lease.agent_id != self.agent_id or lease.generation != self.generation:
                continue
            task = self.repository.get_task(lease.task_id)
            if task is None or task.status.name != "RUNNING":
                continue
            try:
                executor = self.executor_for(task.type)
                def supervised_executor(payload, context):
                    lost = Event()
                    supervisor = LeaseRenewalSupervisor(context.renew, self.renewal_interval_seconds, lost.set)
                    supervisor.start()
                    try:
                        result = executor(payload, context)
                        if lost.is_set():
                            raise LeaseLost("lease renewal lost during execution")
                        return result
                    finally:
                        supervisor.stop()
                self.worker.execute(task.task_id, self.agent_id, self.generation,
                                    supervised_executor, self.verifier_for(task.type))
                executed += 1
            except LeaseLost:
                failures += 1
            except Exception:
                failures += 1
        previous = self.stats
        self.stats = WorkerLoopStats(previous.polls + 1, previous.executed + executed,
                                     previous.failures + failures)
        return self.stats

    def run(self, max_polls: int | None = None) -> WorkerLoopStats:
        polls = 0
        while not self._stop.is_set() and (max_polls is None or polls < max_polls):
            started = monotonic()
            self.poll_once()
            polls += 1
            if self._stop.is_set() or (max_polls is not None and polls >= max_polls):
                break
            sleep(max(0.0, self.interval_seconds - (monotonic() - started)))
        return self.stats


class LeaseRenewalSupervisor:
    """Renews a lease independently of task execution; loss is surfaced through a callback."""

    def __init__(self, renew: Callable[[], Any], interval_seconds: float, on_lost: Callable[[], None]):
        if interval_seconds <= 0:
            raise ValueError("interval_seconds and renewal_interval_seconds must be positive")
        self.renew = renew
        self.interval_seconds = interval_seconds
        self.on_lost = on_lost
        self._stop = Event()
        self._thread: Thread | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = Thread(target=self._run, name="mediahub-lease-renewer", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=max(1.0, self.interval_seconds * 2))
            self._thread = None

    def _run(self) -> None:
        # Establish a renewal immediately so very short-lived leases do not
        # depend on scheduler timing before the first interval elapses.
        try:
            self.renew()
        except Exception:
            self.on_lost()
            return
        while not self._stop.wait(self.interval_seconds):
            try:
                self.renew()
            except Exception:
                self.on_lost()
                return
