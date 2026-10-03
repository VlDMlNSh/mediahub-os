import os
import unittest
from unittest.mock import patch

from runtime.mediahub_runtime.execution_adapter import (
    CodexAdapter,
    CursorAdapter,
    ExecutionAdapterError,
)
from runtime.mediahub_runtime.execution_backends import (
    BackendKind,
    ExecutionBackend,
    VerificationState,
)


def backend(backend_id: str, state: VerificationState) -> ExecutionBackend:
    return ExecutionBackend(
        backend_id=backend_id,
        display_name=backend_id.title(),
        kind=BackendKind.ENGINEERING_AGENT,
        node_id="mh-dev-01",
        command_env=f"MEDIAHUB_{backend_id.upper()}_COMMAND",
        verification_state=state,
    )


class ExecutionAdapterTests(unittest.TestCase):
    def test_unverified_backend_cannot_execute(self):
        adapter = CodexAdapter(backend("codex", VerificationState.UNVERIFIED))
        with self.assertRaisesRegex(ExecutionAdapterError, "backend_not_verified"):
            adapter.execute("hello")

    def test_cursor_unverified_backend_cannot_execute(self):
        adapter = CursorAdapter(backend("cursor", VerificationState.BLOCKED))
        with self.assertRaisesRegex(ExecutionAdapterError, "backend_not_verified"):
            adapter.execute("hello")

    def test_verified_backend_uses_argument_vector_without_shell(self):
        adapter = CodexAdapter(backend("codex", VerificationState.VERIFIED))
        with patch.dict(os.environ, {"MEDIAHUB_CODEX_COMMAND": "python3 -c \"print(\\\"ok\\\")\""}, clear=False):
            result = adapter.execute("bounded prompt")
        self.assertEqual(result.backend_id, "codex")
        self.assertEqual(result.output, "ok")
        self.assertEqual(result.returncode, 0)

    def test_missing_command_is_blocked(self):
        adapter = CursorAdapter(backend("cursor", VerificationState.VERIFIED))
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("MEDIAHUB_CURSOR_COMMAND", None)
            with self.assertRaisesRegex(ExecutionAdapterError, "backend_command_unavailable"):
                adapter.execute("hello")

    def test_empty_prompt_is_rejected(self):
        adapter = CodexAdapter(backend("codex", VerificationState.VERIFIED))
        with patch.dict(os.environ, {"MEDIAHUB_CODEX_COMMAND": "python -c \"print(\\\"ok\\\")\""}, clear=False):
            with self.assertRaisesRegex(ExecutionAdapterError, "invalid_prompt"):
                adapter.execute("   ")

    def test_timeout_is_mapped_to_bounded_execution_failure(self):
        adapter = CodexAdapter(backend("codex", VerificationState.VERIFIED), timeout=1)
        with patch.dict(
            os.environ,
            {"MEDIAHUB_CODEX_COMMAND": "python3 -c \"import time; time.sleep(10)\""},
            clear=False,
        ):
            with self.assertRaisesRegex(ExecutionAdapterError, "backend_execution_failed"):
                adapter.execute("bounded prompt")


if __name__ == "__main__":
    unittest.main()
