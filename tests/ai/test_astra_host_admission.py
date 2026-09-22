import pytest

from ops.ai.astra_host_admission import AstraHostAdmission, HostAdmissionDenied
from ops.ai.astra_host_envelope import AstraHostEnvelope
from ops.ai.task_delivery import DeliveryState, TaskDeliveryJournal
from ops.ai.task_lease import TaskLease


def envelope(**overrides):
    values = dict(
        version=1, request_id="req-1", session_id="sess-1",
        conversation_id="conv-1", generation=1, host_id="host-1",
        workload_id="work-1", source_sha="sha-1", command="pytest -q",
        timeout_seconds=60, output_limit_bytes=65536,
        authorization_id="auth-1", capabilities=frozenset({"host.execute"}),
    )
    values.update(overrides)
    return AstraHostEnvelope(**values)


def make(tmp_path):
    delivery = TaskDeliveryJournal(tmp_path / "delivery.json")
    lease = TaskLease(tmp_path / "lease.json", "work-1", "host-1", worktree=str(tmp_path))
    return AstraHostAdmission(delivery, lease), delivery, lease


def test_prepare_binds_delivery_and_lease_without_execution(tmp_path):
    admission, delivery, lease = make(tmp_path)
    result = admission.prepare(envelope())
    assert result.envelope_fingerprint == envelope().fingerprint()
    assert result.delivery.state is DeliveryState.PREPARED
    assert lease.read_record()["task_id"] == "work-1"
    assert not (tmp_path / "execution.marker").exists()
    admission.safe_stop()
    delivery.release()
    lease.release()


def test_same_envelope_is_idempotent_during_prepared_state(tmp_path):
    admission, delivery, lease = make(tmp_path)
    first = admission.prepare(envelope())
    second = admission.prepare(envelope())
    assert first == second
    admission.safe_stop()
    delivery.release()
    lease.release()


def test_replay_with_different_request_is_denied(tmp_path):
    admission, delivery, lease = make(tmp_path)
    admission.prepare(envelope())
    with pytest.raises(HostAdmissionDenied):
        admission.prepare(envelope(request_id="req-2"))
    admission.safe_stop()
    delivery.release()
    lease.release()


def test_context_mismatch_is_denied(tmp_path):
    admission, delivery, lease = make(tmp_path)
    admission.prepare(envelope())
    with pytest.raises(HostAdmissionDenied):
        admission.prepare(envelope(generation=2))
    admission.safe_stop()
    delivery.release()
    lease.release()


def test_different_workload_is_denied(tmp_path):
    admission, delivery, lease = make(tmp_path)
    with pytest.raises(HostAdmissionDenied):
        admission.prepare(envelope(workload_id="other"))
    delivery.release()
    lease.release()


def test_no_dispatch_transition_occurs(tmp_path):
    admission, delivery, lease = make(tmp_path)
    result = admission.prepare(envelope())
    assert result.delivery.state is DeliveryState.PREPARED
    assert result.delivery.attempt == 0
    admission.safe_stop()
    delivery.release()
    lease.release()
