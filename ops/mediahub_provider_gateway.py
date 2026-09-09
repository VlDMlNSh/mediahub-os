"""MediaHub-native multi-provider gateway primitives.

LiteLLM is used only as a reference implementation. Production routing here
is intentionally dependency-free, deterministic and fail-closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from time import monotonic


class FailureClass(StrEnum):
    SUCCESS = "SUCCESS"
    POLICY_BLOCKED = "POLICY_BLOCKED"
    TRANSIENT = "TRANSIENT"
    PERMANENT = "PERMANENT"


@dataclass(frozen=True)
class Provider:
    name: str
    base_url: str
    priority: int
    enabled: bool = True


@dataclass
class Circuit:
    failures: int = 0
    opened_at: float | None = None


@dataclass(frozen=True)
class GatewayDecision:
    provider: str | None
    failure: FailureClass | None
    retry: bool
    reason: str


class ProviderGateway:
    """Deterministic provider selection with bounded circuit state."""

    def __init__(self, providers: tuple[Provider, ...], *, threshold: int = 2,
                 cooldown_seconds: float = 60.0) -> None:
        if threshold < 1 or cooldown_seconds <= 0:
            raise ValueError("invalid circuit policy")
        self.providers = tuple(sorted(providers, key=lambda p: p.priority))
        self.threshold = threshold
        self.cooldown_seconds = cooldown_seconds
        self.circuits = {p.name: Circuit() for p in self.providers}

    @staticmethod
    def classify(status: int | None, message: str = "") -> FailureClass:
        text = message.casefold()
        if status in (401, 403) or any(x in text for x in (
            "access denied by security policy", "not authorized",
            "region not supported", "country not supported",
        )):
            return FailureClass.POLICY_BLOCKED
        if status in (408, 425, 429, 500, 502, 503, 504) or status is None:
            return FailureClass.TRANSIENT
        if 400 <= status < 500:
            return FailureClass.PERMANENT
        return FailureClass.SUCCESS

    def available(self, provider: str, now: float | None = None) -> bool:
        circuit = self.circuits[provider]
        if circuit.opened_at is None:
            return True
        current = monotonic() if now is None else now
        return current - circuit.opened_at >= self.cooldown_seconds

    def record(self, provider: str, failure: FailureClass, now: float | None = None) -> None:
        circuit = self.circuits[provider]
        if failure is FailureClass.SUCCESS:
            circuit.failures = 0
            circuit.opened_at = None
            return
        if failure is FailureClass.POLICY_BLOCKED:
            circuit.failures = self.threshold
            circuit.opened_at = monotonic() if now is None else now
            return
        if failure is FailureClass.TRANSIENT:
            circuit.failures += 1
            if circuit.failures >= self.threshold:
                circuit.opened_at = monotonic() if now is None else now

    def choose(self, *, excluded: frozenset[str] = frozenset(),
               now: float | None = None) -> GatewayDecision:
        for provider in self.providers:
            if provider.enabled and provider.name not in excluded and self.available(provider.name, now):
                return GatewayDecision(provider.name, None, False, "highest-priority available provider")
        return GatewayDecision(None, FailureClass.TRANSIENT, False, "all providers unavailable")

    def failover(self, provider: str, status: int | None, message: str = "") -> GatewayDecision:
        failure = self.classify(status, message)
        self.record(provider, failure)
        excluded = frozenset({provider})
        if failure is FailureClass.POLICY_BLOCKED:
            decision = self.choose(excluded=excluded)
            return GatewayDecision(decision.provider, failure, False, "provider policy blocked; deterministic failover")
        if failure is FailureClass.TRANSIENT:
            decision = self.choose(excluded=excluded)
            return GatewayDecision(decision.provider, failure, True, "transient failure; bounded failover")
        return GatewayDecision(None, failure, False, "permanent provider failure")
