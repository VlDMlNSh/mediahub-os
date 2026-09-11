from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from ops.ai.hybrid_development_controller import (
    ControllerState, HybridDevelopmentController, HybridDevelopmentDenied,
)
from ops.ai.hybrid_session import HybridSessionController, SessionJournal
from ops.ai.task_delivery import TaskDeliveryJournal
from ops.ai.text_conversation import TextConversationController
from ops.hybrid_cloud_egress import HybridCloudEgressAdapter, TransportCandidate, TransportProbe


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


def test_stop_is_terminal(tmp_path):
    c = controller(tmp_path)
    c.start("s1", "baseline", "r4", timedelta(hours=1))
    c.stop()
    assert c.state is ControllerState.STOPPED
