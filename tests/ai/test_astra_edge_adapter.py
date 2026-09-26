import pytest

from ops.ai.astra_edge_adapter import AstraEdgeAdapter, AstraEdgeDenied, EdgeStatus, EdgeTask
from ops.ai.ai_routing import ProviderState, Route
from runtime.mediahub_runtime.consumer_boundary import ConsumerBoundary
from runtime.mediahub_runtime.composition_root import build_runtime
from runtime.mediahub_runtime.state_authority import AuthorizationContext


def test_local_execution_and_reconciliation():
    graph = build_runtime()
    authority = graph["state_authority"]
    boundary = graph["consumer_boundary"]
    authorization = AuthorizationContext("astra", True, frozenset({"state.write"}))
    request = boundary.request("astra-edge", "corr-1", authorization)
    task = EdgeTask("req-e2e", "sess-1", "Return only READY", "approved")
    result = AstraEdgeAdapter().execute_and_reconcile(task, boundary, request)
    assert result.status is EdgeStatus.SUCCEEDED
    assert result.route is Route.LOCAL
    stored = authority.read()["astra"]["tasks"]["req-e2e"]
    assert stored["status"] == "succeeded"
    assert stored["output"].strip() == "READY"


def test_pending_task_is_rejected():
    with pytest.raises(AstraEdgeDenied):
        AstraEdgeAdapter().execute(EdgeTask("req", "sess", "x", "pending"))


def test_cloud_failure_does_not_execute_local_when_local_unavailable():
    result = AstraEdgeAdapter().execute(
        EdgeTask("req", "sess", "x", "approved"),
        provider_state=ProviderState.POLICY_BLOCKED,
        local_available=False,
    )
    assert result.route is Route.SAFE_STOP
    assert result.status is EdgeStatus.BLOCKED
