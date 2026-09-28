import tempfile
import unittest
from pathlib import Path

from runtime.mediahub_runtime.astra_memory import AstraMemory
from runtime.mediahub_runtime.astra_retrieval import AstraRetriever


class FailingScorer:
    def score(self, query, records):
        raise RuntimeError("backend unavailable")


class AstraRetrievalTests(unittest.TestCase):
    def test_lexical_retrieval_is_deterministic_fallback(self):
        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            expected = memory.remember("project", "MediaHub architecture decision")
            memory.remember("episodic", "unrelated note")
            result = AstraRetriever(memory, FailingScorer()).retrieve("architecture", project_id=None)
            self.assertEqual(result.mode, "lexical_fallback")
            self.assertEqual(result.records[0].memory_id, expected.memory_id)

    def test_semantic_scores_only_re_rank_scoped_lexical_candidates(self):
        class Scorer:
            def score(self, query, records):
                return [0.1, 0.9]

        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            first = memory.remember("project", "alpha architecture")
            second = memory.remember("project", "architecture beta")
            result = AstraRetriever(memory, Scorer()).retrieve("architecture", limit=2)
            self.assertEqual(result.mode, "semantic")
            self.assertEqual(result.records[0].memory_id, second.memory_id)
            self.assertEqual({r.memory_id for r in result.records}, {first.memory_id, second.memory_id})

    def test_scope_is_enforced_before_semantic_scoring(self):
        class Scorer:
            def __init__(self):
                self.seen = None
            def score(self, query, records):
                self.seen = tuple(records)
                return [1.0] * len(records)

        with tempfile.TemporaryDirectory() as tmp:
            memory = AstraMemory(Path(tmp) / "memory.jsonl")
            allowed = memory.remember("project", "architecture", project_id="p1")
            memory.remember("project", "architecture", project_id="p2")
            scorer = Scorer()
            result = AstraRetriever(memory, scorer).retrieve("architecture", project_id="p1")
            self.assertEqual(result.records[0].memory_id, allowed.memory_id)
            self.assertEqual(len(scorer.seen), 1)


if __name__ == "__main__":
    unittest.main()
