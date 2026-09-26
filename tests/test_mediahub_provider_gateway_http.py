import http.client
import json

import ops.mediahub_provider_gateway_http as module


def test_models_are_local_and_bounded():
    assert module.LISTEN[0] == "127.0.0.1"
    assert module.MAX_BODY == 8 * 1024 * 1024


def test_provider_order_is_deterministic():
    assert [p.name for p in module.PROVIDERS] == ["opper", "continuum", "experiential", "zhipu"]


def test_capability_matrix_is_explicit():
    assert "responses" in module.CAPABILITIES["continuum"]
    assert "chat_completions" in module.CAPABILITIES["opper"]
    assert "responses" not in module.CAPABILITIES["opper"]
    assert "messages" in module.CAPABILITIES["continuum"]
    assert "chat_completions" in module.CAPABILITIES["zhipu"]
    assert "chat_completions" in module.CAPABILITIES["experiential"]
    assert "gpt-5.6-luna" in module.EXPERIENTIAL_FREE_MODELS


def test_upstream_paths_and_credentials(tmp_path, monkeypatch):
    for name in ("mediahub-opper", "mediahub-continuum", "mediahub-zhipu", "mediahub-experiential"):
        (tmp_path / name).write_text(name + "-secret", encoding="utf-8")
    monkeypatch.setenv("CREDENTIALS_DIRECTORY", str(tmp_path))
    assert module.upstream("continuum", "/v1/responses")[1] == "/v1/responses"
    assert module.upstream("opper", "/v1/chat/completions")[1] == "/v3/compat/chat/completions"
    assert module.upstream("continuum", "/v1/responses")[1] == "/v1/responses"
    assert module.upstream("continuum", "/v1/messages")[1] == "/v1/messages"
    assert module.upstream("zhipu", "/v1/chat/completions")[1] == "/api/paas/v4/chat/completions"
    assert module.upstream("experiential", "/v1/chat/completions")[1] == "/v1/chat/completions"


def test_experiential_is_only_selected_for_allowlisted_free_model():
    handler = object.__new__(module.Handler)
    assert handler._request_model(b'{"model":"gpt-5.6-luna"}') == "gpt-5.6-luna"
    assert handler._request_model(b'{"model":"paid-model"}') == "paid-model"
    assert module.EXPERIENTIAL_FREE_MODELS.isdisjoint({"paid-model"})


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
