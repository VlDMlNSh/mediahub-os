from __future__ import annotations

from dataclasses import dataclass, fields
from threading import Lock


@dataclass(frozen=True, slots=True)
class ControlPlaneMetricSnapshot:
    reconcile_ticks: int = 0
    reconcile_errors: int = 0
    dispatch_attempts: int = 0
    dispatch_successes: int = 0
    dispatch_rejections: int = 0
    claims: int = 0
    claim_conflicts: int = 0
    lease_renewals: int = 0
    lease_expiries: int = 0
    fencing_failures: int = 0
    task_retries: int = 0
    circuit_opened: int = 0
    circuit_closed: int = 0
    circuit_half_open_probes: int = 0


class ControlPlaneMetrics:
    """Process-local telemetry; never authoritative state or persistence."""

    def __init__(self):
        self._lock = Lock()
        self._values = {field.name: 0 for field in fields(ControlPlaneMetricSnapshot)}

    def inc(self, name: str, amount: int = 1) -> None:
        if amount < 0 or name not in self._values:
            raise ValueError("invalid metric increment")
        with self._lock:
            self._values[name] += amount

    def snapshot(self) -> ControlPlaneMetricSnapshot:
        with self._lock:
            return ControlPlaneMetricSnapshot(**self._values)
