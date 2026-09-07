import unittest

from mediahub_runtime.composition_root import build_runtime
from mediahub_runtime.state_authority import AuthorizationContext, AuthorizationDenied, InvalidCommand


class TestMH05RestoreSecurity(unittest.TestCase):
    def test_forged_token_cannot_restore(self):
        graph = build_runtime({"x": 1})
        authority = graph["state_authority"]
        before = authority.read()
        with self.assertRaises(AuthorizationDenied):
            authority.restore(("forged", {"x": 9}, 99, 99))
        self.assertEqual(authority.read(), before)

    def test_malformed_checkpoint_cannot_mutate(self):
        authority = build_runtime({"x": 1})["state_authority"]
        before = (authority.read(), authority.metadata(), authority.events())
        malformed = [(None,), ("", {}, 0, 0), ("bad", [], 0, 0), ("bad", {}, -1, 0), ("bad", {}, 2, 1)]
        for checkpoint in malformed:
            with self.subTest(checkpoint=checkpoint):
                with self.assertRaises((InvalidCommand, AuthorizationDenied)):
                    authority.restore(checkpoint)
                self.assertEqual((authority.read(), authority.metadata(), authority.events()), before)

    def test_unavailable_authority_fails_closed_for_restore(self):
        authority = build_runtime({"x": 1})["state_authority"]
        checkpoint = authority.checkpoint()
        authority.set_available(False)
        with self.assertRaises(Exception):
            authority.restore(checkpoint)

    def test_restore_does_not_create_second_authority(self):
        graph = build_runtime({"x": 1})
        self.assertIs(graph["consumer_boundary"]._authority, graph["state_authority"])


if __name__ == "__main__":
    unittest.main()
