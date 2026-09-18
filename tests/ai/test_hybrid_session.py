from datetime import datetime, timedelta, timezone

import pytest

from ops.ai.hybrid_session import (
    HybridSessionController,
    SessionDenied,
    SessionJournal,
    SessionState,
)


class Clock:
    def __init__(self):
        self.value = datetime(2026, 9, 11, 12, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.value


def controller(tmp_path):
    clock = Clock()
    return HybridSessionController(SessionJournal(tmp_path / "session.jsonl"), clock), clock


def test_start_is_bounded_and_provenance_locked(tmp_path):
    ctl, clock = controller(tmp_path)
    session = ctl.start("s1", "baseline", "r4", duration=timedelta(hours=8))
    assert session.state is SessionState.RUNNING
    assert session.deadline == clock.value + timedelta(hours=8)


def test_second_active_session_is_denied(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    with pytest.raises(SessionDenied):
        ctl.start("s2", "baseline", "r4", duration=timedelta(hours=1))


def test_duration_is_arbitrary_and_only_requires_positive_finite_budget(tmp_path):
    ctl, clock = controller(tmp_path)
    session = ctl.start("s1", "baseline", "r4", duration=timedelta(days=30, minutes=17))
    assert session.deadline == clock.value + timedelta(days=30, minutes=17)


def test_duration_must_be_positive(tmp_path):
    ctl, _ = controller(tmp_path)
    with pytest.raises(SessionDenied):
        ctl.start("s1", "baseline", "r4", duration=timedelta(0))


def test_deadline_transitions_to_expired_and_blocks_new_cycle(tmp_path):
    ctl, clock = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    clock.value += timedelta(hours=1)
    state = ctl.heartbeat()
    assert state.state is SessionState.EXPIRED
    with pytest.raises(SessionDenied):
        ctl.next_cycle("continue")


def test_pause_resume_preserves_original_deadline(tmp_path):
    ctl, clock = controller(tmp_path)
    session = ctl.start("s1", "baseline", "r4", duration=timedelta(hours=8))
    deadline = session.deadline
    ctl.pause()
    clock.value += timedelta(hours=1)
    resumed = ctl.resume()
    assert resumed.state is SessionState.RUNNING
    assert resumed.deadline == deadline


def test_pause_does_not_extend_budget(tmp_path):
    ctl, clock = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    ctl.pause()
    clock.value += timedelta(hours=1)
    state = ctl.resume()
    assert state.state is SessionState.EXPIRED


def test_safe_stop_is_terminal(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    ctl.safe_stop("AI boundary violation")
    with pytest.raises(SessionDenied):
        ctl.next_cycle("continue")


def test_cycle_increments_only_after_heartbeat(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    state = ctl.next_cycle("inspect")
    assert state.cycle == 1
    state = ctl.next_cycle("test")
    assert state.cycle == 2


def test_journal_is_append_only_jsonl_with_provenance(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    ctl.next_cycle("inspect")
    lines = (tmp_path / "session.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lines) == 3
    assert '"baseline_sha":"baseline"' in lines[-1]
    assert '"r4_sha":"r4"' in lines[-1]

def test_restore_rejects_identity_or_provenance_mismatch(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    with pytest.raises(SessionDenied):
        HybridSessionController(SessionJournal(tmp_path / "session.jsonl"), ctl.clock).restore(
            session_id="s1", baseline_sha="other", r4_sha="r4"
        )


def test_restore_rejects_terminal_journal_tail(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    ctl.stop("done")
    with pytest.raises(SessionDenied):
        HybridSessionController(SessionJournal(tmp_path / "session.jsonl"), ctl.clock).restore(
            session_id="s1", baseline_sha="baseline", r4_sha="r4"
        )


def test_restore_expires_when_deadline_has_passed(tmp_path):
    ctl, clock = controller(tmp_path)
    session = ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    clock.value = session.deadline + timedelta(seconds=1)
    restored = HybridSessionController(SessionJournal(tmp_path / "session.jsonl"), ctl.clock).restore(
        session_id="s1", baseline_sha="baseline", r4_sha="r4"
    )
    assert restored.state is SessionState.EXPIRED


def test_restore_preserves_original_deadline(tmp_path):
    ctl, clock = controller(tmp_path)
    session = ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    clock.value += timedelta(minutes=10)
    restored = HybridSessionController(SessionJournal(tmp_path / "session.jsonl"), ctl.clock).restore(
        session_id="s1", baseline_sha="baseline", r4_sha="r4"
    )
    assert restored.state is SessionState.RUNNING
    assert restored.deadline == session.deadline


def test_restore_rejects_invalid_journal_state(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    path = tmp_path / "session.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    record = __import__('json').loads(lines[-1])
    record["state"] = "UNKNOWN"
    path.write_text("\n".join(lines[:-1] + [__import__('json').dumps(record)]) + "\n", encoding="utf-8")
    with pytest.raises(SessionDenied):
        HybridSessionController(SessionJournal(path), ctl.clock).restore(
            session_id="s1", baseline_sha="baseline", r4_sha="r4"
        )


def test_restore_rejects_boolean_cycle_provenance(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start("s1", "baseline", "r4", duration=timedelta(hours=1))
    path = tmp_path / "session.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    record = __import__('json').loads(lines[-1])
    record["cycle"] = True
    path.write_text("\n".join(lines[:-1] + [__import__('json').dumps(record)]) + "\n", encoding="utf-8")
    with pytest.raises(SessionDenied):
        HybridSessionController(SessionJournal(path), ctl.clock).restore(
            session_id="s1", baseline_sha="baseline", r4_sha="r4"
        )
