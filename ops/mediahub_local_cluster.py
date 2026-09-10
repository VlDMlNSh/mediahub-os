"""Provider-neutral Local MediaHub Cluster admission and scheduling contract.

The cluster is compute infrastructure, not an authority. It emits a bounded
assignment proposal; canonical mutation remains outside this module.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class NodeState(StrEnum):
    READY = "READY"
    DEGRADED = "DEGRADED"
    QUARANTINED = "QUARANTINED"


class WorkloadClass(StrEnum):
    INFERENCE = "INFERENCE"
    MEDIA = "MEDIA"
    BATCH = "BATCH"


class ClusterDenied(PermissionError):
    """Raised when cluster admission cannot be proven safe."""


@dataclass(frozen=True)
class ClusterNode:
    node_id: str
    state: NodeState
    cpu_capacity: int
    memory_mb: int
    gpu_count: int = 0


@dataclass(frozen=True)
class ClusterWorkload:
    workload_id: str
    workload_class: WorkloadClass
    cpu: int
    memory_mb: int
    gpu: int = 0
    source_sha: str = ""


@dataclass(frozen=True)
class ClusterAssignment:
    workload_id: str
    node_id: str
    source_sha: str
    policy: str = "local-cluster-v1"


@dataclass(frozen=True)
class LocalClusterScheduler:
    """Deterministic scheduler with fail-closed admission rules."""

    nodes: tuple[ClusterNode, ...]

    def admit(self, workload: ClusterWorkload) -> None:
        if not workload.workload_id or not workload.source_sha:
            raise ClusterDenied("workload identity and provenance are required")
        if workload.cpu <= 0 or workload.memory_mb <= 0:
            raise ClusterDenied("workload resource requests must be positive")
        if workload.gpu < 0:
            raise ClusterDenied("GPU request cannot be negative")
        if workload.workload_class not in WorkloadClass:
            raise ClusterDenied("unsupported workload class")

    def schedule(self, workload: ClusterWorkload) -> ClusterAssignment:
        self.admit(workload)
        candidates = [node for node in self.nodes if self._fits(node, workload)]
        if not candidates:
            raise ClusterDenied("no trusted ready node satisfies workload")
        node = min(candidates, key=lambda item: (item.node_id, item.gpu_count))
        return ClusterAssignment(workload.workload_id, node.node_id, workload.source_sha)

    @staticmethod
    def _fits(node: ClusterNode, workload: ClusterWorkload) -> bool:
        return (
            node.state is NodeState.READY
            and node.cpu_capacity >= workload.cpu
            and node.memory_mb >= workload.memory_mb
            and node.gpu_count >= workload.gpu
        )
