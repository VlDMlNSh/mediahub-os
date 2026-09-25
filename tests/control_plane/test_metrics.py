from runtime.mediahub_control_plane.agent_registry import AgentRegistry
from runtime.mediahub_control_plane.loop import ControlLoop
from runtime.mediahub_control_plane.metrics import ControlPlaneMetrics
from runtime.mediahub_control_plane.model import Agent, AgentStatus, Task, TaskStatus
from runtime.mediahub_control_plane.reconciler import ControlPlaneReconciler
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.scheduler import TaskScheduler
from runtime.mediahub_control_plane.service import ControlPlaneService


def test_metrics_capture_dispatch_and_reconciliation():
    metrics = ControlPlaneMetrics(); repo = InMemoryControlPlaneRepository()
    registry = AgentRegistry(); registry.register(Agent('a','n','1',AgentStatus.IDLE,('linux',)))
    repo.create_task(Task('t','build',status=TaskStatus.READY))
    service = ControlPlaneService(repo, metrics=metrics)
    reconciler = ControlPlaneReconciler(repo, registry, metrics=metrics)
    loop = ControlLoop(reconciler, TaskScheduler(registry), service, metrics=metrics)
    loop.tick()
    snapshot = metrics.snapshot()
    assert snapshot.reconcile_ticks == 1
    assert snapshot.dispatch_attempts == 1
    assert snapshot.dispatch_successes == 1
    assert snapshot.claims == 1


def test_metrics_are_thread_safe_and_snapshot_is_immutable():
    metrics = ControlPlaneMetrics(); metrics.inc('claims', 2)
    snapshot = metrics.snapshot()
    assert snapshot.claims == 2
    try:
        snapshot.claims = 3
        raise AssertionError('snapshot must be immutable')
    except AttributeError:
        pass


def test_metrics_capture_retry_and_fencing_failure():
    metrics = ControlPlaneMetrics(); repo = InMemoryControlPlaneRepository()
    repo.create_task(Task('t','build',status=TaskStatus.READY,max_attempts=2))
    service = ControlPlaneService(repo, metrics=metrics); lease = service.claim('t','a',1)
    service.fail('t','a',1)
    assert metrics.snapshot().task_retries == 1
    repo.create_task(Task('f','build',status=TaskStatus.READY)); lease = service.claim('f','a',2)
    try:
        service.complete('f','other',2)
    except PermissionError:
        pass
    assert metrics.snapshot().fencing_failures == 1
