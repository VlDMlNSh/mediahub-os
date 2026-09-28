"""Bounded adapters for local engineering-agent execution.

The adapter does not prove installation or qualification. It only provides a
safe process boundary; qualification remains an independent evidence gate.
"""
from __future__ import annotations

import os
import shlex
import subprocess
from dataclasses import dataclass

from .execution_backends import ExecutionBackend, VerificationState


class ExecutionAdapterError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ExecutionResult:
    backend_id: str
    output: str
    returncode: int


class LocalAgentAdapter:
    """Run a locally installed agent only when its backend is VERIFIED.

    Commands are supplied through an environment variable as an argument vector
    (shell syntax is rejected); secrets are not accepted by the adapter.
    """

    def __init__(self, backend: ExecutionBackend, timeout: int = 900):
        self.backend = backend
        self.timeout = max(1, min(int(timeout), 900))

    def execute(self, prompt: str) -> ExecutionResult:
        if self.backend.verification_state is not VerificationState.VERIFIED:
            raise ExecutionAdapterError("backend_not_verified")
        if not isinstance(prompt, str) or not prompt.strip():
            raise ExecutionAdapterError("invalid_prompt")
        raw_command = os.environ.get(self.backend.command_env, "").strip()
        if not raw_command:
            raise ExecutionAdapterError("backend_command_unavailable")
        try:
            argv = shlex.split(raw_command)
        except ValueError as exc:
            raise ExecutionAdapterError("backend_command_invalid") from exc
        if not argv or any(part in {";", "&&", "||", "|", ">", "<"} for part in argv):
            raise ExecutionAdapterError("backend_command_invalid")
        try:
            result = subprocess.run(
                [*argv, prompt],
                text=True,
                capture_output=True,
                timeout=self.timeout,
                check=False,
                env={"PATH": os.environ.get("PATH", "")},
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ExecutionAdapterError("backend_execution_failed") from exc
        output = result.stdout.strip()
        if result.returncode != 0:
            raise ExecutionAdapterError("backend_execution_failed")
        if not output:
            raise ExecutionAdapterError("empty_backend_result")
        return ExecutionResult(self.backend.backend_id, output, result.returncode)


class CodexAdapter(LocalAgentAdapter):
    pass


class CursorAdapter(LocalAgentAdapter):
    pass
