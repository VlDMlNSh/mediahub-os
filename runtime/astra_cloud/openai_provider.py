"""OpenAI Responses API adapter with server-side-only credentials."""

import json
import os
import urllib.request


class OpenAIProvider:
    def __init__(self, api_key_env: str = "OPENAI_API_KEY", model_env: str = "ASTRA_OPENAI_MODEL"):
        self._api_key_env = api_key_env
        self._model_env = model_env

    def __call__(self, command: str) -> str:
        api_key = os.environ.get(self._api_key_env)
        model = os.environ.get(self._model_env)
        if not api_key or not model:
            raise RuntimeError("provider_unconfigured")
        payload = json.dumps({"model": model, "input": command}).encode("utf-8")
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses", data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
        output = body.get("output_text")
        if not isinstance(output, str):
            raise RuntimeError("provider_invalid_response")
        return output
