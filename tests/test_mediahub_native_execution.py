import pytest

from ops.mediahub_canonical_protocol import Protocol
from ops.mediahub_native_execution import (
    BoundedExecutionAdapter,
    CredentialRef,
    ExecutionProposal,
    ExecutionTarget,
    NativeExecutionContract,
    VerificationBoundary,
)


def target(provider="openai"):
    return ExecutionTarget(provider, "https://api.example.test/v1", Protocol.OPENAI_RESPONSES if provider == "openai" else Protocol.ANTHROPIC_MESSAGES, "test-model", CredentialRef(provider, "/credential"))

def test_openai_auth_headers_are_native_and_secret_not_logged():
    c=NativeExecutionContract((target(),))
    h=c.prepare_headers(target(), "SECRET")
    assert h["authorization"] == "Bearer SECRET"
    assert "SECRET" not in repr(c)

def test_anthropic_auth_headers_are_native():
    t=target("anthropic"); c=NativeExecutionContract((t,)); h=c.prepare_headers(t,"SECRET")
    assert h["x-api-key"] == "SECRET"
    assert h["anthropic-version"] == "2023-06-01"

def test_missing_credential_fails_closed():
    t=target(); c=NativeExecutionContract((t,))
    try: c.prepare_headers(t, "")
    except PermissionError: pass
    else: assert False

def test_credential_provider_mismatch_denied():
    t=ExecutionTarget("openai","https://api.example.test",Protocol.OPENAI_RESPONSES,"m",CredentialRef("anthropic","/x"))
    try: NativeExecutionContract((t,))
    except PermissionError: pass
    else: assert False

def test_non_https_denied():
    t=ExecutionTarget("openai","http://api.example.test",Protocol.OPENAI_RESPONSES,"m",CredentialRef("openai","/x"))
    try: NativeExecutionContract((t,))
    except PermissionError: pass
    else: assert False

def test_execution_proposal_preserves_identity():
    contract = NativeExecutionContract()
    proposal = contract.prepare_proposal("req-1", "work-1", "sha-1", "openai")
    assert proposal.request_id == "req-1"
    assert proposal.workload_id == "work-1"
    assert proposal.source_sha == "sha-1"
    assert proposal.provider == "openai"


def test_execution_proposal_missing_identity_fails_closed():
    contract = NativeExecutionContract()
    for values in (("", "work-1", "sha-1", "openai"), ("req-1", "", "sha-1", "openai"), ("req-1", "work-1", "", "openai"), ("req-1", "work-1", "sha-1", "")):
        with pytest.raises(PermissionError):
            contract.prepare_proposal(*values)

def test_recovery_evidence_admits_verified_execution_proposal():
    from types import SimpleNamespace

    evidence = SimpleNamespace(verified=True, request_id="req-r", workload_id="work-r", source_sha="sha-r")
    proposal = NativeExecutionContract().prepare_recovery_proposal(evidence, "openai")
    assert proposal.request_id == "req-r"
    assert proposal.workload_id == "work-r"
    assert proposal.source_sha == "sha-r"
    assert proposal.provider == "openai"


def test_unverified_recovery_evidence_fails_closed():
    from types import SimpleNamespace

    evidence = SimpleNamespace(verified=False, request_id="req-r", workload_id="work-r", source_sha="sha-r")
    with pytest.raises(PermissionError):
        NativeExecutionContract().prepare_recovery_proposal(evidence, "openai")


def test_recovery_evidence_missing_identity_fails_closed():
    from types import SimpleNamespace

    for evidence in (
        SimpleNamespace(verified=True, request_id="", workload_id="work-r", source_sha="sha-r"),
        SimpleNamespace(verified=True, request_id="req-r", workload_id="", source_sha="sha-r"),
        SimpleNamespace(verified=True, request_id="req-r", workload_id="work-r", source_sha=""),
    ):
        with pytest.raises(PermissionError):
            NativeExecutionContract().prepare_recovery_proposal(evidence, "openai")



def test_bounded_execution_adapter_admits_matching_proposal_and_target():
    proposal = ExecutionProposal("req-b", "work-b", "sha-b", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target(), 30, 4096)
    assert request.proposal == proposal
    assert request.target.provider == "openai"
    assert request.timeout_seconds == 30
    assert request.max_output_bytes == 4096


def test_bounded_execution_adapter_rejects_provider_mismatch():
    proposal = ExecutionProposal("req-b", "work-b", "sha-b", "anthropic")
    with pytest.raises(PermissionError):
        BoundedExecutionAdapter().admit(proposal, target("openai"))


