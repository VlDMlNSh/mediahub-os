import unittest

from runtime.mediahub_runtime.astra_context import AstraContextManager
from runtime.mediahub_runtime.astra_memory import MemoryRecord


class _Memory:
    def __init__(self, record):
        self.record = record

    def select(self, *args, **kwargs):
        return (self.record,)

    def records(self):
        return (self.record,)


class AstraContextRedactionTests(unittest.TestCase):
    def test_prompt_assembly_redacts_legacy_secret_like_memory(self):
        record = MemoryRecord(
            memory_id="legacy",
            memory_class="episodic",
            content="api_key=legacy-secret-value",
            created_at=0,
            updated_at=0,
            tags=("tag",),
            source="Bearer legacy-token-value",
        )
        prompt = AstraContextManager(_Memory(record)).compose_prompt("continue")
        self.assertNotIn("legacy-secret-value", prompt)
        self.assertNotIn("legacy-token-value", prompt)
        self.assertIn("[REDACTED_SECRET]", prompt)


if __name__ == "__main__":
    unittest.main()
