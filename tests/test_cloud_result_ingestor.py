import json
from pathlib import Path

from ops.mediahub_cloud_result_ingestor import ingest_manifest
from runtime.mediahub_control_plane.model import Task, TaskStatus
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.service import ControlPlaneService


def _fixture(tmp_path):
    repo = InMemoryControlPlaneRepository()
    task = Task("task-e2e-1", "cloud-development", status=TaskStatus.READY,
                idempotency_key="idem-e2e-1", max_attempts=2)
    repo.create_task(task)
    service = ControlPlaneService(repo)
    lease = service.claim("task-e2e-1", "astra-e2e", 7)
    operation = service.begin_external_operation(
        "task-e2e-1", "astra-e2e", 7, "gemini", "gemini-3.5-flash-lite",
        "op:task-e2e-1:exec-e2e-1:g7",
    )
    from runtime.mediahub_control_plane.model import Execution
    repo.record_execution(Execution("exec-e2e-1", "task-e2e-1", "astra-e2e", 7, "DISPATCHED"))
    result = "bounded engineering proposal"
    import hashlib
    manifest = {
        "schema_version": 1,
        "task_id": "task-e2e-1",
        "execution_id": "exec-e2e-1",
        "generation": 7,
        "operation_key": operation.operation_key,
        "provider": "gemini",
        "model": "gemini-3.5-flash-lite",
        "capability": "architecture",
        "result": result,
        "artifact_sha256": hashlib.sha256(result.encode()).hexdigest(),
        "run_id": "123",
        "target_sha": "a" * 40,
    }
    path = Path(tmp_path) / "cloud-evidence.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return repo, path, operation.operation_id


def test_ingestion_is_durable_and_idempotent(tmp_path):
    repo, path, operation_id = _fixture(tmp_path)
    assert ingest_manifest(repo, path) == "RECORDED"
    assert ingest_manifest(repo, path) == "IDEMPOTENT"
    operation = repo.get_operation(operation_id)
    assert operation.result["cloud_evidence"]["execution_id"] == "exec-e2e-1"
    assert any(e.event_type == "CloudEvidenceRecorded" for e in repo.events.values())


def test_ingestion_rejects_generation_mismatch(tmp_path):
    repo, path, _ = _fixture(tmp_path)
    data = json.loads(path.read_text())
    data["generation"] = 8
    path.write_text(json.dumps(data))
    import pytest
    with pytest.raises(PermissionError):
        ingest_manifest(repo, path)
