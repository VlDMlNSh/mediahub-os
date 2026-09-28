"""Durable multi-class memory for Astra's control loop.

The memory layer is an evidence store, not an authority source. It keeps
working, episodic, semantic, procedural, and project memory in a single
append-only JSONL journal and provides bounded relevance selection.
Secrets are never accepted as a special field and callers should redact
sensitive values before recording.
"""
from __future__ import annotations

import json
import re
import time
import uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable, Sequence

from .astra_security import redact, require_safe

MEMORY_CLASSES = (
    "working",
    "episodic",
    "semantic",
    "procedural",
    "project",
)

_TOKEN_RE = re.compile(r"[a-z0-9_./:-]+", re.IGNORECASE)


@dataclass(frozen=True)
class MemoryRecord:
    memory_id: str
    memory_class: str
    content: str
    created_at: float
    updated_at: float
    importance: float = 0.5
    tags: tuple[str, ...] = field(default_factory=tuple)
    task_id: str | None = None
    session_id: str | None = None
    project_id: str | None = None
    source: str | None = None
    ttl_seconds: float | None = None

    def __post_init__(self) -> None:
        if self.memory_class not in MEMORY_CLASSES:
            raise ValueError("invalid_memory_class")
        if not self.content.strip():
            raise ValueError("empty_memory_content")
        if not 0.0 <= self.importance <= 1.0:
            raise ValueError("importance_out_of_range")

    def expired(self, now: float | None = None) -> bool:
        if self.ttl_seconds is None:
            return False
        now = time.time() if now is None else now
        return now > self.updated_at + self.ttl_seconds


class AstraMemory:
    """Append-only durable memory with deterministic bounded retrieval."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def remember(
        self,
        memory_class: str,
        content: str,
        *,
        importance: float = 0.5,
        tags: Iterable[str] = (),
        task_id: str | None = None,
        session_id: str | None = None,
        project_id: str | None = None,
        source: str | None = None,
        ttl_seconds: float | None = None,
        memory_id: str | None = None,
    ) -> MemoryRecord:
        safe_content = require_safe(content, "content") or ""
        safe_source = require_safe(source, "source")
        safe_tags = tuple(require_safe(str(tag), "tag") or "" for tag in tags)
        now = time.time()
        record = MemoryRecord(
            memory_id=memory_id or uuid.uuid4().hex,
            memory_class=memory_class,
            content=safe_content.strip(),
            created_at=now,
            updated_at=now,
            importance=importance,
            tags=tuple(sorted({tag.strip() for tag in safe_tags if tag.strip()})),
            task_id=task_id,
            session_id=session_id,
            project_id=project_id,
            source=safe_source,
            ttl_seconds=ttl_seconds,
        )
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(record), sort_keys=True) + "\n")
        return record

    def records(self, *, include_expired: bool = False) -> tuple[MemoryRecord, ...]:
        if not self.path.exists():
            return ()
        latest: dict[str, MemoryRecord] = {}
        with self.path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if not line.strip():
                    continue
                payload = json.loads(line)
                record = MemoryRecord(
                    memory_id=payload["memory_id"],
                    memory_class=payload["memory_class"],
                    content=payload["content"],
                    created_at=float(payload["created_at"]),
                    updated_at=float(payload["updated_at"]),
                    importance=float(payload.get("importance", 0.5)),
                    tags=tuple(payload.get("tags", ())),
                    task_id=payload.get("task_id"),
                    session_id=payload.get("session_id"),
                    project_id=payload.get("project_id"),
                    source=payload.get("source"),
                    ttl_seconds=payload.get("ttl_seconds"),
                )
                latest[record.memory_id] = record
        values = tuple(latest.values())
        if include_expired:
            return values
        return tuple(record for record in values if not record.expired())

    def select(
        self,
        query: str,
        *,
        memory_classes: Sequence[str] = MEMORY_CLASSES,
        task_id: str | None = None,
        session_id: str | None = None,
        project_id: str | None = None,
        limit: int = 8,
    ) -> tuple[MemoryRecord, ...]:
        if limit <= 0:
            return ()
        allowed = set(memory_classes)
        query_tokens = set(_TOKEN_RE.findall(query.lower()))
        candidates: list[tuple[float, MemoryRecord]] = []
        now = time.time()
        for record in self.records():
            if record.memory_class not in allowed:
                continue
            if task_id and record.task_id not in (None, task_id):
                continue
            if session_id and record.session_id not in (None, session_id):
                continue
            if project_id and record.project_id not in (None, project_id):
                continue
            content_tokens = set(_TOKEN_RE.findall(record.content.lower()))
            tag_tokens = set(_TOKEN_RE.findall(" ".join(record.tags).lower()))
            overlap = len(query_tokens & (content_tokens | tag_tokens))
            recency = 1.0 / (1.0 + max(0.0, now - record.updated_at) / 3600.0)
            class_bonus = 0.15 if record.memory_class == "project" else 0.0
            score = overlap * 2.0 + record.importance + recency + class_bonus
            if overlap or not query_tokens:
                candidates.append((score, record))
        candidates.sort(key=lambda item: (-item[0], item[1].memory_id))
        return tuple(record for _, record in candidates[:limit])

    def export_context(self, records: Iterable[MemoryRecord]) -> str:
        return "\n".join(
            f"[{record.memory_class}] {redact(record.content)}"
            + (
                f" (tags: {', '.join(redact(tag) for tag in record.tags)})"
                if record.tags
                else ""
            )
            for record in records
        )


__all__ = ["AstraMemory", "MEMORY_CLASSES", "MemoryRecord"]
