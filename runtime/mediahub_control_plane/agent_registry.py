from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from .model import Agent, AgentStatus


@dataclass(frozen=True)
class Heartbeat:
    agent_id: str
    node_id: str
    timestamp: datetime
    uptime_seconds: int = 0
    load: float = 0.0
    memory_percent: float = 0.0
    disk_percent: float = 0.0
    network_ok: bool = True
    capabilities: tuple[str, ...] = ()
    version: str = ""
    health: str = "healthy"


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class AgentRegistry:
    def __init__(self, heartbeat_timeout_seconds: int = 30, dead_timeout_seconds: int = 90):
        if heartbeat_timeout_seconds <= 0 or dead_timeout_seconds <= heartbeat_timeout_seconds:
            raise ValueError("timeouts must satisfy 0 < heartbeat_timeout < dead_timeout")
        self.heartbeat_timeout_seconds = heartbeat_timeout_seconds
        self.dead_timeout_seconds = dead_timeout_seconds
        self._agents: dict[str, Agent] = {}
        self._last_heartbeat: dict[str, Heartbeat] = {}

    def register(self, agent: Agent, now: datetime | None = None) -> Agent:
        now = now or _utcnow()
        current = self._agents.get(agent.agent_id)
        if current is not None and current.node_id != agent.node_id:
            raise ValueError("agent identity already bound to another node")
        status = AgentStatus.ONLINE if agent.status == AgentStatus.REGISTERING else agent.status
        updated = replace(agent, status=status)
        self._agents[agent.agent_id] = updated
        return updated

    def heartbeat(self, beat: Heartbeat) -> Agent:
        agent = self._agents.get(beat.agent_id)
        if agent is None:
            raise KeyError(beat.agent_id)
        if agent.node_id != beat.node_id:
            raise ValueError("heartbeat node does not match registered identity")
        self._last_heartbeat[beat.agent_id] = beat
        status = AgentStatus.IDLE if beat.health == "healthy" and agent.status in {AgentStatus.ONLINE, AgentStatus.DEGRADED, AgentStatus.DISCONNECTED} else agent.status
        if beat.health != "healthy":
            status = AgentStatus.DEGRADED
        self._agents[beat.agent_id] = replace(agent, status=status, version=beat.version or agent.version, capabilities=beat.capabilities or agent.capabilities)
        return self._agents[beat.agent_id]

    def reconcile(self, now: datetime | None = None) -> dict[str, AgentStatus]:
        now = now or _utcnow()
        changes: dict[str, AgentStatus] = {}
        for agent_id, agent in list(self._agents.items()):
            beat = self._last_heartbeat.get(agent_id)
            if beat is None:
                continue
            age = max(0.0, (now - beat.timestamp).total_seconds())
            if age >= self.dead_timeout_seconds and agent.status != AgentStatus.OFFLINE:
                self._agents[agent_id] = replace(agent, status=AgentStatus.OFFLINE)
                changes[agent_id] = AgentStatus.OFFLINE
            elif age >= self.heartbeat_timeout_seconds and agent.status not in {AgentStatus.DEGRADED, AgentStatus.DISCONNECTED, AgentStatus.OFFLINE} and agent.status != AgentStatus.DRAINING:
                self._agents[agent_id] = replace(agent, status=AgentStatus.DEGRADED)
                changes[agent_id] = AgentStatus.DEGRADED
        return changes

    def get(self, agent_id: str) -> Agent:
        return self._agents[agent_id]

    def all(self) -> tuple[Agent, ...]:
        return tuple(self._agents.values())
