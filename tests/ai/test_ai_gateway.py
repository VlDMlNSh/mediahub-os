import pytest

from ops.ai.ai_gateway import AIGateway, AIGatewayDenied, AIRoutingRequest
from ops.ai.ai_routing import ProviderState, Route


def request(**overrides):
    values = {
        "request_id": "r1",
        "source_sha": "sha",
        "user_authorized": True,
        "cloud_authorized": False,
        "local_available": True,
        "local_cluster_available": True,
        "cloud_available": True,
    }
    values.update(overrides)
    return AIRoutingRequest(**values)


def test_local_first_is_deterministic():
    decision = AIGateway().route(request())
    assert decision.route is Route.LOCAL
    assert decision.provider_state is ProviderState.AVAILABLE


def test_privacy_local_only_never_escalates():
    decision = AIGateway().route(request(privacy_local_only=True, local_available=True))
    assert decision.route is Route.LOCAL


def test_privacy_local_only_without_local_stops():
    decision = AIGateway().route(request(privacy_local_only=True, local_available=False))
    assert decision.route is Route.SAFE_STOP


def test_distributed_requirement_selects_local_cluster():
    decision = AIGateway().route(request(requires_distributed_compute=True))
    assert decision.route is Route.LOCAL_CLUSTER


def test_cloud_requires_explicit_authorization():
    decision = AIGateway().route(request(
        local_available=False,
        local_cluster_available=False,
        requires_cloud_compute=True,
        cloud_authorized=False,
    ))
    assert decision.route is Route.SAFE_STOP


def test_cloud_requires_exportable_data():
    decision = AIGateway().route(request(
        local_available=False,
        local_cluster_available=False,
        requires_cloud_compute=True,
        cloud_authorized=True,
        data_class="secret",
    ))
    assert decision.route is Route.SAFE_STOP


def test_cloud_is_selected_only_when_authorized_and_available():
    decision = AIGateway().route(request(
        local_available=False,
        local_cluster_available=False,
        requires_cloud_compute=True,
        cloud_authorized=True,
    ))
    assert decision.route is Route.CLOUD


def test_cloud_outage_falls_back_to_cluster_without_retrying_cloud():
    decision = AIGateway().route(request(
        local_available=False,
        local_cluster_available=True,
        requires_cloud_compute=True,
        cloud_authorized=True,
        cloud_available=False,
    ))
    assert decision.route is Route.LOCAL_CLUSTER
    assert decision.provider_state is ProviderState.TRANSIENT_FAILURE
    assert decision.retry_allowed is False


def test_missing_identity_or_provenance_is_denied():
    with pytest.raises(AIGatewayDenied):
        AIGateway().route(request(request_id=""))
    with pytest.raises(AIGatewayDenied):
        AIGateway().route(request(source_sha=""))


def test_unauthorized_user_is_denied():
    with pytest.raises(AIGatewayDenied):
        AIGateway().route(request(user_authorized=False))


def test_cloud_failure_falls_back_to_local_when_cluster_unavailable():
    decision = AIGateway().route(request(
        local_available=True,
        local_cluster_available=False,
        requires_cloud_compute=True,
        cloud_authorized=True,
        cloud_available=False,
    ))
    assert decision.route is Route.LOCAL


def test_free_hybrid_mode_is_text_only():
    with pytest.raises(AIGatewayDenied):
        AIGateway().route(request(text_only=False))


def test_free_hybrid_mode_bounds_prompt_text():
    with pytest.raises(AIGatewayDenied):
        AIGateway().route(request(prompt_chars=24001))


def test_free_hybrid_mode_allows_bounded_text():
    decision = AIGateway().route(request(prompt_chars=12000, text_only=True))
    assert decision.route is Route.LOCAL
