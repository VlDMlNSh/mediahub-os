"""Dependency-free Astra Cloud task lifecycle boundary."""

from dataclasses import dataclass
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


class AstraCloudService:
    """Compile/execute canonical Astra tasks through an injected provider."""

    def __init__(self, provider: Callable[[str], str] | None = None):
        self._provider = provider
        self._tasks: dict[str, TaskRecord] = {}
        self._lock = Lock()

    def submit(self, task: Mapping) -> TaskRecord:
        self._validate_task(task)
        task_id = f"ast_{uuid4().hex}"
        record = TaskRecord(task_id, task["request_id"], task["session_id"], task["user_command"], TaskState.QUEUED)
        with self._lock:
            self._tasks[task_id] = record
        return self.execute(task_id)

    def get(self, task_id: str) -> TaskRecord | None:
        with self._lock:
            return self._tasks.get(task_id)

    def execute(self, task_id: str) -> TaskRecord:
        current = self.get(task_id)
        if current is None:
            raise KeyError("task_not_found")
        if current.state is not TaskState.QUEUED:
            return current
        self._replace(current, state=TaskState.RUNNING)
        try:
            if self._provider is None:
                return self._replace(current, state=TaskState.BLOCKED, error_code="provider_unconfigured")
            output = self._provider(current.user_command)
            return self._replace(current, state=TaskState.SUCCEEDED, output=output)
        except Exception:
            return self._replace(current, state=TaskState.FAILED, error_code="provider_error")

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

    def _replace(self, old: TaskRecord, **changes) -> TaskRecord:
        record = TaskRecord(
            old.task_id, old.request_id, old.session_id, old.user_command,
            changes.get("state", old.state), changes.get("output", old.output),
            changes.get("error_code", old.error_code), old.agent_id, old.artifacts, old.audit_refs,
        )
        with self._lock:
            self._tasks[old.task_id] = record
        return record