def test_bounded_execution_adapter_rejects_timeout_outside_bounds():
    proposal = ExecutionProposal("req-b", "work-b", "sha-b", "openai")
    adapter = BoundedExecutionAdapter()
    with pytest.raises(ValueError):
        adapter.admit(proposal, target(), 0)
    with pytest.raises(ValueError):
        adapter.admit(proposal, target(), 901)


def test_bounded_execution_adapter_rejects_output_limit_outside_bounds():
    proposal = ExecutionProposal("req-b", "work-b", "sha-b", "openai")
    adapter = BoundedExecutionAdapter()
    with pytest.raises(ValueError):
        adapter.admit(proposal, target(), 60, 0)
    with pytest.raises(ValueError):
        adapter.admit(proposal, target(), 60, 1_048_577)


def test_bounded_execution_adapter_rejects_invalid_proposal():
    adapter = BoundedExecutionAdapter()
    with pytest.raises(PermissionError):
        adapter.admit(ExecutionProposal("", "work-b", "sha-b", "openai"), target())


def test_bounded_execution_adapter_never_executes():
    proposal = ExecutionProposal("req-b", "work-b", "sha-b", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target())
    with pytest.raises(PermissionError):
        BoundedExecutionAdapter().execute(request)


def test_bounded_execution_adapter_denies_secret_and_network_access():
    proposal = ExecutionProposal("req-b", "work-b", "sha-b", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target())
    adapter = BoundedExecutionAdapter()
    with pytest.raises(PermissionError):
        adapter.prepare_headers(request)
    with pytest.raises(PermissionError):
        adapter.prepare_network(request)


def test_verification_boundary_accepts_matching_completed_evidence():
    proposal = ExecutionProposal("req-v", "work-v", "sha-v", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target())
    verification = VerificationBoundary().verify(request, "COMPLETED", "sha-v")
    assert verification.status == "COMPLETED"
    assert verification.observed_source_sha == "sha-v"


def test_verification_boundary_accepts_matching_failed_evidence():
    proposal = ExecutionProposal("req-v", "work-v", "sha-v", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target())
    verification = VerificationBoundary().verify(request, "FAILED", "sha-v")
    assert verification.status == "FAILED"


def test_verification_boundary_rejects_unknown_status():
    proposal = ExecutionProposal("req-v", "work-v", "sha-v", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target())
    with pytest.raises(PermissionError):
        VerificationBoundary().verify(request, "RUNNING", "sha-v")


def test_verification_boundary_rejects_provenance_mismatch():
    proposal = ExecutionProposal("req-v", "work-v", "sha-v", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target())
    with pytest.raises(PermissionError):
        VerificationBoundary().verify(request, "COMPLETED", "other-sha")


def test_verification_boundary_rejects_missing_provenance():
    proposal = ExecutionProposal("req-v", "work-v", "sha-v", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target())
    with pytest.raises(PermissionError):
        VerificationBoundary().verify(request, "COMPLETED", "")


def test_verification_boundary_rejects_malformed_request_type():
    with pytest.raises(PermissionError):
        VerificationBoundary().verify(object(), "COMPLETED", "sha-v")


def test_verification_boundary_rejects_non_string_status_types():
    proposal = ExecutionProposal("req-v", "work-v", "sha-v", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target())
    for status in (1, True, None):
        with pytest.raises(PermissionError):
            VerificationBoundary().verify(request, status, "sha-v")


def test_verification_boundary_rejects_non_string_provenance_type():
    proposal = ExecutionProposal("req-v", "work-v", "sha-v", "openai")
    request = BoundedExecutionAdapter().admit(proposal, target())
    for observed_source_sha in (1, True, None):
        with pytest.raises(PermissionError):
            VerificationBoundary().verify(request, "COMPLETED", observed_source_sha)

def test_bounded_execution_request_rejects_malformed_object_types():
    proposal = ExecutionProposal("req-b", "work-b", "sha-b", "openai")
    valid_target = target()
    with pytest.raises(PermissionError):
        BoundedExecutionAdapter().admit(object(), valid_target)
    with pytest.raises(PermissionError):
        BoundedExecutionAdapter().admit(proposal, object())


def test_bounded_execution_request_rejects_non_integer_timeout_types():
    proposal = ExecutionProposal("req-b", "work-b", "sha-b", "openai")
    adapter = BoundedExecutionAdapter()
    for timeout_seconds in (True, False, 1.5, "30", None):
        with pytest.raises(PermissionError):
            adapter.admit(proposal, target(), timeout_seconds)


def test_bounded_execution_request_rejects_non_integer_output_limit_types():
    proposal = ExecutionProposal("req-b", "work-b", "sha-b", "openai")
    adapter = BoundedExecutionAdapter()
    for max_output_bytes in (True, False, 1.5, "4096", None):
        with pytest.raises(PermissionError):
            adapter.admit(proposal, target(), 30, max_output_bytes)
