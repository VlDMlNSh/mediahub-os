from __future__ import annotations
from dataclasses import dataclass
from .model import FailureClass

@dataclass(frozen=True, slots=True)
class RetryDecision:
    retry: bool
    delay_seconds: float
    reason: str

class RetryPolicy:
    """Explicit, deterministic retry policy; task max_attempts remains the hard budget."""
    def __init__(self, base_delay_seconds: float = 5.0, worker_multiplier: float = 2.0, infrastructure_multiplier: float = 3.0):
        if base_delay_seconds < 0 or worker_multiplier < 1 or infrastructure_multiplier < 1:
            raise ValueError("retry policy values are invalid")
        self.base_delay_seconds = base_delay_seconds
        self.worker_multiplier = worker_multiplier
        self.infrastructure_multiplier = infrastructure_multiplier

    def decide(self, failure_class: FailureClass, attempt: int, max_attempts: int) -> RetryDecision:
        if attempt <= 0 or max_attempts <= 0:
            raise ValueError("attempt and max_attempts must be positive")
        if attempt >= max_attempts:
            return RetryDecision(False, 0.0, "retry_budget_exhausted")
        multiplier = {FailureClass.TASK: 1.0, FailureClass.WORKER: self.worker_multiplier, FailureClass.INFRASTRUCTURE: self.infrastructure_multiplier}[failure_class]
        delay = self.base_delay_seconds * multiplier * (2 ** (attempt - 1))
        return RetryDecision(True, delay, f"retryable_{failure_class.value.lower()}")
