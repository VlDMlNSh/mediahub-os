"""Cloud-first multi-provider orchestrator for MediaHub OS.

The orchestrator is a routing/control component, not an authority layer.
MediaHub Codex remains policy authority; the Gateway remains the delegation
boundary; provider adapters execute only after admission. Local providers are
extensions and are selected when a cloud route is unavailable or unsuitable.
No credentials are stored in this module or repository.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Callable, Mapping

from .kimi_k3_in_c import KimiK3InCExecutor
from .local_providers import FreeLLMAPIExecutor


class UnoRouterExecutor:
    """OpenAI-compatible UnoRouter adapter using a secret from the environment."""

    def __init__(self, env=None, timeout=30):
        self._env = dict(os.environ if env is None else env)
        self._timeout = timeout

    def __call__(self, prompt: str) -> str:
        key = self._env.get("UNOROUTER_API_KEY", "").strip()
        model = self._env.get("MEDIAHUB_UNOROUTER_MODEL", "").strip()
        if not key:
            raise CloudOrchestratorError("unorouter_credential_missing")
        if not model:
            raise CloudOrchestratorError("unorouter_model_unconfigured")
        body = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }, separators=(",", ":")).encode("utf-8")
        request = urllib.request.Request(
            "https://api.unorouter.com/v1/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                raw = response.read(1_048_576)
        except urllib.error.HTTPError as exc:
            raise CloudOrchestratorError(_http_error_code(exc.code)) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise CloudOrchestratorError("unorouter_request_failed") from exc
        try:
            data = json.loads(raw.decode("utf-8"))
            output = data["choices"][0]["message"]["content"]
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise CloudOrchestratorError("unorouter_invalid_response") from exc
        if not isinstance(output, str) or not output:
            raise CloudOrchestratorError("unorouter_empty_response")
        return output


class OpenAIResponsesExecutor:
    """OpenAI native Responses API adapter."""

    def __init__(self, env=None, timeout=45):
        self._env = dict(os.environ if env is None else env)
        self._timeout = timeout

    def __call__(self, prompt: str) -> str:
        key = self._env.get("OPENAI_API_KEY", "").strip()
        model = self._env.get("MEDIAHUB_OPENAI_MODEL", "").strip()
        if not key:
            raise CloudOrchestratorError("openai_credential_missing")
        if not model:
            raise CloudOrchestratorError("openai_model_unconfigured")
        body = json.dumps({
            "model": model,
            "input": prompt,
            "max_output_tokens": 1200,
        }, separators=(",", ":")).encode("utf-8")
        request = urllib.request.Request(
            "https://api.openai.com/v1/responses",
            data=body,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                raw = response.read(1_048_576)
        except urllib.error.HTTPError as exc:
            raise CloudOrchestratorError(_http_error_code(exc.code)) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise CloudOrchestratorError("openai_request_failed") from exc
        try:
            data = json.loads(raw.decode("utf-8"))
            output = data.get("output_text", "")
            if not output:
                output = "".join(
                    part.get("text", "")
                    for item in data.get("output", [])
                    if isinstance(item, dict)
                    for part in item.get("content", [])
                    if isinstance(part, dict) and part.get("type") == "output_text"
                )
        except (UnicodeDecodeError, json.JSONDecodeError, TypeError) as exc:
            raise CloudOrchestratorError("openai_invalid_response") from exc
        if not isinstance(output, str) or not output.strip():
            raise CloudOrchestratorError("openai_empty_response")
        return output

class OpenAICompatibleExecutor:
    """OpenAI Chat Completions adapter for compatible cloud gateways."""

    def __init__(self, env=None, credential_env="OPENAI_API_KEY", model_env="MEDIAHUB_OPENAI_MODEL", base_url="", timeout=45):
        self._env = dict(os.environ if env is None else env)
        self._credential_env = credential_env
        self._model_env = model_env
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def __call__(self, prompt: str) -> str:
        key = self._env.get(self._credential_env, "").strip()
        model = self._env.get(self._model_env, "").strip()
        if not key:
            raise CloudOrchestratorError("provider_credential_missing")
        if not model:
            raise CloudOrchestratorError("provider_model_unconfigured")
        body = json.dumps({
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        }, separators=(",", ":")).encode("utf-8")
        request = urllib.request.Request(
            f"{self._base_url}/chat/completions",
            data=body,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                raw = response.read(1_048_576)
        except urllib.error.HTTPError as exc:
            raise CloudOrchestratorError(_http_error_code(exc.code)) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise CloudOrchestratorError("provider_request_failed") from exc
        try:
            data = json.loads(raw.decode("utf-8"))
            output = data["choices"][0]["message"]["content"]
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise CloudOrchestratorError("provider_invalid_response") from exc
        if not isinstance(output, str) or not output:
            raise CloudOrchestratorError("provider_empty_response")
        return output


class GeminiExecutor:
    """Google Gemini native generateContent adapter."""

    def __init__(self, env=None, timeout=45):
        self._env = dict(os.environ if env is None else env)
        self._timeout = timeout

    def __call__(self, prompt: str) -> str:
        key = self._env.get("GEMINI_API_KEY", "").strip()
        model = self._env.get("MEDIAHUB_GEMINI_MODEL", "").strip()
        if not key:
            raise CloudOrchestratorError("gemini_credential_missing")
        if not model:
            raise CloudOrchestratorError("gemini_model_unconfigured")
        body = json.dumps({
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"maxOutputTokens": 1200},
        }, separators=(",", ":")).encode("utf-8")
        request = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
            data=body,
            headers={"x-goog-api-key": key, "Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                raw = response.read(1_048_576)
        except urllib.error.HTTPError as exc:
            raise CloudOrchestratorError(_http_error_code(exc.code)) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise CloudOrchestratorError("gemini_request_failed") from exc
        try:
            data = json.loads(raw.decode("utf-8"))
            output = "".join(
                part.get("text", "")
                for part in data["candidates"][0]["content"]["parts"]
                if isinstance(part, dict) and isinstance(part.get("text"), str)
            )
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, IndexError, TypeError) as exc:
            raise CloudOrchestratorError("gemini_invalid_response") from exc
        if not output.strip():
            raise CloudOrchestratorError("gemini_empty_response")
        return output

class OmniRouteClaudeExecutor:
    """Claude-compatible Anthropic Messages adapter through OmniRoute."""

    def __init__(self, env=None, timeout=45):
        self._env = dict(os.environ if env is None else env)
        self._timeout = timeout

    def __call__(self, prompt: str) -> str:
        key = self._env.get("OMNIROUTE_API_KEY", "").strip()
        model = self._env.get("MEDIAHUB_CLAUDE_MODEL", "").strip()
        base_url = self._env.get("OMNIROUTE_BASE_URL", "http://127.0.0.1:20128").strip().rstrip("/")
        if not key:
            raise CloudOrchestratorError("omniroute_credential_missing")
        if not model:
            raise CloudOrchestratorError("claude_model_unconfigured")
        body = json.dumps({
            "model": model,
            "max_tokens": int(self._env.get("MEDIAHUB_CLAUDE_MAX_OUTPUT_TOKENS", "4096")),
            "messages": [{"role": "user", "content": prompt}],
        }, separators=(",", ":")).encode("utf-8")
        request = urllib.request.Request(
            f"{base_url}/v1/messages",
            data=body,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self._timeout) as response:
                raw = response.read(1_048_576)
        except urllib.error.HTTPError as exc:
            raise CloudOrchestratorError(_http_error_code(exc.code)) from exc
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise CloudOrchestratorError("omniroute_request_failed") from exc
        try:
            data = json.loads(raw.decode("utf-8"))
            output = "".join(
                item.get("text", "") for item in data["content"]
                if isinstance(item, dict) and item.get("type") == "text"
            )
        except (UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
            raise CloudOrchestratorError("omniroute_invalid_response") from exc
        if not output:
            raise CloudOrchestratorError("omniroute_empty_response")
        return output


def _http_error_code(status: int) -> str:
    if status == 401:
        return "provider_auth_failed"
    if status == 402:
        return "provider_billing_blocked"
    if status in (403,):
        return "provider_auth_failed"
    if status == 429:
        return "provider_rate_limited"
    if 400 <= status < 500:
        return "provider_request_rejected"
    if 500 <= status < 600:
        return "provider_server_error"
    return "provider_http_error"


class CloudOrchestratorError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ProviderRoute:
    provider_id: str
    tier: str
    capabilities: frozenset[str]
    credential_env: str | None
    model_env: str | None
    priority: int


@dataclass(frozen=True)
class OrchestrationDecision:
    provider_id: str
    tier: str
    model: str | None
    reason: str


DEFAULT_CLOUD_ROUTES = (
    ProviderRoute("unorouter", "cloud", frozenset({"reasoning", "analysis", "coding", "architecture", "review", "research", "web", "multimodal", "documents", "long_context", "bulk", "repository", "testing", "transform", "classify"}), "UNOROUTER_API_KEY", "MEDIAHUB_UNOROUTER_MODEL", 4),
    ProviderRoute("openrouter", "cloud", frozenset({"reasoning", "analysis", "coding", "architecture", "review", "research", "web", "multimodal", "documents", "long_context", "bulk", "repository", "testing", "transform", "classify"}), "OPENROUTER_API_KEY", "MEDIAHUB_OPENROUTER_MODEL", 5),
    ProviderRoute("openai", "cloud", frozenset({"reasoning", "analysis", "coding"}), "OPENAI_API_KEY", "MEDIAHUB_OPENAI_MODEL", 10),
    ProviderRoute("claude", "cloud", frozenset({"coding", "architecture", "review", "reasoning"}), "OMNIROUTE_API_KEY", "MEDIAHUB_CLAUDE_MODEL", 20),
    ProviderRoute("gemini", "cloud", frozenset({"multimodal", "documents", "reasoning"}), "GEMINI_API_KEY", "MEDIAHUB_GEMINI_MODEL", 30),
    ProviderRoute("perplexity", "cloud", frozenset({"research", "web"}), "PERPLEXITY_API_KEY", "MEDIAHUB_PERPLEXITY_MODEL", 40),
    ProviderRoute("kimi", "cloud", frozenset({"reasoning", "long_context"}), "KIMI_API_KEY", "MEDIAHUB_KIMI_MODEL", 50),
    ProviderRoute("deepseek", "cloud", frozenset({"coding", "reasoning", "bulk"}), "DEEPSEEK_API_KEY", "MEDIAHUB_DEEPSEEK_MODEL", 60),
    ProviderRoute("cursor", "cloud", frozenset({"repository", "coding", "testing"}), "CURSOR_API_KEY", "MEDIAHUB_CURSOR_MODEL", 70),
    ProviderRoute("chatgpt", "cloud", frozenset({"reasoning", "analysis"}), "CHATGPT_API_KEY", "MEDIAHUB_CHATGPT_MODEL", 80),
)

DEFAULT_LOCAL_ROUTES = (
    ProviderRoute("freellmapi", "local_gateway", frozenset({"coding", "reasoning", "analysis", "architecture", "review", "research", "web", "documents", "long_context", "bulk", "repository", "testing", "transform", "classify"}), None, "MEDIAHUB_FREELLMAPI_MODEL", 700),
    ProviderRoute("kimi-k3-in-c", "local", frozenset({"reasoning", "long_context", "coding"}), None, "MEDIAHUB_KIMI_K3_MODEL", 900),
    ProviderRoute("ollama", "local", frozenset({"coding", "transform", "classify", "private"}), None, "MEDIAHUB_OLLAMA_MODEL", 1000),
)


class CloudFirstOrchestrator:
    """Selects an admitted provider without exposing credentials to callers."""

    def __init__(
        self,
        cloud_routes: tuple[ProviderRoute, ...] = DEFAULT_CLOUD_ROUTES,
        local_routes: tuple[ProviderRoute, ...] = DEFAULT_LOCAL_ROUTES,
        credential_env: Mapping[str, str] | None = None,
        executors: Mapping[str, Callable[[str], str]] | None = None,
    ):
        self._env = dict(os.environ if credential_env is None else credential_env)
        self._cloud = self._order_cloud_routes(tuple(cloud_routes))
        self._local = tuple(sorted(local_routes, key=lambda r: r.priority))
        self._executors = dict(executors or {})
        self._freellmapi = FreeLLMAPIExecutor()
        self._kimi_k3 = KimiK3InCExecutor()
        self._executors.setdefault("freellmapi", self._freellmapi)
        self._executors.setdefault("unorouter", UnoRouterExecutor(env=self._env))
        self._executors.setdefault("claude", OmniRouteClaudeExecutor(env=self._env))
        self._executors.setdefault("kimi-k3-in-c", self._kimi_k3)

    def _order_cloud_routes(self, routes: tuple[ProviderRoute, ...]) -> tuple[ProviderRoute, ...]:
        """Apply an explicit cost-optimized routing profile without bypassing provider policy."""
        profile = self._env.get("MEDIAHUB_CLOUD_ROUTING_PROFILE", "balanced").strip().lower()
        if profile != "cost_optimized":
            return tuple(sorted(routes, key=lambda r: r.priority))
        cost_rank = {
            "openrouter": 10,
            "gemini": 20,
            "deepseek": 30,
            "kimi": 40,
            "perplexity": 50,
            "unorouter": 60,
            "openai": 70,
            "claude": 80,
            "cursor": 90,
            "chatgpt": 100,
        }
        return tuple(sorted(routes, key=lambda r: (cost_rank.get(r.provider_id, 1000), r.priority)))

    def decide(self, capability: str, *, allow_local_extension: bool = True) -> OrchestrationDecision:
        if not isinstance(capability, str) or not capability.strip():
            raise CloudOrchestratorError("invalid_capability")

        for route in self._cloud:
            if capability in route.capabilities and self._configured(route) and self._admitted(route):
                return OrchestrationDecision(
                    route.provider_id,
                    route.tier,
                    self._model(route),
                    "cloud_provider_admitted",
                )

        if allow_local_extension:
            for route in self._local:
                if capability not in route.capabilities:
                    continue
                if not self._admitted(route):
                    continue
                executor = self._executors.get(route.provider_id)
                if hasattr(executor, "available") and not executor.available():
                    continue
                return OrchestrationDecision(
                    route.provider_id,
                    route.tier,
                    self._model(route),
                    "cloud_unavailable_local_extension",
                )

        raise CloudOrchestratorError("no_provider_available")

    def execute(self, capability: str, prompt: str, *, allow_local_extension: bool = True) -> tuple[OrchestrationDecision, str]:
        """Execute with bounded provider/model/key failover.

        Failover is driven by the configured route order. A provider may expose
        multiple model slots and credential slots through environment variables:
        MEDIAHUB_<PROVIDER>_MODELS (comma-separated) and
        <CREDENTIAL_ENV>_1, <CREDENTIAL_ENV>_2, ... . The primary singular
        variables remain supported for backward compatibility.

        We retry only on provider execution/configuration failures. The prompt
        is never sent to more than one candidate after a successful response.
        """
        if not isinstance(prompt, str) or not prompt:
            raise CloudOrchestratorError("invalid_prompt")

        candidates = self._candidates(capability, allow_local_extension=allow_local_extension)
        last_error = None
        for decision, executor in candidates:
            try:
                output = executor(prompt)
            except CloudOrchestratorError as exc:
                last_error = exc
                continue
            except Exception as exc:
                last_error = CloudOrchestratorError("provider_execution_failed")
                last_error.__cause__ = exc
                continue
            if isinstance(output, str) and output:
                return decision, output
            last_error = CloudOrchestratorError("empty_provider_result")

        if last_error is not None:
            raise last_error
        raise CloudOrchestratorError("no_provider_available")

    def _candidates(self, capability: str, *, allow_local_extension: bool) -> tuple[tuple[OrchestrationDecision, Callable[[str], str]], ...]:
        if not isinstance(capability, str) or not capability.strip():
            raise CloudOrchestratorError("invalid_capability")

        routes = list(self._cloud)
        if allow_local_extension:
            routes.extend(self._local)

        candidates = []
        for route in routes:
            if capability not in route.capabilities:
                continue
            if not self._configured(route):
                continue
            if not self._admitted(route):
                continue
            models = self._models(route)
            credentials = self._credentials(route)
            if route.credential_env is None:
                credentials = (None,)
            if not models:
                models = (self._model(route),)
            for credential in credentials:
                for model in models:
                    env = dict(self._env)
                    if route.credential_env and credential:
                        env[route.credential_env] = credential
                    if route.model_env and model:
                        env[route.model_env] = model
                    executor = self._executor_for(route.provider_id, env)
                    if executor is None:
                        continue
                    candidates.append((
                        OrchestrationDecision(
                            route.provider_id,
                            route.tier,
                            model,
                            "cloud_provider_admitted" if route.tier == "cloud" else "cloud_unavailable_local_extension",
                        ),
                        executor,
                    ))
        return tuple(candidates)

    def _executor_for(self, provider_id: str, env: Mapping[str, str]):
        if provider_id == "unorouter":
            return UnoRouterExecutor(env=env)
        if provider_id == "claude":
            return OmniRouteClaudeExecutor(env=env)
        if provider_id == "gemini":
            return GeminiExecutor(env=env)
        if provider_id == "openai":
            return OpenAIResponsesExecutor(env=env)
        compatible = {
            "openrouter": ("OPENROUTER_API_KEY", "MEDIAHUB_OPENROUTER_MODEL", "https://openrouter.ai/api/v1"),
            "openai": ("OPENAI_API_KEY", "MEDIAHUB_OPENAI_MODEL", "https://api.openai.com/v1"),
            "perplexity": ("PERPLEXITY_API_KEY", "MEDIAHUB_PERPLEXITY_MODEL", "https://api.perplexity.ai"),
            "kimi": ("KIMI_API_KEY", "MEDIAHUB_KIMI_MODEL", "https://api.moonshot.ai/v1"),
            "deepseek": ("DEEPSEEK_API_KEY", "MEDIAHUB_DEEPSEEK_MODEL", "https://api.deepseek.com"),
        }
        if provider_id in compatible:
            credential_env, model_env, base_url = compatible[provider_id]
            return OpenAICompatibleExecutor(
                env=env,
                credential_env=credential_env,
                model_env=model_env,
                base_url=base_url,
            )
        if provider_id == "freellmapi":
            return FreeLLMAPIExecutor(
                base_url=env.get("MEDIAHUB_FREELLMAPI_URL") or None,
                key_file=env.get("MEDIAHUB_FREELLMAPI_KEY_FILE") or None,
                model=env.get("MEDIAHUB_FREELLMAPI_MODEL") or None,
            )
        return self._executors.get(provider_id)

    def _credentials(self, route: ProviderRoute) -> tuple[str, ...]:
        if not route.credential_env:
            return ()
        values = []
        primary = self._env.get(route.credential_env, "").strip()
        if primary:
            values.append(primary)
        prefix = f"{route.credential_env}_"
        indexed = []
        for name, value in self._env.items():
            if name.startswith(prefix) and name[len(prefix):].isdigit() and value.strip():
                indexed.append((int(name[len(prefix):]), value.strip()))
        values.extend(value for _, value in sorted(indexed))
        return tuple(dict.fromkeys(values))

    def _models(self, route: ProviderRoute) -> tuple[str, ...]:
        if not route.model_env:
            return ()
        values = []
        primary = self._env.get(route.model_env, "").strip()
        if primary:
            values.append(primary)
        plural = self._env.get(f"{route.model_env}S", "")
        if plural:
            values.extend(item.strip() for item in plural.split(",") if item.strip())
        return tuple(dict.fromkeys(values))

    def configured_cloud_providers(self) -> tuple[str, ...]:
        return tuple(route.provider_id for route in self._cloud if self._configured(route))

    def admitted_cloud_providers(self) -> tuple[str, ...]:
        """Return only cloud providers backed by fresh current qualification evidence."""
        return tuple(
            route.provider_id
            for route in self._cloud
            if self._configured(route) and self._admitted(route)
        )

    def _admitted(self, route: ProviderRoute) -> bool:
        """Fail closed unless the route is a built-in baseline or has fresh qualification evidence."""
        # Ollama is the bounded built-in local baseline used by Astra's direct local executor.
        # Every other route, including local gateways/harnesses, requires fresh qualification evidence.
        if route.provider_id == "ollama":
            return True
        evidence_path = self._env.get(
            "MEDIAHUB_PROVIDER_EVIDENCE_FILE", "evidence/provider-model.json"
        ).strip()
        expected_commit = self._env.get(
            "MEDIAHUB_RELEASE_COMMIT", self._env.get("GITHUB_SHA", "")
        ).strip()
        if not evidence_path or not expected_commit:
            return False
        try:
            with open(evidence_path, "r", encoding="utf-8") as handle:
                evidence = json.load(handle)
            timestamp = evidence.get("timestamp")
            evidence_commit = str(evidence.get("commit", "")).strip()
            if not timestamp or evidence_commit != expected_commit:
                return False
            from datetime import datetime, timedelta, timezone
            captured_at = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if captured_at.tzinfo is None:
                captured_at = captured_at.replace(tzinfo=timezone.utc)
            max_age_hours = float(
                self._env.get("MEDIAHUB_PROVIDER_EVIDENCE_MAX_AGE_HOURS", "6")
            )
            if max_age_hours <= 0 or datetime.now(timezone.utc) - captured_at > timedelta(hours=max_age_hours):
                return False
            provider = evidence.get("providers", {}).get(route.provider_id, {})
            return (
                provider.get("catalog_status") == "PASS"
                and provider.get("inference_status") == "PASS"
                and provider.get("qualification_status") == "QUALIFIED"
            )
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return False

    def _configured(self, route: ProviderRoute) -> bool:
        if route.credential_env is None:
            return True
        for env_name in route.credential_env.split("|"):
            if self._env.get(env_name, "").strip():
                return True
            prefix = f"{env_name}_"
            if any(
                name.startswith(prefix)
                and name[len(prefix):].isdigit()
                and value.strip()
                for name, value in self._env.items()
            ):
                return True
        return False

    def _model(self, route: ProviderRoute) -> str | None:
        if route.model_env:
            value = self._env.get(route.model_env)
            if value and value.strip():
                return value.strip()
        return None
