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
    Provider("gigachat", "GIGACHAT_API_PERS", os.environ.get("GIGACHAT_MODELS_URL", "https://api.giga.chat/v1/models"), "gigachat"),
)

def request_for(p: Provider, secret: str) -> urllib.request.Request:
    if p.scheme == "query_key":
        sep = "&" if "?" in p.url else "?"
        return urllib.request.Request(p.url + sep + urllib.parse.urlencode({"key": secret}), headers={"Accept":"application/json"}, method="GET")
    if p.scheme == "anthropic":
        return urllib.request.Request(p.url, headers={"x-api-key": secret, "anthropic-version":"2023-06-01","Accept":"application/json"}, method="GET")
    if p.scheme == "gigachat":
        token = base64.b64encode(secret.encode()).decode()
        return urllib.request.Request(p.url, headers={"Authorization":f"Basic {token}","Accept":"application/json"}, method="GET")
    return urllib.request.Request(p.url, headers={"Authorization":f"Bearer {secret}","Accept":"application/json"}, method="GET")

def probe(p: Provider) -> dict:
    secret = os.environ.get(p.env)
    if not secret:
        return {"id": p.id, "status": "NOT_PROVEN", "reason": "credential_not_present"}
    if not p.url:
        return {"id": p.id, "status": "NOT_PROVEN", "reason": "models_endpoint_not_configured"}
    try:
        with urllib.request.urlopen(request_for(p, secret), timeout=20, context=ssl.create_default_context()) as resp:
            ok = 200 <= resp.status < 300
            return {"id": p.id, "status": "AUTH_SUCCESS" if ok else "BLOCKED", "http_status": resp.status}
    except Exception as exc:
        return {"id": p.id, "status": "BLOCKED", "reason": type(exc).__name__}

def main() -> int:
    results = [probe(p) for p in PROVIDERS]
    print(json.dumps({"schema":"mediahub.astra-gold.hybrid-auth-probe.v2","system":"ASTRA_GOLD",
                      "results":results,"secret_values":"SUPPRESSED","tokens":"SUPPRESSED"}, sort_keys=True))
    return 0 if all(r["status"] == "AUTH_SUCCESS" for r in results) else 2

if __name__ == "__main__":
    raise SystemExit(main())
