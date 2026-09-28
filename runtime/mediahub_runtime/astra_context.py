"""Bounded context assembly for Astra sessions and projects."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .astra_memory import AstraMemory, MemoryRecord


@dataclass(frozen=True)
class AstraContextBudget:
    max_records: int = 12
    max_chars: int = 12_000


class AstraContextManager:
    """Deterministically assemble bounded durable context without becoming an authority."""

    def __init__(self, memory: AstraMemory, budget: AstraContextBudget | None = None):
        self.memory = memory
        self.budget = budget or AstraContextBudget()

    def select(
        self,
        query: str,
        *,
        task_id: str | None = None,
        session_id: str | None = None,
        project_id: str | None = None,
        context_refs: Iterable[str] = (),
    ) -> tuple[MemoryRecord, ...]:
        refs = tuple(str(ref).strip() for ref in context_refs if str(ref).strip())
        records = list(self.memory.select(query, task_id=task_id, session_id=session_id, project_id=project_id, limit=self.budget.max_records))
        if refs:
            selected_ids = {record.memory_id for record in records}
            for record in self.memory.records():
                if record.memory_id not in refs or record.memory_id in selected_ids:
                    continue
                if task_id and record.task_id not in (None, task_id):
                    continue
                if session_id and record.session_id not in (None, session_id):
                    continue
                if project_id and record.project_id not in (None, project_id):
                    continue
                records.append(record)
        return tuple(records[: self.budget.max_records])

    def build(
        self,
        query: str,
        *,
        task_id: str | None = None,
        session_id: str | None = None,
        project_id: str | None = None,
        context_refs: Iterable[str] = (),
    ) -> str:
        records = self.select(query, task_id=task_id, session_id=session_id, project_id=project_id, context_refs=context_refs)
        chunks: list[str] = []
        used = 0
        for record in records:
            chunk = (
                f"[{record.memory_class}] {record.content}"
                + (f" (tags: {', '.join(record.tags)})" if record.tags else "")
                + (f" (source: {record.source})" if record.source else "")
            )
            remaining = self.budget.max_chars - used
            if remaining <= 0:
                break
            if len(chunk) > remaining:
                chunk = chunk[:remaining].rstrip()
            if not chunk:
                continue
            chunks.append(chunk)
            used += len(chunk) + 1
        return "\n".join(chunks)


__all__ = ["AstraContextBudget", "AstraContextManager"]
