import unittest

from mediahub_runtime.composition_root import build_runtime
from mediahub_runtime.consumer_boundary import ConsumerBoundaryError
from mediahub_runtime.state_authority import AuthorizationContext


class TestMH05RestoreReachability(unittest.TestCase):
    def test_boundary_restore_requires_restore_permission(self):
        graph = build_runtime({"value": 1})
        boundary = graph["consumer_boundary"]
        checkpoint = graph["state_authority"].checkpoint()
        request = boundary.request(
            "recovery-service", "restore-corr-1",
            AuthorizationContext("operator", True, frozenset()),
        )
        with self.assertRaises(ConsumerBoundaryError) as ctx:
            boundary.restore(request, checkpoint)
        self.assertEqual(ctx.exception.code, "authorization_denied")
        self.assertEqual(graph["state_authority"].read()["value"], 1)

    def test_boundary_restore_accepts_explicit_source_and_correlation(self):
        graph = build_runtime({"value": 1})
        boundary = graph["consumer_boundary"]
        authority = graph["state_authority"]
        boundary.execute(
            boundary.request(
                "runtime", "c1", AuthorizationContext("writer", True, frozenset({"state.write"}))
            ),
            "set", ("value",), 2, command_id="cmd-1",
        )
        checkpoint = authority.checkpoint()
        boundary.execute(
            boundary.request(
                "runtime", "c2", AuthorizationContext("writer", True, frozenset({"state.write"}))
            ),
            "set", ("value",), 3, command_id="cmd-2",
        )
        restore_request = boundary.request(
            "recovery-service", "restore-corr-2",
            AuthorizationContext("operator", True, frozenset({"state.restore"})),
        )
        self.assertIsNone(boundary.restore(restore_request, checkpoint))
        self.assertEqual(authority.read()["value"], 2)
        self.assertEqual(tuple(e.command_id for e in authority.events()), ("cmd-1",))


if __name__ == "__main__":
    unittest.main()
