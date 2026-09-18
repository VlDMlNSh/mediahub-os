"""Atomic task leases for parallel autonomous worktrees."""
from __future__ import annotations

import fcntl
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Self, TextIO


class LeaseDenied(PermissionError):
    """Raised when another live worker owns the task."""


@dataclass
class TaskLease:
    path: Path
    task_id: str
    worker_id: str
    ttl_seconds: int = 900
    _handle: TextIO | None = None

    def acquire(self) -> None:
        if not self.task_id or not self.worker_id:
            raise LeaseDenied("task and worker identities are required")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle = open(self.path, "a+", encoding="utf-8")  # noqa: SIM115 — handle owns flock lifetime
        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            handle.close()
            raise LeaseDenied("task is already leased") from exc
        self._handle = handle
        now = time.time()
        record = {"task_id": self.task_id, "worker_id": self.worker_id, "expires_at": now + self.ttl_seconds}
        handle.seek(0)
        handle.truncate()
        json.dump(record, handle, sort_keys=True)
        handle.flush()
        os.fsync(handle.fileno())

    def release(self) -> None:
        handle = self._handle
        if handle is None:
            return
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()
        self._handle = None

    def __enter__(self) -> Self:
        self.acquire()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.release()
