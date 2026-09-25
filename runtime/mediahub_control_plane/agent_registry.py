from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone

from .model import Agent, AgentStatus, CircuitState


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
    def __init__(self, heartbeat_timeout_seconds: int = 30, dead_timeout_seconds: int = 90, failure_quarantine_threshold: int = 3):
        if heartbeat_timeout_seconds <= 0 or dead_timeout_seconds <= heartbeat_timeout_seconds:
            raise ValueError("timeouts must satisfy 0 < heartbeat_timeout < dead_timeout")
        self.heartbeat_timeout_seconds = heartbeat_timeout_seconds
        if failure_quarantine_threshold <= 0:
            raise ValueError("failure_quarantine_threshold must be positive")
        self.dead_timeout_seconds = dead_timeout_seconds
        self.failure_quarantine_threshold = failure_quarantine_threshold
        self._failure_counts: dict[str, int] = {}
        self._quarantined: set[str] = set()
        self._circuit: dict[str, CircuitState] = {}
        self._probe_in_flight: set[str] = set()
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
        self._circuit.setdefault(agent.agent_id, CircuitState.CLOSED)
        return updated

    def heartbeat(self, beat: Heartbeat) -> Agent:
        agent = self._agents.get(beat.agent_id)
        if agent is None:
            raise KeyError(beat.agent_id)
        if agent.node_id != beat.node_id:
            raise ValueError("heartbeat node does not match registered identity")
        self._last_heartbeat[beat.agent_id] = beat
        status = AgentStatus.IDLE if beat.health == "healthy" and agent.status in {AgentStatus.ONLINE, AgentStatus.DEGRADED, AgentStatus.DISCONNECTED} and beat.agent_id not in self._quarantined else agent.status
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

    def record_failure(self, agent_id: str) -> Agent:
        agent = self._agents[agent_id]
        count = self._failure_counts.get(agent_id, 0) + 1
        self._failure_counts[agent_id] = count
        if count >= self.failure_quarantine_threshold and agent.status not in {AgentStatus.OFFLINE, AgentStatus.DRAINING}:
            self._quarantined.add(agent_id)
            self._circuit[agent_id] = CircuitState.OPEN
            agent = replace(agent, status=AgentStatus.DEGRADED)
            self._agents[agent_id] = agent
        return agent

    def record_success(self, agent_id: str) -> Agent:
        agent = self._agents[agent_id]
        self._failure_counts[agent_id] = 0
        self._quarantined.discard(agent_id)
        self._circuit[agent_id] = CircuitState.CLOSED
        if agent.status == AgentStatus.DEGRADED:
            agent = replace(agent, status=AgentStatus.IDLE)
            self._agents[agent_id] = agent
        return agent

    def circuit_state(self, agent_id: str) -> CircuitState:
        return self._circuit.get(agent_id, CircuitState.CLOSED)

    def is_dispatch_allowed(self, agent_id: str) -> bool:
        return self.circuit_state(agent_id) is CircuitState.CLOSED

    def begin_probe(self, agent_id: str) -> bool:
        if self.circuit_state(agent_id) is not CircuitState.OPEN or agent_id in self._probe_in_flight:
            return False
        self._circuit[agent_id] = CircuitState.HALF_OPEN
        self._probe_in_flight.add(agent_id)
        return True

    def probe_result(self, agent_id: str, success: bool) -> Agent:
        if agent_id not in self._probe_in_flight:
            raise ValueError('no probe in flight')
        self._probe_in_flight.discard(agent_id)
        if success:
            return self.record_success(agent_id)
        self._circuit[agent_id] = CircuitState.OPEN
        return self._agents[agent_id]

    def probe_from_heartbeat(self, agent_id: str, now: datetime | None = None) -> bool:
        """Run at most one local recovery probe using the latest authenticated heartbeat."""
        if not self.begin_probe(agent_id):
            return False
        now = now or _utcnow()
        beat = self._last_heartbeat.get(agent_id)
        healthy = beat is not None and beat.health == 'healthy' and (now - beat.timestamp).total_seconds() < self.dead_timeout_seconds
        self.probe_result(agent_id, healthy)
        return healthy

    def failure_count(self, agent_id: str) -> int:
        return self._failure_counts.get(agent_id, 0)

    def get(self, agent_id: str) -> Agent:
        return self._agents[agent_id]

    def all(self) -> tuple[Agent, ...]:
        return tuple(self._agents.values())
