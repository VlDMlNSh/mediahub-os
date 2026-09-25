from runtime.mediahub_control_plane.model import Task, TaskStatus
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.reconciler import ControlPlaneReconciler


def test_reconciler_releases_dependency_block_when_predecessor_succeeds():
    r=InMemoryControlPlaneRepository()
    r.create_task(Task('a','build',status=TaskStatus.SUCCEEDED))
    r.create_task(Task('b','build',status=TaskStatus.BLOCKED,dependencies=('a',)))
    assert ControlPlaneReconciler(r).reconcile_once()==('b',)
    assert r.get_task('b').status is TaskStatus.READY


def test_reconciler_expires_stale_lease_and_task():
    r=InMemoryControlPlaneRepository()
    r.create_task(Task('t','build',status=TaskStatus.READY))
    lease=r.claim_task('t','a',1)
    r.update_task(Task('t','build',status=TaskStatus.RUNNING))
    assert ControlPlaneReconciler(r).reconcile_once(lease.expires_at+1)==('t',)
    assert r.get_task('t').status is TaskStatus.EXPIRED
    assert r.get_lease_for_task('t').status.value=='EXPIRED'


def test_reconciler_is_idempotent_after_convergence():
    r=InMemoryControlPlaneRepository()
    r.create_task(Task('a','build',status=TaskStatus.SUCCEEDED))
    r.create_task(Task('b','build',status=TaskStatus.PENDING,dependencies=('a',)))
    rec=ControlPlaneReconciler(r)
    assert rec.reconcile_once()==('b',)
    assert rec.reconcile_once()==()
