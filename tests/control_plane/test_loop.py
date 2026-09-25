from runtime.mediahub_control_plane.agent_registry import AgentRegistry
from runtime.mediahub_control_plane.loop import ControlLoop
from runtime.mediahub_control_plane.model import Agent, AgentStatus, Task, TaskStatus
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.scheduler import TaskScheduler
from runtime.mediahub_control_plane.service import ControlPlaneService
from runtime.mediahub_control_plane.reconciler import ControlPlaneReconciler


def test_loop_tick_reconciles_and_dispatches_ready_task():
    repo=InMemoryControlPlaneRepository(); repo.create_task(Task('t','build'))
    registry=AgentRegistry(); registry.register(Agent('a1','n1','1',AgentStatus.IDLE,('linux',)))
    scheduler=TaskScheduler(registry); service=ControlPlaneService(repo); loop=ControlLoop(ControlPlaneReconciler(repo,registry),scheduler,service,3)
    repo.update_task(Task('t','build',status=TaskStatus.READY))
    stats=loop.tick()
    assert stats.ticks==1 and stats.dispatched==1
    assert repo.get_task('t').status is TaskStatus.RUNNING


def test_loop_run_is_bounded():
    repo=InMemoryControlPlaneRepository(); registry=AgentRegistry(); scheduler=TaskScheduler(registry); service=ControlPlaneService(repo)
    loop=ControlLoop(ControlPlaneReconciler(repo,registry),scheduler,service,interval_seconds=.001)
    assert loop.run(max_ticks=3).ticks==3
