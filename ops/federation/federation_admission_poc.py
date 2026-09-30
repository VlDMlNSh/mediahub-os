#!/usr/bin/env python3
"""Deterministic, non-production Federation Admission PoC harness.

No network access, provider credentials, or production cluster access.
The harness models only the federation admission boundary and emits
machine-readable evidence matching the federation PoC contract.
"""
from __future__ import annotations

import hashlib
import json
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
    CLOSED = "CLOSED"


@dataclass
class Job:
    job_id: str
    source_cluster: str
    workload_class: str
    capability_scope: tuple[str, ...]
    destination_domain: str = "cloud-development"
    admitted: bool = False
    admission_decision: str = "DENY"
    payload_bytes: int = 0
    result_bytes: int = 0
    state: State = State.DENIED
    lease_until: float | None = None
    audit: list[dict] = field(default_factory=list)
    execution_result: str | None = None
    failure_reason: str | None = None
    retry_count: int = 0
    authorization_active: bool = False

    def transition(self, state: State, reason: str, ts: float) -> None:
        self.state = state
        self.audit.append({
            "state": state.value,
            "reason": reason,
            "ts": ts,
        })

    def evidence(self, *, evidence_ts: float) -> dict:
        return {
            "scenario_job_id": self.job_id,
            "job_id": self.job_id,
            "source_cluster": self.source_cluster,
            "destination_domain": self.destination_domain,
            "workload_class": self.workload_class,
            "admission_decision": self.admission_decision,
            "state_transitions": self.audit,
            "payload_bytes": self.payload_bytes,
            "result_bytes": self.result_bytes,
            "capability_scope": list(self.capability_scope),
            "lease_until": self.lease_until,
            "lease_active": self.authorization_active,
            "execution_result": self.execution_result,
            "failure_retry": {
                "failure_reason": self.failure_reason,
                "retry_count": self.retry_count,
            },
            "final_authorization_state": "ACTIVE" if self.authorization_active else "CLOSED",
            "evidence_timestamp": evidence_ts,
        }


def admit(job: Job, *, approved: bool, now: float, lease_seconds: int = 60) -> None:
    if job.workload_class == "CLOUD_DEVELOPMENT_ONLY":
        job.admission_decision = "DENY"
        job.transition(State.DENIED, "company_workload_not_user_escalation", now)
        return
    if not approved or not job.source_cluster:
        job.admission_decision = "DENY"
        job.transition(State.DENIED, "default_deny", now)
        return
    job.admitted = True
    job.admission_decision = "ADMIT"
    job.authorization_active = True
    job.lease_until = now + lease_seconds
    job.transition(State.ADMITTED, "explicit_admission", now)


def run(job: Job, *, now: float, declared_capability: str, payload: bytes) -> None:
    if not job.admitted or job.state != State.ADMITTED:
        raise PermissionError("job is not admitted")
    if job.lease_until is not None and now >= job.lease_until:
        job.transition(State.EXPIRED, "lease_expired_before_run", now)
        job.authorization_active = False
        raise PermissionError("lease expired")
    if declared_capability not in job.capability_scope:
        raise PermissionError("undeclared capability")
    job.payload_bytes = len(payload)
    job.transition(State.RUNNING, "bounded_execution", now)
    result = hashlib.sha256(payload).hexdigest().encode()
    job.result_bytes = len(result)
    job.execution_result = "SUCCESS"
    job.transition(State.RESULT_READY, "bounded_result", now + 0.001)
    job.authorization_active = False
    job.transition(State.CLOSED, "request_scope_ended", now + 0.002)


def expire(job: Job, *, now: float) -> None:
    if job.lease_until is not None and now >= job.lease_until and job.state in {State.ADMITTED, State.RUNNING}:
        job.authorization_active = False
        job.transition(State.LEASE_EXPIRED, "lease_expired", now)
        job.transition(State.TERMINATED, "execution_authority_removed", now + 0.001)
        job.transition(State.CLOSED, "request_scope_ended", now + 0.002)


