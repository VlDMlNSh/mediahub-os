"""Fail-closed Cloud API egress over an externally managed VPN tunnel.

The adapter never establishes or bypasses a VPN. A platform-specific tunnel
provider (such as VPN Proxy Master on a supported host) must expose a healthy
interface before cloud traffic is admitted. All other traffic remains direct.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from urllib.error import URLError
from urllib.request import Request, urlopen

from ops.mediahub_egress_controller import EgressController


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
        if not isinstance(url, str) or not url:
            raise CloudAPIUnavailable("malformed hybrid egress request")
        if not isinstance(method, str) or not method:
            raise CloudAPIUnavailable("malformed hybrid egress request")
        if headers is not None and (not isinstance(headers, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in headers.items())):
            raise CloudAPIUnavailable("malformed hybrid egress request")
        if not isinstance(self.timeout_seconds, (int, float)) or isinstance(self.timeout_seconds, bool) or self.timeout_seconds <= 0:
            raise CloudAPIUnavailable("malformed hybrid egress request")
        self.egress.admit(url)
        status = self.check_tunnel()
        if self.require_vpn and not status.healthy:
            raise CloudAPIUnavailable("required VPN tunnel is unavailable")
        request = Request(url, data=data, headers=headers or {}, method=method)
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                return CloudAPIResponse(response.status, response.read())
        except (TimeoutError, OSError, URLError) as exc:
            raise CloudAPIUnavailable("cloud API transport failed") from exc
