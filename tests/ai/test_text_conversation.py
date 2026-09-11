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
    del tmp_path
    clock = Clock()
    counter = iter(range(100))
    ctl = TextConversationController(
        clock=clock,
        session_factory=lambda: f"session-{next(counter)}",
        conversation_factory=lambda: f"chat-{next(counter)}",
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


def test_safe_stop_blocks_future_rotation(tmp_path):
    ctl, _ = controller(tmp_path)
    ctl.start_clean("s1")
    ctl.mark_safe_stop("protocol violation")
    with pytest.raises(ConversationDenied):
        ctl.open_fresh_session()
