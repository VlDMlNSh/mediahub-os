"""Provider-plane policy and deterministic credential-gated routing.

This module is metadata/policy only. Secret values never enter provider state,
routing decisions, logs, or evidence. External credentials are expected to be
injected by a trusted execution lane.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping

class ProviderHealth(StrEnum):
    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    DOWN = "DOWN"
    UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class ProviderSpec:
    provider: str
    secret_names: tuple[str, ...]
    capabilities: frozenset[str]
    priority: int
    external: bool = True


@dataclass(frozen=True)
class ProviderDecision:
    provider: str | None
    reason: str
    candidates: tuple[str, ...]


PROVIDERS: tuple[ProviderSpec, ...] = (
    ProviderSpec("openai", ("OPENAI_API_KEY",), frozenset({"code_generation", "refactoring", "bug_analysis", "test_failure_analysis", "architecture", "test_design"}), 10),
    ProviderSpec("anthropic", ("ANTHROPIC_API_KEY",), frozenset({"code_generation", "refactoring", "bug_analysis", "test_failure_analysis", "code_review", "architecture", "security_review", "test_design"}), 20),
    ProviderSpec("gemini", ("GEMINI_API_KEY",), frozenset({"code_generation", "refactoring", "bug_analysis", "test_failure_analysis", "code_review", "architecture", "security_review", "test_design", "documentation"}), 30),
    ProviderSpec("openrouter", ("OPENROUTER_API_KEY",), frozenset({"code_generation", "refactoring", "bug_analysis", "test_failure_analysis", "code_review", "architecture", "security_review", "test_design", "documentation"}), 40),
    ProviderSpec("groq", ("GROQ_API_KEY",), frozenset({"code_generation", "bug_analysis", "test_failure_analysis"}), 50),
    ProviderSpec("together", ("TOGETHER_API_KEY",), frozenset({"code_generation", "bug_analysis", "test_failure_analysis", "documentation"}), 60),
    ProviderSpec("huggingface", ("HF_TOKEN",), frozenset({"code_generation", "bug_analysis", "documentation"}), 70),
    ProviderSpec("tabby", ("TABITOKEN_API_KEY",), frozenset({"code_generation", "indexing"}), 80, external=False),
    ProviderSpec("fcm", (), frozenset({"code_generation", "refactoring", "bug_analysis", "test_failure_analysis"}), 90, external=False),
    ProviderSpec("omniroute", (), frozenset({"code_generation", "refactoring", "bug_analysis", "test_failure_analysis", "code_review", "architecture", "security_review", "test_design"}), 100, external=False),
    ProviderSpec("local-qwen", (), frozenset({"code_generation", "refactoring", "bug_analysis", "test_failure_analysis", "documentation", "test_design"}), 110, external=False),
)

SPEC_BY_NAME = {spec.provider: spec for spec in PROVIDERS}


def secret_names(provider: str) -> tuple[str, ...]:
    """Return names only; unknown providers are denied."""
    return SPEC_BY_NAME[provider].secret_names


def credentials_present(provider: str, present_names: frozenset[str]) -> bool:
    spec = SPEC_BY_NAME[provider]
    return not spec.secret_names or all(name in present_names for name in spec.secret_names)


def choose_provider(
    capability: str,
    *,
    healthy: Mapping[str, ProviderHealth],
    credential_names: frozenset[str] = frozenset(),
    external_pr: bool = False,
) -> ProviderDecision:
    """Choose the first qualified, healthy, credential-ready provider.

    External PR work cannot enter a direct credential-bearing provider lane.
    Local/no-secret providers may still be considered when explicitly healthy.
    """
    candidates: list[str] = []
    for spec in sorted(PROVIDERS, key=lambda item: item.priority):
        if capability not in spec.capabilities:
            continue
        if healthy.get(spec.provider, ProviderHealth.UNKNOWN) is not ProviderHealth.HEALTHY:
            continue
        if external_pr and spec.external:
            continue
        if not credentials_present(spec.provider, credential_names):
            continue
        candidates.append(spec.provider)
    if candidates:
        return ProviderDecision(candidates[0], "qualified healthy provider", tuple(candidates))
    return ProviderDecision(None, "no qualified credential-safe provider", tuple())


def provider_capabilities() -> Mapping[str, frozenset[str]]:
    return {spec.provider: spec.capabilities for spec in PROVIDERS}
