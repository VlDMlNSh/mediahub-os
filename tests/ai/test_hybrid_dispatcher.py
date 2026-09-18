from pathlib import Path

import pytest

from ops.ai.hybrid_dispatcher import (
    DispatchAuthorization,
    DispatchDenied,
    DispatchRequest,
    HybridAgentDispatcher,
)
from ops.ai.task_delivery import DeliveryState, TaskDeliveryJournal
from ops.cloud_development_adapter import (
    CloudDevelopmentAdapter,
    ProviderResult,
    SandboxSpec,
)
from ops.hybrid_cloud_egress import (
    HybridCloudEgressAdapter,
    TransportCandidate,
    TransportProbe,
)
from ops.mediahub_credential_broker import CredentialBroker
from ops.mediahub_model_registry import ModelRecord, ModelRegistry

ENDPOINT = "https://api.openai.com/v1"


class FakeEgress(HybridCloudEgressAdapter):
    def __init__(self, healthy=True):
        super().__init__((TransportCandidate("vpn", "tun-vpm", "vpn", 10),))
        self.healthy = healthy

    def require_stable_transport(self, health_url):
        if not self.healthy:
            from ops.hybrid_cloud_api_egress_adapter import CloudAPIUnavailable
            raise CloudAPIUnavailable("transport unavailable")
        return TransportProbe(self._candidates[0], True, "203.0.113.10", "test")


def make_dispatcher(tmp_path: Path, *, enabled=True, healthy=True):
    delivery = TaskDeliveryJournal(tmp_path / "delivery.json")
    delivery.prepare("task-1", "do task", "conversation-1", "session-1", 1)
    adapter = CloudDevelopmentAdapter()
    adapter.authorize(frozenset({ENDPOINT}))
    credentials = tmp_path / "credentials"
    credentials.mkdir()
    secret = credentials / "mediahub-openai"
    secret.write_text("synthetic-secret", encoding="utf-8")
    secret.chmod(0o600)
    broker = CredentialBroker(credentials, frozenset({"openai"}))
    broker.authorize()
    registry = ModelRegistry((ModelRecord("openai", "qualified", enabled),))
    root = tmp_path / "sandbox"
    worktree = root / "worktree"
    worktree.mkdir(parents=True)
    dispatcher = HybridAgentDispatcher(
        delivery, FakeEgress(healthy), adapter, broker, registry,
        SandboxSpec(root, worktree),
        DispatchAuthorization(status="target-gated", allow_cloud_agent=True),
    )
    return dispatcher, delivery


def request(**kwargs):
    values = {"task_id": "task-1", "envelope": "do task", "provider": "codex",
              "model": "qualified", "endpoint": ENDPOINT, "source_sha": "abc", "egress": ENDPOINT}
    values.update(kwargs)
    return DispatchRequest(**values)


def test_default_authorization_blocks_cloud_target(tmp_path):
    dispatcher, _ = make_dispatcher(tmp_path)
    dispatcher.authorization = DispatchAuthorization()
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(), session_id="session-1", conversation_id="conversation-1", generation=1)


def test_identity_mismatch_blocks_dispatch(tmp_path):
    dispatcher, _ = make_dispatcher(tmp_path)
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(), session_id="wrong", conversation_id="conversation-1", generation=1)


def test_wrong_generation_blocks_dispatch(tmp_path):
    dispatcher, _ = make_dispatcher(tmp_path)
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(), session_id="session-1", conversation_id="conversation-1", generation=2)


def test_unqualified_model_blocks_dispatch(tmp_path):
    dispatcher, _ = make_dispatcher(tmp_path, enabled=False)
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(), session_id="session-1", conversation_id="conversation-1", generation=1)


def test_non_target_capability_blocks_dispatch(tmp_path):
    dispatcher, _ = make_dispatcher(tmp_path)
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(capabilities=frozenset({"production"})), session_id="session-1", conversation_id="conversation-1", generation=1)


def test_reconciliation_state_is_not_dispatchable(tmp_path):
    dispatcher, delivery = make_dispatcher(tmp_path)
    delivery.mark_dispatched()
    delivery.mark_transport_unknown("crash after send")
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(), session_id="session-1", conversation_id="conversation-1", generation=1)
    assert dispatcher.reconcile_required()


def test_transport_failure_before_send_keeps_prepared(tmp_path):
    dispatcher, delivery = make_dispatcher(tmp_path, healthy=False)
    with pytest.raises(DispatchDenied):
        dispatcher.dispatch(request(), session_id="session-1", conversation_id="conversation-1", generation=1)
    assert delivery.delivery is not None
    assert delivery.delivery.state is DeliveryState.PREPARED


