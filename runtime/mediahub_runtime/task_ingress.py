"""Safe local Task Contract ingress for Astra.

Only schema-shaped JSON files are accepted. The ingress does not execute shell
commands and does not contain provider credentials.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .astra_gateway import AstraGatewayRuntime, AstraTaskRequest
from .autonomous_task import AutonomousTaskPolicy, AutonomousTaskResult

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
        seen_request_ids: set[str] = set()
        for path in sorted(self.inbox.glob("*.json")):
            task = self._read(path)
            if task.request_id in seen_request_ids:
                raise TaskIngressError("duplicate_request_id")
            seen_request_ids.add(task.request_id)
            tasks.append(task)
        return tuple(tasks)

    def run_pending_bounded(
        self,
        gateway: AstraGatewayRuntime,
        policy: AutonomousTaskPolicy | None = None,
    ) -> tuple[AutonomousTaskResult, ...]:
        """Admit pending contracts through the existing Astra bounded path."""
        if not isinstance(gateway, AstraGatewayRuntime):
            raise TaskIngressError("invalid_gateway")
        return tuple(gateway.run_bounded(task, policy=policy) for task in self.read_pending())

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
        if any(not isinstance(data[key], str) or not data[key].strip()
               for key in ("request_id", "session_id", "user_command", "approval_state")):
            raise TaskIngressError("invalid_task_contract")
        if data["approval_state"] not in {"not_required", "approved", "pending", "rejected"}:
            raise TaskIngressError("invalid_task_contract")
        client = data.get("client") or {}
        if not isinstance(client, dict):
            raise TaskIngressError("invalid_task_contract")
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
