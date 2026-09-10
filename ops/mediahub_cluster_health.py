"""Observation-only Local MediaHub Cluster node health contract.

Health is distinct from identity, trust and authorization. It never grants
membership or execution rights.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class NodeHealth(StrEnum):
    UNKNOWN = "UNKNOWN"
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    FAILED = "FAILED"


class HealthObservationDenied(ValueError):
    """Raised when a health observation is incomplete or ambiguous."""


@dataclass(frozen=True)
class NodeHealthObservation:
    node_id: str
    health: NodeHealth
    source_sha: str


class LocalClusterHealth:
    """Accept immutable observations without changing trust or authority."""

    def __init__(self) -> None:
        self._observations: dict[str, NodeHealthObservation] = {}

    def observe(self, observation: NodeHealthObservation) -> NodeHealthObservation:
        if not observation.node_id or not observation.source_sha:
            raise HealthObservationDenied("node identity and provenance are required")
        if observation.health is NodeHealth.UNKNOWN:
            raise HealthObservationDenied("unknown health cannot be used as evidence")
        self._observations[observation.node_id] = observation
        return observation

    def get(self, node_id: str) -> NodeHealthObservation | None:
        return self._observations.get(node_id)

    def is_eligible_for_observation_only(self, node_id: str) -> bool:
        observation = self.get(node_id)
        return observation is not None and observation.health is NodeHealth.HEALTHY
