import unittest

from mediahub_runtime.composition_root import build_runtime
from mediahub_runtime.consumer_boundary import ConsumerBoundaryError
from mediahub_runtime.state_authority import (
    AuthorizationContext,
    AuthorizationDenied,
    InvalidCommand,
)


class TestMH05Restore(unittest.TestCase):
    def setUp(self):
        self.graph = build_runtime({"value": 1})
        self.authority = self.graph["state_authority"]
        self.boundary = self.graph["consumer_boundary"]
        self.allowed = AuthorizationContext("restore-test", True, frozenset({"state.write"}))
        self.restore_allowed = AuthorizationContext("restore-test", True, frozenset({"state.restore"}))

    def test_checkpoint_round_trip(self):
        self.boundary.execute(self.boundary.request("runtime", "c1", self.allowed), "set", ("value",), 2, command_id="cmd-1")
        checkpoint = self.authority.checkpoint()
        self.boundary.execute(self.boundary.request("runtime", "c2", self.allowed), "set", ("value",), 3, command_id="cmd-2")
        self.authority.restore(checkpoint, self.restore_allowed)
        self.assertEqual(self.authority.read()["value"], 2)
        self.assertEqual(self.authority.metadata()["event_sequence"], 1)
        self.assertEqual(tuple(e.command_id for e in self.authority.events()), ("cmd-1",))

    def test_invalid_checkpoint_is_non_mutating(self):
        before = (self.authority.read(), self.authority.metadata(), self.authority.events())
        with self.assertRaises(InvalidCommand):
            self.authority.restore(("bad", {}, 0, 0), self.restore_allowed)
        after = (self.authority.read(), self.authority.metadata(), self.authority.events())
        self.assertEqual(before, after)

    def test_checkpoint_token_is_not_an_authorization_context(self):
        checkpoint = self.authority.checkpoint()
        self.assertIsInstance(checkpoint, tuple)
        self.assertNotIsInstance(checkpoint[0], AuthorizationContext)

    def test_restore_history_is_prefix_preserving(self):
        event = self.boundary.execute(self.boundary.request("runtime", "c1", self.allowed), "set", ("value",), 2, command_id="cmd-1")
        checkpoint = self.authority.checkpoint()
        self.boundary.execute(self.boundary.request("runtime", "c2", self.allowed), "set", ("value",), 3, command_id="cmd-2")
        self.authority.restore(checkpoint, self.restore_allowed)
        metadata = self.authority.metadata()
        self.assertEqual(metadata["event_sequence"], 1)
        self.assertEqual(self.authority.events(), (event,))

    def test_restore_requires_dedicated_authorization(self):
        checkpoint = self.authority.checkpoint()
        with self.assertRaises(AuthorizationDenied):
            self.authority.restore(checkpoint, self.allowed)
        with self.assertRaises(AuthorizationDenied):
            self.authority.restore(checkpoint, AuthorizationContext("runtime", True, frozenset()))
        with self.assertRaises(AuthorizationDenied):
            self.authority.restore(checkpoint)

    def test_restore_does_not_bypass_normal_mutation_authorization_afterwards(self):
        checkpoint = self.authority.checkpoint()
        self.authority.restore(checkpoint, self.restore_allowed)
        request = self.boundary.request("runtime", "c3", AuthorizationContext("runtime", True, frozenset()))
        with self.assertRaises(ConsumerBoundaryError):
            self.boundary.execute(request, "set", ("value",), 9, command_id="unauthorized-after-restore")
        self.assertEqual(self.authority.read()["value"], 1)


if __name__ == "__main__":
    unittest.main()
