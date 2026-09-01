import unittest

from runtime.mediahub_runtime.authorization import AuthorizationContext, AuthorizationPolicy
from runtime.mediahub_runtime.generation import Generation
from runtime.mediahub_runtime.in_memory_state import (
    Checkpoint,
    InMemoryStateAuthority,
    IntegrityFailure,
    InvalidCheckpoint,
    InvalidTransaction,
    MalformedState,
    StaleTransaction,
    Transaction,
)


class InMemoryStateAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.context = AuthorizationContext("test-service", "state-admin")
        grants = {
            ("test-service", "state-admin", "begin"),
            ("test-service", "state-admin", "commit"),
            ("test-service", "state-admin", "abort"),
            ("test-service", "state-admin", "snapshot"),
            ("test-service", "state-admin", "restore"),
        }
        self.authority = InMemoryStateAuthority(
            Generation("g1", "b1", "s1", "0", "i1"),
            {"value": 0},
            AuthorizationPolicy(grants),
        )

    def test_read_isolation_and_authority_owned_version(self):
        before = self.authority.read()
        tx = self.authority.begin(self.context)
        tx.set_payload({"value": 1, "requested_version": 999})
        self.assertEqual(before.payload, {"value": 0})
        self.assertEqual(self.authority.read().payload, {"value": 0})
        committed = self.authority.commit(tx)
        self.assertEqual(committed.payload, {"value": 1, "requested_version": 999})
        self.assertEqual(committed.state_version, 1)
        self.assertEqual(committed.generation.state_version, "1")

    def test_stale_transaction_rejected_and_canonical_preserved(self):
        first = self.authority.begin(self.context)
        second = self.authority.begin(self.context)
        first.set_payload({"value": 1})
        second.set_payload({"value": 2})
        self.authority.commit(first)
        with self.assertRaises(StaleTransaction):
            self.authority.commit(second)
        self.assertEqual(self.authority.read().payload, {"value": 1})
        self.assertEqual(second.status, Transaction.ACTIVE)

    def test_abort_preserves_state_and_is_terminal(self):
        tx = self.authority.begin(self.context)
        tx.set_payload({"value": 5})
        self.authority.abort(tx)
        self.assertEqual(tx.status, Transaction.ABORTED)
        self.assertEqual(self.authority.read().payload, {"value": 0})
        with self.assertRaises(InvalidTransaction):
            tx.set_payload({"value": 6})
        self.assertIsNone(self.authority.abort(tx))

    def test_terminal_transaction_cannot_be_committed(self):
        tx = self.authority.begin(self.context)
        self.authority.abort(tx)
        with self.assertRaises(InvalidTransaction):
            self.authority.commit(tx)

    def test_unregistered_transaction_is_rejected(self):
        forged = Transaction("tx-forged", self.context, self.authority.read().generation, 0, {"value": 9})
        with self.assertRaises(InvalidTransaction):
            self.authority.commit(forged)

    def test_default_deny_is_preserved_per_operation(self):
        denied = InMemoryStateAuthority(Generation("g1", "b1", "s1", "0", "i1"))
        with self.assertRaises(Exception):
            denied.begin(self.context)
        with self.assertRaises(Exception):
            denied.snapshot(self.context)

    def test_integrity_is_independent_gate(self):
        rejecting = InMemoryStateAuthority(
            Generation("g1", "b1", "s1", "0", "i1"),
            {"value": 0},
            AuthorizationPolicy({
                ("test-service", "state-admin", "begin"),
                ("test-service", "state-admin", "commit"),
            }),
            integrity_validator=lambda _payload, _generation: False,
        )
        tx = rejecting.begin(self.context)
        tx.set_payload({"value": 1})
        with self.assertRaises(IntegrityFailure):
            rejecting.commit(tx)
        self.assertEqual(rejecting.read().payload, {"value": 0})
        self.assertEqual(rejecting.read().state_version, 0)

    def test_checkpoint_is_authority_bound_and_restore_creates_new_revision(self):
        self.authority.begin(self.context).set_payload({"value": 1})
        tx = self.authority.begin(self.context, {"value": 1})
        self.authority.commit(tx)
        checkpoint = self.authority.snapshot(self.context)
        tx2 = self.authority.begin(self.context, {"value": 2})
        self.authority.commit(tx2)
        restored = self.authority.restore(checkpoint, self.context)
        self.assertEqual(restored.payload, {"value": 1})
        self.assertEqual(restored.state_version, 3)
        self.assertEqual(checkpoint.state_version, 1)

    def test_forged_checkpoint_is_rejected(self):
        forged = Checkpoint("cp-forged", {"value": 99}, self.authority.read().generation, 0, True)
        with self.assertRaises(InvalidCheckpoint):
            self.authority.restore(forged, self.context)

    def test_checkpoint_identity_is_immutable(self):
        checkpoint = self.authority.snapshot(self.context)
        with self.assertRaises(Exception):
            checkpoint.checkpoint_id = "cp-mutated"
        self.assertEqual(checkpoint.checkpoint_id, "cp-1")

    def test_malformed_and_oversized_state_is_rejected(self):
        with self.assertRaises(MalformedState):
            self.authority.begin(self.context, {"bad": object()})
        with self.assertRaises(MalformedState):
            self.authority.begin(self.context, {"bad": "x" * 4097})

    def test_hostile_string_remains_data(self):
        payload = {"value": "$(touch /tmp/should-not-exist); subprocess.run()"}
        tx = self.authority.begin(self.context, payload)
        committed = self.authority.commit(tx)
        self.assertEqual(committed.payload, payload)


if __name__ == "__main__":
    unittest.main()
