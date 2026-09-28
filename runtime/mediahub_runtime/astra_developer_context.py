"""Contract for MediaHub Developer chat/project context requests.

This module validates the mobile-facing context envelope before it reaches
Astra. It is transport-neutral and contains no authentication or secrets.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class DeveloperContextRequest:
    request_id: str
    session_id: str
    project_id: str | None
    message: str
    context_refs: tuple[str, ...] = ()
    task_id: str | None = None
    client_platform: str = "ios"
    client_version: str = "unknown"


class DeveloperContextContractError(ValueError):
    pass


class DeveloperContextContract:
    MAX_MESSAGE_BYTES = 65_536
    MAX_CONTEXT_REFS = 32

    @classmethod
    def parse(cls, payload: Mapping[str, Any]) -> DeveloperContextRequest:
        if not isinstance(payload, Mapping):
            raise DeveloperContextContractError("invalid_payload")

        def required(name: str) -> str:
            value = payload.get(name)
            if not isinstance(value, str) or not value.strip():
                raise DeveloperContextContractError(f"invalid_{name}")
            return value.strip()

        request_id = required("request_id")
        session_id = required("session_id")
        message = required("message")
        project_id = payload.get("project_id")
        if project_id is not None and (not isinstance(project_id, str) or not project_id.strip()):
            raise DeveloperContextContractError("invalid_project_id")

        raw_refs = payload.get("context_refs", ())
        if not isinstance(raw_refs, (list, tuple)) or len(raw_refs) > cls.MAX_CONTEXT_REFS:
            raise DeveloperContextContractError("invalid_context_refs")
        refs = tuple(ref.strip() for ref in raw_refs if isinstance(ref, str) and ref.strip())
        if len(refs) != len(raw_refs):
            raise DeveloperContextContractError("invalid_context_refs")
        if len(message.encode("utf-8")) > cls.MAX_MESSAGE_BYTES:
            raise DeveloperContextContractError("message_limit_exceeded")

        task_id = payload.get("task_id")
        if task_id is not None and (not isinstance(task_id, str) or not task_id.strip()):
            raise DeveloperContextContractError("invalid_task_id")

        platform = payload.get("client_platform", "ios")
        version = payload.get("client_version", "unknown")
        if not isinstance(platform, str) or not platform.strip():
            raise DeveloperContextContractError("invalid_client_platform")
        if not isinstance(version, str) or not version.strip():
            raise DeveloperContextContractError("invalid_client_version")

        return DeveloperContextRequest(
            request_id, session_id, project_id.strip() if project_id else None,
            message, refs, task_id.strip() if task_id else None,
            platform.strip(), version.strip(),
        )

    @staticmethod
    def to_gateway_task(request: DeveloperContextRequest):
        from .astra_gateway import AstraTaskRequest
        return AstraTaskRequest(
            request_id=request.request_id,
            session_id=request.session_id,
            project_id=request.project_id,
            user_command=request.message,
            context_refs=request.context_refs,
            client_platform=request.client_platform,
            client_version=request.client_version,
        )


__all__ = ["DeveloperContextContract", "DeveloperContextContractError", "DeveloperContextRequest"]
