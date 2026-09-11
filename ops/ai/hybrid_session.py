"""Bounded autonomous hybrid-development session controller.

This module owns session lifecycle only. It does not execute AI providers,
mutate canonical state, or bypass the MediaHub AI Gateway.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime, timedelta, timezone
from enum import StrEnum
import json
from pathlib import Path
from typing import Callable


class SessionState(StrEnum):
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPING = "STOPPING"
    STOPPED = "STOPPED"
    EXPIRED = "EXPIRED"
    SAFE_STOP = "SAFE_STOP"


class SessionDenied(PermissionError):
    """Raised when a session transition or journal operation is unsafe."""


@dataclass(frozen=True)
class HybridSession:
    session_id: str
    baseline_sha: str
    r4_sha: str
    started_at: datetime
    deadline: datetime
    state: SessionState = SessionState.RUNNING
    cycle: int = 0
    reason: str = "started"

    def remaining(self, now: datetime) -> timedelta:
        return max(self.deadline - now, timedelta(0))


@dataclass
class SessionJournal:
    path: Path

    def append(self, session: HybridSession, event: str, **data: object) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "session_id": session.session_id,
            "cycle": session.cycle,
            "state": session.state.value,
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "baseline_sha": session.baseline_sha,
            "r4_sha": session.r4_sha,
            **data,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")


@dataclass
class HybridSessionController:
    journal: SessionJournal
    clock: Callable[[], datetime] = lambda: datetime.now(timezone.utc)
    session: HybridSession | None = field(default=None, init=False)

    def start(self, session_id: str, baseline_sha: str, r4_sha: str, hours: float = 8.0) -> HybridSession:
        if self.session is not None and self.session.state in {
            SessionState.RUNNING, SessionState.PAUSED, SessionState.STOPPING,
        }:
            raise SessionDenied("an active hybrid session already exists")
        if not session_id or not baseline_sha or not r4_sha:
            raise SessionDenied("session identity and provenance are required")
        if hours <= 0 or hours > 24:
            raise SessionDenied("session duration must be >0 and <=24 hours")
        now = self._now()
        self.session = HybridSession(
            session_id=session_id,
            baseline_sha=baseline_sha,
            r4_sha=r4_sha,
            started_at=now,
            deadline=now + timedelta(hours=hours),
        )
        self.journal.append(self.session, "SESSION_STARTED", duration_hours=hours)
        return self.session

    def heartbeat(self) -> HybridSession:
        session = self._require_active()
        if self._now() >= session.deadline:
            self.session = replace(session, state=SessionState.EXPIRED, reason="deadline reached")
            self.journal.append(self.session, "SESSION_EXPIRED")
            return self.session
        self.journal.append(session, "HEARTBEAT", remaining_seconds=int(session.remaining(self._now()).total_seconds()))
        return session

    def next_cycle(self, action: str) -> HybridSession:
        session = self.heartbeat()
        if session.state is not SessionState.RUNNING:
            raise SessionDenied(f"session is not runnable: {session.state}")
        if not action:
            raise SessionDenied("cycle action is required")
        self.session = replace(session, cycle=session.cycle + 1, reason=action)
        self.journal.append(self.session, "CYCLE_STARTED", action=action)
        return self.session

    def pause(self, reason: str = "operator pause") -> HybridSession:
        session = self._require_active()
        if session.state is not SessionState.RUNNING:
            raise SessionDenied(f"cannot pause session in state {session.state}")
        self.session = replace(session, state=SessionState.PAUSED, reason=reason)
        self.journal.append(self.session, "SESSION_PAUSED", reason=reason)
        return self.session

    def resume(self) -> HybridSession:
        session = self._require_active()
        if session.state is not SessionState.PAUSED:
            raise SessionDenied(f"cannot resume session in state {session.state}")
        if self._now() >= session.deadline:
            self.session = replace(session, state=SessionState.EXPIRED, reason="deadline reached while paused")
            self.journal.append(self.session, "SESSION_EXPIRED")
            return self.session
        self.session = replace(session, state=SessionState.RUNNING, reason="resumed")
        self.journal.append(self.session, "SESSION_RESUMED")
        return self.session

    def safe_stop(self, reason: str) -> HybridSession:
        session = self._require_active()
        self.session = replace(session, state=SessionState.SAFE_STOP, reason=reason)
        self.journal.append(self.session, "SAFE_STOP", reason=reason)
        return self.session

    def stop(self, reason: str = "operator stop") -> HybridSession:
        session = self._require_active()
        self.session = replace(session, state=SessionState.STOPPING, reason=reason)
        self.journal.append(self.session, "SESSION_STOPPING", reason=reason)
        self.session = replace(self.session, state=SessionState.STOPPED)
        self.journal.append(self.session, "SESSION_STOPPED", reason=reason)
        return self.session

    def _require_active(self) -> HybridSession:
        if self.session is None:
            raise SessionDenied("no hybrid session is active")
        if self.session.state in {SessionState.STOPPED, SessionState.EXPIRED, SessionState.SAFE_STOP}:
            raise SessionDenied(f"session is terminal: {self.session.state}")
        return self.session

    def _now(self) -> datetime:
        now = self.clock()
        if now.tzinfo is None:
            raise SessionDenied("clock must return timezone-aware datetime")
        return now
