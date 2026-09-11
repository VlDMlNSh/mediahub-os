from ops.cloud_api_egress_adapter import CloudAPIUnavailable, TunnelStatus
from ops.cloud_api_egress_chain import CloudAPIEgressChain, EgressPath
import pytest


def test_chain_uses_first_healthy_and_stays_sticky():
    state = {"tun-vpm": True, "wg0": True}
    chain = CloudAPIEgressChain(
        (EgressPath("vpm", "tun-vpm", "vpnproxymaster"), EgressPath("wg", "wg0", "wireguard")),
        lambda i: TunnelStatus(i, state[i], "test"),
    )
    assert chain.select().interface == "tun-vpm"
    assert chain.select().interface == "tun-vpm"


def test_chain_fails_over_only_after_active_path_is_unhealthy():
    state = {"tun-vpm": True, "wg0": True}
    chain = CloudAPIEgressChain(
        (EgressPath("vpm", "tun-vpm", "vpnproxymaster"), EgressPath("wg", "wg0", "wireguard")),
        lambda i: TunnelStatus(i, state[i], "test"),
    )
    chain.select()
    state["tun-vpm"] = False
    assert chain.select().interface == "wg0"


def test_chain_fails_closed_when_all_paths_are_unhealthy():
    chain = CloudAPIEgressChain(
        (EgressPath("vpm", "tun-vpm", "vpnproxymaster"), EgressPath("wg", "wg0", "wireguard")),
        lambda i: TunnelStatus(i, False, "test"),
    )
    with pytest.raises(CloudAPIUnavailable):
        chain.select()
