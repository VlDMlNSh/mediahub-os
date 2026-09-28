import tempfile
import unittest
from pathlib import Path

from runtime.mediahub_runtime.astra_memory import AstraMemory, MEMORY_CLASSES


class AstraMemoryTests(unittest.TestCase):
    def test_all_memory_classes_persist_and_reload(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            for memory_class in MEMORY_CLASSES:
                memory.remember(
                    memory_class,
                    f"{memory_class} qualification evidence",
                    tags=("qualification", memory_class),
                    task_id="gold-1",
                )
            reloaded = AstraMemory(Path(tmp) / "memory.jsonl")
            self.assertEqual(
                {record.memory_class for record in reloaded.records()},
                set(MEMORY_CLASSES),
            )

    def test_selector_prefers_relevant_project_and_task_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            memory.remember("project", "Astra GOLD qualification requires fresh evidence", importance=0.6)
            memory.remember("episodic", "unrelated mobile UI observation", task_id="other")
            memory.remember("procedural", "qualification verify pre-soak bundle", task_id="gold-1")
            selected = memory.select("GOLD qualification evidence", task_id="gold-1", limit=2)
            self.assertEqual(len(selected), 2)
            self.assertEqual(selected[0].memory_class, "project")

    def test_working_memory_ttl_is_expired(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            record = memory.remember("working", "temporary selection", ttl_seconds=0)
            self.assertTrue(record.expired())
            self.assertEqual(memory.records(), ())


if __name__ == "__main__":
    unittest.main()
