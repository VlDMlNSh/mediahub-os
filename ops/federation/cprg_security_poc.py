#!/usr/bin/env python3
"""Deterministic, non-production CPRG security PoC.

Models the protected API-key registration boundary only.
No network access, VPN creation, provider calls, or real credentials.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field


FIXED_NOW = 1_700_000_000.0
ALLOWED_OPERATION = "api_key_registration"
ALLOWED_DESTINATION = "provider-registration"
MAX_REQUEST_BYTES = 4096
MAX_CONCURRENT_SESSIONS = 2


@dataclass
class Registration:
    request_id: str
    node_id: str
    operation: str
    destination: str
    lease_until: float
    authenticated: bool = False
    proof_valid: bool = False
    active: bool = False
    closed: bool = False
    request_nonce: str = ""
    audit: list[dict] = field(default_factory=list)

    def transition(self, state: str, reason: str, ts: float) -> None:
        self.audit.append({"state": state, "reason": reason, "ts": ts})

    def evidence(self) -> dict:
        return {
            "request_id": self.request_id,
            "node_id": self.node_id,
            "operation": self.operation,
            "destination": self.destination,
            "lease_until": self.lease_until,
            "active": self.active,
            "closed": self.closed,
            "audit": self.audit,
            "final_state": "CLOSED" if self.closed else ("ACTIVE" if self.active else "DENIED"),
        }


def authenticate(reg: Registration, *, proof_valid: bool, now: float) -> None:
    if reg.closed:
        raise PermissionError("request_closed")
    if not proof_valid:
        reg.transition("DENIED", "invalid_node_proof", now)
        reg.closed = True
        return
    reg.authenticated = True
    reg.proof_valid = True
    reg.transition("AUTHENTICATED", "proof_of_possession", now)


def admit(reg: Registration, *, now: float, replay_seen: set[str], active_sessions: int) -> None:
    if reg.closed or not reg.authenticated:
        raise PermissionError("not_authenticated")
    if reg.request_id in replay_seen:
        reg.transition("DENIED", "replay_detected", now)
        reg.closed = True
        raise PermissionError("replay_detected")
    if reg.operation != ALLOWED_OPERATION:
        reg.transition("DENIED", "operation_not_allowed", now)
        reg.closed = True
        raise PermissionError("operation_not_allowed")
    if reg.destination != ALLOWED_DESTINATION:
        reg.transition("DENIED", "destination_not_allowed", now)
        reg.closed = True
        raise PermissionError("destination_not_allowed")
    if active_sessions >= MAX_CONCURRENT_SESSIONS:
        reg.transition("DENIED", "concurrency_limit", now)
        reg.closed = True
        raise PermissionError("concurrency_limit")
    if reg.lease_until <= now:
        reg.transition("DENIED", "lease_expired", now)
        reg.closed = True
        raise PermissionError("lease_expired")
    replay_seen.add(reg.request_id)
    reg.active = True
    reg.transition("LEASE_ACTIVE", "bounded_registration_lease", now)
    reg.transition("TUNNEL_ACTIVE", "registration_only_path", now)


def register(reg: Registration, *, now: float, payload: bytes) -> None:
    if not reg.active or reg.closed:
        raise PermissionError("registration_not_active")
    if now >= reg.lease_until:
        close(reg, now=now, reason="lease_expired")
        raise PermissionError("lease_expired")
    if len(payload) > MAX_REQUEST_BYTES:
        close(reg, now=now, reason="request_too_large")
        raise PermissionError("request_too_large")
    if ALLOWED_OPERATION not in reg.operation:
        close(reg, now=now, reason="operation_not_allowed")
        raise PermissionError("operation_not_allowed")
    digest = hashlib.sha256(payload).hexdigest()
    reg.transition("REGISTRATION_VERIFIED", "bounded_provider_registration", now + 0.001)
    reg.transition("AUDIT_RECORDED", "sanitized_evidence", now + 0.002)
    close(reg, now=now + 0.003, reason="registration_complete")
    return digest


def close(reg: Registration, *, now: float, reason: str) -> None:
    if not reg.closed:
        reg.active = False
        reg.closed = True
        reg.transition("CLOSED", reason, now)


def make_registration(
    request_id: str,
    *,
    operation: str = ALLOWED_OPERATION,
    destination: str = ALLOWED_DESTINATION,
    lease_seconds: int = 30,
) -> Registration:
    return Registration(
        request_id=request_id,
        node_id="mediahub-node-a",
        operation=operation,
        destination=destination,
        lease_until=FIXED_NOW + lease_seconds,
        request_nonce=hashlib.sha256(request_id.encode()).hexdigest()[:16],
    )


def run_all() -> dict:
    results = []

    def scenario(name: str, fn) -> None:
        try:
            reg = fn()
            results.append({"scenario": name, "pass": True, **reg.evidence()})
        except Exception as exc:
            results.append({
                "scenario": name,
                "pass": False,
                "error": type(exc).__name__ + ": " + str(exc),
            })

    def s1_invalid_identity():
        reg = make_registration("s1")
        authenticate(reg, proof_valid=False, now=FIXED_NOW)
        assert reg.closed and not reg.active
        return reg

    def s2_exact_registration():
        reg = make_registration("s2")
        authenticate(reg, proof_valid=True, now=FIXED_NOW)
        admit(reg, now=FIXED_NOW, replay_seen=set(), active_sessions=0)
        register(reg, now=FIXED_NOW + 1, payload=b"synthetic-registration")
        assert reg.closed and not reg.active
        assert [x["state"] for x in reg.audit][-3:] == [
            "REGISTRATION_VERIFIED", "AUDIT_RECORDED", "CLOSED"
        ]
        return reg

    def s3_route_escape_denied():
        reg = make_registration("s3", destination="arbitrary-internet")
        authenticate(reg, proof_valid=True, now=FIXED_NOW)
        try:
            admit(reg, now=FIXED_NOW, replay_seen=set(), active_sessions=0)
        except PermissionError:
            assert reg.closed and not reg.active
            return reg
        raise AssertionError("unapproved destination accepted")

    def s4_replay_denied():
        replay_seen = {"s4"}
        reg = make_registration("s4")
        authenticate(reg, proof_valid=True, now=FIXED_NOW)
        try:
            admit(reg, now=FIXED_NOW, replay_seen=replay_seen, active_sessions=0)
        except PermissionError:
            assert reg.closed
            return reg
        raise AssertionError("replay accepted")

    def s5_lease_expiry_closes():
        reg = make_registration("s5", lease_seconds=1)
        authenticate(reg, proof_valid=True, now=FIXED_NOW)
        admit(reg, now=FIXED_NOW, replay_seen=set(), active_sessions=0)
        try:
            register(reg, now=FIXED_NOW + 2, payload=b"x")
        except PermissionError:
            assert reg.closed and not reg.active
            return reg
        raise AssertionError("expired lease remained active")

    def s6_payload_bound_denied():
        reg = make_registration("s6")
        authenticate(reg, proof_valid=True, now=FIXED_NOW)
        admit(reg, now=FIXED_NOW, replay_seen=set(), active_sessions=0)
        try:
            register(reg, now=FIXED_NOW + 1, payload=b"x" * (MAX_REQUEST_BYTES + 1))
        except PermissionError:
            assert reg.closed and not reg.active
            return reg
        raise AssertionError("oversized request accepted")

    def s7_concurrency_denied():
        reg = make_registration("s7")
        authenticate(reg, proof_valid=True, now=FIXED_NOW)
        try:
            admit(reg, now=FIXED_NOW, replay_seen=set(), active_sessions=MAX_CONCURRENT_SESSIONS)
        except PermissionError:
            assert reg.closed and not reg.active
            return reg
        raise AssertionError("concurrency limit bypassed")

    def s8_operation_scope_denied():
        reg = make_registration("s8", operation="model_inference")
        authenticate(reg, proof_valid=True, now=FIXED_NOW)
        try:
            admit(reg, now=FIXED_NOW, replay_seen=set(), active_sessions=0)
        except PermissionError:
            assert reg.closed and not reg.active
            return reg
        raise AssertionError("non-registration operation accepted")

    scenario("S1_invalid_identity_denied", s1_invalid_identity)
    scenario("S2_exact_registration_allowed", s2_exact_registration)
    scenario("S3_route_escape_denied", s3_route_escape_denied)
    scenario("S4_replay_denied", s4_replay_denied)
    scenario("S5_lease_expiry_closes", s5_lease_expiry_closes)
    scenario("S6_payload_bound_denied", s6_payload_bound_denied)
    scenario("S7_concurrency_limit_denied", s7_concurrency_denied)
    scenario("S8_operation_scope_denied", s8_operation_scope_denied)

    return {
        "schema": "mediahub.cprg-security-poc.v1",
        "mode": "non-production-deterministic",
        "evidence_timestamp": FIXED_NOW,
        "constraints": {
            "allowed_operation": ALLOWED_OPERATION,
            "allowed_destination": ALLOWED_DESTINATION,
            "max_request_bytes": MAX_REQUEST_BYTES,
            "max_concurrent_sessions": MAX_CONCURRENT_SESSIONS,
        },
        "scenarios": results,
        "pass": all(item["pass"] for item in results),
    }


if __name__ == "__main__":
    print(json.dumps(run_all(), sort_keys=True, separators=(",", ":")))
