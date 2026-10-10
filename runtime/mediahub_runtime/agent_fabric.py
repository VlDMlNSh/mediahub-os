"""Bounded claim/lease primitives for MediaHub Agent Fabric.

Claims are coordination state, not MediaHub domain authority.
One file per claim avoids concurrent rewrites of a shared ledger.
"""
from __future__ import annotations

import json
import os
import time
import fcntl
import tempfile
from contextlib import contextmanager
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
    quarantine_reason: str = ""
    worker_run_id: str = ""
    command_id: str = ""
    node_id: str = ""
    executor: str = ""


def _atomic_write_json(path: Path, data: dict) -> None:
    """Durably replace a JSON state file; clean up only this writer's temp file."""
    payload = json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n"
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, path)
        directory_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        try:
            temp_path.unlink()
        except FileNotFoundError:
            pass


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

    @contextmanager
    def _locked(self):
        """Serialize every claim mutation against acquire/heartbeat/release."""
        lock_path = self.root / ".acquire.lock"
        with lock_path.open("a+", encoding="utf-8") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)

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
            and (c.status == "QUARANTINED" or c.expiry > now)
            and c.status in {"ASSIGNED", "ACTIVE", "READY_FOR_VERIFY", "QUARANTINED"}
            and self._overlap(tuple(paths), c.paths)
        )

    def acquire(self, claim: AgentClaim) -> None:
        if claim.status not in {"ASSIGNED", "ACTIVE"}:
            raise AgentFabricError("invalid_claim_status")
        if claim.expiry <= time.time():
            raise AgentFabricError("claim_expired")
        lock_path = self.root / ".acquire.lock"
        with lock_path.open("a+", encoding="utf-8") as lock_handle:
            fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX)
            try:
                if self.conflicts(claim.paths, exclude_task_id=claim.task_id):
                    raise AgentFabricError("claim_collision")
                path = self._path(claim.task_id)
                payload = json.dumps(asdict(claim), sort_keys=True, separators=(",", ":")) + "\n"
                try:
                    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                except FileExistsError as exc:
                    try:
                        existing = json.loads(path.read_text(encoding="utf-8"))
                    except (OSError, json.JSONDecodeError, TypeError) as read_exc:
                        raise AgentFabricError("invalid_claim_store") from read_exc
                    if existing.get("status") == "QUARANTINED" or existing.get("expiry", 0) > time.time():
                        raise AgentFabricError("claim_exists") from exc
                    try:
                        path.unlink()
                    except OSError as unlink_exc:
                        raise AgentFabricError("expired_claim_reclaim_failed") from unlink_exc
                    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                try:
                    with os.fdopen(fd, "w", encoding="utf-8") as handle:
                        handle.write(payload)
                        handle.flush()
                        os.fsync(handle.fileno())
                    directory_fd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
                    try:
                        os.fsync(directory_fd)
                    finally:
                        os.close(directory_fd)
                except Exception:
                    try:
                        path.unlink()
                    except OSError:
                        pass
                    raise
            finally:
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_UN)

    def heartbeat(self, task_id: str, *, now: float | None = None, lease_seconds: float = 900.0) -> AgentClaim:
        with self._locked():
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
            _atomic_write_json(path, data)
            return AgentClaim(**data)

    def quarantine(self, task_id: str, reason: str = "remote_worker_state_unknown") -> None:
        """Pin a claim when a remote worker may still be active.

        Quarantined claims are never reclaimed by lease expiry; operator recovery
        must establish remote termination before explicitly releasing the claim.
        """
        with self._locked():
            path = self._path(task_id)
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise AgentFabricError("claim_not_found") from exc
            data["status"] = "QUARANTINED"
            data["quarantine_reason"] = str(reason)[:500]
            data["updated"] = time.time()
            data["expiry"] = data["updated"]
            _atomic_write_json(path, data)

    def get_claim(self, task_id: str) -> AgentClaim:
        with self._locked():
            path = self._path(task_id)
            try:
                return AgentClaim(**json.loads(path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError, TypeError) as exc:
                raise AgentFabricError("claim_not_found_or_invalid") from exc

    def set_worker_run_id(self, task_id: str, worker_run_id: str) -> AgentClaim:
        value = str(worker_run_id).strip()
        if not value.isdigit():
            raise AgentFabricError("invalid_worker_run_id")
        with self._locked():
            path = self._path(task_id)
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise AgentFabricError("claim_not_found") from exc
            if data.get("status") not in {"ASSIGNED", "ACTIVE", "QUARANTINED"}:
                raise AgentFabricError("claim_not_active")
            data["worker_run_id"] = value
            data["updated"] = time.time()
            _atomic_write_json(path, data)
            return AgentClaim(**data)

    def set_worker_run_id_if_quarantined_matches(
        self, task_id: str, worker_run_id: str, *, expected_identity: dict[str, str]
    ) -> AgentClaim:
        """Persist discovered run identity only if the quarantined claim still matches.

        This is a compare-and-swap operation: concurrent recovery attempts cannot
        overwrite a different run ID or attach a run to a changed command/node/executor.
        """
        value = str(worker_run_id).strip()
        if not value.isdigit():
            raise AgentFabricError("invalid_worker_run_id")
        identity_fields = ("command_id", "node_id", "executor")
        if set(expected_identity) != set(identity_fields):
            raise AgentFabricError("invalid_expected_run_identity")
        with self._locked():
            path = self._path(task_id)
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise AgentFabricError("claim_not_found") from exc
            if data.get("status") != "QUARANTINED":
                raise AgentFabricError("claim_no_longer_quarantined")
            if any(str(data.get(field, "")) != str(expected_identity[field]) for field in identity_fields):
                raise AgentFabricError("claim_worker_identity_changed")
            current_run_id = str(data.get("worker_run_id", ""))
            if current_run_id and current_run_id != value:
                raise AgentFabricError("claim_worker_run_id_changed")
            data["worker_run_id"] = value
            data["updated"] = time.time()
            _atomic_write_json(path, data)
            return AgentClaim(**data)

    def release_quarantined_if_matches(
        self,
        task_id: str,
        *,
        expected_run_id: str,
        expected_identity: dict[str, str],
        status: str = "REJECTED",
    ) -> AgentClaim:
        """CAS-release only the quarantined claim whose persisted remote identity was checked."""
        if status not in {"REJECTED", "DEFERRED", "CLOSED"}:
            raise AgentFabricError("invalid_recovery_release_status")
        if not str(expected_run_id).isdigit():
            raise AgentFabricError("invalid_worker_run_id")
        identity_fields = ("command_id", "node_id", "executor")
        if set(expected_identity) != set(identity_fields):
            raise AgentFabricError("invalid_expected_run_identity")
        with self._locked():
            path = self._path(task_id)
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise AgentFabricError("claim_not_found") from exc
            if data.get("status") != "QUARANTINED":
                raise AgentFabricError("claim_no_longer_quarantined")
            if str(data.get("worker_run_id", "")) != str(expected_run_id):
                raise AgentFabricError("claim_worker_run_id_changed")
            if any(str(data.get(field, "")) != str(expected_identity[field]) for field in identity_fields):
                raise AgentFabricError("claim_worker_identity_changed")
            data["status"] = status
            data["updated"] = time.time()
            data["expiry"] = data["updated"]
            _atomic_write_json(path, data)
            return AgentClaim(**data)

    def release(self, task_id: str, status: str = "CLOSED", *, remote_terminal_confirmed: bool = False) -> None:
        if status not in {"VERIFIED", "INTEGRATED", "CLOSED", "REJECTED", "DEFERRED"}:
            raise AgentFabricError("invalid_release_status")
        with self._locked():
            path = self._path(task_id)
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                raise AgentFabricError("claim_not_found") from exc
            if data.get("status") == "QUARANTINED" and not remote_terminal_confirmed:
                raise AgentFabricError("quarantined_claim_requires_remote_terminal_confirmation")
            data["status"] = status
            data["updated"] = time.time()
            data["expiry"] = data["updated"]
            _atomic_write_json(path, data)
