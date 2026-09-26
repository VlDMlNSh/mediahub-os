"""Authenticated/provenance-bound ingestion of GitHub Actions cloud evidence.

The GitHub Actions workflow is the credential boundary. This module is deliberately
credential-free: it accepts a verified evidence manifest produced by that workflow
and persists it through the authoritative Control Plane operation journal.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from uuid import uuid4

from runtime.mediahub_control_plane.model import AuditRecord, Event, OperationStatus


SAFE = re.compile(r"^[A-Za-z0-9._:/-]{1,256}$")
SCHEMA_VERSION = 1


def _safe(value: str, name: str) -> str:
    if not isinstance(value, str) or not SAFE.fullmatch(value):
        raise ValueError(f"invalid {name}")
    return value


def _load_manifest(path: str | Path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("unsupported evidence schema")
    required = (
        "task_id", "execution_id", "generation", "operation_key", "provider",
        "model", "capability", "result", "artifact_sha256", "run_id",
        "target_sha",
    )
    for key in required:
        if key not in data:
            raise ValueError(f"missing evidence field: {key}")
    for key in required:
        if key != "generation" and key != "result":
            _safe(str(data[key]), key)
    if not isinstance(data["generation"], int) or data["generation"] < 1:
        raise ValueError("invalid generation")
    if not isinstance(data["result"], str):
        raise ValueError("result must be text")
    if hashlib.sha256(data["result"].encode("utf-8")).hexdigest() != data["artifact_sha256"]:
        raise ValueError("artifact digest mismatch")
    return data


def ingest_manifest(repository, manifest_path: str | Path, *, actor: str = "astra-cloud-ingestor") -> str:
    """Persist one cloud result exactly once, fenced by task/execution/generation."""
    data = _load_manifest(manifest_path)
    operation = repository.get_operation_by_key(data["operation_key"])
    if operation is None:
        raise ValueError("unknown operation_key")
    if operation.task_id != data["task_id"] or operation.generation != data["generation"]:
        raise PermissionError("operation generation/task fence failed")
    if operation.provider != data["provider"]:
        raise PermissionError("provider fence failed")

    executions = [e for e in repository.list_executions() if e.execution_id == data["execution_id"]]
    if not executions:
        raise ValueError("unknown execution_id")
    execution = executions[0]
    if execution.task_id != data["task_id"] or execution.lease_generation != data["generation"]:
        raise PermissionError("execution generation/task fence failed")

    evidence = {
        "schema_version": SCHEMA_VERSION,
        "execution_id": data["execution_id"],
        "run_id": data["run_id"],
        "target_sha": data["target_sha"],
        "capability": data["capability"],
        "artifact_sha256": data["artifact_sha256"],
        "result": data["result"],
    }

    if operation.status is OperationStatus.RESOLVED:
        prior = operation.result or {}
        if prior.get("cloud_evidence") == evidence:
            return "IDEMPOTENT"
        raise ValueError("operation already resolved with different evidence")
    if operation.status is not OperationStatus.RECONCILIATION_REQUIRED:
        raise ValueError(f"operation not ingestible: {operation.status.value}")

    resolved = repository.resolve_operation(
        operation.operation_id,
        {"cloud_evidence": evidence, "provenance": {"provider": data["provider"], "model": data["model"]}},
    )
    now = repository.now() if hasattr(repository, "now") else 0.0
    event_id = str(uuid4())
    repository.append_event(Event(
        event_id, "CloudEvidenceRecorded", now, "operation",
        operation.operation_id, evidence,
        data["execution_id"],
    ))
    repository.append_audit(AuditRecord(
        event_id, now, actor, "CloudEvidenceRecorded", "operation",
        operation.operation_id, OperationStatus.RECONCILIATION_REQUIRED.value,
        resolved.status.value, "RECORDED", data["execution_id"],
    ))
    return "RECORDED"
