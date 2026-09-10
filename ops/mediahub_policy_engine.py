"""Deterministic policy engine for autonomous development requests."""
from __future__ import annotations

from dataclasses import dataclass


class PolicyDenied(PermissionError):
    """Raised when a request violates explicit MediaHub policy."""


@dataclass(frozen=True)
class DevelopmentPolicy:
    providers: frozenset[str]
    protocols: frozenset[str]
    data_classes: frozenset[str]
    max_timeout_seconds: int = 900
    max_prompt_bytes: int = 64 * 1024


@dataclass(frozen=True)
class PolicyRequest:
    provider: str
    protocol: str
    data_class: str
    timeout_seconds: int
    prompt_bytes: int
    capabilities: frozenset[str] = frozenset()


@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str


FORBIDDEN_CAPABILITIES = frozenset({
    "production", "secrets", "state-authority", "host-filesystem"
})


class PolicyEngine:
    def __init__(self, policy: DevelopmentPolicy):
        self.policy = policy
        self.revoked = False

    def revoke(self) -> None:
        self.revoked = True

    def evaluate(self, request: PolicyRequest) -> PolicyDecision:
        if self.revoked:
            return PolicyDecision(False, "policy is revoked")
        if request.provider not in self.policy.providers:
            return PolicyDecision(False, "provider is not allowlisted")
        if request.protocol not in self.policy.protocols:
            return PolicyDecision(False, "protocol is not allowlisted")
        if request.data_class not in self.policy.data_classes:
            return PolicyDecision(False, "data class is not exportable")
        if request.capabilities & FORBIDDEN_CAPABILITIES:
            return PolicyDecision(False, "forbidden capability")
        if not 1 <= request.timeout_seconds <= self.policy.max_timeout_seconds:
            return PolicyDecision(False, "timeout is outside policy")
        if not 0 < request.prompt_bytes <= self.policy.max_prompt_bytes:
            return PolicyDecision(False, "prompt size is outside policy")
        return PolicyDecision(True, "allowed")

    def require(self, request: PolicyRequest) -> None:
        decision = self.evaluate(request)
        if not decision.allowed:
            raise PolicyDenied(decision.reason)
