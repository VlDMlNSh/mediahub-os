"""OpenRouter HTTP adapter behind the MediaHub provider boundary.

The adapter accepts a credential only through explicit dependency injection.
Production MediaHub hosts must not persist provider credentials; GitHub Actions
is the approved credential boundary for cloud execution.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass


class OpenRouterConnectorError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class OpenRouterResult:
    output: str
    model: str
    generation_id: str | None


class OpenRouterConnector:
    provider_id = "openrouter"
    endpoint = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self, api_key: str | None, model: str, timeout: int = 60):
        self._api_key = api_key.strip() if isinstance(api_key, str) else None
        self._model = model.strip() if isinstance(model, str) else ""
        self._timeout = max(1, min(int(timeout), 300))

    @property
    def configured(self) -> bool:
        return bool(self._api_key and self._model)

    def infer(self, prompt: str) -> OpenRouterResult:
        if not self.configured:
            raise OpenRouterConnectorError("openrouter_not_configured")
        if not isinstance(prompt, str) or not prompt.strip():
            raise OpenRouterConnectorError("invalid_prompt")
        if len(prompt.encode("utf-8")) > 65_536:
            raise OpenRouterConnectorError("prompt_limit_exceeded")

        payload = json.dumps(
            {
                "model": self._model,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 1200,
                "temperature": 0.1,
                "stream": False,
            },
            separators=(",", ":"),
        ).encode("utf-8")

        request = urllib.request.Request(
            self.endpoint,
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
                "X-OpenRouter-Title": "MediaHub OS",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                raw = response.read(1_048_576)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise OpenRouterConnectorError("openrouter_unavailable") from exc

        try:
            data = json.loads(raw.decode("utf-8"))
            choices = data["choices"]
            message = choices[0]["message"]
            output = message["content"]
            model = data.get("model", self._model)
            generation_id = data.get("id")
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise OpenRouterConnectorError("openrouter_invalid_response") from exc

        if not isinstance(output, str) or not output.strip():
            raise OpenRouterConnectorError("openrouter_empty_result")
        if not isinstance(model, str) or not model.strip():
            raise OpenRouterConnectorError("openrouter_invalid_response")
        if generation_id is not None and not isinstance(generation_id, str):
            generation_id = None

        return OpenRouterResult(output=output, model=model, generation_id=generation_id)
