import unittest

from mediahub_runtime.event_projection import ProjectionError, project_runtime_event
from mediahub_runtime.state_authority import AuthorizationContext, Command, StateAuthority


AUTH = AuthorizationContext("projection-test", True, frozenset({"state.write"}))
CANONICAL_KEYS = {
    "id", "type", "version", "timestamp", "source", "subject", "payload",
    "severity", "priority", "correlation_id", "causation_id", "metadata",
}


class MH05EventProjectionTests(unittest.TestCase):
    def test_projection_preserves_trusted_provenance_and_time(self):
        authority = StateAuthority()
        runtime_event = authority.execute(
            Command(
                "cmd-projection-1",
                "corr-projection-1",
                "set",
                ("media", "volume"),
                7,
                None,
                AUTH,
                "device-local",
            )
        )
        canonical = project_runtime_event(runtime_event).as_dict()

        self.assertEqual(set(canonical), CANONICAL_KEYS)
        self.assertEqual(canonical["id"], runtime_event.event_id)
        self.assertEqual(canonical["source"], "device-local")
        self.assertEqual(canonical["correlation_id"], "corr-projection-1")
        self.assertEqual(canonical["causation_id"], None)
        self.assertEqual(canonical["timestamp"], runtime_event.timestamp)
        self.assertEqual(canonical["subject"], "state:media/volume")

    def test_projection_preserves_event_trigger_causation(self):
        authority = StateAuthority()
        triggering = authority.execute(
            Command("cmd-trigger", "corr-trigger", "set", ("x",), 1, None, AUTH, "automation")
        )
        followed = authority.execute(
            Command(
                "cmd-followed",
                "corr-followed",
                "set",
                ("y",),
                2,
                None,
                AUTH,
                "automation",
                triggering.event_id,
            )
        )
        canonical = project_runtime_event(followed).as_dict()
        self.assertEqual(canonical["causation_id"], triggering.event_id)
        self.assertEqual(canonical["source"], "automation")

    def test_projection_cannot_accept_substitute_source_or_causation(self):
        authority = StateAuthority()
        runtime_event = authority.execute(
            Command("cmd-substitution", "corr-substitution", "set", ("x",), 1, None, AUTH, "real-source")
        )
        with self.assertRaises(TypeError):
            project_runtime_event(runtime_event, source_identity="attacker")
        with self.assertRaises(TypeError):
            project_runtime_event(runtime_event, causation_id="attacker-event")

    def test_incomplete_event_is_rejected(self):
        class UntrustedEvent:
            event_id = "evt-1"
            command_id = "cmd-1"
            correlation_id = "corr-1"
            operation = "set"
            path = ("x",)

        with self.assertRaises(ProjectionError):
            project_runtime_event(UntrustedEvent())

    def test_projection_is_observational(self):
        authority = StateAuthority({"x": 1})
        runtime_event = authority.execute(
            Command("cmd-observe", "corr-observe", "set", ("x",), 2, None, AUTH, "local-runtime")
        )
        before = authority.read()
        project_runtime_event(runtime_event)
        after = authority.read()
        self.assertEqual(after, before)
        self.assertEqual(authority.metadata()["event_sequence"], 1)


if __name__ == "__main__":
    unittest.main()
