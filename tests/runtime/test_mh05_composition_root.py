import unittest

from mediahub_runtime.composition_root import build_runtime, canonical_authority
from mediahub_runtime.consumer_boundary import ConsumerBoundary
from mediahub_runtime.state_authority import AuthorizationContext, StateAuthority


class TestMH05CompositionRoot(unittest.TestCase):
    def test_builds_one_canonical_authority_and_governed_boundary(self):
        graph = build_runtime()
        authority = canonical_authority(graph)
        self.assertIsInstance(authority, StateAuthority)
        self.assertIsInstance(graph["consumer_boundary"], ConsumerBoundary)
        self.assertIs(graph["consumer_boundary"]._authority, authority)
        self.assertEqual(set(graph), {"state_authority", "consumer_boundary"})

    def test_authorized_mutation_enters_canonical_authority(self):
        graph = build_runtime()
        request = graph["consumer_boundary"].request(
            "prototype-ui", "corr-1",
            AuthorizationContext("tester", True, frozenset({"state.write"})),
        )
        event = graph["consumer_boundary"].execute(
            request, "set", ("demo",), "ok", command_id="cmd-1"
        )
        self.assertEqual(graph["state_authority"].read()["demo"], "ok")
        self.assertEqual(event.command_id, "cmd-1")
        self.assertEqual(event.source_identity, "prototype-ui")


if __name__ == "__main__":
    unittest.main()
