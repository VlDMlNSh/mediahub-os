from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ReplicationPlan:
    artifact_id: str
    targets: tuple[str, ...]

@dataclass(frozen=True)
class RecoveryPlan:
    artifact_id: str
    source_candidates: tuple[str, ...]
    blocked: bool = False

def plan_replication(artifact: dict, replicas: list[dict]) -> ReplicationPlan:
    existing = {r.get("replica_id") for r in replicas if r.get("state") in {"VERIFIED","AVAILABLE"}}
    targets = tuple(r["replica_id"] for r in replicas if r.get("replica_id") and r["replica_id"] not in existing)
    return ReplicationPlan(str(artifact["artifact_id"]), targets)

def mark_replica_event(artifact: dict, replica_id: str, event: str) -> dict:
    result = dict(artifact)
    result["replica_event"] = {"replica_id": replica_id, "event": event}
    return result

def plan_recovery(artifact: dict, replicas: list[dict]) -> RecoveryPlan:
    candidates = tuple(r["replica_id"] for r in replicas if r.get("replica_id") and r.get("state") in {"VERIFIED","AVAILABLE"})
    return RecoveryPlan(str(artifact["artifact_id"]), candidates, blocked=not bool(candidates))
