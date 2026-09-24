"""Persistent, atomic local queue semantics for MediaHub Task Contracts."""
from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

from .lineage import LineageError, TaskEvidenceLineage


class TaskQueueError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class QueueLease:
    request_id: str
    owner: str
    leased_until: float


class FileTaskQueue:
    """Filesystem queue using atomic rename and deterministic request-id idempotency."""

    STATES = frozenset({"inbox", "running", "done", "failed"})

    def __init__(self, root: str | Path, lease_seconds: float = 300.0, clock=time.time):
        self.root = Path(root)
        if lease_seconds <= 0 or lease_seconds > 3600:
            raise TaskQueueError("invalid_lease_seconds")
        self.lease_seconds = lease_seconds
        self.clock = clock
        for state in self.STATES:
            (self.root / state).mkdir(parents=True, exist_ok=True)

    def enqueue(self, contract: dict) -> Path:
        request_id = self._request_id(contract)
        for state in self.STATES:
            if (self.root / state / f"{request_id}.json").exists():
                return self.root / state / f"{request_id}.json"
        path = self.root / "inbox" / f"{request_id}.json"
        self._atomic_write(path, contract)
        return path

    def claim(self, owner: str) -> QueueLease | None:
        if not owner or any(c.isspace() for c in owner):
            raise TaskQueueError("invalid_owner")
        now = self.clock()
        self.recover_expired(now)
        for path in sorted((self.root / "inbox").glob("*.json")):
            request_id = path.stem
            lease_path = self.root / "running" / f"{request_id}.json"
            try:
                os.replace(path, lease_path)
            except OSError:
                continue
            contract = self._load(lease_path)
            metadata = {"request_id": request_id, "owner": owner, "leased_until": now + self.lease_seconds, "contract": contract}
            self._atomic_write(lease_path, metadata)
            return QueueLease(request_id, owner, metadata["leased_until"])
        return None

    def complete(self, lease: QueueLease, evidence: dict) -> Path:
        return self._finish(lease, "done", evidence)

    def fail(self, lease: QueueLease, evidence: dict) -> Path:
        return self._finish(lease, "failed", evidence)

    def recover_expired(self, now: float | None = None) -> int:
        now = self.clock() if now is None else now
        recovered = 0
        for path in sorted((self.root / "running").glob("*.json")):
            data = self._load(path)
            if float(data.get("leased_until", 0)) < now:
                contract = data.get("contract")
                if not isinstance(contract, dict):
                    raise TaskQueueError("invalid_running_record")
                self._atomic_write(self.root / "inbox" / path.name, contract)
                path.unlink()
                recovered += 1
        return recovered

    def _finish(self, lease: QueueLease, state: str, evidence: dict) -> Path:
        path = self.root / "running" / f"{lease.request_id}.json"
        if not path.exists():
            raise TaskQueueError("lease_not_found")
        data = self._load(path)
        if data.get("owner") != lease.owner or float(data.get("leased_until", 0)) != lease.leased_until:
            raise TaskQueueError("lease_mismatch")
        if not isinstance(evidence, dict):
            raise TaskQueueError("invalid_evidence")
        target = self.root / state / path.name
        lineage = TaskEvidenceLineage.create(lease.request_id, data["contract"], evidence)
        self._atomic_write(target, {"request_id": lease.request_id, "contract": data["contract"], "evidence": evidence, "lineage": lineage.as_dict(), "completed_at": self.clock()})
        path.unlink()
        return target

    @staticmethod
    def _request_id(contract: dict) -> str:
        if not isinstance(contract, dict) or not isinstance(contract.get("request_id"), str) or not contract["request_id"].strip():
            raise TaskQueueError("invalid_request_id")
        request_id = contract["request_id"].strip()
        if any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for c in request_id):
            raise TaskQueueError("invalid_request_id")
        return request_id

    def verify_lineage(self, request_id: str, state: str = "done") -> bool:
        if state not in {"done", "failed"}:
            raise TaskQueueError("invalid_state")
        path = self.root / state / f"{request_id}.json"
        if not path.exists():
            raise TaskQueueError("record_not_found")
        data = self._load(path)
        try:
            lineage = TaskEvidenceLineage.from_dict(data.get("lineage"))
        except LineageError as exc:
            raise TaskQueueError("invalid_lineage") from exc
        if lineage.request_id != request_id or not lineage.verify(data.get("contract"), data.get("evidence")):
            raise TaskQueueError("lineage_mismatch")
        return True

    @staticmethod
    def _load(path: Path) -> dict:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TaskQueueError("invalid_queue_record") from exc
        if not isinstance(data, dict):
            raise TaskQueueError("invalid_queue_record")
        return data

    @staticmethod
    def _atomic_write(path: Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
        tmp.write_text(json.dumps(data, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        os.replace(tmp, path)
