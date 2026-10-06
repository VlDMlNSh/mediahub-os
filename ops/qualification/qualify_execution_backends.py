#!/usr/bin/env python3
"""Bounded provider/model qualification for the Astra compute pool.

Secrets are read only from environment variables and are never emitted.
A provider is QUALIFIED only after a live bounded request returns a usable
model response. Missing credentials are SKIPPED, not failures.
"""
from __future__ import annotations

import concurrent.futures
import hashlib
import json
import os
import platform
import argparse
import re
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "ops" / "qualification" / "provider_model_registry.json"
TIMEOUT = max(5, int(os.environ.get("ASTRA_PROVIDER_TIMEOUT_SECONDS", "20")))
MARKER = "MEDIAHUB_PROVIDER_QUALIFICATION_OK"


def digest(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8", "replace")).hexdigest()


def classify_detail(status: int | None, text: str) -> str:
    t = text.lower()
    patterns = (
        ("invalid_api_key", ("invalid api key", "invalid api_key", "invalid_api_key", "incorrect api key", "invalid token", "unauthorized")),
        ("permission_denied", ("permission denied", "access denied", "forbidden", "not permitted")),
        ("regional_restriction", ("country", "region", "territory", "location", "supported countries", "unsupported region")),
        ("insufficient_balance", ("insufficient balance", "insufficient funds", "billing", "payment required", "credits")),
        ("model_unavailable", ("model not found", "model_not_found", "does not exist", "unknown model", "unsupported model")),
        ("rate_limit_or_quota", ("rate limit", "too many requests", "quota", "rate_limit")),
        ("service_unavailable", ("service unavailable", "temporarily unavailable", "overloaded")),
    )
    for label, needles in patterns:
        if any(n in t for n in needles):
            return label
    return "unspecified_http_error" if status is not None else "unspecified_error"


def classify(status: int | None, text: str, exc: Exception | None = None) -> str:
    t = text.lower()
    if status == 402:
        return "insufficient_balance"
    if status in (401, 403):
        if any(x in t for x in ("country", "region", "territory", "location", "supported")):
            return "regional_restriction"
        return "authentication_or_authorization"
    if status == 404 or "model" in t and any(x in t for x in ("not found", "does not exist", "unavailable")):
        return "model_unavailable"
    if status in (408, 504) or isinstance(exc, TimeoutError):
        return "timeout"
    if status == 429 or any(x in t for x in ("rate limit", "too many requests", "quota")):
        return "rate_limit_or_quota"
    if exc is not None:
        if isinstance(exc, urllib.error.URLError):
            reason = str(exc.reason).lower()
            if "name or service not known" in reason or "nodename" in reason:
                return "dns"
            return "network"
        return "network"
    if status is not None and status >= 500:
        return "provider_unavailable"
    return "request_failed"


def credential(provider: dict) -> tuple[str | None, bool]:
    for name in provider.get("credential_env", []):
        if os.environ.get(name):
            return name, True
    return None, False


def request_openai_compatible(provider: dict, model: str, key: str) -> dict:
    url = provider["base_url"].rstrip("/") + "/chat/completions"
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": MARKER}],
        "temperature": 0,
        "max_tokens": 16,
    }).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            raw = response.read(128 * 1024).decode("utf-8", "replace")
            elapsed = round(time.monotonic() - started, 3)
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                payload = {}
            content = ""
            choices = payload.get("choices") or []
            if choices and isinstance(choices[0], dict):
                msg = choices[0].get("message") or {}
                content = str(msg.get("content") or "")
            if not content:
                output_text = payload.get("output_text")
                if output_text:
                    content = str(output_text)
            usable = bool(content.strip())
            return {
                "status_code": response.status,
                "latency_seconds": elapsed,
                "output_bytes": len(raw.encode("utf-8", "replace")),
                "output_sha256": digest(raw),
                "response_usable": usable,
                "marker_echoed": MARKER in content,
                "classification": "PASS" if usable else "request_failed",
            }
    except urllib.error.HTTPError as exc:
        raw = exc.read(32 * 1024).decode("utf-8", "replace")
        return {
            "status_code": exc.code,
            "latency_seconds": round(time.monotonic() - started, 3),
            "output_bytes": len(raw.encode("utf-8", "replace")),
            "output_sha256": digest(raw),
            "classification": classify(exc.code, raw, exc),
            "diagnostic": classify_detail(exc.code, raw),
        }
    except Exception as exc:
        return {
            "status_code": None,
            "latency_seconds": round(time.monotonic() - started, 3),
            "output_bytes": 0,
            "output_sha256": "",
            "classification": classify(None, str(exc), exc),
            "diagnostic": classify_detail(None, str(exc)),
        }


