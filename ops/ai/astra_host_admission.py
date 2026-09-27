"""MH-21 admission-only bridge from Astra host envelopes to local delivery state.

No transport or process execution occurs here. The bridge binds envelope
identity to TaskDeliveryJournal and TaskLease and fails closed on replay,
context mismatch, or unavailable lease ownership.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from ops.ai.astra_host_envelope import AstraHostEnvelope, HostEnvelopeDenied
from ops.ai.task_delivery import DeliveryDenied, DeliveryState, TaskDelivery, TaskDeliveryJournal
from ops.ai.task_lease import LeaseDenied, TaskLease


class HostAdmissionDenied(PermissionError):
    """Raised when an envelope cannot be admitted for host execution."""


@dataclass(frozen=True)
class HostAdmission:
    envelope_fingerprint: str
    delivery: TaskDelivery
    lease_path: Path


class AstraHostAdmission:
    """Prepare exactly one bounded host workload without dispatching it."""

    def __init__(self, delivery: TaskDeliveryJournal, lease: TaskLease) -> None:
        self.delivery = delivery
        self.lease = lease

    def prepare(self, envelope: AstraHostEnvelope) -> HostAdmission:
        if not isinstance(envelope, AstraHostEnvelope):
            raise HostAdmissionDenied("invalid host envelope")
        try:
            existing = self.delivery.delivery
            if existing is not None:
                if existing.task_id != envelope.workload_id:
                    raise HostAdmissionDenied("another workload is already active")
                if existing.request_fingerprint != self.delivery.fingerprint(envelope.canonical_payload()):
                    raise HostAdmissionDenied("workload replay or envelope mismatch")
                if (
                    existing.session_id != envelope.session_id
                    or existing.conversation_id != envelope.conversation_id
                    or existing.generation != envelope.generation
                ):
                    raise HostAdmissionDenied("delivery identity does not match envelope")
                if existing.state is not DeliveryState.PREPARED:
                    raise HostAdmissionDenied("workload is no longer in admission state")
                return HostAdmission(
                    envelope.fingerprint(), existing, self.lease.path
                )

            if self.lease.task_id != envelope.workload_id:
                raise HostAdmissionDenied("lease workload identity mismatch")
            if self.lease.worker_id != envelope.host_id:
                raise HostAdmissionDenied("lease host identity mismatch")

            # Lease ownership is acquired only for the admission window. This does
            # not execute the workload or authorize transport.
            self.lease.acquire()
            delivery = self.delivery.prepare(
                envelope.workload_id,
                envelope.canonical_payload(),
                envelope.conversation_id,
                envelope.session_id,
                envelope.generation,
            )
            return HostAdmission(envelope.fingerprint(), delivery, self.lease.path)
        except (DeliveryDenied, LeaseDenied, OSError, HostEnvelopeDenied) as exc:
            try:
                self.lease.release()
            finally:
                if isinstance(exc, HostAdmissionDenied):
                    raise
            raise HostAdmissionDenied(str(exc)) from exc

    def safe_stop(self, reason: str = "host admission stopped") -> None:
        if self.delivery.delivery is not None:
            self.delivery.mark_safe_stop(reason)
        self.lease.release()
