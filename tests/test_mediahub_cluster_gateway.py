import ast

import pytest

from ops.ai.ai_routing import ProviderState, Route, RoutingDecision
from ops.mediahub_cluster_gateway import ClusterGatewayDenied, LocalClusterGateway
from ops.mediahub_local_cluster import (
    ClusterNode,
    ClusterWorkload,
    LocalClusterScheduler,
    NodeState,
    WorkloadClass,
)


def gateway() -> LocalClusterGateway:
    return LocalClusterGateway(
        LocalClusterScheduler((ClusterNode("node-a", NodeState.READY, 8, 16384, 1),))
    )


def decision(route: Route) -> RoutingDecision:
    return RoutingDecision(route, ProviderState.AVAILABLE, False, "test")


def workload(source_sha="sha") -> ClusterWorkload:
    return ClusterWorkload("w1", WorkloadClass.INFERENCE, 1, 1, 0, source_sha)


def test_approved_local_cluster_route_creates_proposal():
    proposal = gateway().propose("req-1", workload(), decision(Route.LOCAL_CLUSTER))
    assert proposal.route is Route.LOCAL_CLUSTER
    assert proposal.assignment.node_id == "node-a"
    assert proposal.source_sha == "sha"


def test_other_routes_are_denied():
    with pytest.raises(ClusterGatewayDenied):
        gateway().propose("req-1", workload(), decision(Route.LOCAL))
    with pytest.raises(ClusterGatewayDenied):
        gateway().propose("req-1", workload(), decision(Route.CLOUD))
    with pytest.raises(ClusterGatewayDenied):
        gateway().propose("req-1", workload(), decision(Route.SAFE_STOP))


def test_missing_request_identity_is_denied():
    with pytest.raises(ClusterGatewayDenied):
        gateway().propose("", workload(), decision(Route.LOCAL_CLUSTER))


def test_missing_provenance_is_denied():
    with pytest.raises(ClusterGatewayDenied):
        gateway().propose("req-1", workload(""), decision(Route.LOCAL_CLUSTER))


def test_cluster_admission_fail_closed_is_preserved():
    denied = LocalClusterGateway(
        LocalClusterScheduler((ClusterNode("q", NodeState.QUARANTINED, 8, 16384, 1),))
    )
    with pytest.raises(ClusterGatewayDenied):
        denied.propose("req-1", workload(), decision(Route.LOCAL_CLUSTER))


def test_policy_blocked_cloud_can_fallback_to_local_cluster():
    routed = RoutingDecision(Route.LOCAL_CLUSTER, ProviderState.POLICY_BLOCKED, False, "403")
    proposal = gateway().propose("req-1", workload(), routed)
    assert proposal.route is Route.LOCAL_CLUSTER


def test_proposal_contains_no_state_authority_object():
    proposal = gateway().propose("req-1", workload(), decision(Route.LOCAL_CLUSTER))
    assert not hasattr(proposal, "state")
    assert not hasattr(proposal, "authority")


def test_gateway_has_no_network_or_state_authority_imports():
    gateway_path = __file__.replace("tests/test_mediahub_cluster_gateway.py", "ops/mediahub_cluster_gateway.py")
    with open(gateway_path, encoding="utf-8") as handle:
        tree = ast.parse(handle.read())
    imports = [node.names[0].name for node in tree.body if isinstance(node, ast.Import)]
    imports += [node.module for node in tree.body if isinstance(node, ast.ImportFrom) and node.module]
    assert all(not name.startswith(("http", "urllib", "requests")) for name in imports)
    assert all("state_authority" not in name for name in imports)
