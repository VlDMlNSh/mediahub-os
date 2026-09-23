"""Cloud-first multi-provider orchestrator for MediaHub OS.

The orchestrator is a routing/control component, not an authority layer.
MediaHub Codex remains policy authority; the Gateway remains the delegation
boundary; provider adapters execute only after admission. Local providers are
extensions and are selected when a cloud route is unavailable or unsuitable.
No credentials are stored in this module or repository.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Callable, Mapping


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
    ProviderRoute("openrouter", "cloud", frozenset({"reasoning", "analysis", "coding", "architecture", "review", "research", "web", "multimodal", "documents", "long_context", "bulk", "repository", "testing", "transform", "classify"}), "OPENROUTER_API_KEY", "MEDIAHUB_OPENROUTER_MODEL", 5),
    ProviderRoute("openai", "cloud", frozenset({"reasoning", "analysis", "coding"}), "OPENAI_API_KEY", "MEDIAHUB_OPENAI_MODEL", 10),
    ProviderRoute("claude", "cloud", frozenset({"coding", "architecture", "review", "reasoning"}), "ANTHROPIC_API_KEY", "MEDIAHUB_CLAUDE_MODEL", 20),
    ProviderRoute("gemini", "cloud", frozenset({"multimodal", "documents", "reasoning"}), "GEMINI_API_KEY", "MEDIAHUB_GEMINI_MODEL", 30),
    ProviderRoute("perplexity", "cloud", frozenset({"research", "web"}), "PERPLEXITY_API_KEY", "MEDIAHUB_PERPLEXITY_MODEL", 40),
    ProviderRoute("kimi", "cloud", frozenset({"reasoning", "long_context"}), "KIMI_API_KEY", "MEDIAHUB_KIMI_MODEL", 50),
    ProviderRoute("deepseek", "cloud", frozenset({"coding", "reasoning", "bulk"}), "DEEPSEEK_API_KEY", "MEDIAHUB_DEEPSEEK_MODEL", 60),
    ProviderRoute("cursor", "cloud", frozenset({"repository", "coding", "testing"}), "CURSOR_API_KEY", "MEDIAHUB_CURSOR_MODEL", 70),
    ProviderRoute("chatgpt", "cloud", frozenset({"reasoning", "analysis"}), "CHATGPT_API_KEY", "MEDIAHUB_CHATGPT_MODEL", 80),
)

DEFAULT_LOCAL_ROUTES = (
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
        self._cloud = tuple(sorted(cloud_routes, key=lambda r: r.priority))
        self._local = tuple(sorted(local_routes, key=lambda r: r.priority))
        self._env = dict(credential_env or os.environ)
        self._executors = dict(executors or {})

    def decide(self, capability: str, *, allow_local_extension: bool = True) -> OrchestrationDecision:
        if not isinstance(capability, str) or not capability.strip():
            raise CloudOrchestratorError("invalid_capability")

        for route in self._cloud:
            if capability in route.capabilities and self._configured(route):
                return OrchestrationDecision(
                    route.provider_id,
                    route.tier,
                    self._model(route),
                    "cloud_provider_configured",
                )

        if allow_local_extension:
            for route in self._local:
                if capability in route.capabilities:
                    return OrchestrationDecision(
                        route.provider_id,
                        route.tier,
                        self._model(route),
                        "cloud_unavailable_local_extension",
                    )

        raise CloudOrchestratorError("no_provider_available")

    def execute(self, capability: str, prompt: str, *, allow_local_extension: bool = True) -> tuple[OrchestrationDecision, str]:
        if not isinstance(prompt, str) or not prompt:
            raise CloudOrchestratorError("invalid_prompt")
        decision = self.decide(capability, allow_local_extension=allow_local_extension)
        executor = self._executors.get(decision.provider_id)
        if executor is None:
            raise CloudOrchestratorError("provider_adapter_unavailable")
        try:
            output = executor(prompt)
        except Exception as exc:
            raise CloudOrchestratorError("provider_execution_failed") from exc
        if not isinstance(output, str) or not output:
            raise CloudOrchestratorError("empty_provider_result")
        return decision, output

    def configured_cloud_providers(self) -> tuple[str, ...]:
        return tuple(route.provider_id for route in self._cloud if self._configured(route))

    def _configured(self, route: ProviderRoute) -> bool:
        if route.credential_env is None:
            return True
        value = self._env.get(route.credential_env)
        return bool(value and value.strip())

    def _model(self, route: ProviderRoute) -> str | None:
        if route.model_env:
            value = self._env.get(route.model_env)
            if value and value.strip():
                return value.strip()
        return None
