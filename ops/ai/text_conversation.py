"""Rate-limit-aware text conversation lifecycle for Free ChatGPT hybrid mode.

The controller never bypasses provider limits. It waits for the declared
retry window, then rotates to a fresh conversation identity. Opening an
actual ChatGPT UI conversation remains a transport/UI responsibility.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import math
import os
import tempfile
import uuid
from collections.abc import Callable
from dataclasses import dataclass, replace
from datetime import datetime, timedelta, timezone
from enum import StrEnum
from pathlib import Path


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
    _lock_handle: object | None = None

    def __post_init__(self) -> None:
        if self.journal_path is None:
            return
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        lock_path = self.journal_path.with_name(self.journal_path.name + ".lock")
        try:
            handle = open(lock_path, "a+")  # noqa: SIM115 — handle lifetime owns the inter-process lock
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            try:
                handle.close()
            except UnboundLocalError:
                pass
            raise ConversationDenied("conversation controller ownership is already held") from exc
        self._lock_handle = handle

    def release(self) -> None:
        handle = self._lock_handle
        if handle is None:
            return
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()
        self._lock_handle = None

    def start_clean(self, session_id: str | None = None) -> ConversationSession:
        sid = session_id or self.session_factory()
        generation = 1 if self.session is None else self.session.generation + 1
        self.session = ConversationSession(
            conversation_id=self.conversation_factory(),
            session_id=sid,
            generation=generation,
            state=ConversationState.READY,
            reason="clean session started",
        )
        self.persist()
        return self.session

    def persist(self) -> None:
        if self.session is None or self.journal_path is None:
            return
        self.journal_path.parent.mkdir(parents=True, exist_ok=True)
        record = {"version": 1, "conversation_id": self.session.conversation_id, "session_id": self.session.session_id,
                  "generation": self.session.generation, "state": self.session.state.value,
                  "retry_at": self.session.retry_at.isoformat() if self.session.retry_at else None,
                  "reason": self.session.reason, "last_request_fingerprint": self.session.last_request_fingerprint,
                  "last_response_fingerprint": self.session.last_response_fingerprint}
        payload = json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n"
        fd, temp_name = tempfile.mkstemp(prefix=self.journal_path.name + ".", dir=self.journal_path.parent)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                tmp.write(payload)
                tmp.flush()
                os.fsync(tmp.fileno())
            os.replace(temp_name, self.journal_path)
            dir_fd = os.open(self.journal_path.parent, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError as exc:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass
            raise ConversationDenied("conversation checkpoint durability failed") from exc

    def restore(self) -> ConversationSession:
        if self.journal_path is None or not self.journal_path.exists():
            raise ConversationDenied("conversation checkpoint is unavailable")
        try:
            data = json.loads(self.journal_path.read_text(encoding="utf-8"))
            if data.get("version") != 1:
                raise ConversationDenied("unsupported conversation checkpoint version")
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
