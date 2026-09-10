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
