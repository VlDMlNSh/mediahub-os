"""Bounded autonomous task lifecycle for the existing MediaHub Control Plane."""
from __future__ import annotations

import hashlib
import time
from dataclasses import dataclass
from typing import Callable, Generic, TypeVar

T = TypeVar("T")
P = TypeVar("P")


class AutonomousTaskError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class AutonomousTaskPolicy:
    max_attempts: int = 3
    max_repairs: int = 2
    max_duration_seconds: float = 120.0
    max_evidence_bytes: int = 4096

    def validate(self) -> None:
        if not 1 <= self.max_attempts <= 8:
            raise AutonomousTaskError("invalid_max_attempts")
        if not 0 <= self.max_repairs < self.max_attempts:
            raise AutonomousTaskError("invalid_max_repairs")
        if not 0 < self.max_duration_seconds <= 900:
            raise AutonomousTaskError("invalid_max_duration")
        if not 256 <= self.max_evidence_bytes <= 65536:
            raise AutonomousTaskError("invalid_evidence_limit")


@dataclass(frozen=True)
class AutonomousEvidence:
    attempt: int
    phase: str
    status: str
    detail_sha256: str
    detail_bytes: int


@dataclass(frozen=True)
class AutonomousTaskResult(Generic[T]):
    status: str
    attempts: int
    repairs: int
    result: T | None
    evidence: tuple[AutonomousEvidence, ...]


class BoundedAutonomousTask(Generic[T, P]):
    """Run Plan -> Execute -> Verify -> bounded Repair without hidden retries."""

    def __init__(
        self,
        plan: Callable[[], P],
        execute: Callable[[P, int], T],
        verify: Callable[[T, int], tuple[bool, str]],
        repair: Callable[[P, T, int], P] | None = None,
        policy: AutonomousTaskPolicy = AutonomousTaskPolicy(),
        clock: Callable[[], float] = time.monotonic,
    ):
        self._plan = plan
        self._execute = execute
        self._verify = verify
        self._repair = repair
        self._policy = policy
        self._clock = clock
        policy.validate()

    def run(self) -> AutonomousTaskResult[T]:
        started = self._clock()
        evidence: list[AutonomousEvidence] = []
        repairs = 0
        try:
            plan = self._plan()
        except Exception as exc:
            self._record(evidence, 0, "plan", "failed", type(exc).__name__)
            return AutonomousTaskResult("FAILED", 0, 0, None, tuple(evidence))
        self._record(evidence, 0, "plan", "completed", "plan_ready")

        last_result: T | None = None
        for attempt in range(1, self._policy.max_attempts + 1):
            if self._expired(started):
                self._record(evidence, attempt, "execute", "timeout", "deadline_exceeded")
                return AutonomousTaskResult("REPAIR_EXHAUSTED", attempt - 1, repairs, None, tuple(evidence))
            try:
                last_result = self._execute(plan, attempt)
                self._record(evidence, attempt, "execute", "completed", "result_ready")
            except TimeoutError as exc:
                self._record(evidence, attempt, "execute", "timeout", type(exc).__name__)
                return AutonomousTaskResult("REPAIR_EXHAUSTED", attempt, repairs, None, tuple(evidence))
            except Exception as exc:
                self._record(evidence, attempt, "execute", "failed", type(exc).__name__)
                if not self._can_repair(attempt, repairs, started):
                    return AutonomousTaskResult("FAILED", attempt, repairs, None, tuple(evidence))
                plan, repairs = self._do_repair(plan, last_result, attempt, repairs, evidence)
                continue

            try:
                valid, detail = self._verify(last_result, attempt)
            except Exception as exc:
                valid, detail = False, type(exc).__name__
            self._record(evidence, attempt, "verify", "passed" if valid else "failed", detail)
            if valid:
                return AutonomousTaskResult("PASS", attempt, repairs, last_result, tuple(evidence))
            if not self._can_repair(attempt, repairs, started):
                return AutonomousTaskResult("REPAIR_EXHAUSTED", attempt, repairs, None, tuple(evidence))
            plan, repairs = self._do_repair(plan, last_result, attempt, repairs, evidence)

        return AutonomousTaskResult("REPAIR_EXHAUSTED", self._policy.max_attempts, repairs, None, tuple(evidence))

    def _can_repair(self, attempt: int, repairs: int, started: float) -> bool:
        return (
            self._repair is not None
            and repairs < self._policy.max_repairs
            and attempt < self._policy.max_attempts
            and not self._expired(started)
        )

    def _do_repair(self, plan, result, attempt, repairs, evidence):
        try:
            next_plan = self._repair(plan, result, attempt)
        except Exception as exc:
            self._record(evidence, attempt, "repair", "failed", type(exc).__name__)
            return plan, self._policy.max_repairs
        self._record(evidence, attempt, "repair", "completed", "repair_ready")
        return next_plan, repairs + 1

    def _expired(self, started: float) -> bool:
        return self._clock() - started >= self._policy.max_duration_seconds

    def _record(self, evidence, attempt, phase, status, detail):
        raw = str(detail).encode("utf-8", errors="replace")
        if len(raw) > self._policy.max_evidence_bytes:
            raw = raw[: self._policy.max_evidence_bytes]
        evidence.append(AutonomousEvidence(
            attempt, phase, status, hashlib.sha256(raw).hexdigest(), len(raw)
        ))
