import pytest

from ops.ai.astra_host_envelope import AstraHostEnvelope
from ops.ai.astra_host_execution_gate import AstraHostExecutionGate, HostExecutionGateDenied
from ops.mediahub_canonical_protocol import Protocol
from ops.mediahub_native_execution import CredentialRef, ExecutionTarget


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


def target():
    return ExecutionTarget(
        provider="openai",
        endpoint="https://api.openai.com/v1",
        protocol=Protocol.OPENAI_RESPONSES,
        model="qualified-model",
        credential=CredentialRef("openai", "credential-ref"),
    )


def test_requires_explicit_authorization_and_recovery():
    gate = AstraHostExecutionGate()
    with pytest.raises(HostExecutionGateDenied):
        gate.admit(envelope(), target(), authorized=False, recovery_verified=True,
                   observed_source_sha="sha-1")
    with pytest.raises(HostExecutionGateDenied):
        gate.admit(envelope(), target(), authorized=True, recovery_verified=False,
                   observed_source_sha="sha-1")


def test_requires_boolean_verification_flags():
    gate = AstraHostExecutionGate()
    with pytest.raises(HostExecutionGateDenied):
        gate.admit(envelope(), target(), authorized=1, recovery_verified=True,
                   observed_source_sha="sha-1")
    with pytest.raises(HostExecutionGateDenied):
        gate.admit(envelope(), target(), authorized=True, recovery_verified=1,
                   observed_source_sha="sha-1")


def test_provenance_mismatch_is_denied():
    gate = AstraHostExecutionGate()
    with pytest.raises(HostExecutionGateDenied):
        gate.admit(envelope(), target(), authorized=True, recovery_verified=True,
                   observed_source_sha="different")


def test_qualified_bounded_request_is_created_without_execution():
    gate = AstraHostExecutionGate()
    result = gate.admit(
        envelope(), target(), authorized=True, recovery_verified=True,
        observed_source_sha="sha-1",
    )
    assert result.proposal.request_id == "req-1"
    assert result.proposal.workload_id == "work-1"
    assert result.bounded_request.timeout_seconds == 60
    assert result.bounded_request.max_output_bytes == 65536


def test_envelope_bounds_flow_into_native_contract():
    gate = AstraHostExecutionGate()
    result = gate.admit(
        envelope(timeout_seconds=900, output_limit_bytes=1_048_576),
        target(), authorized=True, recovery_verified=True,
        observed_source_sha="sha-1",
    )
    assert result.bounded_request.timeout_seconds == 900
    assert result.bounded_request.max_output_bytes == 1_048_576