def test_native_result_failure_after_send_requires_reconciliation(tmp_path, monkeypatch):
    dispatcher, delivery = make_dispatcher(tmp_path)
    monkeypatch.setattr(dispatcher.adapter, "execute_native_agent", lambda *args, **kwargs: (_ for _ in ()).throw(RuntimeError("agent unavailable")))
    with pytest.raises(DispatchDenied):
        dispatcher.dispatch(request(), session_id="session-1", conversation_id="conversation-1", generation=1)
    assert delivery.delivery is not None
    assert delivery.delivery.state is DeliveryState.RECONCILIATION_REQUIRED
    assert dispatcher.reconcile_required()


def test_restart_restores_and_blocks_unknown_outcome(tmp_path):
    first = TaskDeliveryJournal(tmp_path / "delivery.json")
    first.prepare("task-1", "do task", "conversation-1", "session-1", 1)
    first.mark_dispatched()
    first.mark_transport_unknown("crash after send")
    first.release()
    restored = TaskDeliveryJournal(tmp_path / "delivery.json")
    restored.restore()
    assert restored.delivery is not None
    assert restored.delivery.state is DeliveryState.RECONCILIATION_REQUIRED
    dispatcher, _ = make_dispatcher(tmp_path / "other")
    dispatcher.delivery.release()
    dispatcher.delivery = restored
    with pytest.raises(DispatchDenied):
        dispatcher.dispatch(request(), session_id="session-1", conversation_id="conversation-1", generation=1)


def test_restart_identity_mismatch_is_fail_closed(tmp_path):
    first = TaskDeliveryJournal(tmp_path / "delivery.json")
    first.prepare("task-1", "do task", "conversation-1", "session-1", 1)
    first.release()
    restored = TaskDeliveryJournal(tmp_path / "delivery.json")
    restored.restore()
    dispatcher, _ = make_dispatcher(tmp_path / "other")
    dispatcher.delivery.release()
    dispatcher.delivery = restored
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(), session_id="session-2", conversation_id="conversation-1", generation=1)


def test_restore_for_current_session_requires_exact_identity(tmp_path):
    first = TaskDeliveryJournal(tmp_path / "delivery.json")
    first.prepare("task-1", "do task", "conversation-1", "session-1", 1)
    first.release()
    restored = TaskDeliveryJournal(tmp_path / "delivery.json")
    dispatcher, _ = make_dispatcher(tmp_path / "other")
    dispatcher.delivery.release()
    dispatcher.delivery = restored
    result = dispatcher.restore_for_current_session(
        session_id="session-1", conversation_id="conversation-1", generation=1)
    assert result.state is DeliveryState.PREPARED


def test_restore_for_current_session_blocks_identity_mismatch(tmp_path):
    first = TaskDeliveryJournal(tmp_path / "delivery.json")
    first.prepare("task-1", "do task", "conversation-1", "session-1", 1)
    first.release()
    restored = TaskDeliveryJournal(tmp_path / "delivery.json")
    dispatcher, _ = make_dispatcher(tmp_path / "other")
    dispatcher.delivery.release()
    dispatcher.delivery = restored
    with pytest.raises(DispatchDenied):
        dispatcher.restore_for_current_session(
            session_id="session-2", conversation_id="conversation-1", generation=1)


def test_success_can_be_acknowledged(tmp_path, monkeypatch):
    dispatcher, delivery = make_dispatcher(tmp_path)
    result = ProviderResult("codex", "task-1", "ok", "DONE", 0, {"task_id": "task-1"})
    monkeypatch.setattr(dispatcher.adapter, "execute_native_agent", lambda *args, **kwargs: result)
    assert dispatcher.dispatch(request(), session_id="session-1", conversation_id="conversation-1", generation=1) == result
    dispatcher.acknowledge(result.output)
    assert delivery.delivery is not None
    assert delivery.delivery.state is DeliveryState.ACKNOWLEDGED


def test_malformed_dispatch_identity_types_are_denied(tmp_path):
    dispatcher, _ = make_dispatcher(tmp_path)
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(), session_id=1, conversation_id="conversation-1", generation=1)
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(), session_id="session-1", conversation_id="conversation-1", generation=True)
    with pytest.raises(DispatchDenied):
        dispatcher.admit(request(timeout_seconds=True), session_id="session-1", conversation_id="conversation-1", generation=1)
