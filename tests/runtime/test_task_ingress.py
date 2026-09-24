import json

import pytest
from mediahub_runtime import AstraGatewayRuntime, AstraTaskRequest
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


def test_ingress_runs_pending_contracts_through_bounded_astra(tmp_path):
    task = AstraTaskRequest("req-2", "session-2", "Return READY")
    (tmp_path / "req-2.json").write_text(json.dumps(task_to_contract(task)), encoding="utf-8")
    gateway = AstraGatewayRuntime(executor=lambda _: "READY")

    results = FileTaskIngress(tmp_path).run_pending_bounded(gateway)

    assert len(results) == 1
    assert results[0].status == "PASS"
    assert results[0].result.output == "READY"


def test_ingress_rejects_invalid_bounded_gateway(tmp_path):
    with pytest.raises(TaskIngressError) as exc:
        FileTaskIngress(tmp_path).run_pending_bounded(object())
    assert exc.value.code == "invalid_gateway"


def test_ingress_rejects_wrong_schema(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(json.dumps({"schema_id": "wrong"}), encoding="utf-8")
    with pytest.raises(TaskIngressError) as exc:
        FileTaskIngress(tmp_path).read_pending()
    assert exc.value.code == "invalid_task_contract"


def test_ingress_rejects_duplicate_request_ids(tmp_path):
    first = AstraTaskRequest("req-dup", "session-1", "Return ONE")
    second = AstraTaskRequest("req-dup", "session-2", "Return TWO")
    (tmp_path / "a.json").write_text(json.dumps(task_to_contract(first)), encoding="utf-8")
    (tmp_path / "b.json").write_text(json.dumps(task_to_contract(second)), encoding="utf-8")

    with pytest.raises(TaskIngressError) as exc:
        FileTaskIngress(tmp_path).read_pending()
    assert exc.value.code == "duplicate_request_id"


def test_ingress_rejects_malformed_field_types(tmp_path):
    task = task_to_contract(AstraTaskRequest("req-type", "session-type", "Return READY"))
    task["approval_state"] = 123
    (tmp_path / "bad-type.json").write_text(json.dumps(task), encoding="utf-8")

    with pytest.raises(TaskIngressError) as exc:
        FileTaskIngress(tmp_path).read_pending()
    assert exc.value.code == "invalid_task_contract"


def test_ingress_rejects_oversized_file(tmp_path):
    path = tmp_path / "large.json"
    path.write_bytes(b"x" * 70_001)
    with pytest.raises(TaskIngressError) as exc:
        FileTaskIngress(tmp_path).read_pending()
    assert exc.value.code == "task_file_too_large"
