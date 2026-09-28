"""Provenance and lifecycle controls for durable Astra memory."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .astra_memory import AstraMemory, MemoryRecord


@dataclass(frozen=True)
class MemoryLifecycle:
    supersedes: tuple[str, ...] = ()
    confidence: float = 0.5
    authoritative_source: bool = False


class AstraMemoryLifecycle:
    """Derived lifecycle metadata; it never elevates memory above system authority."""

    def __init__(self, memory: AstraMemory):
        self.memory = memory

    def remember_fact(
        self,
        content: str,
        *,
        memory_class: str = "semantic",
        session_id: str | None = None,
        project_id: str | None = None,
        task_id: str | None = None,
        source: str | None = None,
        tags: Iterable[str] = (),
        supersedes: Iterable[str] = (),
        confidence: float = 0.5,
        authoritative_source: bool = False,
    ) -> MemoryRecord:
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("confidence_out_of_range")
        superseded = tuple(dict.fromkeys(supersedes))
        lifecycle_tags = tuple(tags) + tuple(f"supersedes:{item}" for item in superseded)
        if authoritative_source:
            lifecycle_tags += ("source:github-confirmed",)
        lifecycle_tags += (f"confidence:{confidence:.3f}",)
        return self.memory.remember(
            memory_class,
            content,
            session_id=session_id,
            project_id=project_id,
            task_id=task_id,
            source=source,
            tags=lifecycle_tags,
        )

    def active(self, *, session_id: str | None = None, project_id: str | None = None) -> tuple[MemoryRecord, ...]:
        records = self.memory.records()
        superseded_ids = {
            tag.split(":", 1)[1]
            for record in records
            for tag in record.tags
            if tag.startswith("supersedes:") and ":" in tag
        }
        return tuple(
            record for record in records
            if record.memory_id not in superseded_ids
            and (session_id is None or record.session_id in (None, session_id))
            and (project_id is None or record.project_id in (None, project_id))
        )

    @staticmethod
    def is_authoritative(record: MemoryRecord) -> bool:
        return "source:github-confirmed" in record.tags


__all__ = ["AstraMemoryLifecycle", "MemoryLifecycle"]
