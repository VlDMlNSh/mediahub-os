"""Execution-backend registry for Astra engineering agents.

This module describes engineering executors, not model providers. Installation and
runtime qualification remain external evidence gates; registry entries never imply
that a backend is installed or qualified.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Mapping


class BackendKind(str, Enum):
    ENGINEERING_AGENT = "engineering_agent"


class VerificationState(str, Enum):
    UNVERIFIED = "UNVERIFIED"
    VERIFIED = "VERIFIED"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class ExecutionBackend:
    backend_id: str
    display_name: str
    kind: BackendKind
    node_id: str
    command_env: str
    verification_state: VerificationState = VerificationState.UNVERIFIED

    def __post_init__(self) -> None:
        for name, value in (
            ("backend_id", self.backend_id),
            ("display_name", self.display_name),
            ("node_id", self.node_id),
            ("command_env", self.command_env),
        ):
            if not value or not value.strip():
                raise ValueError(f"{name} must be non-empty")


DEFAULT_ENGINEERING_BACKENDS: tuple[ExecutionBackend, ...] = (
    ExecutionBackend(
        backend_id="codex",
        display_name="Codex",
        kind=BackendKind.ENGINEERING_AGENT,
        node_id="mh-dev-01",
        command_env="MEDIAHUB_CODEX_COMMAND",
    ),
    ExecutionBackend(
        backend_id="cursor",
        display_name="Cursor",
        kind=BackendKind.ENGINEERING_AGENT,
        node_id="mh-dev-01",
        command_env="MEDIAHUB_CURSOR_COMMAND",
    ),
)


class ExecutionBackendRegistry:
    """Immutable-by-default registry used by orchestration policy.

    A registry entry is descriptive only. Callers must require VERIFIED evidence
    before dispatching a production task to a backend.
    """

    def __init__(
        self,
        backends: tuple[ExecutionBackend, ...] = DEFAULT_ENGINEERING_BACKENDS,
    ) -> None:
        by_id: dict[str, ExecutionBackend] = {}
        for backend in backends:
            if backend.backend_id in by_id:
                raise ValueError(f"duplicate backend_id: {backend.backend_id}")
            by_id[backend.backend_id] = backend
        self._backends: Mapping[str, ExecutionBackend] = by_id

    def get(self, backend_id: str) -> ExecutionBackend:
        try:
            return self._backends[backend_id]
        except KeyError as exc:
            raise KeyError(f"unknown execution backend: {backend_id}") from exc

    def all(self) -> tuple[ExecutionBackend, ...]:
        return tuple(self._backends.values())

    def verified(self) -> tuple[ExecutionBackend, ...]:
        return tuple(
            backend
            for backend in self._backends.values()
            if backend.verification_state is VerificationState.VERIFIED
        )
