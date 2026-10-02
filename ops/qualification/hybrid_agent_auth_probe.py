#!/usr/bin/env python3
"""ASTRA GOLD non-secret hybrid cloud authentication/model-discovery probe."""
from __future__ import annotations
import base64, json, os, ssl, urllib.parse, urllib.request
from dataclasses import dataclass

@dataclass(frozen=True)
class Provider:
    id: str
    env: str
    url: str
    scheme: str = "bearer"

PROVIDERS = (
    Provider("gemini", "GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/models", "query_key"),
    Provider("perplexity", "PERPLEXITY_API_KEY", "https://api.perplexity.ai/models"),
    Provider("kimi", "KIMI_API_KEY", os.environ.get("KIMI_MODELS_URL", "https://api.moonshot.ai/v1/models")),
    Provider("deepseek", "DEEPSEEK_API_KEY", "https://api.deepseek.com/models"),
    Provider("chatgpt", "OPENAI_API_KEY", "https://api.openai.com/v1/models"),
    Provider("openrouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/models"),
    Provider("unorouter", "UNOROUTER_API_KEY", os.environ.get("UNOROUTER_MODELS_URL", "")),
    Provider("claude", "ANTHROPIC_API_KEY", os.environ.get("CLAUDE_MODELS_URL", "https://api.anthropic.com/v1/models"), "anthropic"),
    Provider("gigachat", "GIGACHAT_API_PERS", "", "gigachat"),
)

def gigachat_models(secret: str) -> dict:
    client_id = os.environ.get("GIGACHAT_CLIENT_ID", "01a0e9b4-b923-79b2-9996-e2e33d3fd63f")
    token_url = os.environ.get("GIGACHAT_TOKEN_URL", "https://ngw.devices.sberbank.ru:9443/api/v2/oauth")
    scope = os.environ.get("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
    basic = base64.b64encode(f"{client_id}:{secret}".encode()).decode()
    body = urllib.parse.urlencode({"scope": scope}).encode()
    req = urllib.request.Request(token_url, data=body, headers={"Authorization": f"Basic {basic}", "RqUID": os.environ.get("GIGACHAT_RQUID", ""), "Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    token = payload.get("access_token")
    if not token:
        raise RuntimeError("gigachat_token_missing")
    models_url = os.environ.get("GIGACHAT_MODELS_URL", "https://api.giga.chat/v1/models")
    req = urllib.request.Request(models_url, headers={"Authorization": f"Bearer {token}", "Accept": "application/json"}, method="GET")
    with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as resp:
        return {"http_status": resp.status}

def request_for(p: Provider, secret: str) -> urllib.request.Request:
    if p.scheme == "query_key":
        sep = "&" if "?" in p.url else "?"
        return urllib.request.Request(p.url + sep + urllib.parse.urlencode({"key": secret}), headers={"Accept":"application/json"}, method="GET")
    if p.scheme == "anthropic":
        return urllib.request.Request(p.url, headers={"x-api-key": secret, "anthropic-version":"2023-06-01","Accept":"application/json"}, method="GET")
    return urllib.request.Request(p.url, headers={"Authorization":f"Bearer {secret}","Accept":"application/json"}, method="GET")

def probe(p: Provider) -> dict:
    secret = os.environ.get(p.env)
    if not secret:
        return {"id": p.id, "status": "NOT_PROVEN", "reason": "credential_not_present"}
    if p.id == "unorouter" and not p.url:
        return {"id": p.id, "status": "NOT_PROVEN", "reason": "models_endpoint_not_configured"}
    try:
        if p.id == "gigachat":
            return {"id": p.id, "status": "AUTH_SUCCESS", **gigachat_models(secret)}
        with urllib.request.urlopen(request_for(p, secret), timeout=20, context=ssl.create_default_context()) as resp:
            ok = 200 <= resp.status < 300
            return {"id": p.id, "status": "AUTH_SUCCESS" if ok else "BLOCKED", "http_status": resp.status}
    except Exception as exc:
        return {"id": p.id, "status": "BLOCKED", "reason": type(exc).__name__}

def main() -> int:
    results = [probe(p) for p in PROVIDERS]
    print(json.dumps({"schema":"mediahub.astra-gold.hybrid-auth-probe.v3","system":"ASTRA_GOLD","results":results,"secret_values":"SUPPRESSED","tokens":"SUPPRESSED"}, sort_keys=True))
    return 0 if all(r["status"] == "AUTH_SUCCESS" for r in results) else 2

if __name__ == "__main__":
    raise SystemExit(main())
