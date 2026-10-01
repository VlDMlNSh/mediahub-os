import unittest

from mediahub_runtime.consumer_boundary import ConsumerBoundary, ConsumerBoundaryError
from mediahub_runtime.state_authority import AuthorizationContext, StateAuthority


class ConsumerBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.authority = StateAuthority({"value": 1})
        self.boundary = ConsumerBoundary(self.authority)
        self.allowed = AuthorizationContext("runtime", True, frozenset({"state.write"}))
        self.denied = AuthorizationContext("ui", True, frozenset())

    def request(self, auth=None, source="runtime"):
        return self.boundary.request(source, "corr-1", auth or self.allowed)

    def test_governed_mutation_reaches_single_authority(self):
        result = self.boundary.execute(self.request(), "set", ("value",), 2, command_id="cmd-1")
        self.assertEqual(result.command_id, "cmd-1")
        self.assertEqual(self.boundary.read()["value"], 2)
        self.assertEqual(self.authority.metadata()["event_sequence"], 1)

    def test_missing_identity_fails_before_authority(self):
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            self.boundary.request("", "corr-1", self.allowed)
        self.assertEqual(ctx.exception.code, "invalid_identity")
        self.assertEqual(self.authority.metadata()["event_sequence"], 0)

    def test_unauthorized_request_is_non_mutating(self):
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            self.boundary.execute(self.request(self.denied, "ui"), "set", ("value",), 9, command_id="cmd-2")
        self.assertEqual(ctx.exception.code, "authorization_denied")
        self.assertEqual(self.boundary.read()["value"], 1)
        self.assertEqual(self.authority.metadata()["event_sequence"], 0)

    def test_readiness_or_presence_is_not_authorization(self):
        context = AuthorizationContext("device-present", True, frozenset())
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            self.boundary.execute(self.request(context, "device-present"), "set", ("value",), 7, command_id="cmd-3")
        self.assertEqual(ctx.exception.code, "authorization_denied")

    def test_duplicate_command_does_not_mutate_twice(self):
        self.boundary.execute(self.request(), "set", ("value",), 2, command_id="cmd-4")
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            self.boundary.execute(self.request(), "set", ("value",), 3, command_id="cmd-4")
        self.assertEqual(ctx.exception.code, "duplicate_command")
        self.assertEqual(self.boundary.read()["value"], 2)
        self.assertEqual(self.authority.metadata()["event_sequence"], 1)

    def test_stale_generation_is_rejected(self):
        self.boundary.execute(self.request(), "set", ("value",), 2, expected_generation=0, command_id="cmd-5")
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            self.boundary.execute(self.request(), "set", ("value",), 3, expected_generation=0, command_id="cmd-6")
        self.assertEqual(ctx.exception.code, "stale_generation")
        self.assertEqual(self.boundary.read()["value"], 2)

    def test_oversized_payload_is_rejected_without_authority_call(self):
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            self.boundary.execute(self.request(), "set", ("value",), "x" * 4097, command_id="cmd-7")
        self.assertEqual(ctx.exception.code, "operation_rejected")
        self.assertEqual(self.authority.metadata()["event_sequence"], 0)

    def test_event_remains_observational(self):
        seen = []
        self.authority.subscribe(seen.append)
        self.boundary.execute(self.request(), "set", ("value",), 4, command_id="cmd-8")
        self.assertEqual(len(seen), 1)
        self.assertEqual(seen[0].command_id, "cmd-8")
        self.assertEqual(self.boundary.read()["value"], 4)

    def test_boundary_has_no_shadow_state_or_checkpoint_store(self):
        self.assertFalse(hasattr(self.boundary, "_state"))
        self.assertFalse(hasattr(self.boundary, "_events"))
        self.assertFalse(hasattr(self.boundary, "checkpoint"))

    def test_invalid_request_object_is_rejected(self):
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            self.boundary.execute(object(), "set", ("value",), 2, command_id="cmd-9")
        self.assertEqual(ctx.exception.code, "invalid_request")


if __name__ == "__main__":
    unittest.main()
