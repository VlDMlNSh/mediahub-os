import pytest

from runtime.mediahub_control_plane.model import AuditRecord, Event, Execution, Task, TaskStatus
from runtime.mediahub_control_plane.sqlite_repository import SQLiteControlPlaneRepository


def ready(repo):
    repo.create_task(Task("t", "build", status=TaskStatus.READY, idempotency_key="k", payload={"x": 1}))


def test_state_survives_repository_restart(tmp_path):
    path = tmp_path / "control-plane.db"
    first = SQLiteControlPlaneRepository(path)
    ready(first)
    lease = first.claim_task("t", "agent-a", 7)
    first.append_event(Event("e", "Claimed", 1.0, "task", "t", {"secret": "must-not-be-logged"}))
    first.append_audit(AuditRecord("e", 1.0, "agent-a", "claim", "task", "t", "READY", "CLAIMED", "RECORDED"))
    first = None

    second = SQLiteControlPlaneRepository(path)
    assert second.get_task("t").status is TaskStatus.CLAIMED
    assert second.get_lease_for_task("t").lease_id == lease.lease_id
    assert second.list_tasks()[0].payload == {"x": 1}


def test_claim_is_single_owner_and_idempotency_is_durable(tmp_path):
    path = tmp_path / "control-plane.db"
    repo = SQLiteControlPlaneRepository(path)
    ready(repo)
    repo2 = SQLiteControlPlaneRepository(path)
    with pytest.raises(ValueError):
        repo2.create_task(Task("other", "build", idempotency_key="k"))
    repo.claim_task("t", "agent-a", 1)
    with pytest.raises(ValueError):
        repo2.claim_task("t", "agent-b", 1)


def test_stale_generation_is_fenced_after_restart(tmp_path):
    path = tmp_path / "control-plane.db"
    repo = SQLiteControlPlaneRepository(path)
    ready(repo)
    repo.claim_task("t", "agent-a", 9)
    repo = SQLiteControlPlaneRepository(path)
    with pytest.raises(PermissionError):
        repo.record_execution(Execution("e", "t", "agent-a", 8, "SUCCEEDED"))


def test_event_and_audit_append_are_idempotent(tmp_path):
    repo = SQLiteControlPlaneRepository(tmp_path / "control-plane.db")
    event = Event("e", "X", 1.0, "task", "t")
    audit = AuditRecord("e", 1.0, "x", "claim", "task", "t", "READY", "CLAIMED", "ok")
    assert repo.append_event(event) == event
    assert repo.append_event(event) == event
    assert repo.append_audit(audit) == audit
    assert repo.append_audit(audit) == audit
