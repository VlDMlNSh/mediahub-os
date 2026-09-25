"""Native bounded retry and circuit-resilience primitives.

Prior art informs behavior, but this module is dependency-free and MediaHub-owned.
"""
from __future__ import annotations

from dataclasses import dataclass
from random import Random

from ops.mediahub_provider_gateway import FailureClass, ProviderGateway


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 2
    base_delay_seconds: float = 0.25
    max_delay_seconds: float = 4.0
    jitter_ratio: float = 0.0

    def __post_init__(self) -> None:
        if not isinstance(self.max_attempts, int) or isinstance(self.max_attempts, bool):
            raise ValueError("max_attempts must be an integer")  # noqa: TRY004
        if not isinstance(self.base_delay_seconds, (int, float)) or isinstance(self.base_delay_seconds, bool):
            raise ValueError("base_delay_seconds must be numeric")  # noqa: TRY004
        if not isinstance(self.max_delay_seconds, (int, float)) or isinstance(self.max_delay_seconds, bool):
            raise ValueError("max_delay_seconds must be numeric")  # noqa: TRY004
        if not isinstance(self.jitter_ratio, (int, float)) or isinstance(self.jitter_ratio, bool):
            raise ValueError("jitter_ratio must be numeric")  # noqa: TRY004
        if self.max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        if not 0 <= self.base_delay_seconds <= self.max_delay_seconds:
            raise ValueError("invalid retry delay bounds")
        if not 0 <= self.jitter_ratio <= 1:
            raise ValueError("jitter_ratio must be between 0 and 1")

    def delay(self, attempt: int, *, retry_after: float | None = None, rng: Random | None = None) -> float:
        if attempt < 1:
            raise ValueError("attempt must be >= 1")
        if retry_after is not None:
            return max(0.0, min(retry_after, self.max_delay_seconds))
        raw = min(self.base_delay_seconds * (2 ** (attempt - 1)), self.max_delay_seconds)
        if self.jitter_ratio == 0:
            return raw
        source = rng or Random(0)  # nosec B311 — deterministic non-cryptographic retry jitter only.
        return raw * (1 - self.jitter_ratio * source.random())


@dataclass(frozen=True)
class ResilienceDecision:
    provider: str | None
    failure: FailureClass | None
    retry: bool
    attempt: int
    delay_seconds: float
    reason: str


class ResilienceEngine:
    """Combines deterministic provider failover with a strict attempt budget."""

    def __init__(self, gateway: ProviderGateway, policy: RetryPolicy | None = None) -> None:
        self.gateway = gateway
        self.policy = policy if policy is not None else RetryPolicy()

    def first(
        self, *, excluded: frozenset[str] = frozenset(), now: float | None = None
    ) -> ResilienceDecision:
        decision = self.gateway.choose(excluded=excluded, now=now)
        return ResilienceDecision(decision.provider, None, False, 1, 0.0, decision.reason)

    def after_failure(
        self,
        provider: str,
        status: int | None,
        message: str = "",
        *,
        attempt: int,
        retry_after: float | None = None,
        excluded: frozenset[str] = frozenset(),
        now: float | None = None,
    ) -> ResilienceDecision:
        if attempt >= self.policy.max_attempts:
            failure = self.gateway.classify(status, message)
            self.gateway.record(provider, failure, now)
            return ResilienceDecision(None, failure, False, attempt, 0.0, "retry budget exhausted")
        decision = self.gateway.failover(provider, status, message, excluded=excluded)
        if decision.provider is None:
            return ResilienceDecision(None, decision.failure, False, attempt, 0.0, decision.reason)
        if decision.failure is FailureClass.PERMANENT:
            return ResilienceDecision(None, decision.failure, False, attempt, 0.0, decision.reason)
        delay = self.policy.delay(attempt, retry_after=retry_after)
        return ResilienceDecision(decision.provider, decision.failure, decision.retry, attempt + 1, delay, decision.reason)
