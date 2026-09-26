import unittest

from runtime.mediahub_runtime.state_authority import (
    AuthorityUnavailable,
    AuthorizationContext,
    AuthorizationDenied,
    Command,
    ConflictDetected,
    DuplicateCommand,
    InvalidCommand,
    StateAuthority,
)

AUTH = AuthorizationContext("test-operator", True, frozenset({"state.write"}))


def command(cid, op="set", path=("system", "mode"), value="ready", gen=None, auth=AUTH):
    return Command(cid, "corr-" + cid, op, path, value, gen, auth)


class MH04QualificationEdgeTests(unittest.TestCase):
    def test_identity_is_required_before_mutation(self):
        sa = StateAuthority()
        with self.assertRaises(InvalidCommand):
            sa.execute(Command("", "corr-x", "set", ("x",), 1, None, AUTH))
        with self.assertRaises(InvalidCommand):
            sa.execute(Command("x", "", "set", ("x",), 1, None, AUTH))
        self.assertEqual(sa.read(), {})

    def test_authorization_is_not_implied_by_presence_or_readiness(self):
        sa = StateAuthority()
        unauthenticated = AuthorizationContext("device-present", False, frozenset({"state.write"}))
        with self.assertRaises(AuthorizationDenied):
            sa.execute(command("presence", auth=unauthenticated))
        self.assertEqual(sa.read(), {})

    def test_event_is_observation_not_mutation_authority(self):
        sa = StateAuthority()
        seen = []
        sa.subscribe(seen.append)
        sa.execute(command("event-source"))
        self.assertEqual(len(seen), 1)
        # Event delivery is observational; only execute(Command) can mutate.
        event = seen[0]
        self.assertEqual(sa.read()["system"]["mode"], "ready")
        self.assertEqual(event.command_id, "event-source")

    def test_local_operation_does_not_need_network_dependency(self):
        sa = StateAuthority()
        sa.set_available(True)
        sa.execute(command("offline"))
        self.assertEqual(sa.read()["system"]["mode"], "ready")

    def test_invalid_delete_is_atomic(self):
        sa = StateAuthority({"system": {"mode": "ready"}})
        before = sa.read()
        with self.assertRaises(InvalidCommand):
            sa.execute(command("bad-delete", "delete", ("system", "missing"), None))
        self.assertEqual(sa.read(), before)

    def test_authority_failure_is_non_mutating(self):
        sa = StateAuthority({"x": 1})
        sa.set_available(False)
        with self.assertRaises(AuthorityUnavailable):
            sa.execute(command("blocked"))
        self.assertEqual(sa._generation, 0)

    def test_generation_conflict_is_non_mutating_and_has_no_event(self):
        sa = StateAuthority()
        sa.execute(command("base"))
        before_events = sa.events()
        with self.assertRaises(ConflictDetected):
            sa.execute(command("stale", gen=0))
        self.assertEqual(sa.events(), before_events)

    def test_duplicate_command_cannot_create_second_event(self):
        sa = StateAuthority()
        first = sa.execute(command("same"))
        with self.assertRaises(DuplicateCommand):
            sa.execute(command("same", value="changed"))
        self.assertEqual(sa.events(), (first,))
        self.assertEqual(sa.read()["system"]["mode"], "ready")


if __name__ == "__main__":
    unittest.main()
