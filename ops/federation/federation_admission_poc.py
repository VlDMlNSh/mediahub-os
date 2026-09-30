#!/usr/bin/env python3
"""Deterministic, non-production Federation Admission PoC harness.

No network access, provider credentials, or production cluster access.
The harness models only the federation admission boundary.
"""
from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum


class State(str, Enum):
    DENIED = "DENIED"
    ADMITTED = "ADMITTED"
    RUNNING = "RUNNING"
    RESULT_READY = "RESULT_READY"
    EXPIRED = "EXPIRED"
    FAILED = "FAILED"
    LEASE_EXPIRED = "LEASE_EXPIRED"
    TERMINATED = "TERMINATED"
    RETRY_OR_CLOSED = "RETRY_OR_CLOSED"
    CLOSED = "CLOSED"


@dataclass
class Job:
    job_id: str
    source_cluster: str
    workload_class: str
    capability_scope: tuple[str, ...]
    admitted: bool = False
    payload_bytes: int = 0
    result_bytes: int = 0
    state: State = State.DENIED
    lease_until: float | None = None
    audit: list[dict] = field(default_factory=list)

    def transition(self, state: State, reason: str) -> None:
        self.state = state
        self.audit.append({
            "state": state.value,
            "reason": reason,
            "ts": time.time(),
        })


def admit(job: Job, *, approved: bool, now: float, lease_seconds: int = 60) -> None:
    if job.workload_class == "CLOUD_DEVELOPMENT_ONLY":
        job.transition(State.DENIED, "company_workload_not_user_escalation")
        return
    if not approved or not job.source_cluster:
        job.transition(State.DENIED, "default_deny")
        return
    job.admitted = True
    job.lease_until = now + lease_seconds
    job.transition(State.ADMITTED, "explicit_admission")


def run(job: Job, *, now: float, declared_capability: str, payload: bytes) -> None:
    if not job.admitted or job.state != State.ADMITTED:
        raise PermissionError("job is not admitted")
    if job.lease_until is not None and now >= job.lease_until:
        job.transition(State.EXPIRED, "lease_expired_before_run")
        raise PermissionError("lease expired")
    if declared_capability not in job.capability_scope:
        raise PermissionError("undeclared capability")
    job.payload_bytes = len(payload)
    job.transition(State.RUNNING, "bounded_execution")
    result = hashlib.sha256(payload).hexdigest().encode()
    job.result_bytes = len(result)
    job.transition(State.RESULT_READY, "bounded_result")
    job.transition(State.CLOSED, "request_scope_ended")


def expire(job: Job, *, now: float) -> None:
    if job.lease_until is not None and now >= job.lease_until and job.state in {State.ADMITTED, State.RUNNING}:
        job.transition(State.LEASE_EXPIRED, "lease_expired")
        job.transition(State.TERMINATED, "execution_authority_removed")
        job.transition(State.CLOSED, "request_scope_ended")


def retry(job: Job, *, now: float) -> None:
    if job.state != State.FAILED:
        raise ValueError("retry requires FAILED state")
    if not job.capability_scope:
        raise PermissionError("retry has no declared scope")
    job.transition(State.ADMITTED, "retry_same_scope")
    job.lease_until = now + 60


def scenario(name: str, fn) -> dict:
    try:
        fn()
        return {"scenario": name, "pass": True}
    except Exception as exc:
        return {"scenario": name, "pass": False, "error": type(exc).__name__ + ": " + str(exc)}


def run_all() -> dict:
    fixed_now = 1_700_000_000.0
    results = []

    def s1():
        j = Job("s1", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=False, now=fixed_now)
        assert j.state == State.DENIED and j.payload_bytes == 0

    def s2():
        j = Job("s2", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        assert j.state == State.ADMITTED and j.lease_until is not None

    def s3():
        j = Job("s3", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        run(j, now=fixed_now + 1, declared_capability="ai.infer", payload=b"bounded")
        assert j.state == State.CLOSED and j.result_bytes > 0

    def s4():
        j = Job("s4", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        run(j, now=fixed_now + 1, declared_capability="ai.infer", payload=b"x")
        assert j.payload_bytes == 1 and j.result_bytes == 64

    def s5():
        j = Job("s5", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now, lease_seconds=1)
        expire(j, now=fixed_now + 2)
        assert j.state == State.CLOSED
        assert [x["state"] for x in j.audit][-2:] == ["TERMINATED", "CLOSED"]

    def s6():
        j = Job("s6", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        j.transition(State.FAILED, "injected_failure")
        retry(j, now=fixed_now + 2)
        assert j.state == State.ADMITTED
        assert j.capability_scope == ("ai.infer",)

    def s7():
        j = Job("s7", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        try:
            run(j, now=fixed_now + 1, declared_capability="storage.enumerate", payload=b"x")
        except PermissionError:
            return
        raise AssertionError("undeclared capability was accepted")

    def s8():
        j = Job("s8", "local-a", "CLOUD_DEVELOPMENT_ONLY", ("ci.build",))
        admit(j, approved=True, now=fixed_now)
        assert j.state == State.DENIED

    for name, fn in [
        ("S1_default_denial", s1),
        ("S2_valid_admission", s2),
        ("S3_bounded_execution", s3),
        ("S4_bounded_result", s4),
        ("S5_lease_expiry", s5),
        ("S6_retry_after_failure", s6),
        ("S7_isolation_probe", s7),
        ("S8_company_workload_separation", s8),
    ]:
        results.append(scenario(name, fn))

    evidence = {
        "schema": "mediahub.federation-admission-poc.v1",
        "mode": "non-production-deterministic",
        "scenarios": results,
        "pass": all(x["pass"] for x in results),
    }
    return evidence


if __name__ == "__main__":
    print(json.dumps(run_all(), sort_keys=True, separators=(",", ":")))
