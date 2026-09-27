import pytest

from ops.ai.astra_host_gateway import AstraHostGateway, HostGatewayDenied, HostTrust


def kwargs(**overrides):
    values = dict(
        request_id="req-1", host_id="mh-dev-01", workload_id="work-1",
        source_sha="sha-1", expected_source_sha="sha-1", command="pytest -q",
        timeout_seconds=60, output_limit_bytes=65536,
        trust=HostTrust.ACTIVE, authorization_id="auth-1",
        capabilities=frozenset({"host.execute"}),
    )
    values.update(overrides)
    return values


def test_active_authorized_host_produces_bounded_proposal():
    proposal = AstraHostGateway.propose(**kwargs())
    assert proposal.host_id == "mh-dev-01"
    assert proposal.trust is HostTrust.ACTIVE
    assert proposal.capabilities == frozenset({"host.execute"})


@pytest.mark.parametrize("trust", [
    HostTrust.UNKNOWN, HostTrust.VERIFIED, HostTrust.ENROLLED,
    HostTrust.AUTHORIZED, HostTrust.SUSPENDED, HostTrust.QUARANTINED, HostTrust.REVOKED,
])
def test_reachability_or_enrollment_never_implies_active_authorization(trust):
    with pytest.raises(HostGatewayDenied):
        AstraHostGateway.propose(**kwargs(trust=trust))


def test_capability_does_not_create_authorization():
    with pytest.raises(HostGatewayDenied):
        AstraHostGateway.propose(**kwargs(capabilities=frozenset()))


def test_provenance_mismatch_is_denied():
    with pytest.raises(HostGatewayDenied):
        AstraHostGateway.propose(**kwargs(expected_source_sha="sha-other"))


def test_bounds_are_fail_closed():
    with pytest.raises(HostGatewayDenied):
        AstraHostGateway.propose(**kwargs(timeout_seconds=901))
    with pytest.raises(HostGatewayDenied):
        AstraHostGateway.propose(**kwargs(output_limit_bytes=1_048_577))
    with pytest.raises(HostGatewayDenied):
        AstraHostGateway.propose(**kwargs(command="x" * (64 * 1024 + 1)))


def test_identity_and_authorization_id_are_required():
    with pytest.raises(HostGatewayDenied):
        AstraHostGateway.propose(**kwargs(host_id=""))
    with pytest.raises(HostGatewayDenied):
        AstraHostGateway.propose(**kwargs(authorization_id=""))
