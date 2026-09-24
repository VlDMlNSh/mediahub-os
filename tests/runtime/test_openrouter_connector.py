from __future__ import annotations
import json
from mediahub_runtime.connectors.openrouter import OpenRouterConnector, OpenRouterConnectorError

class _Response:
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, limit):
        return json.dumps({"id":"gen-test","model":"z-ai/glm-5.2","choices":[{"message":{"content":"OK"}}]}).encode()

def test_infer_uses_explicit_injected_credential(monkeypatch):
    import mediahub_runtime.connectors.openrouter as mod
    monkeypatch.setattr(mod.urllib.request, "urlopen", lambda request, timeout: _Response())
    result = OpenRouterConnector("runtime-only", "z-ai/glm-5.2").infer("hello")
    assert result.output == "OK"
    assert result.model == "z-ai/glm-5.2"
    assert result.generation_id == "gen-test"

def test_missing_credential_fails_closed():
    connector = OpenRouterConnector(None, "z-ai/glm-5.2")
    try: connector.infer("hello")
    except OpenRouterConnectorError as exc: assert exc.code == "openrouter_not_configured"
    else: raise AssertionError("expected fail-closed connector")

def test_empty_prompt_fails_closed():
    connector = OpenRouterConnector("runtime-only", "z-ai/glm-5.2")
    try: connector.infer(" ")
    except OpenRouterConnectorError as exc: assert exc.code == "invalid_prompt"
    else: raise AssertionError("expected invalid prompt")
