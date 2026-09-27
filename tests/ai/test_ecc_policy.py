import pytest

from ops.ai.ecc_policy import ECCDenied, ECCPolicy, ECCRequest, ECCRole


@pytest.mark.parametrize(
    "role",
    [ECCRole.EXPLORER, ECCRole.REVIEWER, ECCRole.DOCS_RESEARCHER, ECCRole.VERIFICATION_LOOP],
)
def test_allowlisted_roles_are_advisory_and_provenance_bound(role):
    policy = ECCPolicy()
    auth = policy.admit(
        ECCRequest("task-1", role, "sha-1", frozenset({"read-repo", "review"}))
    )
    assert auth.role is role
    assert auth.scope == "advisory"
    assert auth.source_sha == "sha-1"
    assert policy.audit_events[-1]["event"] == "admitted"


def test_state_authority_production_release_and_secret_capabilities_are_denied():
    policy = ECCPolicy()
    for capability in ("state-authority", "production", "release", "secrets", "credential-access"):
        with pytest.raises(ECCDenied):
            policy.admit(ECCRequest("task-1", ECCRole.REVIEWER, "sha-1", frozenset({capability})))


def test_network_write_is_denied():
    with pytest.raises(ECCDenied):
        ECCPolicy().admit(ECCRequest("task-1", ECCRole.EXPLORER, "sha-1", frozenset({"network-write"})))


def test_non_advisory_scope_is_denied():
    with pytest.raises(ECCDenied):
        ECCPolicy().admit(ECCRequest("task-1", ECCRole.REVIEWER, "sha-1", scope="execution"))


def test_missing_provenance_is_denied():
    with pytest.raises(ECCDenied):
        ECCPolicy().admit(ECCRequest("task-1", ECCRole.REVIEWER, ""))


def test_malformed_request_is_denied():
    with pytest.raises(ECCDenied):
        ECCPolicy().admit(object())
