"""Deterministic Local MediaHub Cluster resource accounting contract."""
from __future__ import annotations

from dataclasses import dataclass


class ResourceDenied(PermissionError):
    """Raised when a resource reservation cannot be proven safe."""


@dataclass(frozen=True)
class ResourceCapacity:
    cpu: int
    memory_mb: int
    gpu: int = 0


@dataclass(frozen=True)
class ResourceReservation:
    workload_id: str
    node_id: str
    capacity: ResourceCapacity


class ClusterResourceLedger:
    """Tracks reservations without mutating cluster authority or node trust."""

    def __init__(self, capacities: dict[str, ResourceCapacity]) -> None:
        self._capacities = dict(capacities)
        self._reservations: dict[str, ResourceReservation] = {}

    def reserve(self, reservation: ResourceReservation) -> ResourceReservation:
        self._validate(reservation)
        if reservation.workload_id in self._reservations:
            raise ResourceDenied("duplicate workload reservation")
        capacity = self._capacities.get(reservation.node_id)
        if capacity is None:
            raise ResourceDenied("unknown node capacity")
        used = self._used(reservation.node_id)
        if not self._fits(capacity, used, reservation.capacity):
            raise ResourceDenied("resource overcommit denied")
        self._reservations[reservation.workload_id] = reservation
        return reservation

    def can_replace(self, reservation: ResourceReservation) -> bool:
        """Check replacement admission without changing the reservation ledger."""
        self._validate(reservation)
        current = self._reservations.get(reservation.workload_id)
        if current is None:
            return False
        capacity = self._capacities.get(reservation.node_id)
        if capacity is None:
            return False
        return self._fits(
            capacity,
            self._used_excluding(reservation.node_id, reservation.workload_id),
            reservation.capacity,
        )

    def replace(self, reservation: ResourceReservation) -> ResourceReservation:
        """Atomically replace an existing workload reservation if it fits."""
        self._validate(reservation)
        current = self._reservations.get(reservation.workload_id)
        if current is None:
            raise ResourceDenied("unknown workload reservation")
        capacity = self._capacities.get(reservation.node_id)
        if capacity is None:
            raise ResourceDenied("unknown node capacity")
        used = self._used_excluding(reservation.node_id, reservation.workload_id)
        if not self._fits(capacity, used, reservation.capacity):
            raise ResourceDenied("resource overcommit denied")
        self._reservations[reservation.workload_id] = reservation
        return reservation

    def release(self, workload_id: str) -> ResourceReservation:
        reservation = self._reservations.pop(workload_id, None)
        if reservation is None:
            raise ResourceDenied("unknown workload reservation")
        return reservation

    def reserved(self, workload_id: str) -> ResourceReservation | None:
        return self._reservations.get(workload_id)

    def _used(self, node_id: str) -> ResourceCapacity:
        return self._used_excluding(node_id, None)

    def _used_excluding(self, node_id: str, workload_id: str | None) -> ResourceCapacity:
        items = [
            r.capacity for r in self._reservations.values()
            if r.node_id == node_id and r.workload_id != workload_id
        ]
        return ResourceCapacity(
            sum(item.cpu for item in items),
            sum(item.memory_mb for item in items),
            sum(item.gpu for item in items),
        )

    @staticmethod
    def _fits(total: ResourceCapacity, used: ResourceCapacity, requested: ResourceCapacity) -> bool:
        return (
            used.cpu + requested.cpu <= total.cpu
            and used.memory_mb + requested.memory_mb <= total.memory_mb
            and used.gpu + requested.gpu <= total.gpu
        )

    @staticmethod
    def _validate(reservation: ResourceReservation) -> None:
        if not reservation.workload_id or not reservation.node_id:
            raise ResourceDenied("workload and node identity are required")
        if reservation.capacity.cpu <= 0 or reservation.capacity.memory_mb <= 0:
            raise ResourceDenied("CPU and memory reservations must be positive")
        if reservation.capacity.gpu < 0:
            raise ResourceDenied("GPU reservation cannot be negative")
