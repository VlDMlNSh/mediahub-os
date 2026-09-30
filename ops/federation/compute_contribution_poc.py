#!/usr/bin/env python3
"""Deterministic, non-production compute-contribution PoC.

Models the boundary between a MediaHub contributor and the developer compute
fabric. No network I/O, credentials, process execution, or production access.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

SCHEMA = "mediahub.compute-contribution-poc.v1"


@dataclass(frozen=True)
class ComputeCapability:
    node_id: str
    administrative_domain: str
    resources: tuple[str, ...]
    max_lease_seconds: int
    capability_digest: str

    @classmethod
    def advertise(
        cls,
        node_id: str,
        administrative_domain: str,
        resources: tuple[str, ...],
        max_lease_seconds: int,
    ) -> "ComputeCapability":
        material = "|".join(
            [node_id, administrative_domain, *sorted(resources), str(max_lease_seconds)]
        ).encode()
        digest = hashlib.sha256(material).hexdigest()
        return cls(node_id, administrative_domain, tuple(sorted(resources)), max_lease_seconds, digest)


@dataclass(frozen=True)
class Workload:
    workload_id: str
    workload_class: str
    required_resource: str
    max_lease_seconds: int


def verify_capability(capability: ComputeCapability) -> tuple[bool, str]:
    material = "|".join(
        [
            capability.node_id,
            capability.administrative_domain,
            *sorted(capability.resources),
            str(capability.max_lease_seconds),
        ]
    ).encode()
    expected = hashlib.sha256(material).hexdigest()
    if capability.capability_digest != expected:
        return False, "capability_integrity_failure"
    if not capability.node_id or not capability.administrative_domain:
        return False, "incomplete_capability_identity"
    if capability.max_lease_seconds <= 0:
        return False, "invalid_lease_limit"
    return True, "capability_verified"


def admit_compute_contribution(
    capability: ComputeCapability,
    workload: Workload,
    *,
    requested_lease_seconds: int,
    contributor_enabled: bool,
) -> dict:
    verified, verification_reason = verify_capability(capability)
    if not verified:
        decision, reason = "DENY", verification_reason
    elif not contributor_enabled:
        decision, reason = "DENY", "contribution_disabled"
    elif workload.workload_class != "CLOUD_DEVELOPMENT_ONLY":
        decision, reason = "DENY", "non_developer_workload"
    elif workload.required_resource not in capability.resources:
        decision, reason = "DENY", "required_resource_not_advertised"
    elif requested_lease_seconds <= 0 or requested_lease_seconds > capability.max_lease_seconds:
        decision, reason = "DENY", "lease_exceeds_capability_limit"
    elif requested_lease_seconds > workload.max_lease_seconds:
        decision, reason = "DENY", "lease_exceeds_workload_limit"
    else:
        decision, reason = "ALLOW", "verified_capability_and_bounded_developer_lease"

    return {
        "schema": SCHEMA,
        "workload_id": workload.workload_id,
        "workload_class": workload.workload_class,
        "contributor_node": capability.node_id,
        "required_resource": workload.required_resource,
        "requested_lease_seconds": requested_lease_seconds,
        "contributor_enabled": contributor_enabled,
        "decision": decision,
        "reason": reason,
        "pass": True,
    }


def run_all() -> dict:
    contributor = ComputeCapability.advertise(
        "mediahub-node-a",
        "user-local",
        ("cpu", "gpu", "npu"),
        max_lease_seconds=900,
    )
    developer_job = Workload("dev-build-1", "CLOUD_DEVELOPMENT_ONLY", "cpu", 600)
    user_job = Workload("user-escalation-1", "CLOUD_ESCALATED_USER", "cpu", 600)
    oversized_job = Workload("dev-build-2", "CLOUD_DEVELOPMENT_ONLY", "gpu", 1200)
    tampered = ComputeCapability(
        contributor.node_id,
        contributor.administrative_domain,
        contributor.resources,
        contributor.max_lease_seconds,
        "0" * 64,
    )

    scenarios = [
        admit_compute_contribution(contributor, developer_job, requested_lease_seconds=300, contributor_enabled=True),
        admit_compute_contribution(contributor, user_job, requested_lease_seconds=300, contributor_enabled=True),
        admit_compute_contribution(contributor, oversized_job, requested_lease_seconds=1200, contributor_enabled=True),
        admit_compute_contribution(tampered, developer_job, requested_lease_seconds=300, contributor_enabled=True),
    ]
    names = (
        "S1_bounded_developer_compute_admission",
        "S2_user_workload_separation",
        "S3_lease_bound_enforcement",
        "S4_capability_integrity_denial",
    )
    for item, name in zip(scenarios, names):
        item["scenario"] = name

    assert scenarios[0]["decision"] == "ALLOW"
    assert scenarios[1]["decision"] == "DENY"
    assert scenarios[2]["decision"] == "DENY"
    assert scenarios[3]["decision"] == "DENY"

    return {
        "schema": SCHEMA,
        "mode": "non-production-deterministic",
        "scenarios": scenarios,
        "pass": all(item["pass"] for item in scenarios),
    }


if __name__ == "__main__":
    print(json.dumps(run_all(), sort_keys=True, separators=(",", ":")))
