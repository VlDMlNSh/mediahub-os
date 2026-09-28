"""Deterministic retrieval adapter with optional semantic backend.

The lexical selector remains the mandatory fallback. Semantic backends are
advisory ranking hints only and can never bypass memory scope or budgets.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Sequence

from .astra_memory import AstraMemory, MemoryRecord


class SemanticScorer(Protocol):
    def score(self, query: str, records: Sequence[MemoryRecord]) -> Sequence[float]:
        """Return one score per record; failures are handled by the caller."""


@dataclass(frozen=True)
class RetrievalResult:
    records: tuple[MemoryRecord, ...]
    mode: str


class AstraRetriever:
    def __init__(self, memory: AstraMemory, semantic_scorer: SemanticScorer | None = None):
        self.memory = memory
        self.semantic_scorer = semantic_scorer

    def retrieve(
        self,
        query: str,
        *,
        task_id: str | None = None,
        session_id: str | None = None,
        project_id: str | None = None,
        memory_classes: Sequence[str] | None = None,
        limit: int = 8,
    ) -> RetrievalResult:
        lexical = self.memory.select(
            query,
            memory_classes=memory_classes or self.memory_classes(),
            task_id=task_id,
            session_id=session_id,
            project_id=project_id,
            limit=limit,
        )
        if not self.semantic_scorer or not lexical:
            return RetrievalResult(lexical, "lexical")

        try:
            scores = tuple(float(value) for value in self.semantic_scorer.score(query, lexical))
            if len(scores) != len(lexical):
                raise ValueError("semantic_score_count_mismatch")
            ranked = tuple(record for _, record in sorted(
                zip(scores, lexical), key=lambda item: (-item[0], item[1].memory_id)
            ))
            return RetrievalResult(ranked, "semantic")
        except Exception:
            return RetrievalResult(lexical, "lexical_fallback")

    def memory_classes(self) -> Sequence[str]:
        return ("working", "episodic", "semantic", "procedural", "project")


__all__ = ["AstraRetriever", "RetrievalResult", "SemanticScorer"]
