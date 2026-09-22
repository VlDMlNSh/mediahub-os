"""Minimal dependency-free Astra Cloud orchestration runtime.

This module owns task lifecycle and provider delegation; it does not own
MediaHub canonical state and never accepts provider credentials in task data.
"""

from dataclasses import dataclass, field
from enum import Enum
from threading import Lock
from typing import Callable, Mapping
from uuid import uuid4


class TaskState(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    BLOCKED = "blocked"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True)
class TaskRecord:
    task_id: str
    request_id: str
    session_id: str
    user_command: str
    state: TaskState
    output: str | None = None
    error_code: str | None = None
    agent_id: str | None = None
    artifacts: tuple[str, ...] = ()
    audit_refs: tuple[str, ...] = ()


@dataclass
class _MutableTask:
    record: TaskRecord
    metadata: dict = field(default_factory=dict)


class AstraCloudService:
    """Compile and execute canonical Astra tasks through an injected provider."""

    def __init__(self, provider: Callable[[str], str] | None = None):
        self._provider = provider
        self._tasks: dict[str, _MutableTask] = {}
        self._lock = Lock()

    def submit(self, task: Mapping) -> TaskRecord:
        self._validate_task(task)
        task_id = f"ast_{uuid4().hex}"
        record = TaskRecord(
            task_id=task_id,
            request_id=task["request_id"],
            session_id=task["session_id"],
            user_command=task["user_command"],
            state=TaskState.QUEUED,
        )
        with self._lock:
            self._tasks[task_id] = _MutableTask(record=record)
        return self.execute(task_id)

    def get(self, task_id: str) -> TaskRecord | None:
        with self._lock:
            item = self._tasks.get(task_id)
            return item.record if item else None

    def execute(self, task_id: str) -> TaskRecord:
        current = self.get(task_id)
        if current is None:
            raise KeyError("task_not_found")
        if current.state is not TaskState.QUEUED:
            return current
        self._set_state(task_id, TaskState.RUNNING)
        try:
            if self._provider is None:
                return self._set_state(task_id, TaskState.BLOCKED, error_code="provider_unconfigured")
            output = self._provider(current.user_command)
            return self._set_state(task_id, TaskState.SUCCEEDED, output=output)
        except Exception:
            return self._set_state(task_id, TaskState.FAILED, error_code="provider_error")

    @staticmethod
    def _validate_task(task: Mapping) -> None:
        required = ("schema_id", "schema_version", "owner", "request_id", "session_id", "user_command", "approval_state")
        if not isinstance(task, Mapping) or any(not isinstance(task.get(k), str) or not task[k] for k in required):
            raise ValueError("invalid_task")
        if task["schema_id"] != "mediahub.ai.astra-task" or task["schema_version"] != "1.0.0" or task["owner"] != "mediahub-ai":
            raise ValueError("invalid_task")
        if task["approval_state"] not in {"not_required", "pending", "approved", "rejected"}:
            raise ValueError("invalid_task")
        if task["approval_state"] == "rejected":
            raise ValueError("task_rejected")

    def _set_state(self, task_id: str, state: TaskState, **changes) -> TaskRecord:
        with self._lock:
            item = self._tasks[task_id]
            old = item.record
            item.record = TaskRecord(
                task_id=old.task_id, request_id=old.request_id, session_id=old.session_id,
                user_command=old.user_command, state=state,
                output=changes.get("output", old.output), error_code=changes.get("error_code", old.error_code),
                agent_id=changes.get("agent_id", old.agent_id), artifacts=old.artifacts, audit_refs=old.audit_refs,
            )
            return item.record
