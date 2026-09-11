"""Fail-closed Cloud API egress over an externally managed VPN tunnel.

The adapter never establishes or bypasses a VPN. A platform-specific tunnel
provider (such as VPN Proxy Master on a supported host) must expose a healthy
interface before cloud traffic is admitted. All other traffic remains direct.
"""
from __future__ import annotations

from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import Request, urlopen
from urllib.parse import urlparse
import socket
import subprocess

from ops.mediahub_egress_controller import EgressController, EgressDenied


class CloudAPIUnavailable(ConnectionError):
    """Raised when the required VPN-backed egress is unavailable."""


@dataclass(frozen=True)
class TunnelStatus:
    interface: str
    healthy: bool
    source: str


@dataclass(frozen=True)
class CloudAPIResponse:
    status: int
    body: bytes


@dataclass
class HybridCloudAPIEgressAdapter:
    egress: EgressController
    tunnel_interface: str = ""
    require_vpn: bool = True
    timeout_seconds: float = 10.0

    def check_tunnel(self) -> TunnelStatus:
        if not self.tunnel_interface:
            return TunnelStatus("", False, "not-configured")
        try:
            result = subprocess.run(
                ["ip", "link", "show", "dev", self.tunnel_interface],
                check=False, capture_output=True, text=True, timeout=2,
            )
        except (OSError, subprocess.SubprocessError):
            return TunnelStatus(self.tunnel_interface, False, "probe-error")
        healthy = result.returncode == 0 and "UP" in result.stdout
        return TunnelStatus(self.tunnel_interface, healthy, "linux-link")

    def authorize(self) -> TunnelStatus:
        status = self.check_tunnel()
        if self.require_vpn and not status.healthy:
            raise CloudAPIUnavailable("required VPN tunnel is unavailable")
        self.egress.authorize()
        return status

    def request(self, url: str, *, method: str = "GET", data: bytes | None = None,
                headers: dict[str, str] | None = None) -> CloudAPIResponse:
        self.egress.admit(url)
        status = self.check_tunnel()
        if self.require_vpn and not status.healthy:
            raise CloudAPIUnavailable("required VPN tunnel is unavailable")
        request = Request(url, data=data, headers=headers or {}, method=method)
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return CloudAPIResponse(response.status, response.read())
        except (OSError, URLError, socket.timeout) as exc:
            raise CloudAPIUnavailable("cloud API transport failed") from exc
