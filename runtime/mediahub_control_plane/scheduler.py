from __future__ import annotations
from dataclasses import dataclass
from .model import Agent, AgentStatus, Task

@dataclass(frozen=True, slots=True)
class ScheduleDecision:
    task_id: str
    agent_id: str | None
    reason: str

class TaskScheduler:
    def __init__(self, registry, dependency_resolver=None):
        self.registry = registry
        self.dependency_resolver = dependency_resolver

    @staticmethod
    def _eligible(agent: Agent, task: Task) -> bool:
        if agent.status not in {AgentStatus.ONLINE, AgentStatus.IDLE}:
            return False
        required = set(getattr(task, 'required_capabilities', ()) or ())
        return required.issubset(set(agent.capabilities))

    def select(self, task: Task, agents: tuple[Agent, ...] | None = None) -> ScheduleDecision:
        if task.status.name != 'READY':
            return ScheduleDecision(task.task_id, None, 'task_not_ready')
        agents = self.registry.all() if agents is None else agents
        candidates = sorted((a for a in agents if self._eligible(a, task)), key=lambda a: a.agent_id)
        if not candidates:
            return ScheduleDecision(task.task_id, None, 'no_eligible_agent')
        return ScheduleDecision(task.task_id, candidates[0].agent_id, 'eligible')
