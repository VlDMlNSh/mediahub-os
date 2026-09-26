from __future__ import annotations
from dataclasses import dataclass
from .model import Agent, AgentStatus, Task, TaskStatus

@dataclass(frozen=True, slots=True)
class ScheduleDecision:
    task_id: str
    agent_id: str | None
    reason: str

class TaskScheduler:
    """Deterministic capability/architecture-aware scheduler with bounded fair admission."""
    def __init__(self, registry, dependency_resolver=None, max_concurrency_per_agent: int = 1):
        if max_concurrency_per_agent <= 0: raise ValueError('max_concurrency_per_agent must be positive')
        self.registry=registry; self.dependency_resolver=dependency_resolver; self.max_concurrency_per_agent=max_concurrency_per_agent

    @staticmethod
    def _eligible(agent: Agent, task: Task) -> bool:
        if agent.status not in {AgentStatus.ONLINE, AgentStatus.IDLE}: return False
        if task.architecture is not None and agent.architecture != task.architecture: return False
        return set(task.required_capabilities).issubset(agent.capabilities)

    def select(self, task: Task, agents: tuple[Agent, ...] | None = None, active_by_agent: dict[str, int] | None = None, failure_by_agent: dict[str, int] | None = None) -> ScheduleDecision:
        if task.status is not TaskStatus.READY: return ScheduleDecision(task.task_id,None,'task_not_ready')
        if self.dependency_resolver is not None and not self.dependency_resolver(task): return ScheduleDecision(task.task_id,None,'dependencies_blocked')
        agents=self.registry.all() if agents is None else agents; active_by_agent={} if active_by_agent is None else active_by_agent; failure_by_agent={} if failure_by_agent is None else failure_by_agent
        candidates=[a for a in agents if self._eligible(a,task) and self.registry.is_dispatch_allowed(a.agent_id) and active_by_agent.get(a.agent_id,0)<self.max_concurrency_per_agent]
        if not candidates:
            compatible=[a for a in agents if (task.architecture is None or a.architecture == task.architecture) and set(task.required_capabilities).issubset(a.capabilities)]
            if any(not self.registry.is_dispatch_allowed(a.agent_id) for a in compatible): return ScheduleDecision(task.task_id,None,'agent_circuit_open')
            if any(self._eligible(a,task) for a in agents): return ScheduleDecision(task.task_id,None,'agent_capacity_exhausted')
            return ScheduleDecision(task.task_id,None,'no_eligible_agent')
        # Least-loaded first prevents deterministic starvation while task_id remains the tie-break.
        candidates.sort(key=lambda a:(active_by_agent.get(a.agent_id,0),failure_by_agent.get(a.agent_id,0),a.agent_id))
        return ScheduleDecision(task.task_id,candidates[0].agent_id,'eligible')

    def order_ready(self, tasks: tuple[Task, ...]) -> tuple[Task, ...]:
        return tuple(sorted((t for t in tasks if t.status is TaskStatus.READY), key=lambda t:(-t.priority,t.task_id)))
