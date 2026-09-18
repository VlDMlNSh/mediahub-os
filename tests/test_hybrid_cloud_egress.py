from unittest.mock import patch

import pytest

from ops.hybrid_cloud_api_egress_adapter import CloudAPIUnavailable
from ops.hybrid_cloud_egress import HybridCloudEgressAdapter, TransportCandidate


def candidates():
    return (
        TransportCandidate("vpn-proxy-master", "vpnproxymaster0", "external-vpn", 10),
        TransportCandidate("wireguard", "wg0", "wireguard", 20),
        TransportCandidate("openvpn", "tun0", "openvpn", 30),
    )


def probe(candidate, healthy, ip=""):
    return type("P", (), {"candidate": candidate, "healthy": healthy,
                           "public_ip": ip, "detail": "test"})()


def test_fail_closed_when_all_candidates_fail():
    adapter = HybridCloudEgressAdapter(candidates())
    with patch.object(adapter, "_probe", side_effect=lambda c, u: probe(c, False)), pytest.raises(CloudAPIUnavailable):
            adapter.select("https://health.example.test")


def test_prefers_vpm_and_sticks_to_it():
    adapter = HybridCloudEgressAdapter(candidates())
    with patch.object(adapter, "_probe", side_effect=lambda c, u: probe(c, True, "203.0.113.10")):
        first = adapter.select("https://health.example.test")
        second = adapter.select("https://health.example.test")
    assert first.candidate.name == "vpn-proxy-master"
    assert second.candidate.name == "vpn-proxy-master"
    assert adapter.active_ip == "203.0.113.10"


def test_falls_back_only_after_primary_failure():
    adapter = HybridCloudEgressAdapter(candidates())
    def fake(c, _):
        return probe(c, c.name != "vpn-proxy-master", "203.0.113.20")
    with patch.object(adapter, "_probe", side_effect=fake):
        result = adapter.select("https://health.example.test")
    assert result.candidate.name == "wireguard"
    assert adapter.active_ip == "203.0.113.20"


def test_request_uses_selected_interface_and_returns_status():
    adapter = HybridCloudEgressAdapter(candidates())
    adapter._active = candidates()[0]
    fake = type("R", (), {"returncode": 0, "stdout": b"ok\n__MH_HTTP_STATUS__200", "stderr": b""})()
    with patch("ops.hybrid_cloud_egress.run", return_value=fake) as run_call:
        status, body = adapter.request("https://api.example.test", method="POST", data=b"{}", headers={"Content-Type": "application/json"})
    assert status == 200
    assert body == b"ok"
    args = run_call.call_args.args[0]
    assert "--interface" in args and "vpnproxymaster0" in args
    assert "--data-binary" in args


def test_request_requires_selected_transport():
    adapter = HybridCloudEgressAdapter(candidates())
    with pytest.raises(CloudAPIUnavailable):
        adapter.request("https://api.example.test")
