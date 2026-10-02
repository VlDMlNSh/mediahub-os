#!/usr/bin/env python3
"""Deterministic, non-production privacy/data-boundary PoC.

This harness models the separation between compute contribution, user data,
and developer personnel access. It performs no network I/O, credential access,
or production execution.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

SCHEMA = "mediahub.privacy-data-boundary-poc.v1"


@dataclass(frozen=True)
class DataClass:
    name: str
    personal: bool


@dataclass(frozen=True)
class WorkloadContract:
    workload_id: str
    workload_class: str
    required_data: tuple[str, ...]
    result_fields: tuple[str, ...]
    developer_personnel_access: bool


def digest_material(values: tuple[str, ...]) -> str:
    return hashlib.sha256("|".join(values).encode()).hexdigest()


def evaluate_boundary(
    contract: WorkloadContract,
    available_data: tuple[DataClass, ...],
    *,
    developer_execution_allowed: bool,
) -> dict:
    personal_requested = any(
        item.personal and item.name in contract.required_data for item in available_data
    )
    # Pre-decision condition: raw personal data would cross the boundary if the
    # request were admitted. This is the attempt, not the outcome.
    raw_personal_data_would_cross = personal_requested and developer_execution_allowed

    if contract.developer_personnel_access:
        decision, reason = "DENY", "developer_personnel_access_forbidden"
    elif raw_personal_data_would_cross:
        decision, reason = "DENY", "raw_personal_data_would_cross_boundary"
    elif not developer_execution_allowed:
        decision, reason = "DENY", "developer_execution_not_admitted"
    elif contract.workload_class not in {"CLOUD_DEVELOPMENT_ONLY", "CLOUD_ESCALATED_USER"}:
        decision, reason = "DENY", "unsupported_workload_class"
    else:
        decision, reason = "ALLOW", "privacy_boundary_satisfied"

    # Exposure is a post-decision fact: it is True only when raw personal data
    # actually crossed the boundary, i.e. only on an ALLOW that requested it.
    # The pre-decision condition is reported separately so a blocked attempt
    # stays visible in the evidence without being counted as exposure.
    raw_personal_data_exposed = decision == "ALLOW" and raw_personal_data_would_cross

    return {
        "schema": SCHEMA,
        "workload_id": contract.workload_id,
        "workload_class": contract.workload_class,
        "required_data": list(contract.required_data),
        "result_fields": list(contract.result_fields),
        "developer_personnel_access": contract.developer_personnel_access,
        "personal_data_requested": personal_requested,
        "raw_personal_data_would_cross": raw_personal_data_would_cross,
        "raw_personal_data_exposed": raw_personal_data_exposed,
        "developer_execution_allowed": developer_execution_allowed,
        "decision": decision,
        "reason": reason,
        "contract_digest": digest_material(
            (contract.workload_id, contract.workload_class, *contract.required_data)
        ),
        "pass": True,
    }


def run_all() -> dict:
    engineering = DataClass("build_artifact", False)
    personal = DataClass("user_media", True)

    scenarios = [
        evaluate_boundary(
            WorkloadContract(
                "s1", "CLOUD_DEVELOPMENT_ONLY", ("build_artifact",),
                ("build_result",), False
            ),
            (engineering, personal),
            developer_execution_allowed=True,
        ),
        evaluate_boundary(
            WorkloadContract(
                "s2", "CLOUD_ESCALATED_USER", ("user_media",),
                ("bounded_result",), False
            ),
            (engineering, personal),
            developer_execution_allowed=True,
        ),
        evaluate_boundary(
            WorkloadContract(
                "s3", "CLOUD_ESCALATED_USER", ("build_artifact",),
                ("bounded_result",), True
            ),
            (engineering, personal),
            developer_execution_allowed=True,
        ),
        evaluate_boundary(
            WorkloadContract(
                "s4", "CLOUD_ESCALATED_USER", ("user_media",),
                ("bounded_result",), False
            ),
            (engineering, personal),
            developer_execution_allowed=False,
        ),
    ]
    names = (
        "S1_developer_workload_without_personal_data",
        "S2_raw_personal_data_crossing_denied",
        "S3_developer_personnel_access_denied",
        "S4_local_personal_data_retained",
    )
    for item, name in zip(scenarios, names):
        item["scenario"] = name

    assert scenarios[0]["decision"] == "ALLOW"
    assert scenarios[0]["raw_personal_data_exposed"] is False
    assert scenarios[1]["decision"] == "DENY"
    assert scenarios[2]["decision"] == "DENY"
    assert scenarios[3]["decision"] == "DENY"

    # A denied attempt must stay visible as an attempt, and must never be
    # recorded as an actual exposure.
    assert scenarios[1]["raw_personal_data_would_cross"] is True
    assert scenarios[1]["raw_personal_data_exposed"] is False
    assert all(item["raw_personal_data_exposed"] is False for item in scenarios)

    return {
        "schema": SCHEMA,
        "mode": "non-production-deterministic",
        "scenarios": scenarios,
        "pass": all(item["pass"] for item in scenarios),
    }


if __name__ == "__main__":
    print(json.dumps(run_all(), sort_keys=True, separators=(",", ":")))
