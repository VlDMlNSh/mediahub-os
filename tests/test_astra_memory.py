import tempfile
import unittest
from pathlib import Path

from runtime.mediahub_runtime.astra_memory import AstraMemory, MEMORY_CLASSES
from runtime.mediahub_runtime.astra_context import AstraContextBudget, AstraContextManager


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
                    session_id="session-1",
                    project_id="project-1",
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

    def test_context_manager_enforces_record_and_character_budget(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            memory.remember("project", "project architecture decision " + ("x" * 100))
            memory.remember("episodic", "recent session result")
            context = AstraContextManager(memory, AstraContextBudget(max_records=1, max_chars=80))
            rendered = context.build("project architecture")
            self.assertLessEqual(len(rendered), 80)
            self.assertTrue(rendered.startswith("[project]"))

    def test_context_manager_can_retrieve_explicit_memory_reference(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            record = memory.remember("semantic", "stable project fact")
            context = AstraContextManager(memory)
            selected = context.select("unrelated query", context_refs=(record.memory_id,))
            self.assertEqual(selected[0].memory_id, record.memory_id)

    def test_memory_scopes_by_session_and_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            memory.remember("project", "shared project fact", session_id="s1", project_id="p1")
            memory.remember("project", "other project fact", session_id="s2", project_id="p2")
            selected = memory.select("project fact", session_id="s1", project_id="p1")
            self.assertEqual(len(selected), 1)
            self.assertEqual(selected[0].project_id, "p1")

    def test_explicit_reference_cannot_escape_project_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            foreign = memory.remember("project", "foreign project fact", session_id="s2", project_id="p2")
            selected = AstraContextManager(memory).select(
                "unrelated", session_id="s1", project_id="p1", context_refs=(foreign.memory_id,)
            )
            self.assertEqual(selected, ())

    def test_explicit_reference_respects_session_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            foreign = memory.remember("project", "foreign session fact", session_id="s2", project_id="p1")
            selected = AstraContextManager(memory).select(
                "unrelated", session_id="s1", project_id="p1", context_refs=(foreign.memory_id,)
            )
            self.assertEqual(selected, ())

    def test_context_manager_scopes_to_session_and_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            memory.remember("project", "MediaHub architecture", session_id="s1", project_id="p1")
            memory.remember("project", "unrelated architecture", session_id="s2", project_id="p2")
            context = AstraContextManager(memory)
            rendered = context.build("architecture", session_id="s1", project_id="p1")
            self.assertIn("MediaHub architecture", rendered)
            self.assertNotIn("unrelated architecture", rendered)


if __name__ == "__main__":
    unittest.main()
