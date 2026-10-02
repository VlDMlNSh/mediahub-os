#!/usr/bin/env python3
"""Non-secret ASTRA GOLD hybrid-agent admission probe.

This probe never prints credentials or authorization tokens. It only verifies
that configured provider credentials can be used to reach a provider's
non-mutating model-discovery endpoint. Task execution and A3 verification
remain separate gates.
"""
from __future__ import annotations

import json
import os
import ssl
import urllib.request
from dataclasses import dataclass

@dataclass(frozen=True)
class Provider:
    id: str
    env: str
    url: str

PROVIDERS = (
    Provider("gemini", "GEMINI_API_KEY", "https://generativelanguage.googleapis.com/v1beta/models"),
    Provider("perplexity", "PERPLEXITY_API_KEY", "https://api.perplexity.ai/models"),
    Provider("deepseek", "DEEPSEEK_API_KEY", "https://api.deepseek.com/models"),
    Provider("openrouter", "OPENROUTER_API_KEY", "https://openrouter.ai/api/v1/models"),
    Provider("unorouter", "UNOROUTER_API_KEY", os.environ.get("UNOROUTER_MODELS_URL", "")),
)

def probe(p: Provider) -> dict:
    secret = os.environ.get(p.env)
    if not secret:
        return {"id": p.id, "status": "NOT_PROVEN", "reason": "credential_not_present"}
    if not p.url:
        return {"id": p.id, "status": "NOT_PROVEN", "reason": "models_endpoint_not_configured"}
    headers = {"Authorization": f"Bearer {secret}", "Accept": "application/json"}
    req = urllib.request.Request(p.url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as resp:
            ok = 200 <= resp.status < 300
            return {"id": p.id, "status": "AUTH_SUCCESS" if ok else "BLOCKED", "http_status": resp.status}
    except Exception as exc:
        return {"id": p.id, "status": "BLOCKED", "reason": type(exc).__name__}

def main() -> int:
    results = [probe(p) for p in PROVIDERS]
    print(json.dumps({
        "schema": "mediahub.astra-gold.hybrid-auth-probe.v1",
        "system": "ASTRA_GOLD",
        "results": results,
        "secret_values": "SUPPRESSED",
        "tokens": "SUPPRESSED",
    }, sort_keys=True))
    return 0 if all(r["status"] == "AUTH_SUCCESS" for r in results) else 2

if __name__ == "__main__":
    raise SystemExit(main())
