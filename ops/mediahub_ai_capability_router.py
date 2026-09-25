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
    FCM = "fcm"
    OMNIROUTE = "omniroute"
    LOCAL_QWEN = "local-qwen"


@dataclass(frozen=True)
class AICapability:
    provider: AIProvider
    tasks: frozenset[str]
    requires_external_credential: bool = False


ALL_GEMINI_TASKS = frozenset(kind.value for kind in GeminiTaskKind)

CAPABILITIES = (
    AICapability(AIProvider.GEMINI, ALL_GEMINI_TASKS, True),
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
