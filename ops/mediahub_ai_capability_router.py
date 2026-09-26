"""Deterministic AI capability routing for Astra.

Policy/selection only: never executes model output, reads secret values, or
grants repository/production authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from ops.mediahub_gemini_task_policy import GeminiTaskKind, capability_for


class AIProvider(StrEnum):
    GEMINI = "gemini"
    OPENROUTER = "openrouter"
    FCM = "fcm"
    OMNIROUTE = "omniroute"
    LOCAL_QWEN = "local-qwen"
    OTHER_CLOUD = "other-cloud"


@dataclass(frozen=True)
class AICapability:
    provider: AIProvider
    tasks: frozenset[str]
    requires_external_credential: bool = False


ALL_GEMINI_TASKS = frozenset(kind.value for kind in GeminiTaskKind)

CAPABILITIES = (
    # Gemini is a specialist lane: only tasks explicitly qualified for Gemini
    # are assigned here. Credentials are supplied by GitHub Actions, never by
    # MediaHub hosts.
    AICapability(AIProvider.GEMINI, frozenset({
        "code_review", "bug_analysis", "architecture", "security_review",
        "test_design", "test_failure_analysis", "documentation",
        "incident_analysis", "recovery_analysis", "performance_analysis",
        "dependency_analysis", "release_evidence",
    }), True),
    # The local-development lane is ordered separately; these providers are
    # not fallbacks for Gemini and must never receive a Gemini task implicitly.
    AICapability(AIProvider.OPENROUTER, frozenset({
        "code_generation", "refactoring", "bug_analysis", "test_failure_analysis",
        "code_review", "test_design",
    }), True),
    AICapability(AIProvider.FCM, frozenset({
        "code_generation", "refactoring", "bug_analysis", "test_failure_analysis",
    })),
    AICapability(AIProvider.OMNIROUTE, frozenset({
        "code_generation", "refactoring", "bug_analysis", "test_failure_analysis",
        "code_review", "architecture", "security_review", "test_design",
    })),
    AICapability(AIProvider.LOCAL_QWEN, frozenset({
        "code_generation", "refactoring", "bug_analysis", "test_failure_analysis",
        "documentation", "test_design",
    })),
)


def qualify_gemini(kind: GeminiTaskKind | str) -> bool:
    capability_for(kind)
    return True


def providers_for(kind: GeminiTaskKind | str, *, healthy: frozenset[AIProvider]) -> tuple[AIProvider, ...]:
    normalized = kind.value if isinstance(kind, GeminiTaskKind) else GeminiTaskKind(kind).value
    return tuple(
        capability.provider
        for capability in CAPABILITIES
        if normalized in capability.tasks and capability.provider in healthy
    )


def routing_lanes(kind: GeminiTaskKind | str, *, healthy: frozenset[AIProvider]) -> tuple[tuple[AIProvider, ...], ...]:
    """Return the eligible lane(s) for this task class.

    Parallelism is across independent tasks, not duplicate execution of one
    task. Gemini specialist work therefore stays in the Gemini lane. Local
    development work uses the ordered OpenRouter -> FCM -> OmniRoute -> local
    degradation chain. Other qualified cloud specialists are separate lanes.
    """
    normalized = kind.value if isinstance(kind, GeminiTaskKind) else GeminiTaskKind(kind).value
    if normalized in CAPABILITIES[0].tasks:
        return ((AIProvider.GEMINI,),) if AIProvider.GEMINI in healthy else ()
    local = tuple(p for p in (
        AIProvider.OPENROUTER, AIProvider.FCM, AIProvider.OMNIROUTE, AIProvider.LOCAL_QWEN
    ) if p in healthy and any(normalized in c.tasks and c.provider is p for c in CAPABILITIES))
    if local:
        return (local,)
    return ((AIProvider.OTHER_CLOUD,),) if AIProvider.OTHER_CLOUD in healthy else ()
