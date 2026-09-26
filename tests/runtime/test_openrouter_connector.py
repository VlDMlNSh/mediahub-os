import json
import urllib.request

from mediahub_runtime.connectors.openrouter import OpenRouterConnector, OpenRouterConnectorError


class FakeResponse:
    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, _limit):
        return json.dumps({
            "id": "gen-1",
            "model": "z-ai/glm-5.2",
            "choices": [{"message": {"content": "OK"}}],
        }).encode()


def test_openrouter_connector_is_explicitly_injected():
    connector = OpenRouterConnector("test-key", "z-ai/glm-5.2")
    original = urllib.request.urlopen
    urllib.request.urlopen = lambda request, timeout: FakeResponse()
    try:
        result = connector.infer("hello")
    finally:
        urllib.request.urlopen = original

    assert result.output == "OK"
    assert result.model == "z-ai/glm-5.2"
    assert result.generation_id == "gen-1"


def test_openrouter_connector_does_not_accept_missing_credential():
    connector = OpenRouterConnector(None, "z-ai/glm-5.2")
    try:
        connector.infer("hello")
    except OpenRouterConnectorError as exc:
        assert exc.code == "openrouter_not_configured"
    else:
        raise AssertionError("expected fail-closed configuration")


def test_openrouter_connector_rejects_empty_prompt():
    connector = OpenRouterConnector("test-key", "z-ai/glm-5.2")
    try:
        connector.infer("")
    except OpenRouterConnectorError as exc:
        assert exc.code == "invalid_prompt"
    else:
        raise AssertionError("expected invalid prompt")
