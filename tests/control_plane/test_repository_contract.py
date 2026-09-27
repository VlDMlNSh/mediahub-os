import pytest
from runtime.mediahub_control_plane.model import Task,TaskStatus,Execution
from runtime.mediahub_control_plane.repository import InMemoryControlPlaneRepository

def ready(repo):
    repo.create_task(Task('t','build',status=TaskStatus.READY,idempotency_key='k'))

def test_duplicate_task_identity_is_rejected():
    r=InMemoryControlPlaneRepository(); ready(r)
    with pytest.raises(ValueError): r.create_task(Task('t','build'))

def test_single_owner_claim():
    r=InMemoryControlPlaneRepository(); ready(r)
    a=r.claim_task('t','a',1)
    with pytest.raises(ValueError): r.claim_task('t','b',1)
    assert a.agent_id=='a' and r.get_task('t').status is TaskStatus.CLAIMED

def test_execution_rejects_stale_generation():
    r=InMemoryControlPlaneRepository(); ready(r); r.claim_task('t','a',2)
    with pytest.raises(PermissionError): r.record_execution(Execution('e','t','a',1,'SUCCEEDED'))

def test_event_and_audit_append_are_idempotent():
    from runtime.mediahub_control_plane.model import Event,AuditRecord
    r=InMemoryControlPlaneRepository(); e=Event('e','X',1,'task','t'); assert r.append_event(e)==r.append_event(e)
    a=AuditRecord('a',1,'x','claim','task','t','READY','CLAIMED','ok'); assert r.append_audit(a)==r.append_audit(a)
