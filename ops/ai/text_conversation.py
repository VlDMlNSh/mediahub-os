"""Rate-limit-aware text conversation lifecycle for Free ChatGPT hybrid mode.

The controller never bypasses provider limits. It waits for the declared
retry window, then rotates to a fresh conversation identity. Opening an
actual ChatGPT UI conversation remains a transport/UI responsibility.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from enum import StrEnum
import hashlib
import math
import uuid
from typing import Callable
import json


class ConversationState(StrEnum):
    READY = "READY"
    WAITING_RATE_LIMIT = "WAITING_RATE_LIMIT"
    NEW_SESSION_REQUIRED = "NEW_SESSION_REQUIRED"
    SAFE_STOP = "SAFE_STOP"


class ConversationDenied(PermissionError):
    """Raised when a conversation transition is unsafe."""


@dataclass(frozen=True)
class ConversationSession:
    conversation_id: str
    session_id: str
    generation: int
    state: ConversationState
    retry_at: datetime | None = None
    reason: str = "ready"
    last_request_fingerprint: str = ""
    last_response_fingerprint: str = ""


@dataclass
class TextConversationController:
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)
    session_factory: Callable[[], str] = lambda: uuid.uuid4().hex
    conversation_factory: Callable[[], str] = lambda: uuid.uuid4().hex
    session: ConversationSession | None = None
    journal_path: Path | None = None

    def start_clean(self, session_id: str | None = None) -> ConversationSession:
        now = self._now()
        sid = session_id or self.session_factory()
        generation = 1 if self.session is None else self.session.generation + 1
        self.session = ConversationSession(
            conversation_id=self.conversation_factory(),
            session_id=sid,
            generation=generation,
            state=ConversationState.READY,
            reason="clean session started",
        )
        return self.session

    def persist(self) -> None:
        if self.session is None or self.journal_path is None:
            return
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        record = {"conversation_id": self.session.conversation_id, "session_id": self.session.session_id,
                  "generation": self.session.generation, "state": self.session.state.value,
                  "retry_at": self.session.retry_at.isoformat() if self.session.retry_at else None,
                  "reason": self.session.reason, "last_request_fingerprint": self.session.last_request_fingerprint,
                  "last_response_fingerprint": self.session.last_response_fingerprint}
        self.journal_path.write_text(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")

    def restore(self) -> ConversationSession:
        if self.journal_path is None or not self.journal_path.exists():
            raise ConversationDenied("conversation checkpoint is unavailable")
        try:
            data = json.loads(self.journal_path.read_text(encoding="utf-8"))
            state = ConversationState(data["state"])
            retry_at = datetime.fromisoformat(data["retry_at"]) if data.get("retry_at") else None
            self.session = ConversationSession(data["conversation_id"], data["session_id"],
                int(data["generation"]), state, retry_at, data.get("reason", "restored"),
                data.get("last_request_fingerprint", ""), data.get("last_response_fingerprint", ""))
        except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as exc:
            raise ConversationDenied("conversation checkpoint is invalid") from exc
        return self.poll()

    def register_rate_limit(self, retry_after: timedelta, reason: str = "provider rate limit") -> ConversationSession:
        session = self._require()
        if session.state is ConversationState.WAITING_RATE_LIMIT:
            raise ConversationDenied("rate-limit wait is already active")
        seconds = retry_after.total_seconds()
        if not math.isfinite(seconds) or seconds <= 0:
            raise ConversationDenied("retry window must be a positive finite timedelta")
        retry_at = self._now() + retry_after
        self.session = replace(
            session,
            state=ConversationState.WAITING_RATE_LIMIT,
            retry_at=retry_at,
            reason=reason,
        )
        self.persist()
        return self.session

    def poll(self) -> ConversationSession:
        session = self._require()
        if session.state is ConversationState.NEW_SESSION_REQUIRED:
            return session
        if session.state is not ConversationState.WAITING_RATE_LIMIT:
            return session
        if session.retry_at is None:
            raise ConversationDenied("rate-limit wait has no retry deadline")
        if self._now() < session.retry_at:
            return session
        self.session = replace(
            session,
            state=ConversationState.NEW_SESSION_REQUIRED,
            retry_at=None,
            reason="rate-limit window elapsed; fresh chat required",
        )
        self.persist()
        return self.session

    def open_fresh_session(self) -> ConversationSession:
        session = self.poll()
        if session.state is not ConversationState.NEW_SESSION_REQUIRED:
            raise ConversationDenied("fresh session is not yet permitted")
        fresh = self.start_clean()
        self.persist()
        return fresh

    def mark_safe_stop(self, reason: str) -> ConversationSession:
        session = self._require()
        self.session = replace(session, state=ConversationState.SAFE_STOP, reason=reason)
        self.persist()
        return self.session

    def request_fingerprint(self, envelope: str) -> str:
        return hashlib.sha256(envelope.encode("utf-8")).hexdigest()

    def accept_request(self, envelope: str) -> bool:
        session = self._require()
        fingerprint = self.request_fingerprint(envelope)
        if fingerprint == session.last_request_fingerprint:
            return False
        self.session = replace(session, last_request_fingerprint=fingerprint)
        self.persist()
        return True

    def accept_response(self, response: str) -> bool:
        session = self._require()
        fingerprint = self.request_fingerprint(response)
        if fingerprint == session.last_response_fingerprint:
            return False
        self.session = replace(session, last_response_fingerprint=fingerprint)
        self.persist()
        return True

    def _require(self) -> ConversationSession:
        if self.session is None:
            raise ConversationDenied("no conversation session is active")
        if self.session.state is ConversationState.SAFE_STOP:
            raise ConversationDenied("conversation is in SAFE_STOP")
        return self.session

    def _now(self) -> datetime:
        now = self.clock()
        if now.tzinfo is None:
            raise ConversationDenied("clock must return timezone-aware datetime")
        return now
