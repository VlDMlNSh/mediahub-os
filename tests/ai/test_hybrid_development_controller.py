from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from ops.ai.hybrid_development_controller import (
    ControllerState,
    HybridDevelopmentController,
    HybridDevelopmentDenied,
)
from ops.ai.hybrid_session import HybridSessionController, SessionJournal, SessionState
from ops.ai.task_delivery import DeliveryState, TaskDeliveryJournal
from ops.ai.text_conversation import ConversationState, TextConversationController
from ops.hybrid_cloud_egress import (
    HybridCloudEgressAdapter,
    TransportCandidate,
    TransportProbe,
)


class FakeEgress(HybridCloudEgressAdapter):
    def __init__(self, healthy=True):
        super().__init__((TransportCandidate("vpm", "tun-vpm", "vpnproxymaster", 10),))
        self.healthy = healthy

    def require_stable_transport(self, health_url):
        if not self.healthy:
            from ops.hybrid_cloud_api_egress_adapter import CloudAPIUnavailable
            raise CloudAPIUnavailable("down")
        return TransportProbe(self._candidates[0], True, "203.0.113.10", "test")


def controller(tmp_path: Path, healthy=True):
    clock = lambda: datetime(2026, 9, 11, tzinfo=timezone.utc)
    session = HybridSessionController(SessionJournal(tmp_path / "session.jsonl"), clock=clock)
    conversation = TextConversationController(clock=clock, journal_path=tmp_path / "conversation.json")
    delivery = TaskDeliveryJournal(tmp_path / "delivery.json")
    return HybridDevelopmentController(session, conversation, delivery, FakeEgress(healthy),
                                       "https://example.invalid/health")


def test_start_preflight_and_task_lifecycle(tmp_path):
    c = controller(tmp_path)
    assert c.start("s1", "baseline", "r4", timedelta(hours=1)).state is ControllerState.RUNNING
    snap = c.prepare_task("t1", "text-only task")
    assert snap.delivery_state.value == "PREPARED"
    assert c.mark_dispatched().delivery_state.value == "DISPATCHED"
    assert c.acknowledge("ok").delivery_state.value == "ACKNOWLEDGED"


def test_no_transport_safe_stops(tmp_path):
    c = controller(tmp_path, healthy=False)
    c.start("s1", "baseline", "r4", timedelta(hours=1))
    with pytest.raises(HybridDevelopmentDenied):
        c.preflight()
    assert c.state is ControllerState.WAITING


def test_restore_delivery_binds_checkpoint_to_current_identity(tmp_path):
    c = controller(tmp_path)
    c.start("s1", "baseline", "r4", timedelta(hours=1))
    c.delivery.prepare("t1", "text-only task", c.conversation.session.conversation_id, "s1", 1)
    assert c.restore_delivery().delivery_state.value == "PREPARED"


def test_restore_delivery_mismatch_safe_stops_controller(tmp_path):
    c = controller(tmp_path)
    c.start("s1", "baseline", "r4", timedelta(hours=1))
    c.delivery.prepare("t1", "text-only task", "other-conversation", "s1", 1)
    with pytest.raises(HybridDevelopmentDenied):
        c.restore_delivery()
    assert c.state is ControllerState.SAFE_STOP


def test_stop_is_terminal(tmp_path):
    c = controller(tmp_path)
    c.start("s1", "baseline", "r4", timedelta(hours=1))
    c.stop()
    assert c.state is ControllerState.STOPPED


def test_controller_restore_reconstructs_session_and_conversation(tmp_path):
    first = controller(tmp_path)
    first.start("s1", "baseline", "r4", timedelta(hours=1))
    conversation_id = first.conversation.session.conversation_id
    first.delivery.prepare("t1", "text-only task", conversation_id, "s1", 1)
    first.delivery.release()
    first.conversation.release()

    restored = controller(tmp_path)
    snapshot = restored.restore("s1", "baseline", "r4")
    assert snapshot.state is ControllerState.RUNNING
    assert snapshot.session_state is SessionState.RUNNING
    assert snapshot.conversation_state is ConversationState.READY
    assert snapshot.delivery_state is DeliveryState.PREPARED
    assert restored.conversation.session.conversation_id == conversation_id


def test_controller_restore_rejects_wrong_session_provenance(tmp_path):
    first = controller(tmp_path)
    first.start("s1", "baseline", "r4", timedelta(hours=1))
    first.delivery.release()
    first.conversation.release()
    restored = controller(tmp_path)
    with pytest.raises(HybridDevelopmentDenied):
        restored.restore("s2", "baseline", "r4")
    assert restored.state is ControllerState.SAFE_STOP


def test_controller_restore_rejects_conversation_session_mismatch(tmp_path):
    first = controller(tmp_path)
    first.start("s1", "baseline", "r4", timedelta(hours=1))
    first.conversation.session = first.conversation.session.__class__(
        first.conversation.session.conversation_id,
        "s2", first.conversation.session.generation,
        first.conversation.session.state, first.conversation.session.retry_at,
        first.conversation.session.reason, first.conversation.session.last_request_fingerprint,
        first.conversation.session.last_response_fingerprint,
    )
    first.conversation.persist()
    first.delivery.release()
    first.conversation.release()
    restored = controller(tmp_path)
    with pytest.raises(HybridDevelopmentDenied):
        restored.restore("s1", "baseline", "r4")
    assert restored.state is ControllerState.SAFE_STOP
