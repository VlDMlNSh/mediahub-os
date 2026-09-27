import hashlib
import json
from pathlib import Path

from ops.mediahub_cloud_result_ingestor import ingest_github_run, ingest_manifest
from runtime.mediahub_control_plane.model import Execution, Task, TaskStatus
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.service import ControlPlaneService


def _fixture(tmp_path):
    repo = InMemoryControlPlaneRepository()
    task = Task("task-e2e-1", "cloud-development", status=TaskStatus.READY,
                idempotency_key="idem-e2e-1", max_attempts=2)
    repo.create_task(task)
    service = ControlPlaneService(repo)
    service.claim("task-e2e-1", "astra-e2e", 7)
    operation = service.begin_external_operation(
        "task-e2e-1", "astra-e2e", 7, "gemini", "gemini-3.5-flash-lite",
        "op:task-e2e-1:exec-e2e-1:g7",
    )
    repo.record_execution(Execution("exec-e2e-1", "task-e2e-1", "astra-e2e", 7, "DISPATCHED"))
    result = "bounded engineering proposal"
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


def test_github_run_ingestion_authenticates_run_and_artifact(tmp_path, monkeypatch):
    repo, path, _ = _fixture(tmp_path)
    manifest = json.loads(path.read_text())
    manifest["target_sha"] = "b" * 40

    class Result:
        returncode = 0
        stdout = json.dumps({
            "databaseId": "123",
            "workflowName": "MediaHub Cloud Development Agent",
            "status": "completed",
            "conclusion": "success",
            "event": "workflow_dispatch",
            "headSha": "b" * 40,
        })
        stderr = ""

    def fake_run(argv, **kwargs):
        if argv[1:4] == ["run", "view", "123"]:
            return Result()
        download_dir = Path(argv[-1])
        artifact = download_dir / "cloud-evidence.json"
        artifact.write_text(json.dumps(manifest), encoding="utf-8")
        return type("DownloadResult", (), {"returncode": 0, "stdout": "", "stderr": ""})()

    monkeypatch.setattr("ops.mediahub_cloud_result_ingestor.subprocess.run", fake_run)
    assert ingest_github_run(repo, "123") == "RECORDED"


def test_github_run_ingestion_rejects_untrusted_workflow(tmp_path, monkeypatch):
    repo, _, _ = _fixture(tmp_path)

    class Result:
        returncode = 0
        stdout = json.dumps({
            "databaseId": "123",
            "workflowName": "Untrusted Workflow",
            "status": "completed",
            "conclusion": "success",
            "event": "workflow_dispatch",
            "headSha": "c" * 40,
        })
        stderr = ""

    monkeypatch.setattr("ops.mediahub_cloud_result_ingestor.subprocess.run", lambda *a, **k: Result())
    import pytest
    with pytest.raises(PermissionError):
        ingest_github_run(repo, "123")
