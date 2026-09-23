"""Safe local Task Contract ingress for Astra.

Only schema-shaped JSON files are accepted. The ingress does not execute shell
commands and does not contain provider credentials.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .astra_gateway import AstraTaskRequest

MAX_TASK_BYTES = 70_000


class TaskIngressError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


class FileTaskIngress:
    """Convert an approved Task Contract file into an Astra task request."""

    def __init__(self, inbox: str | Path):
        self.inbox = Path(inbox)

    def read_pending(self) -> tuple[AstraTaskRequest, ...]:
        if not self.inbox.exists():
            return ()
        tasks: list[AstraTaskRequest] = []
        for path in sorted(self.inbox.glob("*.json")):
            tasks.append(self._read(path))
        return tuple(tasks)

    @staticmethod
    def _read(path: Path) -> AstraTaskRequest:
        try:
            if path.stat().st_size > MAX_TASK_BYTES:
                raise TaskIngressError("task_file_too_large")
            data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        except TaskIngressError:
            raise
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise TaskIngressError("invalid_task_file") from exc

        required = ("schema_id", "schema_version", "owner", "request_id",
                    "session_id", "user_command", "approval_state")
        if any(key not in data for key in required):
            raise TaskIngressError("invalid_task_contract")
        if data["schema_id"] != "mediahub.ai.astra-task" or data["schema_version"] != "1.0.0":
            raise TaskIngressError("invalid_task_contract")
        if data["owner"] != "mediahub-ai":
            raise TaskIngressError("invalid_task_contract")
        client = data.get("client") or {}
        context = data.get("context_refs", [])
        if not isinstance(context, list) or any(not isinstance(x, str) for x in context):
            raise TaskIngressError("invalid_task_contract")
        try:
            return AstraTaskRequest(
                request_id=data["request_id"],
                session_id=data["session_id"],
                user_command=data["user_command"],
                approval_state=data["approval_state"],
                context_refs=tuple(context),
                client_platform=client.get("platform", "unknown"),
                client_version=client.get("version", "unknown"),
            )
        except (KeyError, TypeError, AttributeError) as exc:
            raise TaskIngressError("invalid_task_contract") from exc


def task_to_contract(task: AstraTaskRequest) -> dict[str, Any]:
    """Serialize only non-secret Task Contract fields."""
    return {
        "schema_id": "mediahub.ai.astra-task",
        "schema_version": "1.0.0",
        "owner": "mediahub-ai",
        "request_id": task.request_id,
        "session_id": task.session_id,
        "user_command": task.user_command,
        "context_refs": list(task.context_refs),
        "approval_state": task.approval_state,
        "client": {"platform": task.client_platform, "version": task.client_version},
    }
