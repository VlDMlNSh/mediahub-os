import threading
import unittest

from runtime.mediahub_runtime.state_authority import (
    AuthorizationContext,
    Command,
    ConflictDetected,
    StateAuthority,
)


AUTH = AuthorizationContext("qualification-operator", True, frozenset({"state.write"}))


class MH04QualificationConcurrencyTests(unittest.TestCase):
    def test_concurrent_same_generation_has_single_winner(self):
        sa = StateAuthority({"counter": 0})
        generation = sa.metadata()["generation"]
        barrier = threading.Barrier(2)
        results = []

        def worker(command_id, value):
            barrier.wait()
            try:
                event = sa.execute(
                    Command(command_id, "corr-" + command_id, "set", ("counter",), value, generation, AUTH)
                )
                results.append(("ok", event.command_id))
            except ConflictDetected:
                results.append(("conflict", command_id))

        threads = [threading.Thread(target=worker, args=("concurrent-a", 1)), threading.Thread(target=worker, args=("concurrent-b", 2))]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(len(results), 2)
        self.assertEqual(sum(result[0] == "ok" for result in results), 1)
        self.assertEqual(sum(result[0] == "conflict" for result in results), 1)
        self.assertEqual(len(sa.events()), 1)
        self.assertEqual(sa.metadata()["generation"], 1)

    def test_observer_cannot_reenter_mutation_without_governed_authorization(self):
        sa = StateAuthority()
        attempts = []

        def observer(event):
            attempts.append(event.command_id)
            # An observer receives a fact, not mutation authority. A direct
            # command still requires an explicit authorization context.
            with self.assertRaises(Exception):
                sa.execute(Command("observer-bypass", "corr-observer", "set", ("x",), 99, None, None))

        sa.subscribe(observer)
        sa.execute(Command("source", "corr-source", "set", ("x",), 1, None, AUTH))
        self.assertEqual(attempts, ["source"])
        self.assertEqual(sa.read()["x"], 1)
        self.assertEqual(len(sa.events()), 1)


if __name__ == "__main__":
    unittest.main()
