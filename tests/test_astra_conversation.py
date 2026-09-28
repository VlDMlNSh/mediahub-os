import tempfile
import unittest
from pathlib import Path

from runtime.mediahub_runtime.astra_memory import AstraMemory
from runtime.mediahub_runtime.astra_conversation import (
    AstraConversationCompactor,
    ConversationMessage,
)


class AstraConversationTests(unittest.TestCase):
    def test_raw_messages_survive_compaction(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            compactor = AstraConversationCompactor(memory)
            compactor.append_message(ConversationMessage("m1", "user", "Keep this raw message", "s1", "p1"))
            compactor.append_message(ConversationMessage("m2", "assistant", "And this response", "s1", "p1"))
            summary = compactor.compact("s1", project_id="p1")
            self.assertIsNotNone(summary)
            records = memory.records()
            self.assertEqual(len([r for r in records if "conversation:raw" in r.tags]), 2)
            self.assertEqual(len([r for r in records if "conversation:summary" in r.tags]), 1)

    def test_compaction_is_scoped(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            compactor = AstraConversationCompactor(memory)
            compactor.append_message(ConversationMessage("m1", "user", "project one", "s1", "p1"))
            compactor.append_message(ConversationMessage("m2", "user", "project two", "s1", "p2"))
            summary = compactor.compact("s1", project_id="p1")
            self.assertIn("project one", summary.content)
            self.assertNotIn("project two", summary.content)

    def test_summary_is_bounded(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            compactor = AstraConversationCompactor(memory, max_summary_chars=32)
            compactor.append_message(ConversationMessage("m1", "user", "x" * 100, "s1"))
            summary = compactor.compact("s1")
            self.assertLessEqual(len(summary.content), 32 + len("\n[summary truncated]"))

    def test_invalid_role_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            compactor = AstraConversationCompactor(AstraMemory(Path(tmp) / "memory.jsonl"))
            with self.assertRaises(ValueError):
                compactor.append_message(ConversationMessage("m1", "evil", "x", "s1"))


if __name__ == "__main__":
    unittest.main()
