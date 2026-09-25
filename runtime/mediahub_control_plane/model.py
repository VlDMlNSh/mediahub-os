from dataclasses import dataclass
from enum import Enum
from typing import Any

class AgentStatus(str, Enum):
    REGISTERING='REGISTERING'; ONLINE='ONLINE'; IDLE='IDLE'; CLAIMING='CLAIMING'; BUSY='BUSY'; VERIFYING='VERIFYING'; DEGRADED='DEGRADED'; UNHEALTHY='UNHEALTHY'; DISCONNECTED='DISCONNECTED'; DRAINING='DRAINING'; OFFLINE='OFFLINE'
class TaskStatus(str, Enum):
    PENDING='PENDING'; READY='READY'; CLAIMED='CLAIMED'; RUNNING='RUNNING'; VERIFYING='VERIFYING'; SUCCEEDED='SUCCEEDED'; FAILED='FAILED'; RETRY_WAIT='RETRY_WAIT'; BLOCKED='BLOCKED'; CANCELLED='CANCELLED'; EXPIRED='EXPIRED'
class LeaseStatus(str, Enum):
    ACTIVE='ACTIVE'; RENEWED='RENEWED'; EXPIRING='EXPIRING'; EXPIRED='EXPIRED'; RELEASED='RELEASED'; REVOKED='REVOKED'

@dataclass(frozen=True, slots=True)
class Node:
    node_id: str; hostname: str; platform: str; architecture: str; capabilities: tuple[str,...]=(); status: str='OFFLINE'; last_seen: float=0.0
@dataclass(frozen=True, slots=True)
class Agent:
    agent_id: str; node_id: str; version: str; status: AgentStatus=AgentStatus.REGISTERING; capabilities: tuple[str,...]=(); architecture: str|None=None
@dataclass(frozen=True, slots=True)
class Task:
    task_id: str; type: str; payload: Any=None; priority: int=0; status: TaskStatus=TaskStatus.PENDING; dependencies: tuple[str,...]=(); idempotency_key: str|None=None; attempt: int=0; max_attempts: int=1; required_capabilities: tuple[str,...]=(); architecture: str|None=None; retry_not_before: float|None=None
@dataclass(frozen=True, slots=True)
class Lease:
    lease_id: str; task_id: str; agent_id: str; created_at: float; expires_at: float; last_renewed_at: float; generation: int=1; status: LeaseStatus=LeaseStatus.ACTIVE
@dataclass(frozen=True, slots=True)
class Execution:
    execution_id: str; task_id: str; agent_id: str; lease_generation: int; status: str; result: Any=None
@dataclass(frozen=True, slots=True)
class Checkpoint:
    checkpoint_id: str; task_id: str; sequence: int; payload: Any
@dataclass(frozen=True, slots=True)
class Event:
    event_id: str; event_type: str; timestamp: float; entity_type: str; entity_id: str; payload: Any=None; correlation_id: str|None=None
@dataclass(frozen=True, slots=True)
class AuditRecord:
    event_id: str; timestamp: float; actor: str; action: str; resource: str; resource_id: str; previous_state: str|None; new_state: str|None; result: str; correlation_id: str|None=None

_TASK = {TaskStatus.PENDING:{TaskStatus.READY,TaskStatus.BLOCKED,TaskStatus.CANCELLED},TaskStatus.READY:{TaskStatus.CLAIMED,TaskStatus.CANCELLED,TaskStatus.BLOCKED},TaskStatus.CLAIMED:{TaskStatus.RUNNING,TaskStatus.EXPIRED,TaskStatus.CANCELLED},TaskStatus.RUNNING:{TaskStatus.VERIFYING,TaskStatus.FAILED,TaskStatus.EXPIRED},TaskStatus.VERIFYING:{TaskStatus.SUCCEEDED,TaskStatus.FAILED},TaskStatus.FAILED:{TaskStatus.RETRY_WAIT,TaskStatus.CANCELLED},TaskStatus.RETRY_WAIT:{TaskStatus.READY,TaskStatus.BLOCKED},TaskStatus.BLOCKED:{TaskStatus.READY,TaskStatus.CANCELLED},TaskStatus.EXPIRED:{TaskStatus.RETRY_WAIT,TaskStatus.CANCELLED}}
_AGENT = {AgentStatus.REGISTERING:{AgentStatus.ONLINE,AgentStatus.OFFLINE},AgentStatus.ONLINE:{AgentStatus.IDLE,AgentStatus.BUSY,AgentStatus.DEGRADED,AgentStatus.DRAINING,AgentStatus.OFFLINE},AgentStatus.IDLE:{AgentStatus.CLAIMING,AgentStatus.DRAINING,AgentStatus.OFFLINE,AgentStatus.DEGRADED},AgentStatus.CLAIMING:{AgentStatus.BUSY,AgentStatus.IDLE,AgentStatus.DEGRADED},AgentStatus.BUSY:{AgentStatus.VERIFYING,AgentStatus.IDLE,AgentStatus.DEGRADED,AgentStatus.DISCONNECTED},AgentStatus.VERIFYING:{AgentStatus.IDLE,AgentStatus.BUSY,AgentStatus.DEGRADED},AgentStatus.DEGRADED:{AgentStatus.ONLINE,AgentStatus.IDLE,AgentStatus.DISCONNECTED,AgentStatus.OFFLINE},AgentStatus.UNHEALTHY:{AgentStatus.DEGRADED,AgentStatus.OFFLINE},AgentStatus.DISCONNECTED:{AgentStatus.ONLINE,AgentStatus.DEGRADED,AgentStatus.OFFLINE},AgentStatus.DRAINING:{AgentStatus.IDLE,AgentStatus.OFFLINE}}
_LEASE = {LeaseStatus.ACTIVE:{LeaseStatus.RENEWED,LeaseStatus.EXPIRING,LeaseStatus.EXPIRED,LeaseStatus.REVOKED,LeaseStatus.RELEASED},LeaseStatus.RENEWED:{LeaseStatus.RENEWED,LeaseStatus.EXPIRING,LeaseStatus.EXPIRED,LeaseStatus.REVOKED,LeaseStatus.RELEASED},LeaseStatus.EXPIRING:{LeaseStatus.EXPIRED,LeaseStatus.RENEWED,LeaseStatus.REVOKED},LeaseStatus.EXPIRED:{LeaseStatus.RELEASED},LeaseStatus.REVOKED:{LeaseStatus.RELEASED}}
def _validate(table,current,target):
    if target not in table.get(current,set()): raise ValueError(f'invalid transition: {current} -> {target}')
def validate_task_transition(current,target): _validate(_TASK,current,target)
def validate_agent_transition(current,target): _validate(_AGENT,current,target)
def validate_lease_transition(current,target): _validate(_LEASE,current,target)
