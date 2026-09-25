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