def retry(job: Job, *, now: float) -> None:
    if job.state != State.FAILED:
        raise ValueError("retry requires FAILED state")
    if not job.capability_scope:
        raise PermissionError("retry has no declared scope")
    job.retry_count += 1
    job.admitted = True
    job.admission_decision = "ADMIT_RETRY"
    job.authorization_active = True
    job.lease_until = now + 60
    job.transition(State.ADMITTED, "retry_same_scope", now)


def scenario(name: str, fn, *, evidence_ts: float) -> dict:
    try:
        job = fn()
        return {
            **job.evidence(evidence_ts=evidence_ts),
            "scenario": name,
            "pass": True,
        }
    except Exception as exc:
        return {
            "scenario": name,
            "pass": False,
            "error": type(exc).__name__ + ": " + str(exc),
            "evidence_timestamp": evidence_ts,
        }


def run_all() -> dict:
    fixed_now = 1_700_000_000.0
    results = []

    def s1():
        j = Job("s1", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=False, now=fixed_now)
        assert j.state == State.DENIED and j.payload_bytes == 0
        assert not j.authorization_active
        return j

    def s2():
        j = Job("s2", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        assert j.state == State.ADMITTED and j.lease_until is not None
        assert j.authorization_active
        return j

    def s3():
        j = Job("s3", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        run(j, now=fixed_now + 1, declared_capability="ai.infer", payload=b"bounded")
        assert j.state == State.CLOSED and j.result_bytes > 0
        assert [x["state"] for x in j.audit] == ["ADMITTED", "RUNNING", "RESULT_READY", "CLOSED"]
        return j

    def s4():
        j = Job("s4", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        run(j, now=fixed_now + 1, declared_capability="ai.infer", payload=b"x")
        assert j.payload_bytes == 1 and j.result_bytes == 64
        assert any(x["state"] == "RESULT_READY" for x in j.audit)
        return j

    def s5():
        j = Job("s5", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now, lease_seconds=1)
        expire(j, now=fixed_now + 2)
        assert j.state == State.CLOSED and not j.authorization_active
        assert [x["state"] for x in j.audit][-3:] == ["LEASE_EXPIRED", "TERMINATED", "CLOSED"]
        return j

    def s6():
        j = Job("s6", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        j.failure_reason = "injected_failure"
        j.transition(State.FAILED, "injected_failure", fixed_now + 1)
        retry(j, now=fixed_now + 2)
        assert j.state == State.ADMITTED and j.retry_count == 1
        assert j.capability_scope == ("ai.infer",)
        return j

    def s7():
        j = Job("s7", "local-a", "CLOUD_ESCALATED_USER", ("ai.infer",))
        admit(j, approved=True, now=fixed_now)
        try:
            run(j, now=fixed_now + 1, declared_capability="storage.enumerate", payload=b"x")
        except PermissionError:
            return j
        raise AssertionError("undeclared capability was accepted")

    def s8():
        j = Job("s8", "local-a", "CLOUD_DEVELOPMENT_ONLY", ("ci.build",))
        admit(j, approved=True, now=fixed_now)
        assert j.state == State.DENIED
        return j

    for index, (name, fn) in enumerate([
        ("S1_default_denial", s1),
        ("S2_valid_admission", s2),
        ("S3_bounded_execution", s3),
        ("S4_bounded_result", s4),
        ("S5_lease_expiry", s5),
        ("S6_retry_after_failure", s6),
        ("S7_isolation_probe", s7),
        ("S8_company_workload_separation", s8),
    ], start=1):
        results.append(scenario(name, fn, evidence_ts=fixed_now + index / 1000))

    evidence = {
        "schema": "mediahub.federation-admission-poc.v2",
        "mode": "non-production-deterministic",
        "evidence_timestamp": fixed_now,
        "scenarios": results,
        "pass": all(x["pass"] for x in results),
    }
    return evidence


if __name__ == "__main__":
    print(json.dumps(run_all(), sort_keys=True, separators=(",", ":")))
