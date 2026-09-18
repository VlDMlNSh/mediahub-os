import json
from pathlib import Path

import pytest

from ops.ai.task_delivery import DeliveryDenied, DeliveryState, TaskDeliveryJournal


def test_prepare_is_durable_and_idempotent(tmp_path: Path):
    path = tmp_path / "delivery.json"
    j = TaskDeliveryJournal(path)
    first = j.prepare("task-1", "payload", "conv-1", "sess-1", 1)
    again = j.prepare("task-1", "payload", "conv-1", "sess-1", 1)
    assert first == again
    assert j.restore() == first
    j.release()


def test_second_task_is_rejected(tmp_path: Path):
    j = TaskDeliveryJournal(tmp_path / "delivery.json")
    j.prepare("task-1", "payload", "conv", "sess", 1)
    with pytest.raises(DeliveryDenied):
        j.prepare("task-2", "other", "conv", "sess", 1)
    j.release()


def test_dispatch_is_durable_and_increments_attempt(tmp_path: Path):
    path = tmp_path / "delivery.json"
    j = TaskDeliveryJournal(path)
    prepared = j.prepare("task", "payload", "conv", "sess", 2)
    dispatched = j.mark_dispatched()
    assert dispatched.state is DeliveryState.DISPATCHED
    assert dispatched.attempt == prepared.attempt + 1
    j.release()
    restored = TaskDeliveryJournal(path)
    assert restored.restore() == dispatched
    restored.release()
    j.release()


def test_unknown_transport_outcome_requires_reconciliation(tmp_path: Path):
    j = TaskDeliveryJournal(tmp_path / "delivery.json")
    j.prepare("task", "payload", "conv", "sess", 1)
    j.mark_dispatched()
    state = j.mark_transport_unknown()
    assert state.state is DeliveryState.RECONCILIATION_REQUIRED
    with pytest.raises(DeliveryDenied):
        j.mark_dispatched()
    j.release()


def test_response_ack_is_idempotent(tmp_path: Path):
    j = TaskDeliveryJournal(tmp_path / "delivery.json")
    j.prepare("task", "payload", "conv", "sess", 1)
    j.mark_dispatched()
    first = j.mark_acknowledged("response")
    second = j.mark_acknowledged("response")
    assert first == second
    j.release()


def test_second_owner_is_blocked(tmp_path: Path):
    path = tmp_path / "delivery.json"
    first = TaskDeliveryJournal(path)
    with pytest.raises(DeliveryDenied):
        TaskDeliveryJournal(path)
    first.release()
    second = TaskDeliveryJournal(path)
    second.release()


def test_restart_after_dispatch_never_blindly_resends(tmp_path: Path):
    path = tmp_path / "delivery.json"
    first = TaskDeliveryJournal(path)
    first.prepare("task", "payload", "conv", "sess", 1)
    dispatched = first.mark_dispatched()
    first.release()
    second = TaskDeliveryJournal(path)
    restored = second.restore()
    assert restored == dispatched
    assert restored.state is DeliveryState.DISPATCHED
    assert second.mark_dispatched() == restored
    second.mark_transport_unknown("crash after send")
    second.release()


def test_corrupt_checkpoint_fails_closed(tmp_path: Path):
    path = tmp_path / "delivery.json"
    path.write_text(json.dumps({"version": 999}), encoding="utf-8")
    j = TaskDeliveryJournal(path)
    with pytest.raises(DeliveryDenied):
        j.restore()
    j.release()
