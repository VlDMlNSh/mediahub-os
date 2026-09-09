from ops.mediahub_provider_gateway import FailureClass, Provider, ProviderGateway


def gateway():
    return ProviderGateway((
        Provider("openrouter", "https://openrouter.ai/api/v1", 1),
        Provider("opper", "https://api.opper.ai/v3/compat", 2),
        Provider("continuum", "https://continuumcode.ai/v1", 3),
    ), threshold=2, cooldown_seconds=60)


def test_403_is_policy_blocked_and_skips_retry():
    g = gateway()
    d = g.failover("openrouter", 403, "Access denied by security policy")
    assert d.failure is FailureClass.POLICY_BLOCKED
    assert d.provider == "opper"
    assert d.retry is False


def test_transient_failure_allows_bounded_failover():
    g = gateway()
    d = g.failover("openrouter", 503, "upstream unavailable")
    assert d.failure is FailureClass.TRANSIENT
    assert d.provider == "opper"
    assert d.retry is True


def test_permanent_4xx_does_not_fallback():
    g = gateway()
    d = g.failover("openrouter", 400, "bad request")
    assert d.failure is FailureClass.PERMANENT
    assert d.provider is None
    assert d.retry is False


def test_second_transient_failure_opens_circuit():
    g = gateway()
    g.failover("openrouter", 503)
    g.failover("openrouter", 504)
    assert not g.available("openrouter", now=0)
    d = g.choose(now=0)
    assert d.provider == "opper"


def test_policy_blocked_provider_reopens_only_after_cooldown():
    g = gateway()
    g.record("openrouter", FailureClass.POLICY_BLOCKED, now=10)
    assert not g.available("openrouter", now=69)
    assert g.available("openrouter", now=70)
