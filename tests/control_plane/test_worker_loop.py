import threading
import time

from runtime.mediahub_control_plane.model import Task, TaskStatus
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.service import ControlPlaneService
from runtime.mediahub_control_plane.worker import WorkerRuntime
from runtime.mediahub_control_plane.worker_loop import LeaseRenewalSupervisor, WorkerLoop


def test_worker_loop_executes_assigned_task_and_returns_to_polling():
    repo = InMemoryControlPlaneRepository()
    service = ControlPlaneService(repo)
    repo.create_task(Task("t", "build", status=TaskStatus.READY))
    service.claim("t", "agent", 7)
    loop = WorkerLoop(repo, WorkerRuntime(service), "agent", 7,
                      lambda task_type: lambda payload, ctx: "ok",
                      lambda task_type: lambda result: result == "ok")
    assert loop.run(max_polls=2).executed == 1
    assert loop.stats.polls == 2
    assert repo.get_task("t").status is TaskStatus.SUCCEEDED


def test_lease_renewal_supervisor_renews_until_stopped():
    calls = []
    supervisor = LeaseRenewalSupervisor(lambda: calls.append(time.monotonic()), 0.01, lambda: None)
    supervisor.start()
    time.sleep(0.04)
    supervisor.stop()
    assert len(calls) >= 2


def test_lease_renewal_supervisor_surfaces_loss():
    lost = threading.Event()
    supervisor = LeaseRenewalSupervisor(lambda: (_ for _ in ()).throw(RuntimeError("lost")), 0.01, lost.set)
    supervisor.start()
    assert lost.wait(0.2)
    supervisor.stop()


def test_worker_loop_renews_short_lease_while_executor_runs():
    from dataclasses import replace

    repo = InMemoryControlPlaneRepository()
    service = ControlPlaneService(repo)
    repo.create_task(Task("t", "build", status=TaskStatus.READY))
    lease = service.claim("t", "agent", 7)
    repo.leases[lease.lease_id] = replace(lease, expires_at=lease.last_renewed_at + 0.02)
    loop = WorkerLoop(repo, WorkerRuntime(service), "agent", 7,
                      lambda task_type: lambda payload, ctx: (time.sleep(0.05), "ok")[1],
                      lambda task_type: lambda result: result == "ok",
                      renewal_interval_seconds=0.005)

    assert loop.run(max_polls=1).executed == 1
    assert repo.get_task("t").status is TaskStatus.SUCCEEDED


def test_worker_loop_stops_authoritative_completion_when_renewal_fails():
    class FailingRenewRepository(InMemoryControlPlaneRepository):
        def renew_lease(self, lease_id, agent_id, generation, expires_at):
            raise ConnectionError("control plane unavailable")

    repo = FailingRenewRepository()
    service = ControlPlaneService(repo)
    repo.create_task(Task("t", "build", status=TaskStatus.READY, max_attempts=2))
    service.claim("t", "agent", 7)
    loop = WorkerLoop(repo, WorkerRuntime(service), "agent", 7,
                      lambda task_type: lambda payload, ctx: (time.sleep(0.03), "ok")[1],
                      lambda task_type: lambda result: result == "ok",
                      renewal_interval_seconds=0.005)

    assert loop.run(max_polls=1).failures == 1
    assert repo.get_task("t").status is TaskStatus.RETRY_WAIT
    assert repo.list_executions()[0].failure_class.value == "INFRASTRUCTURE"
