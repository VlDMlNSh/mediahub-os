"""Evidence-backed catalog of external free development model candidates.

This catalog is discovery metadata only. A model remains non-routable until
live qualification records it in ModelRegistry. Pricing labels distinguish
perpetual/free-tier access from introductory or daily free allocations.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class FreeTier(str, Enum):
    PERPETUAL = "perpetual"
    DAILY_ALLOCATION = "daily-allocation"
    INTRODUCTORY = "introductory"
    UNQUALIFIED = "unqualified"


@dataclass(frozen=True)
class FreeModelCandidate:
    provider: str
    model: str
    free_tier: FreeTier
    protocol: str
    endpoint: str
    credential_env: str
    development_role: str
    source: str


# Only models/provider programs with current public evidence are listed here.
# This is deliberately broader than the runtime registry and is not a routing list.
FREE_MODEL_CANDIDATES: tuple[FreeModelCandidate, ...] = (
    FreeModelCandidate(
        "google-gemini", "gemini-2.5-flash", FreeTier.PERPETUAL,
        "gemini.generateContent", "https://generativelanguage.googleapis.com/v1beta",
        "GEMINI_API_KEY", "primary-cloud-code", "ai.google.dev",
    ),
    FreeModelCandidate(
        "google-gemini", "gemini-2.5-flash-lite", FreeTier.PERPETUAL,
        "gemini.generateContent", "https://generativelanguage.googleapis.com/v1beta",
        "GEMINI_API_KEY", "fast-cloud-code", "ai.google.dev",
    ),
    FreeModelCandidate(
        "cerebras", "llama3.1-8b", FreeTier.PERPETUAL,
        "openai.chat.completions", "https://api.cerebras.ai/v1",
        "CEREBRAS_API_KEY", "fast-code", "inference-docs.cerebras.ai",
    ),
    FreeModelCandidate(
        "cerebras", "gpt-oss-120b", FreeTier.PERPETUAL,
        "openai.chat.completions", "https://api.cerebras.ai/v1",
        "CEREBRAS_API_KEY", "frontier-code", "inference-docs.cerebras.ai",
    ),
    FreeModelCandidate(
        "sambanova", "DeepSeek-R1-0528", FreeTier.PERPETUAL,
        "openai.chat.completions", "https://api.sambanova.ai/v1",
        "SAMBANOVA_API_KEY", "reasoning", "docs.sambanova.ai",
    ),
    FreeModelCandidate(
        "sambanova", "Deepseek-V3.1", FreeTier.PERPETUAL,
        "openai.chat.completions", "https://api.sambanova.ai/v1",
        "SAMBANOVA_API_KEY", "code", "docs.sambanova.ai",
    ),
    FreeModelCandidate(
        "cloudflare-workers-ai", "@cf/zai-org/glm-4.7-flash", FreeTier.DAILY_ALLOCATION,
        "cloudflare.ai.run", "https://api.cloudflare.com/client/v4",
        "CLOUDFLARE_API_TOKEN", "fast-code", "developers.cloudflare.com",
    ),
    FreeModelCandidate(
        "cloudflare-workers-ai", "@cf/google/gemma-4-26b-a4b-it", FreeTier.DAILY_ALLOCATION,
        "cloudflare.ai.run", "https://api.cloudflare.com/client/v4",
        "CLOUDFLARE_API_TOKEN", "general-code", "developers.cloudflare.com",
    ),
    FreeModelCandidate(
        "cloudflare-workers-ai", "@cf/nvidia/nemotron-3-120b-a12b", FreeTier.DAILY_ALLOCATION,
        "cloudflare.ai.run", "https://api.cloudflare.com/client/v4",
        "CLOUDFLARE_API_TOKEN", "reasoning-code", "developers.cloudflare.com",
    ),
    FreeModelCandidate(
        "scaleway-generative-api", "qwen3.5-397b-a17b", FreeTier.INTRODUCTORY,
        "openai.chat.completions", "https://api.scaleway.ai/v1",
        "SCW_SECRET_KEY", "frontier-code", "scaleway.com",
    ),
    FreeModelCandidate(
        "scaleway-generative-api", "qwen3.6-35b-a3b", FreeTier.INTRODUCTORY,
        "openai.chat.completions", "https://api.scaleway.ai/v1",
        "SCW_SECRET_KEY", "efficient-code", "scaleway.com",
    ),
    FreeModelCandidate(
        "mistral", "mistral-small-latest", FreeTier.PERPETUAL,
        "openai.chat.completions", "https://api.mistral.ai/v1",
        "MISTRAL_API_KEY", "general-code", "docs.mistral.ai",
    ),
)


def candidates(provider: str | None = None) -> tuple[FreeModelCandidate, ...]:
    if provider is None:
        return FREE_MODEL_CANDIDATES
    return tuple(item for item in FREE_MODEL_CANDIDATES if item.provider == provider)


def providers() -> tuple[str, ...]:
    return tuple(sorted({item.provider for item in FREE_MODEL_CANDIDATES}))
