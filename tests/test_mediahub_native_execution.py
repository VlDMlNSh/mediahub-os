import pytest

from ops.mediahub_canonical_protocol import Protocol
from ops.mediahub_native_execution import (
    CredentialRef,
    ExecutionTarget,
    NativeExecutionContract,
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

