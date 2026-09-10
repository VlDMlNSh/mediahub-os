"""Deterministic Local Cluster workload lifecycle and bounded failover."""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import ClassVar


class LifecycleState(StrEnum):
    ADMITTED = "ADMITTED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REASSIGNED = "REASSIGNED"
    VERIFIED = "VERIFIED"
    RECOVERED = "RECOVERED"


class FailureClass(StrEnum):
    NODE_FAILED = "NODE_FAILED"
    WORKLOAD_FAILED = "WORKLOAD_FAILED"
    AMBIGUOUS = "AMBIGUOUS"


class LifecycleDenied(PermissionError):
    """Raised when a lifecycle transition or failover is unsafe."""


@dataclass(frozen=True)
class WorkloadIdentity:
    workload_id: str
    assignment_id: str
    node_id: str
    request_id: str
    source_sha: str


@dataclass(frozen=True)
class LifecycleRecord:
    identity: WorkloadIdentity
    state: LifecycleState
    transition_id: str


@dataclass(frozen=True)
class FailoverDecision:
    allowed: bool
    failure: FailureClass
    reason: str


class ClusterWorkloadLifecycle:
    """In-memory lifecycle boundary; no authority or execution side effects."""

    _allowed: ClassVar[dict[LifecycleState, set[LifecycleState]]] = {
        LifecycleState.ADMITTED: {LifecycleState.RUNNING, LifecycleState.FAILED},
        LifecycleState.RUNNING: {LifecycleState.COMPLETED, LifecycleState.FAILED},
        LifecycleState.FAILED: {LifecycleState.REASSIGNED},
        LifecycleState.REASSIGNED: {LifecycleState.VERIFIED, LifecycleState.FAILED},
        LifecycleState.VERIFIED: {LifecycleState.RECOVERED},
    }

    def __init__(self) -> None:
        self._records: dict[str, LifecycleRecord] = {}
        self._assignments: set[str] = set()

    def admit(self, identity: WorkloadIdentity) -> LifecycleRecord:
        self._validate(identity)
        if identity.workload_id in self._records:
            raise LifecycleDenied("duplicate workload")
        if identity.assignment_id in self._assignments:
            raise LifecycleDenied("duplicate assignment")
        record = LifecycleRecord(identity, LifecycleState.ADMITTED, self._transition(identity, "admitted"))
        self._records[identity.workload_id] = record
        self._assignments.add(identity.assignment_id)
        return record

    def transition(self, workload_id: str, state: LifecycleState) -> LifecycleRecord:
        current = self._records.get(workload_id)
        if current is None:
            raise LifecycleDenied("unknown workload")
        if state not in self._allowed.get(current.state, set()):
            raise LifecycleDenied("invalid lifecycle transition")
        updated = LifecycleRecord(current.identity, state, self._transition(current.identity, state.value))
        self._records[workload_id] = updated
        return updated

    def failover(self, workload_id: str, failure: FailureClass) -> FailoverDecision:
        current = self._records.get(workload_id)
        if current is None:
            raise LifecycleDenied("unknown workload")
        if current.state is not LifecycleState.RUNNING:
            raise LifecycleDenied("failover requires running workload")
        if failure is FailureClass.AMBIGUOUS:
            return FailoverDecision(False, failure, "ambiguous failure is fail-closed")
        self.transition(workload_id, LifecycleState.FAILED)
        return FailoverDecision(True, failure, "bounded failover permitted")

    def reassign(self, workload_id: str, new_assignment_id: str, new_node_id: str) -> LifecycleRecord:
        current = self._records.get(workload_id)
        if current is None:
            raise LifecycleDenied("unknown workload")
        if current.state is not LifecycleState.FAILED:
            raise LifecycleDenied("reassignment requires failed workload")
        if not new_assignment_id or not new_node_id:
            raise LifecycleDenied("replacement assignment identity is required")
        if new_assignment_id in self._assignments:
            raise LifecycleDenied("duplicate reassignment")
        identity = WorkloadIdentity(
            current.identity.workload_id,
            new_assignment_id,
            new_node_id,
            current.identity.request_id,
            current.identity.source_sha,
        )
        self._assignments.add(new_assignment_id)
        record = LifecycleRecord(identity, LifecycleState.REASSIGNED, self._transition(identity, "reassigned"))
        self._records[workload_id] = record
        return record

    def record(self, workload_id: str) -> LifecycleRecord:
        record = self._records.get(workload_id)
        if record is None:
            raise LifecycleDenied("unknown workload")
        return record

    @staticmethod
    def _validate(identity: WorkloadIdentity) -> None:
        if not all((identity.workload_id, identity.assignment_id, identity.node_id,
                    identity.request_id, identity.source_sha)):
            raise LifecycleDenied("all workload identity and provenance fields are required")

    @staticmethod
    def _transition(identity: WorkloadIdentity, label: str) -> str:
        return f"{identity.workload_id}:{identity.assignment_id}:{label}:{identity.source_sha}"
