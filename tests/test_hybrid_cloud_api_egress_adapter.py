from __future__ import annotations

from unittest.mock import patch

import pytest

from ops.hybrid_cloud_api_egress_adapter import (
    CloudAPIUnavailable,
    HybridCloudAPIEgressAdapter,
)
from ops.mediahub_egress_controller import EgressController, EgressDenied, EgressPolicy

API = "https://api.example.test"


def adapter(*, interface: str = "tun-vpm") -> HybridCloudAPIEgressAdapter:
    controller = EgressController(EgressPolicy(frozenset({API})))
    return HybridCloudAPIEgressAdapter(controller, tunnel_interface=interface)


def test_fail_closed_without_vpn_interface() -> None:
    client = adapter(interface="missing-vpn0")
    with pytest.raises(CloudAPIUnavailable):
        client.authorize()


def test_destination_not_allowlisted_is_denied() -> None:
    client = adapter()
    with patch.object(client, "check_tunnel", return_value=client.check_tunnel()), pytest.raises(EgressDenied):
        client.request("https://not-allowed.example.test")


def test_request_requires_healthy_tunnel() -> None:
    client = adapter()
    healthy = type(client.check_tunnel())("tun-vpm", True, "test")
    with patch.object(client, "check_tunnel", return_value=healthy), patch("ops.hybrid_cloud_api_egress_adapter.urlopen") as open_url:
        open_url.return_value.__enter__.return_value.status = 200
        open_url.return_value.__enter__.return_value.read.return_value = b"ok"
        client.authorize()
        response = client.request(API)
    assert response.status == 200
    assert response.body == b"ok"


def test_transport_failure_is_fail_closed() -> None:
    client = adapter()
    healthy = type(client.check_tunnel())("tun-vpm", True, "test")
    with patch.object(client, "check_tunnel", return_value=healthy), patch("ops.hybrid_cloud_api_egress_adapter.urlopen", side_effect=OSError("down")):
        client.authorize()
        with pytest.raises(CloudAPIUnavailable):
            client.request(API)


def test_request_rejects_malformed_types() -> None:
    client = adapter()
    healthy = type(client.check_tunnel())("tun-vpm", True, "test")
    with patch.object(client, "check_tunnel", return_value=healthy), pytest.raises(CloudAPIUnavailable):
        client.request(123)
    with patch.object(client, "check_tunnel", return_value=healthy), pytest.raises(CloudAPIUnavailable):
        client.request(API, method=123)
    with patch.object(client, "check_tunnel", return_value=healthy), pytest.raises(CloudAPIUnavailable):
        client.request(API, headers={"X-Test": 1})


def test_request_rejects_invalid_timeout_type() -> None:
    client = adapter()
    healthy = type(client.check_tunnel())("tun-vpm", True, "test")
    client.timeout_seconds = True
    with patch.object(client, "check_tunnel", return_value=healthy), pytest.raises(CloudAPIUnavailable):
        client.request(API)