def discover_default_model(provider: dict, key: str) -> dict:
    url = provider["base_url"].rstrip("/") + "/models"
    req = urllib.request.Request(url, method="GET", headers={"Authorization": "Bearer " + key, "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            payload = json.loads(response.read(128 * 1024).decode("utf-8", "replace"))
            for item in payload.get("data") or []:
                if isinstance(item, dict) and item.get("id"): return {"model": str(item["id"])}
            return {"classification": "model_unavailable"}
    except urllib.error.HTTPError as exc:
        raw = exc.read(32 * 1024).decode("utf-8", "replace")
        return {"classification": classify(exc.code, raw, exc)}
    except Exception as exc:
        return {"classification": classify(None, str(exc), exc)}

def request_responses_compatible(provider: dict, model: str, key: str) -> dict:
    url = provider["base_url"].rstrip("/") + "/responses"
    body = json.dumps({"model": model, "input": MARKER}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={
        "Authorization": "Bearer " + key, "Content-Type": "application/json", "Accept": "application/json"
    })
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            raw = response.read(128 * 1024).decode("utf-8", "replace")
            elapsed = round(time.monotonic() - started, 3)
            payload = json.loads(raw)
            content = str(payload.get("output_text") or "")
            if not content:
                for item in payload.get("output") or []:
                    if not isinstance(item, dict): continue
                    for part in item.get("content") or []:
                        if isinstance(part, dict) and part.get("text"):
                            content += str(part["text"])
            return {"status_code": response.status, "latency_seconds": elapsed, "output_bytes": len(raw.encode("utf-8","replace")), "output_sha256": digest(raw), "response_usable": bool(content.strip()), "marker_echoed": MARKER in content, "classification": "PASS" if content.strip() else "request_failed"}
    except urllib.error.HTTPError as exc:
        raw = exc.read(32 * 1024).decode("utf-8", "replace")
        return {"status_code": exc.code, "latency_seconds": round(time.monotonic()-started,3), "output_bytes": len(raw.encode("utf-8","replace")), "output_sha256": digest(raw), "classification": classify(exc.code, raw, exc), "diagnostic": classify_detail(exc.code, raw)}
    except Exception as exc:
        return {"status_code": None, "latency_seconds": round(time.monotonic()-started,3), "output_bytes": 0, "output_sha256": "", "classification": classify(None, str(exc), exc), "diagnostic": classify_detail(None, str(exc))}

def request_cloudflare_workers_ai(provider: dict, model: str, key: str) -> dict:
    account_env = (provider.get("account_id_env") or [None])[0]
    account_id = os.environ.get(account_env or "")
    if not account_id: return {"classification": "account_id_absent"}
    url = provider["base_url"].rstrip("/") + "/" + account_id + "/ai/run/" + model
    body = json.dumps({"messages": [{"role": "user", "content": MARKER}], "max_tokens": 16}).encode()
    req = urllib.request.Request(url, data=body, method="POST", headers={"Authorization": "Bearer " + key, "Content-Type": "application/json", "Accept": "application/json"})
    started = time.monotonic()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            raw = response.read(128 * 1024).decode("utf-8", "replace")
            payload = json.loads(raw); result = payload.get("result") or {}
            content = str(result.get("response") or result.get("text") or "")
            return {"status_code": response.status, "latency_seconds": round(time.monotonic()-started,3), "output_bytes": len(raw.encode("utf-8","replace")), "output_sha256": digest(raw), "response_usable": bool(content.strip()), "marker_echoed": MARKER in content, "classification": "PASS" if content.strip() else "request_failed"}
    except urllib.error.HTTPError as exc:
        raw = exc.read(32 * 1024).decode("utf-8", "replace")
        return {"status_code": exc.code, "latency_seconds": round(time.monotonic()-started,3), "output_bytes": len(raw.encode("utf-8","replace")), "output_sha256": digest(raw), "classification": classify(exc.code, raw, exc)}
    except Exception as exc:
        return {"status_code": None, "latency_seconds": round(time.monotonic()-started,3), "output_bytes": 0, "output_sha256": "", "classification": classify(None, str(exc), exc)}

def _bounded_request(provider: dict, model: str, key: str) -> list[dict]:
    max_attempts = 3
    retryable = {"timeout", "provider_unavailable", "rate_limit_or_quota", "network"}
    attempts = []
    for attempt in range(1, max_attempts + 1):
        if provider.get("adapter") == "cloudflare_workers_ai":
            result = request_cloudflare_workers_ai(provider, model, key)
        elif provider.get("adapter") == "responses_compatible":
            result = request_responses_compatible(provider, model, key)
        else:
            result = request_openai_compatible(provider, model, key)
        safe = {k: v for k, v in result.items() if k != "response_body"}
        safe["attempt"] = attempt
        attempts.append(safe)
        if result.get("classification") == "PASS" or result.get("classification") not in retryable:
            break
        if attempt < max_attempts:
            time.sleep(min(2 ** (attempt - 1), 4))
    return attempts


def qualify(provider: dict) -> dict:
    env_name, present = credential(provider)
    base = {
        "provider_id": provider["id"],
        "provider": provider["provider"],
        "family": provider["family"],
        "credential_present": present,
        "credential_env": env_name or "SUPPRESSED",
        "models": provider["models"],
        "capabilities": provider["capabilities"],
        "cost_class": provider["cost_class"],
        "persistence_class": provider["persistence_class"],
        "verification_state": "SKIPPED" if not present else "UNVERIFIED",
        "models_tested": [],
        "region_availability": "UNVERIFIED",
    }
    if not present:
        base["reason"] = "credential_absent"
        return base

    key = os.environ[env_name]
    for model in provider["models"]:
        if model == "default":
            discovered = discover_default_model(provider, key)
            if discovered.get("model"):
                model = discovered["model"]
            else:
                base["models_tested"].append({"model": "default", "status": "BLOCKED", "reason": discovered.get("classification", "model_discovery_failed")})
                continue
        attempt_records = _bounded_request(provider, model, key)
        final = attempt_records[-1]
        for item in attempt_records:
            item["model"] = model
            base["models_tested"].append(item)
        if final.get("classification") == "PASS":
            base["verification_state"] = "QUALIFIED"
            base["region_availability"] = "AVAILABLE"
            base["selected_model"] = model
            base["latency_seconds"] = final["latency_seconds"]
            if len(attempt_records) > 1:
                base["qualification_attempts"] = len(attempt_records)
            return base
        if final.get("classification") == "regional_restriction":
            base["region_availability"] = "REGION_UNAVAILABLE"
            base["verification_state"] = "SKIPPED"
            base["reason"] = "regional_restriction"
            return base

    base["reason"] = "no_model_qualified"
    return base


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-sha", default=None)
    args = parser.parse_args()

    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    providers = registry["providers"]
    started = time.monotonic()
    try:
        current_revision = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
            capture_output=True, timeout=10, check=False,
        ).stdout.strip()
    except Exception:
        current_revision = ""

    if args.target_sha:
        if not re.fullmatch(r"[0-9a-f]{40}", args.target_sha):
            payload = {
                "schema": "mediahub.provider-model-qualification.v1",
                "status": "BLOCKED",
                "captured_at": int(time.time()),
                "node_id": platform.node(),
                "target_sha": args.target_sha,
                "repo_revision": current_revision,
                "reason": "invalid_target_sha",
                "providers": [],
                "summary": {"qualified_providers": 0, "qualified_models": 0, "provider_families": 0, "families": []},
                "secret_values": "SUPPRESSED",
            }
            payload["evidence_digest"] = digest(json.dumps(payload, sort_keys=True, separators=(",", ":")))
            print(json.dumps(payload, sort_keys=True))
            return 2
        if current_revision != args.target_sha:
            payload = {
                "schema": "mediahub.provider-model-qualification.v1",
                "status": "BLOCKED",
                "captured_at": int(time.time()),
                "node_id": platform.node(),
                "target_sha": args.target_sha,
                "repo_revision": current_revision,
                "reason": "target_sha_not_exact_current_head",
                "providers": [],
                "summary": {"qualified_providers": 0, "qualified_models": 0, "provider_families": 0, "families": []},
                "secret_values": "SUPPRESSED",
            }
            payload["evidence_digest"] = digest(json.dumps(payload, sort_keys=True, separators=(",", ":")))
            print(json.dumps(payload, sort_keys=True))
            return 2

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(providers))) as pool:
        results = list(pool.map(qualify, providers))

    qualified = [r for r in results if r["verification_state"] == "QUALIFIED"]
    families = sorted({r["family"] for r in qualified})
    payload = {
        "schema": "mediahub.provider-model-qualification.v1",
        "status": "PASS" if qualified else "BLOCKED",
        "captured_at": int(time.time()),
        "node_id": platform.node(),
        "target_sha": args.target_sha or current_revision,
        "repo_revision": current_revision,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "providers": results,
        "summary": {
            "qualified_providers": len(qualified),
            "qualified_models": sum(1 for r in qualified if r.get("selected_model")),
            "provider_families": len(families),
            "families": families,
        },
        "secret_values": "SUPPRESSED",
    }
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    payload["evidence_digest"] = digest(canonical)
    print(json.dumps(payload, sort_keys=True))
    return 0 if qualified else 2


if __name__ == "__main__":
    raise SystemExit(main())
