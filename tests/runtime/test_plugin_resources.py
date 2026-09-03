import time

import pytest

from mediahub_runtime.plugin_resources import (
    ConcurrencyGuard,
    ExecutionDeadline,
    OutputLimiter,
    RateLimiter,
    ResourceLimitError,
    ResourceLimits,
    bounded_value_size,
)


def test_resource_limits_are_immutable_and_bounded() -> None:
    limits = ResourceLimits()
    assert limits.max_message_bytes == 256 * 1024
    with pytest.raises((AttributeError, TypeError)):
        limits.max_message_bytes = 1  # type: ignore[misc]
    with pytest.raises(ResourceLimitError):
        ResourceLimits(max_concurrent_requests=129)
    with pytest.raises(ResourceLimitError):
        ResourceLimits(max_message_bytes=256 * 1024 + 1)


def test_concurrency_guard_has_no_unbounded_queue() -> None:
    guard = ConcurrencyGuard(1)
    assert guard.acquire() is True
    assert guard.acquire() is False
    guard.release()
    assert guard.acquire() is True
    guard.release()


def test_concurrency_release_without_acquisition_fails_closed() -> None:
    guard = ConcurrencyGuard(1)
    with pytest.raises(ResourceLimitError):
        guard.release()


def test_rate_limiter_denies_after_bound() -> None:
    limiter = RateLimiter(2, 60.0)
    assert limiter.allow() is True
    assert limiter.allow() is True
    assert limiter.allow() is False


def test_rate_limiter_window_expires() -> None:
    limiter = RateLimiter(1, 0.01)
    assert limiter.allow() is True
    assert limiter.allow() is False
    time.sleep(0.02)
    assert limiter.allow() is True


def test_execution_deadline_is_bounded_and_monotonic() -> None:
    deadline = ExecutionDeadline.start(0.01)
    assert deadline.remaining_seconds() > 0.0
    assert deadline.expired() is False
    time.sleep(0.02)
    assert deadline.expired() is True
    assert deadline.remaining_seconds() == 0.0


def test_output_limiter_rejects_oversized_output() -> None:
    limiter = OutputLimiter(16)
    assert limiter.check({"ok": "yes"}) <= 16
    with pytest.raises(ResourceLimitError):
        limiter.check("x" * 17)


def test_structure_limits_reject_depth_and_node_exhaustion() -> None:
    with pytest.raises(ResourceLimitError):
        bounded_value_size([[[[1]]]], max_depth=2, max_nodes=32)
    with pytest.raises(ResourceLimitError):
        bounded_value_size([1, 2, 3], max_depth=8, max_nodes=2)


def test_structure_limits_reject_non_finite_values() -> None:
    with pytest.raises(ResourceLimitError):
        bounded_value_size(float("inf"), max_depth=8, max_nodes=32)


def test_structure_limits_reject_unsupported_values() -> None:
    with pytest.raises(ResourceLimitError):
        bounded_value_size(object(), max_depth=8, max_nodes=32)
