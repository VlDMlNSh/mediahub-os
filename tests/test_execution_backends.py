import unittest

from runtime.mediahub_runtime.execution_backends import (
    BackendKind,
    ExecutionBackend,
    ExecutionBackendRegistry,
    VerificationState,
)


class ExecutionBackendRegistryTests(unittest.TestCase):
    def test_default_registry_declares_codex_and_cursor(self):
        registry = ExecutionBackendRegistry()
        self.assertEqual(
            [backend.backend_id for backend in registry.all()],
            ["codex", "cursor"],
        )
        self.assertTrue(
            all(
                backend.kind is BackendKind.ENGINEERING_AGENT
                and backend.node_id == "mh-dev-01"
                and backend.verification_state is VerificationState.UNVERIFIED
                for backend in registry.all()
            )
        )

    def test_unverified_backends_are_not_dispatchable_as_verified(self):
        registry = ExecutionBackendRegistry()
        self.assertEqual(registry.verified(), ())

    def test_duplicate_backend_ids_are_rejected(self):
        backend = ExecutionBackend(
            backend_id="codex",
            display_name="Codex",
            kind=BackendKind.ENGINEERING_AGENT,
            node_id="mh-dev-01",
            command_env="MEDIAHUB_CODEX_COMMAND",
        )
        with self.assertRaisesRegex(ValueError, "duplicate backend_id"):
            ExecutionBackendRegistry((backend, backend))


if __name__ == "__main__":
    unittest.main()
