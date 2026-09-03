"""P0-08 bounded plugin resource controls.

Resource controls are transient, local enforcement primitives. They do not grant
authorization, do not expose OS authority, and do not persist accounting state.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from enum import Enum
from threading import BoundedSemaphore, Lock
from time import monotonic
from typing import Any


class ResourceLimitError(ValueError):
    """Raised when a resource limit is malformed or exceeded."""


class ResourceClass(str, Enum):
    MESSAGE = "message"
    STRUCTURE = "structure"
    CONCURRENCY = "concurrency"
    RATE = "rate"
    EXECUTION = "execution"
    MEMORY = "memory"
    OUTPUT = "output"
    LIFECYCLE = "lifecycle"


@dataclass(frozen=True)
class ResourceLimits:
    """Immutable, bounded resource limits.

    MEMORY is declarative in v1; this module does not claim OS-level memory
    enforcement. CPU is intentionally represented by the execution budget.
    """

    max_message_bytes: int = 256 * 1024
    max_structure_depth: int = 8
    max_structure_nodes: int = 512
    max_concurrent_requests: int = 1
    rate_limit_count: int = 60
    rate_window_seconds: float = 60.0
    execution_timeout_seconds: float = 30.0
    max_output_bytes: int = 256 * 1024

    def __post_init__(self) -> None:
        integer_fields = (
            "max_message_bytes",
            "max_structure_depth",
            "max_structure_nodes",
            "max_concurrent_requests",
            "rate_limit_count",
            "max_output_bytes",
        )
        for name in integer_fields:
            value = getattr(self, name)
            if type(value) is not int or value <= 0:
                raise ResourceLimitError(f"invalid {name}")
        float_fields = ("rate_window_seconds", "execution_timeout_seconds")
        for name in float_fields:
            value = getattr(self, name)
            if type(value) is not float or value <= 0.0:
                raise ResourceLimitError(f"invalid {name}")
        if self.max_message_bytes > 256 * 1024:
            raise ResourceLimitError("max_message_bytes exceeds hard bound")
        if self.max_structure_depth > 8 or self.max_structure_nodes > 512:
            raise ResourceLimitError("structure limit exceeds hard bound")
        if self.max_concurrent_requests > 128:
            raise ResourceLimitError("concurrency limit exceeds hard bound")
        if self.rate_limit_count > 4096 or self.rate_window_seconds > 3600.0:
            raise ResourceLimitError("rate limit exceeds hard bound")
        if self.execution_timeout_seconds > 300.0:
            raise ResourceLimitError("execution timeout exceeds hard bound")
        if self.max_output_bytes > 256 * 1024:
            raise ResourceLimitError("max_output_bytes exceeds hard bound")


@dataclass(frozen=True)
class ExecutionDeadline:
    """Monotonic deadline for bounded work; it executes nothing itself."""

    deadline: float

    @classmethod
    def start(cls, timeout_seconds: float) -> "ExecutionDeadline":
        if type(timeout_seconds) is not float or timeout_seconds <= 0.0:
            raise ResourceLimitError("invalid execution timeout")
        return cls(monotonic() + timeout_seconds)

    def expired(self) -> bool:
        return monotonic() >= self.deadline

    def remaining_seconds(self) -> float:
        return max(0.0, self.deadline - monotonic())


class ConcurrencyGuard:
    """Bounded in-memory concurrency guard with no unbounded queue."""

    def __init__(self, limit: int) -> None:
        if type(limit) is not int or limit <= 0 or limit > 128:
            raise ResourceLimitError("invalid concurrency limit")
        self._semaphore = BoundedSemaphore(limit)

    def acquire(self) -> bool:
        return self._semaphore.acquire(blocking=False)

    def release(self) -> None:
        try:
            self._semaphore.release()
        except ValueError as exc:
            raise ResourceLimitError("concurrency release without acquisition") from exc


class RateLimiter:
    """Bounded sliding-window limiter using transient monotonic timestamps."""

    def __init__(self, count: int, window_seconds: float) -> None:
        if type(count) is not int or count <= 0 or count > 4096:
            raise ResourceLimitError("invalid rate count")
        if type(window_seconds) is not float or window_seconds <= 0.0 or window_seconds > 3600.0:
            raise ResourceLimitError("invalid rate window")
        self._count = count
        self._window = window_seconds
        self._events: deque[float] = deque(maxlen=count)
        self._lock = Lock()

    def allow(self) -> bool:
        now = monotonic()
        with self._lock:
            cutoff = now - self._window
            while self._events and self._events[0] <= cutoff:
                self._events.popleft()
            if len(self._events) >= self._count:
                return False
            self._events.append(now)
            return True


def bounded_value_size(value: Any, *, max_depth: int, max_nodes: int, max_string_bytes: int = 4096) -> int:
    """Return a deterministic bounded byte estimate, rejecting oversized structure."""

    if type(max_depth) is not int or max_depth <= 0:
        raise ResourceLimitError("invalid max_depth")
    if type(max_nodes) is not int or max_nodes <= 0:
        raise ResourceLimitError("invalid max_nodes")
    nodes = 0

    def visit(item: Any, depth: int) -> int:
        nonlocal nodes
        nodes += 1
        if nodes > max_nodes or depth > max_depth:
            raise ResourceLimitError("structure limit exceeded")
        if item is None:
            return 4
        if type(item) is bool:
            return 5
        if type(item) is int:
            return len(str(item))
        if type(item) is float:
            if item != item or item in (float("inf"), float("-inf")):
                raise ResourceLimitError("non-finite numeric value")
            return len(repr(item))
        if type(item) is str:
            size = len(item.encode("utf-8"))
            if size > max_string_bytes:
                raise ResourceLimitError("string size limit exceeded")
            return size
        if type(item) in (bytes, bytearray):
            return len(item)
        if type(item) in (list, tuple):
            return sum(visit(child, depth + 1) for child in item)
        if type(item) is dict:
            total = 0
            for key, child in item.items():
                if type(key) is not str or len(key.encode("utf-8")) > 128:
                    raise ResourceLimitError("object key limit exceeded")
                total += len(key.encode("utf-8")) + visit(child, depth + 1)
            return total
        raise ResourceLimitError("unsupported value type")

    return visit(value, 0)


class OutputLimiter:
    """Checks output against the same bounded structure model used by the boundary."""

    def __init__(self, max_output_bytes: int) -> None:
        if type(max_output_bytes) is not int or max_output_bytes <= 0 or max_output_bytes > 256 * 1024:
            raise ResourceLimitError("invalid output limit")
        self._max_output_bytes = max_output_bytes

    def check(self, value: Any) -> int:
        size = bounded_value_size(value, max_depth=8, max_nodes=512)
        if size > self._max_output_bytes:
            raise ResourceLimitError("output limit exceeded")
        return size
