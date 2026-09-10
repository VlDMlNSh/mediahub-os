import pytest

from ops.mediahub_provider_gateway import FailureClass, Provider, ProviderGateway
from ops.mediahub_resilience import RetryPolicy, ResilienceEngine


def gateway():
    return ProviderGateway(
        (Provider("a", "https://a.example", 10), Provider("b", "https://b.example", 20)),
        threshold=2,
        cooldown_seconds=10,
    )


def test_retry_after_is_bounded():
    policy = RetryPolicy(max_attempts=3, max_delay_seconds=2.0)
    assert policy.delay(1, retry_after=10.0) == 2.0
    assert policy.delay(1, retry_after=-1.0) == 0.0


def test_permanent_failure_never_fails_over():
    engine = ResilienceEngine(gateway(), RetryPolicy(max_attempts=3))
    result = engine.after_failure("a", 400, "bad request", attempt=1)
    assert result.provider is None
    assert result.failure is FailureClass.PERMANENT
    assert result.retry is False


def test_policy_blocked_fails_over_without_retry_delay_semantics():
    engine = ResilienceEngine(gateway(), RetryPolicy(max_attempts=3))
    result = engine.after_failure("a", 403, "access denied by security policy", attempt=1)
    assert result.provider == "b"
    assert result.failure is FailureClass.POLICY_BLOCKED
    assert result.retry is False


def test_transient_failure_uses_next_provider_and_budget():
    engine = ResilienceEngine(gateway(), RetryPolicy(max_attempts=2, base_delay_seconds=0.5))
    result = engine.after_failure("a", 503, "upstream unavailable", attempt=1)
    assert result.provider == "b"
    assert result.retry is True
    assert result.attempt == 2
    assert result.delay_seconds == 0.5


def test_retry_budget_is_fail_closed():
    engine = ResilienceEngine(gateway(), RetryPolicy(max_attempts=1))
    result = engine.after_failure("a", 503, "upstream unavailable", attempt=1)
    assert result.provider is None
    assert result.retry is False
    assert result.reason == "retry budget exhausted"


def test_invalid_retry_policy_rejected():
    with pytest.raises(ValueError):
        RetryPolicy(max_attempts=0)
    with pytest.raises(ValueError):
        RetryPolicy(base_delay_seconds=3, max_delay_seconds=2)
