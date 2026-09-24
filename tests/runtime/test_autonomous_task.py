import pytest

from mediahub_runtime import (
    AutonomousTaskError,
    AutonomousTaskPolicy,
    BoundedAutonomousTask,
)


def test_autonomous_task_repairs_then_passes():
    seen = []

    def execute(plan, attempt):
        seen.append((plan, attempt))
        return plan

    def verify(result, attempt):
        return result == "fixed", "verification"

    def repair(plan, result, attempt):
        return "fixed"

    result = BoundedAutonomousTask(
        plan=lambda: "broken",
        execute=execute,
        verify=verify,
        repair=repair,
    ).run()

    assert result.status == "PASS"
    assert result.attempts == 2
    assert result.repairs == 1
    assert result.result == "fixed"
    assert [item[1] for item in seen] == [1, 2]
    assert all(len(item.detail_sha256) == 64 for item in result.evidence)


def test_autonomous_task_exhausts_repair_budget():
    result = BoundedAutonomousTask(
        plan=lambda: "broken",
        execute=lambda plan, attempt: plan,
        verify=lambda result, attempt: (False, "not_ready"),
        repair=lambda plan, result, attempt: plan,
        policy=AutonomousTaskPolicy(max_attempts=3, max_repairs=2),
    ).run()

    assert result.status == "REPAIR_EXHAUSTED"
    assert result.attempts == 3
    assert result.repairs == 2
    assert result.result is None


def test_autonomous_task_plan_failure_is_terminal():
    result = BoundedAutonomousTask(
        plan=lambda: (_ for _ in ()).throw(ValueError("ignored")),
        execute=lambda plan, attempt: plan,
        verify=lambda result, attempt: (True, "ok"),
    ).run()
    assert result.status == "FAILED"
    assert result.attempts == 0


def test_autonomous_task_policy_is_bounded():
    with pytest.raises(AutonomousTaskError) as exc:
        AutonomousTaskPolicy(max_attempts=9).validate()
    assert exc.value.code == "invalid_max_attempts"


def test_autonomous_task_deadline_is_terminal():
    ticks = iter((0.0, 0.0, 2.0))

    result = BoundedAutonomousTask(
        plan=lambda: "work",
        execute=lambda plan, attempt: plan,
        verify=lambda result, attempt: (False, "not_ready"),
        repair=lambda plan, result, attempt: plan,
        policy=AutonomousTaskPolicy(max_attempts=3, max_repairs=2, max_duration_seconds=1.0),
        clock=lambda: next(ticks),
    ).run()

    assert result.status == "REPAIR_EXHAUSTED"
    assert result.attempts == 1
    assert result.repairs == 0


def test_autonomous_task_evidence_is_bounded_and_does_not_store_detail():
    secret_like = "SECRET_VALUE_" + ("x" * 10000)
    result = BoundedAutonomousTask(
        plan=lambda: "work",
        execute=lambda plan, attempt: plan,
        verify=lambda result, attempt: (False, secret_like),
        policy=AutonomousTaskPolicy(max_attempts=1, max_repairs=0, max_evidence_bytes=256),
    ).run()

    assert result.status == "REPAIR_EXHAUSTED"
    assert result.evidence[2].detail_bytes == 256
    assert secret_like not in repr(result.evidence)
    assert len(result.evidence[2].detail_sha256) == 64


def test_autonomous_task_worker_timeout_is_terminal_without_repair():
    def execute(plan, attempt):
        raise TimeoutError("worker deadline")

    result = BoundedAutonomousTask(
        plan=lambda: "work",
        execute=execute,
        verify=lambda result, attempt: (True, "ok"),
        repair=lambda plan, result, attempt: "retry",
        policy=AutonomousTaskPolicy(max_attempts=3, max_repairs=2),
    ).run()

    assert result.status == "REPAIR_EXHAUSTED"
    assert result.attempts == 1
    assert result.repairs == 0
    assert result.evidence[-1].phase == "execute"
    assert result.evidence[-1].status == "timeout"
