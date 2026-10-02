#!/usr/bin/env python3
"""Fail-closed validator for the ASTRA GOLD governance contract.

The reference-scheme review found three systemic risks that no test caught:

1. gate numbering was restated with different names in different documents;
2. numeric thresholds (heartbeat/lease/timeout/freshness) did not exist at all;
3. invariants, credential lifecycle and the human approval record existed only
   as prose.

`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml` is the single machine-readable
source for those values. This validator enforces that it cannot drift from the
canonical qualification schema, the unified system model and the reference
architecture, and that every invariant is bound to an enforcing test.

Exit code is 0 on success and 1 on the first failure (fail-closed).
"""

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]

GOVERNANCE = ROOT / "architecture" / "ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml"
QUALIFICATION = ROOT / "architecture" / "ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml"
UNIFIED = ROOT / "architecture" / "ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml"
REFERENCE = ROOT / "architecture" / "ASTRA-GOLD-REFERENCE-ARCHITECTURE.md"

GOVERNANCE_SCHEMA = "mediahub.astra-gold.governance.v1"

POSITIVE_INT_THRESHOLDS = (
    "heartbeat_ttl_seconds",
    "lease_ttl_seconds",
    "executor_timeout_seconds",
    "evidence_freshness_window_seconds",
    "result_publication_timeout_seconds",
    "retry_backoff_seconds",
    "max_parallel_autonomous_claims",
    "soak_duration_hours",
    "minimum_rounds_per_mandatory_path",
)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def verify(governance: dict, qualification: dict, unified: dict, reference_text: str, root: Path) -> dict:
    failures = []

    if governance.get("schema") != GOVERNANCE_SCHEMA:
        failures.append(f"unexpected governance schema: {governance.get('schema')}")

    # 1. Gate registry must equal the qualification schema and the unified model.
    registry = governance.get("gate_registry", {})
    registry_gates = registry.get("gates", [])
    registry_ids = [gate.get("id") for gate in registry_gates]
    qualification_ids = list(qualification.get("gates", {}))
    unified_ids = list(unified.get("qualification", {}).get("gate_contract", []))

    if registry_ids != qualification_ids:
        failures.append(f"gate_registry ids != qualification schema: {registry_ids} != {qualification_ids}")
    if registry_ids != unified_ids:
        failures.append(f"gate_registry ids != unified gate_contract: {registry_ids} != {unified_ids}")
    if [gate.get("order") for gate in registry_gates] != list(range(len(registry_gates))):
        failures.append("gate_registry order is not a contiguous 0..N sequence")

    # 2. Every gate name must appear canonically in the reference architecture.
    for gate in registry_gates:
        needle = f"G{gate.get('order')} — {gate.get('name')}"
        if needle not in reference_text:
            failures.append(f"reference architecture is missing canonical gate label: {needle!r}")

    # 3. Numeric thresholds are positive and mirror the qualification schema.
    thresholds = governance.get("runtime_thresholds", {})
    for key in POSITIVE_INT_THRESHOLDS:
        value = thresholds.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            failures.append(f"threshold {key} must be a positive integer, got {value!r}")

    gates = qualification.get("gates", {})
    if thresholds.get("max_parallel_autonomous_claims") != gates.get(
        "G5_CONCURRENCY", {}
    ).get("max_parallel_autonomous_claims"):
        failures.append("max_parallel_autonomous_claims does not mirror G5_CONCURRENCY")
    if thresholds.get("soak_duration_hours") != gates.get("G9_24H_SOAK", {}).get("duration_hours"):
        failures.append("soak_duration_hours does not mirror G9_24H_SOAK")
    if thresholds.get("minimum_rounds_per_mandatory_path") != gates.get(
        "G4_23_WAVE_QUALIFICATION", {}
    ).get("minimum_rounds_per_mandatory_path"):
        failures.append("minimum_rounds_per_mandatory_path does not mirror G4_23_WAVE_QUALIFICATION")

    # 4. Every invariant must name an existing enforcing test.
    invariants = governance.get("invariant_registry", {}).get("invariants", [])
    if len(invariants) < 16:
        failures.append(f"invariant registry is incomplete: {len(invariants)} < 16")
    seen_ids = set()
    for invariant in invariants:
        inv_id = invariant.get("id")
        if not inv_id or inv_id in seen_ids:
            failures.append(f"invariant id missing or duplicated: {inv_id!r}")
        seen_ids.add(inv_id)
        if not invariant.get("statement"):
            failures.append(f"invariant {inv_id} has no statement")
        enforced_by = invariant.get("enforced_by")
        if not enforced_by or not (root / enforced_by).exists():
            failures.append(f"invariant {inv_id} is not bound to an existing test: {enforced_by!r}")

    # 5. Credential lifecycle must be fail-closed.
    lifecycle = governance.get("credential_lifecycle", {})
    if lifecycle.get("credentials_in_git") is not False:
        failures.append("credential_lifecycle.credentials_in_git must be false")
    if lifecycle.get("credentials_in_evidence") is not False:
        failures.append("credential_lifecycle.credentials_in_evidence must be false")
    for flag in ("rotation_required", "revocation_supported", "audit_required", "per_provider_isolation"):
        if lifecycle.get(flag) is not True:
            failures.append(f"credential_lifecycle.{flag} must be true")
    if lifecycle.get("auxiliary_creation_allowed") is not False:
        failures.append("credential_lifecycle.auxiliary_creation_allowed must be false")
    if not isinstance(lifecycle.get("max_credential_age_days"), int) or lifecycle.get("max_credential_age_days", 0) <= 0:
        failures.append("credential_lifecycle.max_credential_age_days must be a positive integer")

    # 6. Human approval record must be human-only, signed and complete.
    approval = governance.get("human_approval_record", {})
    if approval.get("decision_authority") != "HUMAN_ONLY":
        failures.append("human_approval_record.decision_authority must be HUMAN_ONLY")
    if approval.get("unsigned_approval_rejected") is not True:
        failures.append("human_approval_record.unsigned_approval_rejected must be true")
    if approval.get("approval_expires_with_sha_change") is not True:
        failures.append("human_approval_record.approval_expires_with_sha_change must be true")
    required_fields = set(approval.get("required_fields", []))
    for field in ("approver_identity", "approval_timestamp", "approved_source_sha", "approval_signature", "rollback_target"):
        if field not in required_fields:
            failures.append(f"human_approval_record is missing required field: {field}")
    launch_inputs = qualification.get("launch_contract", {}).get("required_inputs", [])
    if list(approval.get("covers_launch_inputs", [])) != list(launch_inputs):
        failures.append(
            "human_approval_record.covers_launch_inputs != launch_contract.required_inputs: "
            f"{approval.get('covers_launch_inputs')} != {launch_inputs}"
        )

    # 7. Executor classes: mandatory paths mirror G4, cloud candidates carry no authority.
    executors = governance.get("executor_classes", {})
    mandatory = executors.get("mandatory_execution_paths", [])
    if mandatory != gates.get("G4_23_WAVE_QUALIFICATION", {}).get("mandatory_paths"):
        failures.append(f"executor_classes.mandatory_execution_paths != G4 mandatory_paths: {mandatory}")
    local = set(executors.get("local_executors", []))
    if not {"codex", "claude_code"} <= local:
        failures.append("executor_classes.local_executors must include codex and claude_code")
    candidate_paths = executors.get("candidate_cloud_executor_paths", [])
    if not candidate_paths:
        failures.append("executor_classes.candidate_cloud_executor_paths must not be empty")
    for candidate in candidate_paths:
        if candidate.get("authority") != "none":
            failures.append(f"cloud executor {candidate.get('id')} must have authority none")
        if candidate.get("status") != "NOT_PROVEN":
            failures.append(f"cloud executor {candidate.get('id')} must be NOT_PROVEN until independently qualified")
    rules = executors.get("rules", {})
    for flag in (
        "cloud_executor_requires_admission",
        "each_executor_path_requires_fresh_rounds",
        "gateway_path_is_not_native_provider_qualification",
        "provider_identity_preserved",
        "credential_boundary_isolated",
        "no_cloud_executor_authority",
        "independent_a3_required",
        "no_self_promotion",
    ):
        if rules.get(flag) is not True:
            failures.append(f"executor_classes.rules.{flag} must be true")
    if rules.get("executor_authority") != "EXECUTOR_ONLY":
        failures.append("executor_classes.rules.executor_authority must be EXECUTOR_ONLY")

    # 8. Evidence metadata must mirror the qualification evidence contract.
    evidence = governance.get("evidence_metadata", {})
    if list(evidence.get("required_metadata", [])) != list(
        qualification.get("evidence_bundle", {}).get("required_metadata", [])
    ):
        failures.append("evidence_metadata.required_metadata != qualification evidence contract")

    return {
        "status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "gates": len(registry_ids),
        "invariants": len(invariants),
        "cloud_executor_candidates": len(candidate_paths),
    }


def main() -> int:
    governance = load_yaml(GOVERNANCE)
    qualification = load_yaml(QUALIFICATION)
    unified = load_yaml(UNIFIED)
    reference_text = REFERENCE.read_text(encoding="utf-8")
    result = verify(governance, qualification, unified, reference_text, ROOT)
    for failure in result["failures"]:
        print(f"FAIL: {failure}")
    print(f"GOVERNANCE_GATES={result['gates']}")
    print(f"GOVERNANCE_INVARIANTS={result['invariants']}")
    print(f"GOVERNANCE_CLOUD_EXECUTOR_CANDIDATES={result['cloud_executor_candidates']}")
    print(f"GOVERNANCE_VALIDATION={result['status']}")
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
