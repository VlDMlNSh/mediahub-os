from datetime import datetime, timedelta, timezone

import pytest

from ops.ai.text_conversation import (
    ConversationDenied,
    ConversationState,
    TextConversationController,
)


class Clock:
    def __init__(self):
        self.value = datetime(2026, 9, 11, 12, 0, tzinfo=timezone.utc)

    def __call__(self):
        return self.value


def controller(tmp_path):
    clock = Clock()
    counter = iter(range(100))
    ctl = TextConversationController(
        clock=clock,
        session_factory=lambda: f"session-{next(counter)}",
        conversation_factory=lambda: f"chat-{next(counter)}",
        journal_path=tmp_path / "conversation.json",
    )
    return ctl, clock


def test_rate_limit_waits_without_new_session(tmp_path):
    ctl, clock = controller(tmp_path)
    first = ctl.start_clean("s1")
    ctl.register_rate_limit(timedelta(minutes=10))
    clock.value += timedelta(minutes=9)
    state = ctl.poll()
    assert state.state is ConversationState.WAITING_RATE_LIMIT
    assert state.conversation_id == first.conversation_id


def test_expired_rate_limit_requires_fresh_chat(tmp_path):
    ctl, clock = controller(tmp_path)
    first = ctl.start_clean("s1")
    ctl.register_rate_limit(timedelta(minutes=10))
    clock.value += timedelta(minutes=10)
    state = ctl.poll()
    assert state.state is ConversationState.NEW_SESSION_REQUIRED
    assert state.conversation_id == first.conversation_id
    fresh = ctl.open_fresh_session()
    assert fresh.state is ConversationState.READY
    assert fresh.generation == first.generation + 1
    assert fresh.conversation_id != first.conversation_id
    assert fresh.session_id != first.session_id


def test_cannot_open_fresh_chat_before_window(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start_clean("s1")
    ctl.register_rate_limit(timedelta(minutes=1))
    with pytest.raises(ConversationDenied):
        ctl.open_fresh_session()


def test_retry_window_must_be_positive(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start_clean("s1")
    with pytest.raises(ConversationDenied):
        ctl.register_rate_limit(timedelta(0))


def test_duplicate_rate_limit_registration_is_denied(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start_clean("s1")
    ctl.register_rate_limit(timedelta(minutes=1))
    with pytest.raises(ConversationDenied):
        ctl.register_rate_limit(timedelta(minutes=1))


def test_duplicate_request_is_rejected(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start_clean("s1")
    assert ctl.accept_request("same") is True
    assert ctl.accept_request("same") is False
    assert ctl.accept_request("new") is True


def test_duplicate_response_is_rejected(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start_clean("s1")
    assert ctl.accept_response("same") is True
    assert ctl.accept_response("same") is False
    assert ctl.accept_response("new") is True


def test_rate_limit_without_active_session_is_denied(tmp_path):
    ctl, _ = controller(tmp_path)
    with pytest.raises(ConversationDenied):
        ctl.register_rate_limit(timedelta(minutes=1))


def test_poll_is_idempotent_after_wait_window(tmp_path):
    ctl, clock = controller(tmp_path)
    ctl.start_clean("s1")
    ctl.register_rate_limit(timedelta(minutes=1))
    clock.value += timedelta(minutes=1)
    first = ctl.poll()
    second = ctl.poll()
    assert first == second
    assert second.state is ConversationState.NEW_SESSION_REQUIRED


def test_safe_stop_blocks_future_rotation(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start_clean("s1")
    ctl.mark_safe_stop("protocol violation")
    with pytest.raises(ConversationDenied):
        ctl.open_fresh_session()


def test_restart_restores_wait_and_rotates_only_after_deadline(tmp_path):
    ctl, clock = controller(tmp_path)
    first = ctl.start_clean("s1")
    ctl.register_rate_limit(timedelta(minutes=10))
    ctl.release()
    restored, restored_clock = controller(tmp_path)
    restored_clock.value = clock.value + timedelta(minutes=5)
    state = restored.restore()
    assert state.state is ConversationState.WAITING_RATE_LIMIT
    assert state.conversation_id == first.conversation_id
    restored_clock.value += timedelta(minutes=5)
    state = restored.restore()
    assert state.state is ConversationState.NEW_SESSION_REQUIRED
    fresh = restored.open_fresh_session()
    assert fresh.conversation_id != first.conversation_id
    assert fresh.generation == 2
    restored.release()


def test_corrupt_checkpoint_fails_closed(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start_clean("s1")
    (tmp_path / "conversation.json").write_text("{broken", encoding="utf-8")
    with pytest.raises(ConversationDenied):
        ctl.restore()


def test_unsupported_checkpoint_version_fails_closed(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start_clean("s1")
    (tmp_path / "conversation.json").write_text('{"version": 99}', encoding="utf-8")
    with pytest.raises(ConversationDenied):
        ctl.restore()
