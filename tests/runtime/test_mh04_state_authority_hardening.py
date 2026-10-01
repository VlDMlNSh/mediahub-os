import unittest

from runtime.mediahub_runtime.state_authority import (
    AuthorizationContext,
    Command,
    InvalidCommand,
    StateAuthority,
)


AUTH = AuthorizationContext("hardening-operator", True, frozenset({"state.write"}))


class MH04StateAuthorityHardeningTests(unittest.TestCase):
    def test_nested_digest_is_order_independent(self):
        left = {"z": {"b": 2, "a": 1}, "a": [3, {"d": 4, "c": 5}]}
        right = {"a": [3, {"c": 5, "d": 4}], "z": {"a": 1, "b": 2}}
        self.assertEqual(StateAuthority._digest(left), StateAuthority._digest(right))

    def test_source_identity_is_preserved_in_command_execution_trace(self):
        sa = StateAuthority()
        event = sa.execute(
            Command(
                "source-trace",
                "corr-source-trace",
                "set",
                ("trace",),
                "ok",
                None,
                AUTH,
                "local-runtime",
            )
        )
        self.assertEqual(event.command_id, "source-trace")
        self.assertEqual(event.correlation_id, "corr-source-trace")
        self.assertEqual(sa.read()["trace"], "ok")

    def test_non_string_source_identity_is_rejected(self):
        sa = StateAuthority()
        with self.assertRaises(InvalidCommand):
            sa.execute(
                Command(
                    "bad-source",
                    "corr-bad-source",
                    "set",
                    ("x",),
                    1,
                    None,
                    AUTH,
                    123,
                )
            )
        self.assertEqual(sa.read(), {})


if __name__ == "__main__":
    unittest.main()
