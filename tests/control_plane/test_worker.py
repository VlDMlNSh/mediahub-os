import pytest

from runtime.mediahub_control_plane.model import Task, TaskStatus, LeaseStatus
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.service import ControlPlaneService
from runtime.mediahub_control_plane.worker import LeaseLost, WorkerRuntime


def running_task():
    repo = InMemoryControlPlaneRepository()
    service = ControlPlaneService(repo)
    repo.create_task(Task("t", "build", payload={"x": 1}, status=TaskStatus.READY))
    lease = service.claim("t", "a", 1)
    return repo, service, lease


def test_worker_success_verifies_and_releases_lease():
    repo, service, lease = running_task()
    worker = WorkerRuntime(service)
    execution = worker.execute("t", "a", 1, lambda payload, ctx: {"ok": payload["x"]}, lambda result: result["ok"] == 1)
    assert execution.status == "SUCCEEDED"
    assert repo.get_task("t").status is TaskStatus.SUCCEEDED
    assert repo.get_lease_for_task("t") is None
    assert worker.completed_tasks == 1


def test_stale_generation_is_rejected_before_executor():
    repo, service, lease = running_task()
    called = False

    def executor(payload, context):
        nonlocal called
        called = True
        return payload

    with pytest.raises(LeaseLost):
        WorkerRuntime(service).execute("t", "a", 99, executor, lambda result: True)
    assert called is False
    assert repo.get_task("t").status is TaskStatus.RUNNING
    assert repo.get_lease_for_task("t").status is LeaseStatus.ACTIVE


def test_renewal_failure_prevents_authoritative_completion():
    repo, service, lease = running_task()

    def executor(payload, context):
        repo.expire_lease(lease.lease_id, lease.expires_at)
        with pytest.raises(LeaseLost):
            context.renew()
        return payload

    with pytest.raises(LeaseLost):
        WorkerRuntime(service).execute("t", "a", 1, executor, lambda result: True)
    assert repo.get_task("t").status is TaskStatus.RUNNING


def test_verifier_failure_records_failed_and_releases_lease():
    repo, service, lease = running_task()
    with pytest.raises(ValueError, match="verification"):
        WorkerRuntime(service).execute("t", "a", 1, lambda payload, ctx: payload, lambda result: False)
    assert repo.get_task("t").status is TaskStatus.FAILED
    assert repo.get_lease_for_task("t") is None


def test_worker_runtime_can_process_sequential_tasks():
    repo = InMemoryControlPlaneRepository()
    service = ControlPlaneService(repo)
    worker = WorkerRuntime(service)
    for task_id in ("t1", "t2"):
        repo.create_task(Task(task_id, "build", status=TaskStatus.READY))
        service.claim(task_id, "a", 1)
        worker.run_once(task_id, "a", 1, lambda payload, ctx: "done", lambda result: result == "done")
    assert worker.completed_tasks == 2
    assert all(repo.get_task(task_id).status is TaskStatus.SUCCEEDED for task_id in ("t1", "t2"))
