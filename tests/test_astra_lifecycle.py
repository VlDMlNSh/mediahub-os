import tempfile
import unittest
from pathlib import Path

from runtime.mediahub_runtime.astra_memory import AstraMemory
from runtime.mediahub_runtime.astra_lifecycle import AstraMemoryLifecycle


class AstraLifecycleTests(unittest.TestCase):
    def test_superseded_record_is_not_active(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            lifecycle = AstraMemoryLifecycle(memory)
            old = lifecycle.remember_fact("old architecture", project_id="p1")
            lifecycle.remember_fact("new architecture", project_id="p1", supersedes=(old.memory_id,))
            active = lifecycle.active(project_id="p1")
            self.assertEqual([r.content for r in active], ["new architecture"])

    def test_confidence_is_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            lifecycle = AstraMemoryLifecycle(AstraMemory(Path(tmp) / "memory.jsonl"))
            with self.assertRaises(ValueError):
                lifecycle.remember_fact("bad", confidence=1.5)

    def test_github_confirmation_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            lifecycle = AstraMemoryLifecycle(AstraMemory(Path(tmp) / "memory.jsonl"))
            record = lifecycle.remember_fact("commit verified", authoritative_source=True)
            self.assertTrue(lifecycle.is_authoritative(record))


if __name__ == "__main__":
    unittest.main()
