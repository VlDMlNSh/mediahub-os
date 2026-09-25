from __future__ import annotations
from dataclasses import dataclass
from .model import Agent, AgentStatus, Task, TaskStatus

@dataclass(frozen=True, slots=True)
class ScheduleDecision:
    task_id: str
    agent_id: str | None
    reason: str

class TaskScheduler:
    """Deterministic capability/architecture-aware selector."""
    def __init__(self, registry, dependency_resolver=None):
        self.registry = registry
        self.dependency_resolver = dependency_resolver

    @staticmethod
    def _eligible(agent: Agent, task: Task) -> bool:
        if agent.status not in {AgentStatus.ONLINE, AgentStatus.IDLE}:
            return False
        if task.architecture is not None and agent.architecture != task.architecture:
            return False
        required = set(task.required_capabilities)
        return required.issubset(agent.capabilities)

    def select(self, task: Task, agents: tuple[Agent, ...] | None = None) -> ScheduleDecision:
        if task.status is not TaskStatus.READY:
            return ScheduleDecision(task.task_id, None, 'task_not_ready')
        if self.dependency_resolver is not None and not self.dependency_resolver(task):
            return ScheduleDecision(task.task_id, None, 'dependencies_blocked')
        agents = self.registry.all() if agents is None else agents
        candidates = sorted((a for a in agents if self._eligible(a, task)), key=lambda a: a.agent_id)
        if not candidates:
            return ScheduleDecision(task.task_id, None, 'no_eligible_agent')
        return ScheduleDecision(task.task_id, candidates[0].agent_id, 'eligible')

    def order_ready(self, tasks: tuple[Task, ...]) -> tuple[Task, ...]:
        """Priority-first deterministic queue ordering; task_id is the stable tie-breaker."""
        return tuple(sorted((t for t in tasks if t.status is TaskStatus.READY),
                            key=lambda t: (-t.priority, t.task_id)))
