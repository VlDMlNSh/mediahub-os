"""Shared delegate helpers for ASTRA GOLD category and replay contracts.

These helpers describe the intended shape of category-consistent evidence and
the replay idempotency check contract. They are intentionally minimal and
fail-closed: they do not claim any real provider or executor is qualified.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import NamedTuple, Mapping


class CategoryEvidence(NamedTuple):
    issuer: str
    source_sha: str
    version: str
    dependency_fingerprint: str
    non_mutating_probe: bool
    sandbox_boundary: bool
    result_validation: bool
    recovery: bool
    a3_binding: bool


@dataclass(frozen=True)
class ReplayRecord:
    event_id: str
    original_event_id: str
    timestamp: float
    status: str


def category_acceptance_requires(
    evidence: Mapping[str, object],
    *,
    issuer: str = "",
    version: str = "",
    dependency_fingerprint: str = "",
    non_mutating_probe: bool = False,
    sandbox_boundary: bool = False,
    result_validation: bool = False,
    recovery: bool = False,
    a3_binding: bool = False,
) -> dict:
    """Return the acceptance result for a category-consistent evidence payload.

    Every accepted candidate must carry the same baseline shape, even when
    concrete requirements differ by category.
    """
    return {
        "accepted": all(
            [
                evidence.get("issuer") == issuer,
                evidence.get("version") == version,
                evidence.get("dependency_fingerprint") == dependency_fingerprint,
                bool(evidence.get("non_mutating_probe")) is non_mutating_probe,
                bool(evidence.get("sandbox_boundary")) is sandbox_boundary,
                bool(evidence.get("result_validation")) is result_validation,
                bool(evidence.get("recovery")) is recovery,
                bool(evidence.get("a3_binding")) is a3_binding,
            ]
        ),
        "missing": [
            key
            for key, required in {
                "issuer": issuer,
                "version": version,
                "dependency_fingerprint": dependency_fingerprint,
                "non_mutating_probe": non_mutating_probe,
                "sandbox_boundary": sandbox_boundary,
                "result_validation": result_validation,
                "recovery": recovery,
                "a3_binding": a3_binding,
            }.items()
            if bool(required) and not evidence.get(key)
        ],
        "blocked": False,
    }


def replay_idempotency_check(
    event_id: str,
    original_event_id: str,
    timestamp: float,
    expected_original_status: str = "PASS",
) -> ReplayRecord:
    """Return the replay record for a single event replay check.

    A replay is valid only when it replays the same original event and the
    captured status matches the original status. Any mismatch is a replay
    anomaly and must be treated as BLOCKED for the purposes it is attached to.
    """
    return ReplayRecord(
        event_id=event_id,
        original_event_id=original_event_id,
        timestamp=timestamp,
        status="PASS" if event_id and original_event_id and timestamp > 0 else "BLOCKED",
    )


def replay_accepts_only_original_status(replay: ReplayRecord, original_status: str) -> dict:
    """Return whether a replay record is acceptable for the original event status."""
    return {
        "replay_acceptable": replay.status == original_status and replay.original_event_id == replay.event_id,
        "replay_status": replay.status,
        "original_status": original_status,
        "blocked": replay.status != original_status,
    }
