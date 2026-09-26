import pytest
from runtime.mediahub_control_plane.model import *
def test_task_rejects_running_to_ready():
    with pytest.raises(ValueError): validate_task_transition(TaskStatus.RUNNING, TaskStatus.READY)
def test_lease_rejects_released_to_active():
    with pytest.raises(ValueError): validate_lease_transition(LeaseStatus.RELEASED, LeaseStatus.ACTIVE)
def test_valid_task_transition(): validate_task_transition(TaskStatus.READY, TaskStatus.CLAIMED)
def test_records_are_immutable():
    t=Task('t','x')
    with pytest.raises((AttributeError,TypeError)): t.status=TaskStatus.READY

def test_reconciliation_transition_invariants():
    validate_task_transition(TaskStatus.RUNNING, TaskStatus.RECONCILIATION_REQUIRED)
    validate_task_transition(TaskStatus.RECONCILIATION_REQUIRED, TaskStatus.VERIFYING)
    validate_task_transition(TaskStatus.RECONCILIATION_REQUIRED, TaskStatus.READY)
    with pytest.raises(ValueError): validate_task_transition(TaskStatus.READY, TaskStatus.RECONCILIATION_REQUIRED)
    with pytest.raises(ValueError): validate_task_transition(TaskStatus.SUCCEEDED, TaskStatus.RECONCILIATION_REQUIRED)
