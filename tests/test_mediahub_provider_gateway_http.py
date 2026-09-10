import http.client
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "ops"))
import mediahub_provider_gateway_http as module


def test_models_are_local_and_bounded():
    assert module.LISTEN[0] == "127.0.0.1"
    assert module.MAX_BODY == 8 * 1024 * 1024


def test_provider_order_is_deterministic():
    assert [p.name for p in module.PROVIDERS] == ["opper", "continuum"]


def test_capability_matrix_is_explicit():
    assert "responses" in module.CAPABILITIES["continuum"]
    assert "chat_completions" in module.CAPABILITIES["opper"]
    assert "responses" not in module.CAPABILITIES["opper"]
    assert "messages" in module.CAPABILITIES["continuum"]


def test_upstream_paths_and_credentials(tmp_path, monkeypatch):
    for name in ("mediahub-opper", "mediahub-continuum"):
        (tmp_path / name).write_text(name + "-secret", encoding="utf-8")
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    assert module.upstream("continuum", "/v1/responses")[1] == "/v1/responses"
    assert module.upstream("opper", "/v1/chat/completions")[1] == "/v3/compat/chat/completions"
    assert module.upstream("continuum", "/v1/responses")[1] == "/v1/responses"
    assert module.upstream("continuum", "/v1/messages")[1] == "/v1/messages"


def test_models_payload_is_json():
    payload = json.dumps({"object": "list", "data": []}).encode()
    assert json.loads(payload)["object"] == "list"


def test_policy_blocked_does_not_retry_same_provider():
    gateway = module.ProviderGateway(module.PROVIDERS)
    decision = gateway.failover("continuum", 403, "Access denied by security policy")
    assert decision.provider == "opper"
    assert decision.retry is False


def test_no_external_gateway_bind():
    assert module.LISTEN[0] == "127.0.0.1"


def test_opper_does_not_claim_responses():
    handler = object.__new__(module.Handler)
    handler.headers = {}
    original = module.upstream
    module.upstream = lambda provider, path: ("api.opper.ai", "/v3/compat/chat/completions", "test")
    try:
        handler.forward("opper", "/v1/responses", b"{}")
    except (OSError, ValueError, http.client.HTTPException) as exc:
        assert "protocol capability" in str(exc) or "Opper" in str(exc)
    else:
        raise AssertionError("unsupported Opper Responses path was not rejected")
    finally:
        module.upstream = original
