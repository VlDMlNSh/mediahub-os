from runtime.mediahub_control_plane.model import Task, TaskStatus, LeaseStatus
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository
from runtime.mediahub_control_plane.service import ControlPlaneService

def test_vertical_happy_path():
    r=InMemoryControlPlaneRepository(); s=ControlPlaneService(r)
    r.create_task(Task('t','build',status=TaskStatus.PENDING))
    s.mark_ready('t'); lease=s.claim('t','a',1)
    assert r.get_task('t').status is TaskStatus.RUNNING
    execution=s.complete('t','a',1,{'verified':True})
    assert execution.status=='SUCCEEDED'; assert r.get_task('t').status is TaskStatus.SUCCEEDED
    assert r.get_lease_for_task('t') is None

def test_expired_lease_requires_recovery():
    r=InMemoryControlPlaneRepository(); s=ControlPlaneService(r)
    r.create_task(Task('t','build',status=TaskStatus.READY)); lease=r.claim_task('t','a',1)
    r.update_task(Task('t','build',status=TaskStatus.RUNNING))
    assert s.recover_expired('t', lease.expires_at+1) is True
    assert r.get_task('t').status is TaskStatus.EXPIRED


def test_fail_sets_deterministic_exponential_retry_backoff():
    from runtime.mediahub_control_plane.service import ControlPlaneService
    r=InMemoryControlPlaneRepository(); r.create_task(Task('retry','build',status=TaskStatus.READY,max_attempts=3))
    s=ControlPlaneService(r,retry_backoff_seconds=10.0); s.claim('retry','a',1); s.fail('retry','a',1,'EXECUTION_FAILED')
    t=r.get_task('retry')
    assert t.status is TaskStatus.RETRY_WAIT and t.attempt==1 and t.retry_not_before is not None
    assert 9.0 <= t.retry_not_before - __import__('time').monotonic() <= 11.0
