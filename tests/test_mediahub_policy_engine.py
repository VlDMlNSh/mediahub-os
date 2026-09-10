import pytest

from ops.mediahub_policy_engine import (
    DevelopmentPolicy,
    PolicyDenied,
    PolicyEngine,
    PolicyRequest,
)


@pytest.fixture
def engine():
    return PolicyEngine(DevelopmentPolicy(
        providers=frozenset({"openai", "anthropic"}),
        protocols=frozenset({"openai.responses", "anthropic.messages"}),
        data_classes=frozenset({"non-sensitive"}),
    ))


def request(**overrides):
    values = dict(provider="openai", protocol="openai.responses",
                  data_class="non-sensitive", timeout_seconds=60, prompt_bytes=10)
    values.update(overrides)
    return PolicyRequest(**values)


def test_valid_request_is_allowed(engine):
    assert engine.evaluate(request()).allowed is True
    engine.require(request())


def test_provider_protocol_and_data_class_are_allowlists(engine):
    for field, value in (("provider", "other"), ("protocol", "other"),
                         ("data_class", "credential")):
        with pytest.raises(PolicyDenied):
            engine.require(request(**{field: value}))


def test_forbidden_capabilities_are_denied(engine):
    for capability in ("production", "secrets", "state-authority", "host-filesystem"):
        with pytest.raises(PolicyDenied):
            engine.require(request(capabilities=frozenset({capability})))


def test_bounds_are_enforced(engine):
    for timeout in (0, 901):
        with pytest.raises(PolicyDenied):
            engine.require(request(timeout_seconds=timeout))
    for size in (0, 65 * 1024):
        with pytest.raises(PolicyDenied):
            engine.require(request(prompt_bytes=size))


def test_revocation_is_fail_closed(engine):
    engine.revoke()
    assert engine.evaluate(request()).allowed is False
    with pytest.raises(PolicyDenied):
        engine.require(request())
