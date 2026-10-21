#!/usr/bin/env python3
"""Proposed, fixture-only semantic crosswalk for MediaHub cloud-agent v0.2.

This is an engineering test profile, not an accepted issuer, admission, scheduler,
provider, qualification, or promotion contract. Synthetic fixture references are
never resolved to live authority and no provider or credential is accessed.
"""
from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "docs" / "checkpoints"
FIXTURE_DIR = ROOT / "tests" / "fixtures" / "cloud-agent-schemas" / "valid"
REPORT_PATH = ROOT / "artifacts" / "cloud-agent-semantic-validation-report.json"

SCHEMAS = {
    "task_envelope": {
        "path": SCHEMA_DIR / "MEDIAHUB-CLOUD-AGENT-TASK-ENVELOPE-SCHEMA-V0.2-WAVE-16-2026-10-16.json",
        "blob_sha1": "6f3cd3d40b2c5fe3f21bb6085536769fbef8322a",
    },
    "agent_registry": {
        "path": SCHEMA_DIR / "MEDIAHUB-CLOUD-AGENT-REGISTRY-SCHEMA-V0.2-WAVE-16-2026-10-16.json",
        "blob_sha1": "b49b89b8fbdfc180862e3dc78f8198f35e486035",
    },
    "evidence_manifest": {
        "path": SCHEMA_DIR / "MEDIAHUB-CLOUD-AGENT-EVIDENCE-MANIFEST-SCHEMA-V0.2-WAVE-16-2026-10-16.json",
        "blob_sha1": "40c402432fd0f3899d45fde0fa0a8af4d34c593a",
    },
}

FIXTURE_FILES = {
    "task": FIXTURE_DIR / "task-envelope-v0.2.json",
    "registry": FIXTURE_DIR / "agent-registry-v0.2.json",
    "manifest": FIXTURE_DIR / "evidence-manifest-v0.2.json",
}
SHA256_RE = re.compile(r"^sha256:[a-f0-9]{64}$")
GIT_SHA_RE = re.compile(r"^[a-f0-9]{40}$")
SENSITIVITY = {"public": 0, "internal": 1, "confidential": 2, "restricted": 3}


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: Any) -> str:
    """SHA-256 of UTF-8 JSON sorted by key, with compact separators and no trailing newline."""
    encoded = json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    return "sha256:" + sha256_hex(encoded)


def current_commit() -> str | None:
    try:
        value = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
        return value if GIT_SHA_RE.fullmatch(value) else None
    except (OSError, subprocess.CalledProcessError):
        return None


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_time(value: Any) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            return None
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        return None


def path_covers(parent: str, child: str) -> bool:
    """Conservative path-prefix check for repository-relative allowlist entries."""
    parent = parent.replace("\\", "/")
    child = child.replace("\\", "/")
    if parent.startswith("/") or child.startswith("/") or ".." in child.split("/"):
        return False
    normalized_parent = parent.rstrip("/")
    normalized_child = child.rstrip("/")
    return normalized_child == normalized_parent or normalized_child.startswith(normalized_parent + "/")


def path_overlaps(left: str, right: str) -> bool:
    return path_covers(left, right) or path_covers(right, left)


