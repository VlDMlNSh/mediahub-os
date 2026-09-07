"""Observational evidence binding for governed runtime executions."""

from datetime import datetime, timezone
from typing import Any, Mapping

from .event_projection import CanonicalEvent, ProjectionError, validate_canonical_event


class EvidenceError(ValueError):
    """Raised when an evidence record cannot be bound reproducibly."""


def build_evidence_record(
    *,
    test_id: str,
    contract: str,
    verification_target: str,
    git_sha: str,
    branch: str,
    runtime: str,
    platform: str,
    dependency_lock: str,
    command: str,
    started_at: str,
    completed_at: str,
    exit_code: int,
    canonical_event: CanonicalEvent,
    pre_state: Any,
    post_state: Any,
    authorization_result: str,
    validation_result: str,
    mutation_result: str,
    stdout_reference: str,
    structured_result_reference: str,
    reproducibility_reference: str,
    reviewer: str,
    review_basis: str,
    unknowns: list[str],
    contradictions: list[str],
    blockers: list[str],
    stderr_reference: str | None = None,
    concurrency_context: str | None = None,
    rejection_reason: str | None = None,
    failure_class: str | None = None,
) -> dict[str, Any]:
    """Create an observational record bound to one canonical event.

    This helper has no mutation capability. The emitted event is represented by
    its canonical serialization and deterministic fingerprint.
    """
    if not isinstance(canonical_event, CanonicalEvent):
        raise EvidenceError("canonical event required")
    event_dict = canonical_event.as_dict()
    validate_canonical_event(event_dict)
    fingerprint = canonical_event.evidence_fingerprint()

    required_strings = {
        "test_id": test_id, "contract": contract, "verification_target": verification_target,
        "git_sha": git_sha, "branch": branch, "runtime": runtime, "platform": platform,
        "dependency_lock": dependency_lock, "command": command, "started_at": started_at,
        "completed_at": completed_at, "stdout_reference": stdout_reference,
        "structured_result_reference": structured_result_reference,
        "reproducibility_reference": reproducibility_reference, "reviewer": reviewer,
        "review_basis": review_basis, "authorization_result": authorization_result,
        "validation_result": validation_result, "mutation_result": mutation_result,
    }
    if any(not isinstance(value, str) or not value for value in required_strings.values()):
        raise EvidenceError("required evidence identity is missing")
    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
        raise EvidenceError("invalid exit code")

    now = datetime.now(timezone.utc).isoformat()
    emitted_event = dict(event_dict)
    emitted_event["evidence_fingerprint"] = fingerprint
    record = {
        "test_id": test_id,
        "contract": contract,
        "verification_target": verification_target,
        "git_sha": git_sha,
        "branch": branch,
        "environment": {
            "runtime": runtime,
            "platform": platform,
            "dependency_lock": dependency_lock,
        },
        "execution": {
            "command": command,
            "started_at": started_at,
            "completed_at": completed_at,
            "exit_code": exit_code,
        },
        "input": {
            "command_id": canonical_event.metadata.get("command_id", ""),
            "correlation_id": canonical_event.correlation_id,
            "source_identity": canonical_event.source,
            "authorization_context": "observed-at-execution",
            "target": canonical_event.subject,
            "operation": canonical_event.payload.get("operation", ""),
        },
        "observation": {
            "pre_state": pre_state,
            "post_state": post_state,
            "authorization_result": authorization_result,
            "validation_result": validation_result,
            "mutation_result": mutation_result,
            "emitted_events": [emitted_event],
        },
        "evidence": {
            "stdout_reference": stdout_reference,
            "structured_result_reference": structured_result_reference,
            "artifact_hash": fingerprint,
            "reproducibility_reference": reproducibility_reference,
        },
        "assessment": {
            "result": "TESTED" if exit_code == 0 else "BLOCKED",
            "reviewer": reviewer,
            "review_basis": review_basis,
            "unknowns": list(unknowns),
            "contradictions": list(contradictions),
            "blockers": list(blockers),
            "generated_at": now,
        },
    }
    if stderr_reference is not None:
        record["evidence"]["stderr_reference"] = stderr_reference
    if concurrency_context is not None:
        record["input"]["concurrency_context"] = concurrency_context
    if rejection_reason is not None:
        record["observation"]["rejection_reason"] = rejection_reason
    if failure_class is not None:
        record["observation"]["failure_class"] = failure_class
    return record
