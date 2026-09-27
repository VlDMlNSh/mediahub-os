import pytest

from ops.ai.astra_host_envelope import AstraHostEnvelope, HostEnvelopeDenied


def envelope(**overrides):
    values = dict(
        version=1, request_id="req-1", session_id="sess-1",
        conversation_id="conv-1", generation=1, host_id="mh-dev-01",
        workload_id="work-1", source_sha="sha-1", command="pytest -q",
        timeout_seconds=60, output_limit_bytes=65536,
        authorization_id="auth-1", capabilities=frozenset({"host.execute"}),
    )
    values.update(overrides)
    return AstraHostEnvelope(**values)


def test_envelope_is_canonical_and_credential_free():
    first = envelope()
    second = envelope(capabilities=frozenset({"host.execute"}))
    assert first.canonical_payload() == second.canonical_payload()
    assert first.fingerprint() == second.fingerprint()
    assert "credential" not in first.without_credentials()
    assert "api_key" not in first.without_credentials()


@pytest.mark.parametrize("field", ["request_id", "session_id", "conversation_id",
                                   "host_id", "workload_id", "source_sha", "authorization_id"])
def test_required_identity_fields_are_fail_closed(field):
    with pytest.raises(HostEnvelopeDenied):
        envelope(**{field: ""})


def test_generation_and_bounds_are_fail_closed():
    with pytest.raises(HostEnvelopeDenied):
        envelope(generation=True)
    with pytest.raises(HostEnvelopeDenied):
        envelope(generation=0)
    with pytest.raises(HostEnvelopeDenied):
        envelope(timeout_seconds=901)
    with pytest.raises(HostEnvelopeDenied):
        envelope(output_limit_bytes=1_048_577)
    with pytest.raises(HostEnvelopeDenied):
        envelope(command="x" * (64 * 1024 + 1))


def test_capability_is_required_but_is_not_authorization():
    with pytest.raises(HostEnvelopeDenied):
        envelope(capabilities=frozenset())


def test_no_secret_field_can_be_added_to_canonical_payload():
    payload = envelope().without_credentials()
    assert set(payload) == {
        "authorization_id", "capabilities", "command", "conversation_id",
        "generation", "host_id", "output_limit_bytes", "request_id",
        "session_id", "source_sha", "timeout_seconds", "version", "workload_id",
    }
