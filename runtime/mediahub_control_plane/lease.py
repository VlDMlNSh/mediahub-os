from dataclasses import replace
from .model import Lease, LeaseStatus, validate_lease_transition

class LeaseManager:
    def __init__(self, ttl: float = 60.0):
        if ttl <= 0:
            raise ValueError("ttl must be positive")
        self.ttl = ttl

    def issue(self, task_id: str, agent_id: str, now: float, ttl: float | None = None) -> Lease:
        duration = self.ttl if ttl is None else ttl
        return Lease(f"{task_id}:{agent_id}:{now}", task_id, agent_id, now, now + duration, now, 1, LeaseStatus.ACTIVE)

    def renew(self, lease: Lease, agent_id: str, generation: int, now: float, ttl: float | None = None) -> Lease:
        self.assert_owner(lease, agent_id, generation, now)
        duration = self.ttl if ttl is None else ttl
        status = LeaseStatus.RENEWED
        return replace(lease, expires_at=now + duration, last_renewed_at=now, status=status)

    def expire(self, lease: Lease, now: float) -> Lease:
        if now < lease.expires_at:
            raise ValueError("lease has not expired")
        validate_lease_transition(lease.status, LeaseStatus.EXPIRED)
        return replace(lease, status=LeaseStatus.EXPIRED)

    def assert_owner(self, lease: Lease, agent_id: str, generation: int, now: float) -> None:
        if lease.agent_id != agent_id or lease.generation != generation:
            raise PermissionError("stale lease owner")
        if lease.status not in (LeaseStatus.ACTIVE, LeaseStatus.RENEWED):
            raise PermissionError("lease is not active")
        if now >= lease.expires_at:
            raise PermissionError("lease expired")
