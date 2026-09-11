"""Fail-closed egress selector for the hybrid development system."""
from __future__ import annotations

from dataclasses import dataclass
from subprocess import run, SubprocessError
from urllib.parse import urlparse
import re

from ops.hybrid_cloud_api_egress_adapter import CloudAPIUnavailable


@dataclass(frozen=True)
class TransportCandidate:
    name: str
    interface: str
    source: str
    priority: int


@dataclass(frozen=True)
class TransportProbe:
    candidate: TransportCandidate
    healthy: bool
    public_ip: str = ""
    detail: str = ""


class HybridCloudEgressAdapter:
    """Select and pin one verified transport; never deliberately rotate IPs."""

    def __init__(self, candidates: tuple[TransportCandidate, ...], timeout: float = 5.0):
        self._candidates = tuple(sorted(candidates, key=lambda item: item.priority))
        self._timeout = timeout
        self._active: TransportCandidate | None = None
        self._active_ip = ""

    @property
    def active(self) -> TransportCandidate | None:
        return self._active

    @property
    def active_ip(self) -> str:
        return self._active_ip

    @staticmethod
    def _validate_url(url: str) -> None:
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise CloudAPIUnavailable("health endpoint must be HTTPS")

    def _probe(self, candidate: TransportCandidate, health_url: str) -> TransportProbe:
        self._validate_url(health_url)
        try:
            link = run(["ip", "link", "show", "dev", candidate.interface],
                       capture_output=True, text=True, check=False, timeout=2)
            if link.returncode != 0 or "UP" not in link.stdout:
                return TransportProbe(candidate, False, detail="interface-unhealthy")
            result = run(["curl", "--fail", "--silent", "--show-error",
                          "--connect-timeout", "2", "--max-time", str(self._timeout),
                          "--interface", candidate.interface, health_url],
                         capture_output=True, text=True, check=False,
                         timeout=self._timeout + 2)
            if result.returncode != 0:
                return TransportProbe(candidate, False, detail="health-request-failed")
            ip = result.stdout.strip()
            if not re.fullmatch(r"[0-9a-fA-F:.]{3,64}", ip):
                return TransportProbe(candidate, True, detail="health-ok-ip-unavailable")
            return TransportProbe(candidate, True, public_ip=ip, detail="health-ok")
        except (OSError, SubprocessError):
            return TransportProbe(candidate, False, detail="probe-error")

    def select(self, health_url: str) -> TransportProbe:
        order = list(self._candidates)
        if self._active is not None:
            order = [self._active] + [item for item in order if item != self._active]
        for candidate in order:
            probe = self._probe(candidate, health_url)
            if probe.healthy:
                self._active = candidate
                if probe.public_ip:
                    self._active_ip = probe.public_ip
                return probe
        self._active = None
        self._active_ip = ""
        raise CloudAPIUnavailable("no verified hybrid cloud transport is available")

    def require_stable_transport(self, health_url: str) -> TransportProbe:
        return self.select(health_url)

    def request(self, url: str, *, method: str = "GET", data: bytes | None = None,
                headers: dict[str, str] | None = None) -> tuple[int, bytes]:
        """Call an HTTPS cloud API only through the currently verified path.

        Unknown/failed transport is never retried automatically because a
        non-idempotent cloud operation could otherwise be duplicated.
        """
        if self._active is None:
            raise CloudAPIUnavailable("no verified hybrid cloud transport is selected")
        self._validate_url(url)
        candidate = self._active
        args = ["curl", "--fail-with-body", "--silent", "--show-error",
                "--connect-timeout", "3", "--max-time", str(self._timeout),
                "--interface", candidate.interface, "--request", method]
        for key, value in (headers or {}).items():
            if "\n" in key or "\r" in key or "\n" in value or "\r" in value:
                raise CloudAPIUnavailable("invalid HTTP header")
            args += ["--header", f"{key}: {value}"]
        if data is not None:
            args += ["--data-binary", "@-"]
        args += [url, "--write-out", "\n__MH_HTTP_STATUS__%{http_code}"]
        try:
            result = run(args, input=data, capture_output=True, timeout=self._timeout + 3, check=False)
        except (OSError, SubprocessError) as exc:
            raise CloudAPIUnavailable("cloud API transport failed") from exc
        if result.returncode != 0:
            raise CloudAPIUnavailable("cloud API request failed")
        marker = b"\n__MH_HTTP_STATUS__"
        if marker not in result.stdout:
            raise CloudAPIUnavailable("cloud API response status is unverifiable")
        body, status = result.stdout.rsplit(marker, 1)
        try:
            return int(status.strip()), body
        except ValueError as exc:
            raise CloudAPIUnavailable("cloud API response status is invalid") from exc
