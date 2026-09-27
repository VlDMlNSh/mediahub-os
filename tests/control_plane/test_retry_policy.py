import pytest
from runtime.mediahub_control_plane.model import FailureClass
from runtime.mediahub_control_plane.retry_policy import RetryPolicy

def test_retry_policy_scales_by_failure_class_and_attempt():
    p=RetryPolicy(base_delay_seconds=5,worker_multiplier=2,infrastructure_multiplier=3)
    assert p.decide(FailureClass.TASK,1,4).delay_seconds == 5
    assert p.decide(FailureClass.WORKER,2,4).delay_seconds == 20
    assert p.decide(FailureClass.INFRASTRUCTURE,2,4).delay_seconds == 30

def test_retry_policy_stops_at_budget():
    d=RetryPolicy().decide(FailureClass.TASK,3,3)
    assert d.retry is False and d.reason == 'retry_budget_exhausted'

def test_retry_policy_rejects_invalid_inputs():
    with pytest.raises(ValueError): RetryPolicy(-1)
    with pytest.raises(ValueError): RetryPolicy(worker_multiplier=0.5)
    with pytest.raises(ValueError): RetryPolicy().decide(FailureClass.TASK,0,2)
