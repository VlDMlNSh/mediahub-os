"""Local provider adapters for Astra multi-agent routing.

Secrets stay outside the repository. Adapters are bounded and fail closed.
"""
from __future__ import annotations

import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path


class LocalProviderError(RuntimeError):
    pass


def _read_secret(path: str) -> str:
    try:
        value = Path(path).read_text(encoding="utf-8").strip()
    except OSError as exc:
        raise LocalProviderError("credential_unavailable") from exc
    if not value:
        raise LocalProviderError("credential_empty")
    return value


class FreeLLMAPIExecutor:
    provider_id = "freellmapi"
    tier = "local_gateway"

    def __init__(self, base_url: str | None = None, key_file: str | None = None, model: str | None = None, timeout: int = 120):
        self.base_url = (base_url or os.environ.get("MEDIAHUB_FREELLMAPI_URL", "http://127.0.0.1:3001/v1")).rstrip("/")
        self.key_file = key_file or os.environ.get("MEDIAHUB_FREELLMAPI_KEY_FILE", str(Path.home()/".config/mediahub/freellmapi.key"))
        self.model = model or os.environ.get("MEDIAHUB_FREELLMAPI_MODEL", "qwen2.5-coder:3b")
        self.timeout = max(5, min(int(timeout), 300))

    def available(self) -> bool:
        try:
            key = _read_secret(self.key_file)
            req = urllib.request.Request(self.base_url + "/models", headers={"Authorization": "Bearer " + key})
            with urllib.request.urlopen(req, timeout=5) as response:
                return 200 <= response.status < 300
        except (LocalProviderError, urllib.error.URLError, TimeoutError, OSError):
            return False

    def __call__(self, prompt: str) -> str:
        key = _read_secret(self.key_file)
        body = json.dumps({"model": self.model, "messages": [{"role": "user", "content": prompt}], "temperature": 0, "max_tokens": 1200}).encode("utf-8")
        req = urllib.request.Request(self.base_url + "/chat/completions", data=body, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as response:
                data = json.loads(response.read(2_097_152).decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LocalProviderError("freellmapi_unavailable") from exc
        try:
            output = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LocalProviderError("freellmapi_invalid_response") from exc
        if not isinstance(output, str) or not output.strip():
            raise LocalProviderError("freellmapi_empty_response")
        return output
