"""Bounded Gemini task capability policy.

Gemini is an advisory development agent. This module declares task classes it
can cover; it never grants merge, release, production, secret, or State
Authority permissions and never executes model output.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class GeminiTaskKind(StrEnum):
    CODE_REVIEW = "code_review"
    BUG_ANALYSIS = "bug_analysis"
    ARCHITECTURE = "architecture"
    SECURITY_REVIEW = "security_review"
    TEST_DESIGN = "test_design"
    TEST_FAILURE_ANALYSIS = "test_failure_analysis"
    CODE_GENERATION = "code_generation"
    REFACTORING = "refactoring"
    DOCUMENTATION = "documentation"
    INCIDENT_ANALYSIS = "incident_analysis"
    RECOVERY_ANALYSIS = "recovery_analysis"
    PERFORMANCE_ANALYSIS = "performance_analysis"
    DEPENDENCY_ANALYSIS = "dependency_analysis"
    RELEASE_EVIDENCE = "release_evidence"


@dataclass(frozen=True)
class GeminiTaskCapability:
    kind: GeminiTaskKind
    operation: str
    mutates_repository: bool = False
    requires_human_gate: bool = False


CAPABILITIES: tuple[GeminiTaskCapability, ...] = tuple(
    GeminiTaskCapability(kind, "generateContent", kind in {
        GeminiTaskKind.CODE_GENERATION,
        GeminiTaskKind.REFACTORING,
    })
    for kind in GeminiTaskKind
)


def capability_for(kind: GeminiTaskKind | str) -> GeminiTaskCapability:
    try:
        normalized = kind if isinstance(kind, GeminiTaskKind) else GeminiTaskKind(kind)
    except ValueError as exc:
        raise PermissionError(f"Gemini task kind is not qualified: {kind}") from exc
    return next(capability for capability in CAPABILITIES if capability.kind is normalized)


def execution_authority(kind: GeminiTaskKind | str) -> str:
    """Return the only allowed authority class for a Gemini task."""
    capability_for(kind)
    return "advisory-proposal-only"
