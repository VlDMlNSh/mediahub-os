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
