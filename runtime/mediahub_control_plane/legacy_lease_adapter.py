from dataclasses import dataclass
from ops.ai.task_lease import TaskLease
from .model import Lease

@dataclass(frozen=True, slots=True)
class LegacyLeaseAdapter:
    """Compatibility boundary; legacy file locking never becomes CP authority."""
    lease: TaskLease

    def to_model(self, generation: int = 1) -> Lease:
        record = self.lease.read_record()
        if not record:
            raise ValueError("legacy lease record unavailable")
        return Lease(
            lease_id=f"legacy:{record['task_id']}:{record['worker_id']}",
            task_id=record['task_id'],
            agent_id=record['worker_id'],
            created_at=float(record['created_at']),
            expires_at=float(record['expires_at']),
            last_renewed_at=float(record.get('created_at', 0.0)),
            generation=generation,
        )