def issue(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def semantic_issues(
    task: dict[str, Any],
    registry: dict[str, Any],
    manifest: dict[str, Any],
    schema_digests: dict[str, str],
    verify_digest_bindings: bool = True,
    verify_schema_ref_digests: bool = True,
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []

    def add(code: str, path: str, message: str) -> None:
        errors.append(issue(code, path, message))

    # v0.2 cross-document version and immutable schema-digest binding.
    if task.get("evidence", {}).get("manifest_schema") != manifest.get("schema_version"):
        add("SCHEMA_VERSION_CROSSREF", "task.evidence.manifest_schema", "Task manifest_schema does not match the manifest's schema_version.")
    refs = manifest.get("schema_refs", [])
    ref_by_name: dict[str, list[dict[str, Any]]] = {}
    for item in refs:
        if isinstance(item, dict):
            ref_by_name.setdefault(str(item.get("name")), []).append(item)
    expected_names = set(SCHEMAS)
    if set(ref_by_name) != expected_names or any(len(items) != 1 for items in ref_by_name.values()):
        add("SCHEMA_REF_CARDINALITY", "manifest.schema_refs", "Require exactly one reference each for task_envelope, agent_registry, and evidence_manifest.")
    for name in sorted(expected_names):
        items = ref_by_name.get(name, [])
        if len(items) != 1:
            continue
        ref = items[0]
        if ref.get("version") != "0.2":
            add("SCHEMA_REF_VERSION", f"manifest.schema_refs[{name}].version", "Schema reference version must be 0.2 for this pinned test profile.")
        expected_digest = "sha256:" + schema_digests[name]
        if verify_schema_ref_digests and ref.get("sha256") != expected_digest:
            add("SCHEMA_REF_DIGEST", f"manifest.schema_refs[{name}].sha256", f"Expected exact source-byte digest {expected_digest}.")
    # Explicit canonical JSON digest convention used by this proposed profile.
    if verify_digest_bindings:
        expected_task_digest = canonical_sha256(task)
        if manifest.get("task", {}).get("task_envelope_sha256") != expected_task_digest:
            add("TASK_DIGEST_BINDING", "manifest.task.task_envelope_sha256", f"Expected canonical JSON digest {expected_task_digest}.")
        expected_registry_digest = canonical_sha256(registry)
        if manifest.get("agent", {}).get("registry_record_sha256") != expected_registry_digest:
            add("REGISTRY_DIGEST_BINDING", "manifest.agent.registry_record_sha256", f"Expected canonical JSON digest {expected_registry_digest}.")
        idempotency_key = task.get("retry", {}).get("idempotency_key")
        expected_idempotency_digest = "sha256:" + sha256_hex(str(idempotency_key).encode("utf-8"))
        if manifest.get("task", {}).get("idempotency_key_digest") != expected_idempotency_digest:
            add("IDEMPOTENCY_DIGEST_BINDING", "manifest.task.idempotency_key_digest", f"Expected SHA-256 of the idempotency-key UTF-8 bytes: {expected_idempotency_digest}.")

    # The exact repository/ref/commit must be consistent across task and execution evidence.
    task_source = task.get("source", {})
    manifest_source = manifest.get("source", {})
    for left, right, label in (
        (task_source.get("repository"), manifest_source.get("repository"), "repository"),
        (task_source.get("ref"), manifest_source.get("requested_ref"), "ref"),
        (task_source.get("commit_sha"), manifest_source.get("resolved_sha"), "commit_sha"),
    ):
        if left != right:
            add("SOURCE_PROVENANCE_MISMATCH", "manifest.source", f"Task and evidence manifest disagree on source {label}.")

    if manifest.get("task", {}).get("task_id") != task.get("task_id"):
        add("TASK_ID_MISMATCH", "manifest.task.task_id", "Evidence manifest task_id differs from the task envelope.")
    if manifest.get("agent", {}).get("agent_id") != registry.get("agent_id"):
        add("AGENT_ID_MISMATCH", "manifest.agent.agent_id", "Evidence manifest agent_id differs from the registry record.")
    for manifest_key, registry_key in (("provider_id", "provider_id"), ("model_id", "model_id")):
        if manifest.get("agent", {}).get(manifest_key) != registry.get("identity", {}).get(registry_key):
            add("AGENT_IDENTITY_MISMATCH", f"manifest.agent.{manifest_key}", f"Evidence manifest {manifest_key} differs from the registry identity.")
    if manifest.get("policy", {}).get("policy_bundle_sha256") != task.get("semantic_validation", {}).get("policy_bundle_sha256"):
        add("POLICY_BUNDLE_MISMATCH", "manifest.policy.policy_bundle_sha256", "Task semantic-validation policy bundle differs from the manifest policy bundle.")

    # Registry time ordering. This profile intentionally does not claim real-time freshness
    # or verify the referenced revocation source.
    lifecycle = registry.get("lifecycle", {})
    issued = parse_time(lifecycle.get("issued_at"))
    expires = parse_time(lifecycle.get("expires_at"))
    reviewed = parse_time(lifecycle.get("last_reviewed_at"))
    if issued is None or expires is None or issued >= expires:
        add("REGISTRY_LIFETIME_INVALID", "registry.lifecycle", "issued_at must parse with an offset and be strictly earlier than expires_at.")
    if reviewed is None or issued is None or expires is None or not (issued <= reviewed <= expires):
        add("REGISTRY_REVIEW_TIME_INVALID", "registry.lifecycle.last_reviewed_at", "last_reviewed_at must be within the issued_at–expires_at interval.")
    status = registry.get("status")
    evidence_kinds = {e.get("kind") for e in registry.get("evidence", []) if isinstance(e, dict)}
    if status == "revoked" and "revocation" not in evidence_kinds:
        add("REVOCATION_EVIDENCE_MISSING", "registry.evidence", "A record marked revoked must at least reference revocation evidence; live authenticity is not checked here.")
    if status == "authorized" and not {"authorization", "security_review"}.issubset(evidence_kinds):
        add("AUTHORIZATION_EVIDENCE_MISSING", "registry.evidence", "An 'authorized' label requires both authorization and security_review evidence kinds in this fixture profile; authenticity/authority must still be independently verified.")

    # Task grant ∩ registry capability ∩ provider route ∩ output effect.
    task_type = task.get("task_type")
    capabilities = registry.get("capabilities", {})
    if task_type not in capabilities.get("task_types", []):
        add("TASK_TYPE_OUTSIDE_CAPABILITY", "registry.capabilities.task_types", "Registry does not grant the task envelope's task_type.")
    task_class = task.get("data_policy", {}).get("classification")
    if task_class not in SENSITIVITY:
        add("UNKNOWN_DATA_CLASS_FAIL_CLOSED", "task.data_policy.classification", "Unknown data class is not dispatchable under this semantic profile.")
    if task_class not in capabilities.get("data_classes", []):
        add("DATA_CLASS_OUTSIDE_CAPABILITY", "registry.capabilities.data_classes", "Registry does not permit the task's data classification.")
    task_scope = task.get("scope", {})
    registry_allowed = capabilities.get("allowed_paths", [])
    task_allowed = task_scope.get("allowed_paths", [])
    registry_forbidden = capabilities.get("forbidden_paths", [])
    task_forbidden = task_scope.get("forbidden_paths", [])
    for path_value in task_allowed:
        if not any(path_covers(grant, path_value) for grant in registry_allowed):
            add("PATH_OUTSIDE_CAPABILITY", "task.scope.allowed_paths", f"Task path {path_value!r} is not covered by a registry path grant.")
        if any(path_overlaps(path_value, denied) for denied in task_forbidden + registry_forbidden):
            add("ALLOW_DENY_PATH_OVERLAP", "task.scope", f"Task allowed path {path_value!r} overlaps a forbidden path.")
    for path_value in registry_allowed:
        if any(path_overlaps(path_value, denied) for denied in registry_forbidden):
            add("REGISTRY_ALLOW_DENY_OVERLAP", "registry.capabilities", f"Registry allow path {path_value!r} overlaps a forbidden path.")
    if task_scope.get("max_changed_files", 0) > capabilities.get("max_changed_files", -1):
        add("CHANGE_BUDGET_EXCEEDS_CAPABILITY", "task.scope.max_changed_files", "Task changed-file budget exceeds the registry capability.")
    budget = task.get("budget", {})
    execution = registry.get("execution", {})
    if budget.get("max_attempts", 0) > execution.get("max_attempts", -1):
        add("ATTEMPT_BUDGET_EXCEEDS_CAPABILITY", "task.budget.max_attempts", "Task max_attempts exceeds the registry execution cap.")
    if budget.get("max_duration_seconds", 0) > execution.get("timeout_seconds", -1):
        add("TIME_BUDGET_EXCEEDS_CAPABILITY", "task.budget.max_duration_seconds", "Task duration exceeds the registry timeout.")
    if budget.get("max_input_bytes", 0) > execution.get("max_input_bytes", -1):
        add("INPUT_BUDGET_EXCEEDS_CAPABILITY", "task.budget.max_input_bytes", "Task max_input_bytes exceeds the registry execution cap.")
    if budget.get("max_output_bytes", 0) > execution.get("max_output_bytes", -1):
        add("OUTPUT_BUDGET_EXCEEDS_CAPABILITY", "task.budget.max_output_bytes", "Task max_output_bytes exceeds the registry execution cap.")
    if execution.get("isolated_workspace_required") is not True:
        add("ISOLATION_REQUIRED", "registry.execution.isolated_workspace_required", "This semantic profile requires an isolated workspace.")

    mode_to_effect = {"read_only": "read_only", "isolated_branch": "patch_branch", "draft_pr": "pull_request"}
    expected_effect = mode_to_effect.get(task.get("output", {}).get("write_mode"))
    if expected_effect is None or expected_effect not in capabilities.get("effects", []):
        add("OUTPUT_EFFECT_OUTSIDE_CAPABILITY", "task.output.write_mode", "Task output mode has no matching registry capability effect.")

    # Provider/model/authorization/data-class must resolve to one exact registry route.
    destinations = task.get("routing", {}).get("authorized_destinations", [])
    routes = registry.get("provider_routes", [])
    if not destinations:
        add("NO_AUTHORIZED_DESTINATION", "task.routing.authorized_destinations", "No provider destination is available for this fixture task.")
    for index, destination in enumerate(destinations):
        matched = [
            route for route in routes
            if route.get("provider_id") == destination.get("provider_id")
            and route.get("model_id") == destination.get("model_id")
            and route.get("authorization_ref") == destination.get("authorization_ref")
            and task_class in route.get("data_classes", [])
        ]
        if not matched:
            add("PROVIDER_ROUTE_MISMATCH", f"task.routing.authorized_destinations[{index}]", "No registry route matches provider, model, authorization reference and data class.")
        if destination.get("provider_id") != registry.get("identity", {}).get("provider_id") or destination.get("model_id") != registry.get("identity", {}).get("model_id"):
            add("ROUTE_IDENTITY_MISMATCH", f"task.routing.authorized_destinations[{index}]", "Task destination differs from the registry agent identity.")
    # A more restrictive output classification is allowed; weakening it is not.
    output_class = task.get("output", {}).get("artifact_classification")
    if task_class in SENSITIVITY and output_class in SENSITIVITY and SENSITIVITY[output_class] < SENSITIVITY[task_class]:
        add("OUTPUT_CLASSIFICATION_DOWNGRADE", "task.output.artifact_classification", "Output classification is less protective than input/task data classification.")

    # Manifest execution, verification, review, promotion and qualification are distinct.
    execution_record = manifest.get("execution", {})
    execution_status = execution_record.get("status")
    started = parse_time(execution_record.get("started_at"))
    finished = parse_time(execution_record.get("finished_at"))
    if started is None:
        add("EXECUTION_START_INVALID", "manifest.execution.started_at", "started_at must be a timezone-aware date-time.")
    if finished is not None and started is not None and finished < started:
        add("EXECUTION_TIME_REVERSED", "manifest.execution.finished_at", "finished_at must not precede started_at.")
    if execution_status == "running" and finished is not None:
        add("RUNNING_HAS_FINISH_TIME", "manifest.execution.finished_at", "A running execution must not have a finish timestamp.")
    if execution_status in {"completed", "failed", "cancelled"} and finished is None:
        add("TERMINAL_EXECUTION_MISSING_FINISH", "manifest.execution.finished_at", "A terminal execution status must have a finish timestamp.")
    executor_result = manifest.get("disposition", {}).get("executor_result")
    expected_result = {"completed": {"success", "partial"}, "failed": {"failed"}, "cancelled": {"cancelled"}, "indeterminate": {"indeterminate"}}
    if execution_status in expected_result and executor_result not in expected_result[execution_status]:
        add("EXECUTION_RESULT_MISMATCH", "manifest.disposition.executor_result", f"executor_result is inconsistent with execution status {execution_status!r}.")
    if execution_status in {"accepted", "rejected", "running"} and executor_result in {"success", "failed", "cancelled"}:
        add("LIFECYCLE_STATE_COLLAPSE", "manifest", "Admission/active execution state cannot claim a terminal executor result.")

    verification = manifest.get("verification", {})
    verification_status = verification.get("status")
    if verification_status == "passed":
        if not verification.get("reviewer_identity_ref") or not verification.get("evidence_ref"):
            add("VERIFICATION_EVIDENCE_MISSING", "manifest.verification", "Passed verification requires a named reviewer and evidence reference.")
    qualification = manifest.get("qualification", {})
    qualification_status = qualification.get("status")
    if qualification_status == "qualified":
        if verification_status != "passed":
            add("QUALIFICATION_WITHOUT_VERIFICATION", "manifest.qualification.status", "Qualification cannot be qualified unless verification status is passed.")
        if not qualification.get("decision_ref"):
            add("QUALIFICATION_DECISION_MISSING", "manifest.qualification.decision_ref", "Qualified status requires a separate decision reference.")
    if qualification_status == "rejected" and not qualification.get("decision_ref"):
        add("QUALIFICATION_REJECTION_MISSING_DECISION", "manifest.qualification.decision_ref", "Rejected qualification requires a decision reference.")
    review = manifest.get("review", {})
    if manifest.get("disposition", {}).get("promotion_state") == "approved_for_next_gate":
        if review.get("decision") != "approved" or verification_status != "passed":
            add("PROMOTION_WITHOUT_REVIEW", "manifest.disposition.promotion_state", "Next-gate promotion requires an approved review and passed verification.")
    if manifest.get("disposition", {}).get("promotion_state") == "quarantined" and qualification_status == "qualified":
        add("QUALIFIED_BUT_QUARANTINED", "manifest.disposition.promotion_state", "A qualified artifact cannot remain in quarantined disposition under this fixture profile.")

    # Aggregate input/output bounds must obey both task policy and registry limits.
    inputs = manifest.get("inputs", [])
    input_bytes = sum(item.get("bytes", 0) for item in inputs if isinstance(item, dict))
    if input_bytes > budget.get("max_input_bytes", 0):
        add("AGGREGATE_INPUT_BYTES_EXCEEDED", "manifest.inputs", "Aggregate input bytes exceed the task budget.")
    artifacts = manifest.get("artifacts", [])
    output_bytes = sum(item.get("bytes", 0) for item in artifacts if isinstance(item, dict))
    if len(artifacts) > task.get("output", {}).get("max_artifacts", 0):
        add("ARTIFACT_COUNT_EXCEEDED", "manifest.artifacts", "Artifact count exceeds task output.max_artifacts.")
    if output_bytes > budget.get("max_output_bytes", 0):
        add("AGGREGATE_OUTPUT_BYTES_EXCEEDED", "manifest.artifacts", "Aggregate artifact bytes exceed the task output budget.")
    return errors


def reseal(bundle: dict[str, Any], schema_digests: dict[str, str]) -> None:
    """Make a mutated non-digest case internally content-bound before testing its target invariant."""
    manifest = bundle["manifest"]
    manifest["task"]["task_envelope_sha256"] = canonical_sha256(bundle["task"])
    manifest["agent"]["registry_record_sha256"] = canonical_sha256(bundle["registry"])
    manifest["task"]["idempotency_key_digest"] = "sha256:" + sha256_hex(
        str(bundle["task"].get("retry", {}).get("idempotency_key")).encode("utf-8")
    )
    for item in manifest.get("schema_refs", []):
        name = item.get("name")
        if name in SCHEMAS:
            item["version"] = "0.2"
            item["sha256"] = "sha256:" + schema_digests[name]


def build_negative_cases(base: dict[str, Any], schema_digests: dict[str, str]) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []

    def add(case_id: str, mutation: str, apply, reseal_after: bool = True,
            verify_digest_bindings: bool = True, verify_schema_ref_digests: bool = True) -> None:
        candidate = copy.deepcopy(base)
        apply(candidate)
        if reseal_after:
            reseal(candidate, schema_digests)
        issues = semantic_issues(
            candidate["task"], candidate["registry"], candidate["manifest"],
            schema_digests, verify_digest_bindings=verify_digest_bindings,
            verify_schema_ref_digests=verify_schema_ref_digests,
        )
        cases.append({
            "id": case_id,
            "mutation": mutation,
            "result": "PASS" if issues else "FAIL",
            "issue_codes": sorted({item["code"] for item in issues}),
            "issue_count": len(issues),
        })

    add("task-manifest-source-ref-mismatch", "change task source ref without changing manifest ref",
        lambda b: b["task"]["source"].update(ref="refs/heads/unreviewed"), True)
    add("task-id-mismatch", "change manifest task ID",
        lambda b: b["manifest"]["task"].update(task_id="CAF-Q-999"), True)
    add("schema-reference-version-mismatch", "change evidence schema version",
        lambda b: next(x for x in b["manifest"]["schema_refs"] if x["name"] == "evidence_manifest").update(version="0.1"),
        False, True, False)
    add("schema-reference-duplicate", "duplicate task-envelope schema reference",
        lambda b: b["manifest"]["schema_refs"].append(copy.deepcopy(b["manifest"]["schema_refs"][0])),
        True, True, False)
    add("registry-expiry-before-issuance", "set expiry earlier than issuance",
        lambda b: b["registry"]["lifecycle"].update(expires_at="2026-10-16T10:00:00Z"))
    add("registry-review-after-expiry", "set review after the registry expires",
        lambda b: b["registry"]["lifecycle"].update(last_reviewed_at="2027-01-02T00:00:00Z"))
    add("route-authorization-mismatch", "change task destination authorization reference",
        lambda b: b["task"]["routing"]["authorized_destinations"][0].update(authorization_ref="authorization://other"))
    add("task-type-outside-agent-capability", "remove task type from registry capability",
        lambda b: b["registry"]["capabilities"].update(task_types=["documentation"]))
    add("task-data-class-outside-agent-capability", "restrict registry to internal data",
        lambda b: b["registry"]["capabilities"].update(data_classes=["internal"]))
    add("task-path-outside-agent-allowlist", "limit registry paths to docs/readme/",
        lambda b: b["registry"]["capabilities"].update(allowed_paths=["docs/readme/"]))
    add("task-change-budget-exceeds-agent", "reduce registry changed-file cap below task cap",
        lambda b: b["registry"]["capabilities"].update(max_changed_files=-1))
    add("execution-finish-before-start", "reverse execution timestamps",
        lambda b: b["manifest"]["execution"].update(started_at="2026-10-17T10:00:02Z"))
    add("running-execution-has-finish", "mark run running while retaining finish timestamp",
        lambda b: b["manifest"]["execution"].update(status="running"))
    add("completed-execution-no-finish", "remove finish timestamp for a completed execution",
        lambda b: b["manifest"]["execution"].update(finished_at=None))
    add("qualified-without-verification", "set qualification qualified while verification is not_run",
        lambda b: b["manifest"]["qualification"].update(status="qualified", decision_ref="decision://fixture"))
    add("qualified-without-decision", "set qualification qualified without a decision reference",
        lambda b: b["manifest"]["qualification"].update(status="qualified", decision_ref=None),
        True)
    add("promotion-with-pending-review", "approve next gate while review is pending",
        lambda b: b["manifest"]["disposition"].update(promotion_state="approved_for_next_gate"))
    add("output-classification-downgrade", "downgrade output below the task input data class",
        lambda b: (
            b["task"]["data_policy"].update(classification="internal"),
            b["registry"]["capabilities"].update(data_classes=["internal"]),
            b["registry"]["provider_routes"][0].update(data_classes=["internal"]),
            b["task"]["output"].update(artifact_classification="public"),
        ))
    add("idempotency-digest-mismatch", "mutate digest without resealing",
        lambda b: b["manifest"]["task"].update(idempotency_key_digest="sha256:" + "0" * 64),
        False, True, True)
    add("schema-digest-mismatch", "mutate a pinned schema digest without resealing",
        lambda b: next(x for x in b["manifest"]["schema_refs"] if x["name"] == "task_envelope").update(sha256="sha256:" + "0" * 64),
        False, True, True)
    add("registry-record-digest-mismatch", "mutate registry digest without resealing",
        lambda b: b["manifest"]["agent"].update(registry_record_sha256="sha256:" + "0" * 64),
        False, True, True)
    add("aggregate-input-budget-exceeded", "add input bytes above task budget",
        lambda b: b["manifest"].update(inputs=[{"path":"docs/checkpoints/fixture.json","sha256":"sha256:"+"1"*64,"bytes":10001,"data_class":"public"}]))
    add("aggregate-output-budget-exceeded", "set artifact bytes above task output budget",
        lambda b: b["manifest"]["artifacts"][0].update(bytes=10001))
    add("artifact-count-exceeded", "set max artifact count to zero",
        lambda b: b["task"]["output"].update(max_artifacts=0))
    add("revoked-without-revocation-evidence", "mark registry revoked without evidence kind revocation",
        lambda b: b["registry"].update(status="revoked"))
    add("authorized-status-without-independent-evidence", "mark registry authorized without authorization/security review evidence",
        lambda b: b["registry"].update(status="authorized"))
    return cases


def main() -> int:
    report: dict[str, Any] = {
        "report_schema": "mediahub.cloud-agent-semantic-validation-report.v1",
        "profile": {
            "id": "mediahub.cloud-agent-semantic-validation.v0.2",
            "status": "PROPOSED_FIXTURE_ONLY_NOT_ACCEPTED",
            "canonical_json_digest": "UTF-8 JSON with sorted keys, compact separators, ensure_ascii=false, no trailing newline",
        },
        "status": "RUNNING",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": None,
        "source": {
            "repository": "VlDMlNSh/mediahub-os",
            "commit_sha": current_commit(),
            "workflow_run_id": __import__("os").environ.get("GITHUB_RUN_ID"),
            "workflow_run_attempt": __import__("os").environ.get("GITHUB_RUN_ATTEMPT"),
        },
        "schema_bindings": {},
        "failures": [],
        "counts": {
            "schemas_meta_validated": 0,
            "bundle_positive_expected": 1,
            "bundle_positive_passed": 0,
            "semantic_negative_expected": 25,
            "semantic_negative_rejected": 0,
            "failures": 0,
        },
        "positive_bundle": {},
        "negative_cases": [],
        "findings": [],
        "limitations": [
            "This profile is proposed and fixture-only; it is not an accepted A0 issuer/admission contract.",
            "All issuer, grant, reviewer, route, policy and revocation references are inert strings; existence, signature, authority, expiry source and revocation state are not resolved.",
            "No provider call, credential read, workflow dispatch, registry write, scheduler action, qualification, release or deployment occurs.",
            "Canonical JSON digest semantics are proposed for test consistency and require contract review before production consumption.",
        ],
    }

    try:
        schemas: dict[str, dict[str, Any]] = {}
        schema_digests: dict[str, str] = {}
        validators: dict[str, Draft202012Validator] = {}
        for name, spec in SCHEMAS.items():
            raw = spec["path"].read_bytes()
            blob = git_blob_sha1(raw)
            digest = sha256_hex(raw)
            report["schema_bindings"][name] = {
                "path": str(spec["path"].relative_to(ROOT)),
                "expected_git_blob_sha1": spec["blob_sha1"],
                "observed_git_blob_sha1": blob,
                "raw_file_sha256": "sha256:" + digest,
                "git_blob_pin_match": blob == spec["blob_sha1"],
            }
            if blob != spec["blob_sha1"]:
                report["failures"] .append(f"{name}: schema Git blob SHA differs from reviewed pin.")
            schema = read_json(spec["path"])
            Draft202012Validator.check_schema(schema)
            report["counts"]["schemas_meta_validated"] += 1
            schemas[name] = schema
            schema_digests[name] = digest
            validators[name] = Draft202012Validator(schema, format_checker=FormatChecker())

        bundle = {key: read_json(path) for key, path in FIXTURE_FILES.items()}
        fixture_schemas = {"task": "task_envelope", "registry": "agent_registry", "manifest": "evidence_manifest"}
        fixture_validation_errors = []
        for key, schema_name in fixture_schemas.items():
            errors = sorted(validators[schema_name].iter_errors(bundle[key]), key=lambda error: (str(error.json_path), error.message))
            if errors:
                fixture_validation_errors.append({"fixture": key, "errors": [{"path": str(e.json_path), "message": e.message} for e in errors[:5]]})
        report["positive_bundle"]["schema_validation_errors"] = fixture_validation_errors

        base_issues = semantic_issues(bundle["task"], bundle["registry"], bundle["manifest"], schema_digests)
        report["positive_bundle"]["semantic_issues"] = base_issues
        report["positive_bundle"]["expected_digest_bindings"] = {
            "task_envelope_sha256": canonical_sha256(bundle["task"]),
            "registry_record_sha256": canonical_sha256(bundle["registry"]),
            "idempotency_key_digest": "sha256:" + sha256_hex(str(bundle["task"].get("retry", {}).get("idempotency_key")).encode("utf-8")),
            "schema_refs": {name: "sha256:" + digest for name, digest in schema_digests.items()},
        }
        if not fixture_validation_errors and not base_issues:
            report["counts"]["bundle_positive_passed"] += 1
        else:
            report["failures"].append(
                f"Positive semantic bundle failed: schema_errors={len(fixture_validation_errors)}, semantic_issues={len(base_issues)}."
            )

        cases = build_negative_cases(bundle, schema_digests)
        report["counts"]["semantic_negative_expected"] = len(cases)
        report["negative_cases"] = cases
        for case in cases:
            if case["result"] == "PASS":
                report["counts"]["semantic_negative_rejected"] += 1
            else:
                report["failures"].append(f"{case['id']}: semantic mutation unexpectedly passed.")

        # Explicit advisory finding: a schema-valid value/reference is not a real grant.
        report["findings"].append({
            "id": "AUTHORITY_REFERENCES_UNRESOLVED",
            "severity": "P0",
            "status": "OPEN",
            "detail": "The fixture bundle is synthetic. This pass validates only field consistency and digest semantics; it does not establish issuer identity, grant authority, policy validity, route eligibility, or revocation.",
        })
    except Exception as exc:
        report["failures"].append(f"validator_exception: {type(exc).__name__}: {str(exc)[:1000]}")

    report["counts"]["failures"] = len(report["failures"])
    report["status"] = "PASS" if not report["failures"] else "FAIL"
    report["finished_at"] = datetime.now(timezone.utc).isoformat()
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
