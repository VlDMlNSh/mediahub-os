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


def test_reconciler_requeues_expired_task_when_retry_budget_remains():
    r=InMemoryControlPlaneRepository(); r.create_task(Task('retry','build',status=TaskStatus.READY,max_attempts=2))
    lease=r.claim_task('retry','a',1); r.update_task(Task('retry','build',status=TaskStatus.RUNNING,max_attempts=2))
    assert ControlPlaneReconciler(r).reconcile_once(lease.expires_at+1)==('retry',)
    task=r.get_task('retry')
    assert task.status is TaskStatus.RETRY_WAIT and task.attempt==1


def test_reconciler_exhausted_expired_task_is_terminal():
    r=InMemoryControlPlaneRepository(); r.create_task(Task('dead','build',status=TaskStatus.READY,max_attempts=1))
    lease=r.claim_task('dead','a',1); r.update_task(Task('dead','build',status=TaskStatus.RUNNING,max_attempts=1))
    assert ControlPlaneReconciler(r).reconcile_once(lease.expires_at+1)==('dead',)
    assert r.get_task('dead').status is TaskStatus.EXPIRED and r.get_task('dead').attempt==1
