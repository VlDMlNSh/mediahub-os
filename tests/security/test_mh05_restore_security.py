import unittest

from mediahub_runtime.composition_root import build_runtime
from mediahub_runtime.state_authority import (
    AuthorityUnavailable,
    AuthorizationContext,
    AuthorizationDenied,
    InvalidCommand,
    Command,
)


class TestMH05RestoreSecurity(unittest.TestCase):
    def setUp(self):
        self.restore_allowed = AuthorizationContext("security-test", True, frozenset({"state.restore"}))

    def test_forged_token_cannot_restore(self):
        authority = build_runtime({"x": 1})["state_authority"]
        checkpoint = authority.checkpoint()
        forged = ("forged", checkpoint[1], checkpoint[2], checkpoint[3], checkpoint[4], checkpoint[5], checkpoint[6])
        before = (authority.read(), authority.metadata(), authority.events())
        with self.assertRaises(AuthorizationDenied):
            authority.restore(forged, self.restore_allowed)
        self.assertEqual((authority.read(), authority.metadata(), authority.events()), before)

    def test_restore_requires_authorization_even_with_valid_checkpoint(self):
        authority = build_runtime({"x": 1})["state_authority"]
        checkpoint = authority.checkpoint()
        before = (authority.read(), authority.metadata(), authority.events())
        for authorization in (None, AuthorizationContext("unauthenticated", False, frozenset({"state.restore"})), AuthorizationContext("wrong-permission", True, frozenset())):
            with self.subTest(authorization=authorization):
                with self.assertRaises(AuthorizationDenied):
                    authority.restore(checkpoint, authorization)
                self.assertEqual((authority.read(), authority.metadata(), authority.events()), before)

    def test_malformed_checkpoint_cannot_mutate(self):
        authority = build_runtime({"x": 1})["state_authority"]
        before = (authority.read(), authority.metadata(), authority.events())
        malformed = [(None,), ("", {}, 0, 0), ("bad", [], 0, 0), ("bad", {}, -1, 0), ("bad", {}, 2, 1)]
        for checkpoint in malformed:
            with self.subTest(checkpoint=checkpoint):
                with self.assertRaises((InvalidCommand, AuthorizationDenied)):
                    authority.restore(checkpoint, self.restore_allowed)
                self.assertEqual((authority.read(), authority.metadata(), authority.events()), before)

    def test_unavailable_authority_fails_closed_for_restore(self):
        authority = build_runtime({"x": 1})["state_authority"]
        checkpoint = authority.checkpoint()
        authority.set_available(False)
        with self.assertRaises(AuthorityUnavailable):
            authority.restore(checkpoint, self.restore_allowed)

    def test_restore_does_not_create_second_authority(self):
        graph = build_runtime({"x": 1})
        self.assertIs(graph["consumer_boundary"]._authority, graph["state_authority"])


if __name__ == "__main__":
    unittest.main()

    def test_tampered_event_digest_cannot_restore(self):
        from dataclasses import replace

        authority = build_runtime({"x": 1})["state_authority"]
        allowed = AuthorizationContext("security-test", True, frozenset({"state.write"}))
        authority.execute(Command(
            command_id="cmd-1", correlation_id="corr-1", operation="set", path=("x",), value=2,
            authorization=allowed, source_identity="security-test"
        ))
        checkpoint = authority.checkpoint()
        tampered_event = replace(checkpoint[5][0], state_digest="0" * 64)
        tampered = (checkpoint[0], checkpoint[1], checkpoint[2], checkpoint[3], checkpoint[4], (tampered_event,), checkpoint[6])
        before = (authority.read(), authority.metadata(), authority.events())
        with self.assertRaises(InvalidCommand):
            authority.restore(tampered, self.restore_allowed)
        self.assertEqual((authority.read(), authority.metadata(), authority.events()), before)

    def test_tampered_checkpoint_state_cannot_restore(self):
        authority = build_runtime({"x": 1})["state_authority"]
        allowed = AuthorizationContext("security-test", True, frozenset({"state.write"}))
        authority.execute(Command(
            command_id="cmd-1", correlation_id="corr-1", operation="set", path=("x",), value=2,
            authorization=allowed, source_identity="security-test"
        ))
        checkpoint = authority.checkpoint()
        tampered_state = {"x": 999}
        tampered = (checkpoint[0], tampered_state, checkpoint[2], checkpoint[3], checkpoint[4], checkpoint[5], checkpoint[6])
        before = (authority.read(), authority.metadata(), authority.events())
        with self.assertRaises(InvalidCommand):
            authority.restore(tampered, self.restore_allowed)
        self.assertEqual((authority.read(), authority.metadata(), authority.events()), before)
