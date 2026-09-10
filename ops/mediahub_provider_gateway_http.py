"""MediaHub-native localhost HTTP provider gateway.

Canonical client protocols are translated to provider-specific paths only by
qualified adapters. Third-party gateways are references, not product runtime
requirements. The gateway is intentionally fail-closed and localhost-only.
"""
from __future__ import annotations

import http.client
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import requests

from ops.mediahub_provider_gateway import FailureClass, Provider, ProviderGateway

LISTEN = ("127.0.0.1", int(os.environ.get("MEDIAHUB_GATEWAY_PORT", "18080")))
MAX_BODY = 8 * 1024 * 1024
TIMEOUT = 120
PROVIDERS = (
    Provider("opper", "api.opper.ai", 20),
    Provider("continuum", "continuumcode.ai", 30),
)
# Only capabilities explicitly qualified by MediaHub are routable.
CAPABILITIES: dict[str, frozenset[str]] = {
    "opper": frozenset({"chat_completions"}),
    "continuum": frozenset({"responses", "messages"}),
}
PATH_PROTOCOL = {
    "/v1/responses": "responses",
    "/v1/chat/completions": "chat_completions",
    "/v1/messages": "messages",
    "/api/v1/messages": "messages",
}
GATEWAY = ProviderGateway(PROVIDERS)


def credential(name: str) -> str:
    directory = os.environ.get("CREDENTIALS_DIRECTORY", "")
    if not directory:
        raise RuntimeError("CREDENTIALS_DIRECTORY is required")
    with open(os.path.join(directory, name), encoding="utf-8") as fh:
        value = fh.read().strip()
    if not value:
        raise RuntimeError("empty provider credential")
    return value


def protocol_for(path: str) -> str:
    try:
        return PATH_PROTOCOL[path]
    except KeyError as exc:
        raise ValueError("unsupported canonical path") from exc


def compatible(provider: str, protocol: str) -> bool:
    return protocol in CAPABILITIES.get(provider, frozenset())


def provider_target(provider: str, path: str) -> str:
    suffix = path.removeprefix("/api").removeprefix("/v1")
    if provider == "opper":
        if path != "/v1/chat/completions":
            raise http.client.HTTPException("Opper adapter only supports Chat Completions")
        return "/v3/compat/chat/completions"
    if provider == "continuum":
        return "/v1" + suffix
    raise RuntimeError("unknown provider")


def upstream(provider: str, path: str) -> tuple[str, str, str]:
    if provider == "opper":
        return "api.opper.ai", provider_target(provider, path), credential("mediahub-opper")
    if provider == "continuum":
        return "continuumcode.ai", provider_target(provider, path), credential("mediahub-continuum")
    raise RuntimeError("unknown provider")


def json_error(message: str) -> bytes:
    return json.dumps({"error": message}, separators=(",", ":")).encode()


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def reply(self, status: int, body: bytes, headers: dict[str, str] | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Connection", "close")
        for name, value in (headers or {}).items():
            self.send_header(name, value)
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self) -> None:
        if self.path in ("/v1/models", "/api/v1/models"):
            self.reply(200, b'{"object":"list","data":[]}')
            return
        self.reply(403, json_error("MEDIAHUB_GATEWAY_DENIED_PATH"))

    def do_POST(self) -> None:
        if self.path not in PATH_PROTOCOL:
            self.reply(403, json_error("MEDIAHUB_GATEWAY_DENIED_PATH"))
            return
        protocol = protocol_for(self.path)
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 0 or length > MAX_BODY:
                self.reply(413, json_error("MEDIAHUB_GATEWAY_BODY_LIMIT"))
                return
            body = self.rfile.read(length)
            if len(body) != length:
                self.reply(400, json_error("MEDIAHUB_GATEWAY_SHORT_BODY"))
                return
            excluded: set[str] = set()
            last_error = ""
            last_status: int | None = None
            last_retry_after: str | None = None
            for _ in range(len(PROVIDERS)):
                decision = self._choose(protocol, excluded)
                if not decision.provider:
                    break
                try:
                    status, payload, retry_after = self.forward(decision.provider, self.path, body)
                except (OSError, TimeoutError, http.client.HTTPException) as exc:
                    status, payload, retry_after = None, str(exc).encode(), None
                if status is not None and 200 <= status < 300:
                    GATEWAY.record(decision.provider, FailureClass.SUCCESS)
                    return self.reply(status, payload)
                error_text = payload.decode("utf-8", "replace")[:4096]
                failure = GATEWAY.classify(status, error_text)
                GATEWAY.record(decision.provider, failure)
                excluded.add(decision.provider)
                last_error, last_status, last_retry_after = error_text, status, retry_after
                if failure is FailureClass.PERMANENT:
                    break
            if last_status is None and not last_error:
                return self.reply(503, json_error("MEDIAHUB_GATEWAY_NO_COMPATIBLE_PROVIDER"))
            status = last_status if last_status is not None else 502
            response_headers = {"Retry-After": last_retry_after} if last_retry_after else None
            self.reply(status if status >= 400 else 502, last_error.encode(), response_headers)
        except Exception:  # noqa: BLE001 - fail closed at the HTTP boundary
            self.reply(502, json_error("MEDIAHUB_GATEWAY_INTERNAL_FAILURE"))

    def _choose(self, protocol: str, excluded: set[str]):
        ineligible = frozenset(
            p.name for p in PROVIDERS if not compatible(p.name, protocol)
        )
        return GATEWAY.choose(excluded=frozenset(excluded) | ineligible)

    def forward(self, provider: str, path: str, body: bytes) -> tuple[int, bytes, str | None]:
        protocol = protocol_for(path)
        if not compatible(provider, protocol):
            raise http.client.HTTPException("provider protocol capability not qualified")
        host, target, key = upstream(provider, path)
        url = f"https://{host}{target}"
        headers = {
            "Authorization": "Bearer " + key,
            "Content-Type": self.headers.get("Content-Type", "application/json"),
            "Accept": self.headers.get("Accept", "application/json"),
            "User-Agent": "MediaHub-Provider-Gateway/1.1",
        }
        response = requests.post(
            url, data=body, headers=headers, timeout=TIMEOUT, allow_redirects=False, verify=True
        )
        return response.status_code, response.content[: MAX_BODY + 1], response.headers.get("Retry-After")

    def log_message(self, fmt: str, *args: object) -> None:
        # Never log request headers/body: prompts and credentials are sensitive.
        print("provider-gateway", self.address_string(), fmt % args, flush=True)


if __name__ == "__main__":
    ThreadingHTTPServer(LISTEN, Handler).serve_forever()
