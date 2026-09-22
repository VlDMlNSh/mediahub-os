"""OpenAI provider adapter with server-side-only credential lookup."""

import json
import os
import urllib.request


class OpenAIProvider:
    """Small standard-library adapter; credentials are read only from process env."""

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
            "https://api.openai.com/v1/responses",
            data=payload,
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            body = json.loads(response.read().decode("utf-8"))
        return _extract_output(body)


def _extract_output(body: dict) -> str:
    if isinstance(body.get("output_text"), str):
        return body["output_text"]
    raise RuntimeError("provider_invalid_response")
