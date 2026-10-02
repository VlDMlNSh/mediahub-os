"""Bounded claim/lease primitives for MediaHub Agent Fabric.

Claims are coordination state, not MediaHub domain authority.
One file per claim avoids concurrent rewrites of a shared ledger.
"""
from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
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

    def acquire(self, claim: AgentClaim) -> None:
        if claim.status not in {"ASSIGNED", "ACTIVE"}:
            raise AgentFabricError("invalid_claim_status")
        if claim.expiry <= time.time():
            raise AgentFabricError("claim_expired")
        active = tuple(c for c in self.list_claims() if c.task_id != claim.task_id and c.expiry > time.time() and c.status in {"ASSIGNED", "ACTIVE", "READY_FOR_VERIFY"})
        if len(active) >= 2:
            raise AgentFabricError("claim_capacity_exceeded")
        if self.conflicts(claim.paths, exclude_task_id=claim.task_id):
            raise AgentFabricError("claim_collision")
        path = self._path(claim.task_id)
        payload = json.dumps(asdict(claim), sort_keys=True, separators=(",", ":")) + "\n"
        try:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except FileExistsError as exc:
            raise AgentFabricError("claim_exists") from exc
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(payload)
        except Exception:
            try:
                path.unlink()
            except OSError:
                pass
            raise

    def heartbeat(self, task_id: str, *, now: float | None = None, lease_seconds: float = 900.0) -> AgentClaim:
        path = self._path(task_id)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise AgentFabricError("claim_not_found") from exc
        current = time.time() if now is None else now
        if data.get("status") not in {"ASSIGNED", "ACTIVE"}:
            raise AgentFabricError("claim_not_active")
        data["status"] = "ACTIVE"
        data["updated"] = current
        data["expiry"] = current + max(1.0, lease_seconds)
        tmp = path.with_suffix(".tmp")
        try:
            tmp.write_text(json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
            os.replace(tmp, path)
        finally:
            try:
                tmp.unlink()
            except FileNotFoundError:
                pass
        return AgentClaim(**data)

    def release(self, task_id: str, status: str = "CLOSED") -> None:
        if status not in {"VERIFIED", "INTEGRATED", "CLOSED", "REJECTED", "DEFERRED"}:
            raise AgentFabricError("invalid_release_status")
        path = self._path(task_id)
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise AgentFabricError("claim_not_found") from exc
        data["status"] = status
        data["updated"] = time.time()
        data["expiry"] = data["updated"]
        tmp = path.with_suffix(".tmp")
        try:
            tmp.write_text(json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
            os.replace(tmp, path)
        finally:
            try:
                tmp.unlink()
            except FileNotFoundError:
                pass
