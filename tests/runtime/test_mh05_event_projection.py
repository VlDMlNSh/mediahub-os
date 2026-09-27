import unittest

from mediahub_runtime.event_projection import (
    CanonicalEvent,
    ProjectionError,
    project_runtime_event,
    validate_canonical_event,
)
from mediahub_runtime.state_authority import (
    AuthorizationContext,
    Command,
    InvalidCommand,
    StateAuthority,
)

AUTH = AuthorizationContext("projection-test", True, frozenset({"state.write"}))
CANONICAL_KEYS = {
    "id", "type", "version", "timestamp", "source", "subject", "payload",
    "severity", "priority", "correlation_id", "causation_id", "metadata",
}


class MH05EventProjectionTests(unittest.TestCase):
    def _event(self, command_id="cmd-projection", source="device-local"):
        return StateAuthority().execute(Command(command_id, "corr-projection", "set", ("media", "volume"), 7, None, AUTH, source))

    def test_projection_preserves_trusted_provenance_and_time(self):
        runtime_event = self._event()
        canonical = project_runtime_event(runtime_event).as_dict()
        self.assertEqual(set(canonical), CANONICAL_KEYS)
        self.assertEqual(canonical["id"], runtime_event.event_id)
        self.assertEqual(canonical["source"], "device-local")
        self.assertEqual(canonical["correlation_id"], "corr-projection")
        self.assertEqual(canonical["causation_id"], None)
        self.assertEqual(canonical["timestamp"], runtime_event.timestamp)
        self.assertEqual(canonical["subject"], "state:media/volume")

    def test_projection_preserves_event_trigger_causation(self):
        authority = StateAuthority()
        triggering = authority.execute(Command("cmd-trigger", "corr-trigger", "set", ("x",), 1, None, AUTH, "automation"))
        followed = authority.execute(Command("cmd-followed", "corr-followed", "set", ("y",), 2, None, AUTH, "automation", triggering.event_id))
        canonical = project_runtime_event(followed).as_dict()
        self.assertEqual(canonical["causation_id"], triggering.event_id)
        self.assertEqual(canonical["source"], "automation")

    def test_unknown_causation_reference_is_rejected_before_mutation(self):
        authority = StateAuthority({"x": 1})
        before = authority.read()
        with self.assertRaises(InvalidCommand):
            authority.execute(Command("cmd-bad-cause", "corr-bad-cause", "set", ("x",), 2, None, AUTH, "automation", "evt-does-not-exist"))
        self.assertEqual(authority.read(), before)
        self.assertEqual(authority.metadata()["event_sequence"], 0)

    def test_projection_cannot_accept_substitute_source_or_causation(self):
        runtime_event = self._event("cmd-substitution", "real-source")
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

    def test_canonical_schema_rejects_extra_or_invalid_fields(self):
        event = project_runtime_event(self._event("cmd-schema")).as_dict()
        validate_canonical_event(event)
        with self.assertRaises(ProjectionError):
            validate_canonical_event(dict(event, unexpected=True))
        with self.assertRaises(ProjectionError):
            validate_canonical_event(dict(event, timestamp="not-a-date"))
        with self.assertRaises(ProjectionError):
            validate_canonical_event(dict(event, priority=-1))

    def test_canonical_event_is_recursively_immutable(self):
        canonical = CanonicalEvent(
            id="evt-immutable", type="state.set", version="1.0", timestamp="2026-09-07T00:00:00+00:00",
            source="test", subject="state:x", payload={"nested": {"items": [1, 2]}}, severity="INFO",
            priority=0, correlation_id="corr", causation_id=None, metadata={"nested": {"flag": True}},
        )
        with self.assertRaises(TypeError):
            canonical.payload["nested"] = {}
        with self.assertRaises(TypeError):
            canonical.payload["nested"]["items"] = ()
        with self.assertRaises(TypeError):
            canonical.payload["nested"]["items"][0] = 9
        with self.assertRaises(TypeError):
            canonical.metadata["nested"]["flag"] = False

    def test_event_representation_is_detached_from_canonical_event(self):
        canonical = CanonicalEvent(
            id="evt-detached", type="state.set", version="1.0", timestamp="2026-09-07T00:00:00+00:00",
            source="test", subject="state:x", payload={"nested": {"value": 1}}, severity="INFO",
            priority=0, correlation_id="corr", causation_id=None, metadata={"command_id": "cmd"},
        )
        representation = canonical.as_dict()
        representation["payload"]["nested"]["value"] = 99
        representation["metadata"]["command_id"] = "tampered"
        self.assertEqual(canonical.payload["nested"]["value"], 1)
        self.assertEqual(canonical.metadata["command_id"], "cmd")

    def test_evidence_fingerprint_is_deterministic_and_event_bound(self):
        canonical = project_runtime_event(self._event("cmd-fingerprint"))
        fingerprint = canonical.evidence_fingerprint()
        self.assertEqual(fingerprint, canonical.evidence_fingerprint())
        changed = CanonicalEvent(
            id=canonical.id, type=canonical.type, version=canonical.version, timestamp=canonical.timestamp,
            source="different-source", subject=canonical.subject, payload=canonical.payload,
            severity=canonical.severity, priority=canonical.priority, correlation_id=canonical.correlation_id,
            causation_id=canonical.causation_id, metadata=canonical.metadata,
        )
        self.assertNotEqual(fingerprint, changed.evidence_fingerprint())

    def test_projection_is_observational(self):
        authority = StateAuthority({"x": 1})
        runtime_event = authority.execute(Command("cmd-observe", "corr-observe", "set", ("x",), 2, None, AUTH, "local-runtime"))
        before = authority.read()
        project_runtime_event(runtime_event)
        after = authority.read()
        self.assertEqual(after, before)
        self.assertEqual(authority.metadata()["event_sequence"], 1)


if __name__ == "__main__":
    unittest.main()
