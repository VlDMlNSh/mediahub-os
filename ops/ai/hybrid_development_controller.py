"""Orchestrator for the MediaHub hybrid-development control plane.

Owns bounded session, task delivery, text-transport lifecycle and verified
cloud-egress selection. It is not product state authority and never bypasses
provider limits, permissions, or the existing AI Gateway.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from enum import StrEnum
from typing import Callable

from ops.ai.hybrid_session import HybridSessionController, SessionDenied, SessionState
from ops.ai.task_delivery import TaskDeliveryJournal, DeliveryDenied, DeliveryState
from ops.ai.text_conversation import TextConversationController, ConversationDenied, ConversationState
from ops.hybrid_cloud_egress import HybridCloudEgressAdapter, TransportProbe
from ops.hybrid_cloud_api_egress_adapter import CloudAPIUnavailable


class ControllerState(StrEnum):
    READY = "READY"
    RUNNING = "RUNNING"
    WAITING = "WAITING"
    SAFE_STOP = "SAFE_STOP"
    STOPPED = "STOPPED"


class HybridDevelopmentDenied(RuntimeError):
    """Raised when a hybrid-development transition cannot be proven safe."""


@dataclass(frozen=True)
class ControllerSnapshot:
    state: ControllerState
    session_state: SessionState | None
    conversation_state: ConversationState | None
    delivery_state: DeliveryState | None
    transport: str = ""
    public_ip: str = ""


@dataclass
class HybridDevelopmentController:
    session: HybridSessionController
    conversation: TextConversationController
    delivery: TaskDeliveryJournal
    egress: HybridCloudEgressAdapter
    health_url: str
    transport_probe: Callable[[str, str], TransportProbe] | None = None
    state: ControllerState = ControllerState.READY

    def start(self, session_id: str, baseline_sha: str, r4_sha: str,
              duration: timedelta) -> ControllerSnapshot:
        if self.state not in {ControllerState.READY, ControllerState.STOPPED}:
            raise HybridDevelopmentDenied("controller is already active")
        try:
            self.session.start(session_id, baseline_sha, r4_sha, duration)
            self.conversation.start_clean(session_id)
            self.state = ControllerState.RUNNING
            return self.snapshot()
        except (SessionDenied, ConversationDenied) as exc:
            self.state = ControllerState.SAFE_STOP
            raise HybridDevelopmentDenied("controller start failed closed") from exc

    def preflight(self) -> ControllerSnapshot:
        if self.state not in {ControllerState.RUNNING, ControllerState.WAITING}:
            raise HybridDevelopmentDenied("controller is not runnable")
        try:
            probe = self.egress.require_stable_transport(self.health_url)
            if not probe.healthy:
                raise CloudAPIUnavailable("transport health check failed")
            self.state = ControllerState.RUNNING
            return self.snapshot(probe)
        except CloudAPIUnavailable as exc:
            # No cloud operation is admitted while transport is absent; keep the
            # bounded development session alive in WAITING for tunnel recovery.
            self.state = ControllerState.WAITING
            raise HybridDevelopmentDenied("no verified cloud transport; WAITING") from exc

    def prepare_task(self, task_id: str, envelope: str) -> ControllerSnapshot:
        if self.state is not ControllerState.RUNNING:
            raise HybridDevelopmentDenied("controller is not running")
        try:
            self.preflight()
            session = self.session.session
            conversation = self.conversation.session
            if session is None or conversation is None:
                raise HybridDevelopmentDenied("session/conversation identity unavailable")
            self.delivery.prepare(task_id, envelope, conversation.conversation_id,
                                  session.session_id, conversation.generation)
            return self.snapshot()
        except (DeliveryDenied, HybridDevelopmentDenied) as exc:
            raise HybridDevelopmentDenied("task admission failed closed") from exc

    def restore_delivery(self) -> ControllerSnapshot:
        """Restore delivery only against the currently active session/conversation."""
        if self.state not in {ControllerState.RUNNING, ControllerState.WAITING}:
            raise HybridDevelopmentDenied("controller is not in a recoverable state")
        session = self.session.session
        conversation = self.conversation.session
        if session is None or conversation is None:
            raise HybridDevelopmentDenied("session/conversation identity unavailable")
        try:
            self.delivery.restore_for_identity(
                session_id=session.session_id,
                conversation_id=conversation.conversation_id,
                generation=conversation.generation,
            )
        except DeliveryDenied as exc:
            self.state = ControllerState.SAFE_STOP
            raise HybridDevelopmentDenied("delivery recovery failed closed") from exc
        return self.snapshot()

    def request_api(self, url: str, *, method: str = "GET", data: bytes | None = None,
                    headers: dict[str, str] | None = None) -> tuple[int, bytes]:
        """Perform one cloud API operation after verified transport admission."""
        if self.state is not ControllerState.RUNNING:
            raise HybridDevelopmentDenied("controller is not running")
        try:
            self.preflight()
            if self.delivery.delivery is not None and self.delivery.delivery.state is DeliveryState.PREPARED:
                self.delivery.mark_dispatched()
            status, body = self.egress.request(url, method=method, data=data, headers=headers)
            if self.delivery.delivery is not None:
                self.delivery.mark_acknowledged(body.decode("utf-8", errors="replace"))
            return status, body
        except (CloudAPIUnavailable, DeliveryDenied, HybridDevelopmentDenied) as exc:
            if self.delivery.delivery is not None and self.delivery.delivery.state is DeliveryState.DISPATCHED:
                self.delivery.mark_transport_unknown("cloud API outcome unknown")
            self.state = ControllerState.WAITING if isinstance(exc, CloudAPIUnavailable) else ControllerState.SAFE_STOP
            raise HybridDevelopmentDenied("cloud API operation failed closed") from exc

    def mark_dispatched(self) -> ControllerSnapshot:
        try:
            self.delivery.mark_dispatched()
            return self.snapshot()
        except DeliveryDenied as exc:
            self.state = ControllerState.SAFE_STOP
            raise HybridDevelopmentDenied("dispatch state transition failed") from exc

    def acknowledge(self, response: str) -> ControllerSnapshot:
        try:
            self.delivery.mark_acknowledged(response)
            self.conversation.accept_response(response)
            return self.snapshot()
        except (DeliveryDenied, ConversationDenied) as exc:
            self.state = ControllerState.SAFE_STOP
            raise HybridDevelopmentDenied("acknowledgment failed closed") from exc

    def rate_limited(self, retry_after: timedelta) -> ControllerSnapshot:
        try:
            self.conversation.register_rate_limit(retry_after)
            self.state = ControllerState.WAITING
            return self.snapshot()
        except ConversationDenied as exc:
            self.state = ControllerState.SAFE_STOP
            raise HybridDevelopmentDenied("rate-limit transition failed") from exc

    def poll(self) -> ControllerSnapshot:
        try:
            session = self.session.heartbeat()
            conversation = self.conversation.poll()
            if session.state in {SessionState.EXPIRED, SessionState.SAFE_STOP}:
                self.state = ControllerState.SAFE_STOP
            elif conversation.state is ConversationState.NEW_SESSION_REQUIRED:
                self.state = ControllerState.WAITING
            return self.snapshot()
        except (SessionDenied, ConversationDenied) as exc:
            self.state = ControllerState.SAFE_STOP
            raise HybridDevelopmentDenied("controller poll failed closed") from exc

    def safe_stop(self, reason: str) -> ControllerSnapshot:
        try:
            if self.session.session is not None:
                self.session.safe_stop(reason)
            if self.conversation.session is not None:
                self.conversation.mark_safe_stop(reason)
            if self.delivery.delivery is not None:
                self.delivery.mark_safe_stop(reason)
        finally:
            self.state = ControllerState.SAFE_STOP
        return self.snapshot()

    def stop(self, reason: str = "operator stop") -> ControllerSnapshot:
        try:
            if self.session.session is not None:
                self.session.stop(reason)
        except SessionDenied:
            pass
        self.state = ControllerState.STOPPED
        return self.snapshot()

    def snapshot(self, probe: TransportProbe | None = None) -> ControllerSnapshot:
        active = probe.candidate.name if probe else ""
        ip = probe.public_ip if probe else ""
        return ControllerSnapshot(
            self.state,
            self.session.session.state if self.session.session else None,
            self.conversation.session.state if self.conversation.session else None,
            self.delivery.delivery.state if self.delivery.delivery else None,
            active, ip,
        )

    def restore(self, session_id: str, baseline_sha: str, r4_sha: str) -> ControllerSnapshot:
        """Restore a daemon checkpoint without creating a new identity."""
        if self.state not in {ControllerState.READY, ControllerState.STOPPED}:
            raise HybridDevelopmentDenied("controller is already active")
        try:
            session = self.session.restore(session_id=session_id, baseline_sha=baseline_sha, r4_sha=r4_sha)
            conversation = self.conversation.restore()
            if conversation.session_id != session.session_id:
                raise HybridDevelopmentDenied("conversation checkpoint does not match session")
            if conversation.state is ConversationState.SAFE_STOP:
                raise HybridDevelopmentDenied("conversation checkpoint is in SAFE_STOP")
            self.state = ControllerState.RUNNING
            if self.delivery.path.exists():
                self.restore_delivery()
            return self.snapshot()
        except (SessionDenied, ConversationDenied, HybridDevelopmentDenied) as exc:
            self.state = ControllerState.SAFE_STOP
            raise HybridDevelopmentDenied("controller restore failed closed") from exc
