import pytest

from ops.ai.astra_task_gateway import AstraTaskDenied, AstraTaskGateway, CanonicalAstraTask
from ops.ai.ai_routing import Route
from runtime.mediahub_runtime.composition_root import build_runtime
from runtime.mediahub_runtime.state_authority import AuthorizationContext


def make_task(**changes):
    values = {
        "request_id": "astra-1",
        "session_id": "session-1",
        "user_command": "Return only READY",
        "approval_state": "approved",
        "source_sha": "sha-1",
    }
    values.update(changes)
    return CanonicalAstraTask(**values)


def test_canonical_task_reaches_ollama_and_reconciles():
    graph = build_runtime()
    boundary = graph["consumer_boundary"]
    auth = AuthorizationContext("astra", True, frozenset({"state.write"}))
    request = boundary.request("astra", "corr-1", auth)
    result = AstraTaskGateway().dispatch(make_task(), boundary, request)
    assert result.route is Route.LOCAL
    assert result.output.strip() == "READY"
    assert graph["state_authority"].read()["astra"]["tasks"]["astra-1"]["status"] == "succeeded"


def test_cloud_escalation_without_authorization_stops():
    graph = build_runtime()
    boundary = graph["consumer_boundary"]
    auth = AuthorizationContext("astra", True, frozenset({"state.write"}))
    request = boundary.request("astra", "corr-2", auth)
    result = AstraTaskGateway().dispatch(
        make_task(requires_cloud_compute=True, cloud_authorized=False),
        boundary, request,
    )
    assert result.route is Route.SAFE_STOP
    assert result.status.value == "blocked"


def test_pending_task_never_reaches_router():
    with pytest.raises(AstraTaskDenied):
        AstraTaskGateway().validate(make_task(approval_state="pending"))
