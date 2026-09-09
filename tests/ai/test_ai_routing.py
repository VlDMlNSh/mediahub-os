import pytest

from ops.ai.ai_routing import (
    ProviderState,
    Route,
    classify_provider_failure,
    decide_cloud_failure,
)


@pytest.mark.parametrize(
    "message",
    [
        "403 Forbidden: Access denied by security policy",
        "Country, region, or territory not supported",
        "provider says not authorized",
    ],
)
def test_policy_failures_are_not_retryable(message):
    assert classify_provider_failure(message) is ProviderState.POLICY_BLOCKED
    decision = decide_cloud_failure(
        ProviderState.POLICY_BLOCKED,
        local_cluster_available=True,
        local_available=True,
    )
    assert decision.route is Route.LOCAL_CLUSTER
    assert decision.retry_allowed is False


def test_transient_failure_does_not_retry_cloud_implicitly():
    decision = decide_cloud_failure(
        ProviderState.TRANSIENT_FAILURE,
        local_cluster_available=True,
        local_available=True,
    )
    assert decision.route is Route.LOCAL_CLUSTER
    assert decision.retry_allowed is False


def test_fallback_downgrades_to_local():
    decision = decide_cloud_failure(
        ProviderState.POLICY_BLOCKED,
        local_cluster_available=False,
        local_available=True,
    )
    assert decision.route is Route.LOCAL


def test_no_local_capacity_is_safe_stop():
    decision = decide_cloud_failure(
        ProviderState.QUARANTINED,
        local_cluster_available=False,
        local_available=False,
    )
    assert decision.route is Route.SAFE_STOP
    assert decision.retry_allowed is False


def test_available_cloud_is_selected_without_fallback():
    decision = decide_cloud_failure(
        ProviderState.AVAILABLE,
        local_cluster_available=True,
        local_available=True,
    )
    assert decision.route is Route.CLOUD
