import unittest

from runtime.mediahub_runtime.state_authority import (
    AuthorizationContext,
    Command,
    StateAuthority,
)


class MH04SourceIdentityTests(unittest.TestCase):
    def test_source_identity_is_preserved_on_command(self):
        auth = AuthorizationContext("operator", True, frozenset({"state.write"}))
        command = Command(
            "source-1",
            "corr-source-1",
            "set",
            ("system", "mode"),
            "ready",
            authorization=auth,
            source_identity="local-runtime",
        )
        self.assertEqual(command.source_identity, "local-runtime")
        event = StateAuthority().execute(command)
        self.assertEqual(event.command_id, command.command_id)
        self.assertEqual(event.correlation_id, command.correlation_id)


if __name__ == "__main__":
    unittest.main()
