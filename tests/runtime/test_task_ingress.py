import json

import pytest
from mediahub_runtime import AstraTaskRequest
from mediahub_runtime.task_ingress import (
    FileTaskIngress,
    TaskIngressError,
    task_to_contract,
)


def test_task_contract_round_trip(tmp_path):
    task = AstraTaskRequest("req-1", "session-1", "Return READY")
    path = tmp_path / "req-1.json"
    path.write_text(json.dumps(task_to_contract(task)), encoding="utf-8")

    loaded = FileTaskIngress(tmp_path).read_pending()
    assert loaded == (task,)


def test_ingress_rejects_wrong_schema(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"schema_id": "wrong"}), encoding="utf-8")
    with pytest.raises(TaskIngressError) as exc:
        FileTaskIngress(tmp_path).read_pending()
    assert exc.value.code == "invalid_task_contract"


def test_ingress_rejects_oversized_file(tmp_path):
    path = tmp_path / "large.json"
    path.write_bytes(b"x" * 70_001)
    with pytest.raises(TaskIngressError) as exc:
        FileTaskIngress(tmp_path).read_pending()
    assert exc.value.code == "task_file_too_large"
