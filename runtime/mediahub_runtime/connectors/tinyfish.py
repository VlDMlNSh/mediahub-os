"""Optional TinyFish web-agent connector for Astra.

The connector is deliberately provider-boundary only: Astra owns policy and
routing, while TinyFish performs web interaction. Production API keys are
held by GitHub Actions and never stored on the MediaHub host.
"""
from __future__ import annotations

import json
import ipaddress
import socket
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any


class TinyFishConnectorError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class TinyFishRun:
    run_id: str


def _validate_public_url(value: str) -> bool:
    try:
        from urllib.parse import urlsplit
        parsed = urlsplit(value)
        if parsed.scheme not in {"https", "http"} or not parsed.hostname or parsed.username or parsed.password:
            return False
        host = parsed.hostname.rstrip(".").lower()
        if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
            return False
        addresses = {ipaddress.ip_address(info[4][0]) for info in socket.getaddrinfo(host, None)}
        return bool(addresses) and all(not (addr.is_private or addr.is_loopback or addr.is_link_local or addr.is_multicast or addr.is_reserved or addr.is_unspecified) for addr in addresses)
    except (OSError, ValueError):
        return False


class TinyFishConnector:
    endpoint = "https://agent.tinyfish.ai/v1/automation/run-async"
    provider_id = "tinyfish"
    capability = "web"

    def __init__(self, api_key: str | None = None, timeout: int = 30):
        # Direct credentials are accepted only by explicit caller injection.
        # Production Astra uses the GitHub credential boundary instead.
        self._api_key = api_key
        self._timeout = timeout

    @property
    def configured(self) -> bool:
        return bool(self._api_key and self._api_key.strip())

    def start(self, *, url: str, goal: str, webhook_url: str | None = None) -> TinyFishRun:
        if not self.configured:
            raise TinyFishConnectorError("tinyfish_not_configured")
        if not isinstance(url, str) or not _validate_public_url(url):
            raise TinyFishConnectorError("invalid_target_url")
        if not isinstance(goal, str) or not goal.strip():
            raise TinyFishConnectorError("invalid_goal")
        payload: dict[str, Any] = {
            "url": url,
            "goal": goal,
            "browser_profile": "lite",
            "agent_config": {"mode": "strict", "max_steps": 50, "max_duration_seconds": 300},
        }
        if webhook_url:
            if not _validate_public_url(webhook_url) or not webhook_url.lower().startswith("https://"):
                raise TinyFishConnectorError("invalid_webhook_url")
            payload["webhook_url"] = webhook_url
        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
            headers={"Content-Type": "application/json", "X-API-Key": self._api_key or ""},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                raw = response.read(64 * 1024)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise TinyFishConnectorError("tinyfish_unavailable") from exc
        try:
            data = json.loads(raw.decode("utf-8"))
            run_id = data["run_id"]
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise TinyFishConnectorError("tinyfish_invalid_response") from exc
        if not isinstance(run_id, str) or not run_id.strip():
            raise TinyFishConnectorError("tinyfish_invalid_response")
        return TinyFishRun(run_id=run_id)
