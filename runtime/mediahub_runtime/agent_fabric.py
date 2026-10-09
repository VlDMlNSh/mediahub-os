"""Bounded claim/lease primitives for MediaHub Agent Fabric.

Claims are coordination state, not MediaHub domain authority.
One file per claim avoids concurrent rewrites of a shared ledger.
"""
from __future__ import annotations

import json
import os
import time
import fcntl
import uuid
from contextlib import contextmanager
from dataclasses import asdict, dataclass, replace
from pathlib import Path


class AgentFabricError(RuntimeError):
    pass


@dataclass(frozen=True)
class AgentClaim:
    agent: str
    task_id: str
    goal: str
    paths: tuple[str, ...]
    exclusive_actions: tuple[str, ...]
    dependencies: tuple[str, ...]
    status: str
    started: float
    updated: float
    expiry: float
    base_sha: str
    lease_id: str = ""


class ClaimStore:
    def __init__(self, root: str | Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _safe_id(value: str) -> str:
        if not value or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for c in value):
            raise AgentFabricError("invalid_claim_id")
        return value

    def _path(self, task_id: str) -> Path:
        return self.root / f"{self._safe_id(task_id)}.json"

    @staticmethod
    def _norm(path: str) -> str:
        return path.strip().replace("\\", "/").strip("/")

    @classmethod
    def _overlap(cls, left: tuple[str, ...], right: tuple[str, ...]) -> bool:
        for a in left:
            for b in right:
                a, b = cls._norm(a), cls._norm(b)
                if a and b and (a == b or a.startswith(b + "/") or b.startswith(a + "/")):
                    return True
        return False

    def list_claims(self) -> tuple[AgentClaim, ...]:
        claims = []
        for path in sorted(self.root.glob("*.json")):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                if data.get("status") in {"ASSIGNED", "ACTIVE", "READY_FOR_VERIFY"} and data.get("expiry", 0) <= time.time():
                    data["status"] = "EXPIRED"
                claims.append(AgentClaim(**data))
            except (OSError, json.JSONDecodeError, TypeError) as exc:
                raise AgentFabricError("invalid_claim_store") from exc
        return tuple(claims)

    def conflicts(self, paths: tuple[str, ...], *, exclude_task_id: str | None = None) -> tuple[AgentClaim, ...]:
        now = time.time()
        return tuple(
            c for c in self.list_claims()
            if c.task_id != exclude_task_id
            and c.expiry > now
            and c.status in {"ASSIGNED", "ACTIVE", "READY_FOR_VERIFY"}
            and self._overlap(tuple(paths), c.paths)
        )

    @contextmanager
    def _locked(self):
        """Serialize every claim mutation, not only initial acquisitions."""
        lock_path = self.root / ".acquire.lock"
        with lock_path.open("a+", encoding="utf-8") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _read_claim(path: Path) -> dict:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError, TypeError) as exc:
            raise AgentFabricError("claim_not_found_or_invalid") from exc
        if not isinstance(data, dict):
            raise AgentFabricError("invalid_claim_store")
        return data

    @staticmethod
    def _write_claim_atomic(path: Path, payload: dict) -> None:
        """Publish complete claim JSON atomically; readers never see a partial write."""
        tmp = path.with_name(path.name + f".{os.getpid()}.tmp")
        try:
            fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp, path)
        finally:
            try:
                tmp.unlink()
            except FileNotFoundError:
                pass

    def acquire(self, claim: AgentClaim) -> AgentClaim:
        """Acquire a new fenced lease and return the persisted generation identity."""
        if claim.status not in {"ASSIGNED", "ACTIVE"}:
            raise AgentFabricError("invalid_claim_status")
        now = time.time()
        if claim.expiry <= now:
            raise AgentFabricError("claim_expired")
        with self._locked():
            path = self._path(claim.task_id)
            if path.exists():
                existing = self._read_claim(path)
                existing_status = existing.get("status")
                existing_expiry = existing.get("expiry", 0)
                if existing_status in {"ASSIGNED", "ACTIVE", "READY_FOR_VERIFY"} and existing_expiry > now:
                    raise AgentFabricError("claim_exists")
            if self.conflicts(claim.paths, exclude_task_id=claim.task_id):
                raise AgentFabricError("claim_collision")
            acquired = replace(claim, lease_id=uuid.uuid4().hex)
            self._write_claim_atomic(path, asdict(acquired))
            return acquired

    def heartbeat(
        self,
        task_id: str,
        lease_id: str,
        *,
        now: float | None = None,
        lease_seconds: float = 900.0,
    ) -> AgentClaim:
        """Renew only the exact current lease generation; expired/stale workers fail closed."""
        current = time.time() if now is None else now
        with self._locked():
            path = self._path(task_id)
            data = self._read_claim(path)
            if not lease_id or data.get("lease_id") != lease_id:
                raise AgentFabricError("stale_claim_lease")
            if data.get("status") not in {"ASSIGNED", "ACTIVE"}:
                raise AgentFabricError("claim_not_active")
            if float(data.get("expiry", 0)) <= current:
                raise AgentFabricError("claim_expired")
            data["status"] = "ACTIVE"
            data["updated"] = current
            data["expiry"] = current + max(1.0, lease_seconds)
            self._write_claim_atomic(path, data)
            return AgentClaim(**data)

    def release(self, task_id: str, status: str = "CLOSED", *, lease_id: str) -> None:
        """Release only the current lease generation, never a later owner's claim."""
        if status not in {"VERIFIED", "INTEGRATED", "CLOSED", "REJECTED", "DEFERRED"}:
            raise AgentFabricError("invalid_release_status")
        current = time.time()
        with self._locked():
            path = self._path(task_id)
            data = self._read_claim(path)
            if not lease_id or data.get("lease_id") != lease_id:
                raise AgentFabricError("stale_claim_lease")
            if data.get("status") not in {"ASSIGNED", "ACTIVE", "READY_FOR_VERIFY"}:
                raise AgentFabricError("claim_not_active")
            if float(data.get("expiry", 0)) <= current:
                raise AgentFabricError("claim_expired")
            data["status"] = status
            data["updated"] = current
            data["expiry"] = current
            self._write_claim_atomic(path, data)
