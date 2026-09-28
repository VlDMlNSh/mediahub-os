"""Durable conversation log and bounded hierarchical compaction for Astra.

Raw messages are retained as immutable episodic records. Compaction creates
derived summary records; it never deletes or rewrites the raw messages.
Derived summaries are advisory context and do not carry authority.
"""
from __future__ import annotations

from dataclasses import dataclass

from .astra_memory import AstraMemory, MemoryRecord


@dataclass(frozen=True)
class ConversationMessage:
    message_id: str
    role: str
    content: str
    session_id: str
    project_id: str | None = None
    task_id: str | None = None


class AstraConversationCompactor:
    """Persist raw conversation messages and derive bounded summaries."""

    RAW_TAG = "conversation:raw"
    SUMMARY_TAG = "conversation:summary"

    def __init__(self, memory: AstraMemory, max_summary_chars: int = 4_000):
        if max_summary_chars <= 0:
            raise ValueError("invalid_summary_budget")
        self.memory = memory
        self.max_summary_chars = max_summary_chars

    def append_message(self, message: ConversationMessage) -> MemoryRecord:
        if message.role not in {"system", "user", "assistant", "tool"}:
            raise ValueError("invalid_message_role")
        return self.memory.remember(
            "episodic",
            message.content,
            tags=(self.RAW_TAG, f"role:{message.role}", f"message:{message.message_id}"),
            task_id=message.task_id,
            session_id=message.session_id,
            project_id=message.project_id,
            source=f"message:{message.message_id}",
        )

    def compact(
        self,
        session_id: str,
        *,
        project_id: str | None = None,
        task_id: str | None = None,
    ) -> MemoryRecord | None:
        raw = [
            record for record in self.memory.records()
            if self.RAW_TAG in record.tags
            and record.session_id == session_id
            and (project_id is None or record.project_id == project_id)
            and (task_id is None or record.task_id in (None, task_id))
        ]
        if not raw:
            return None

        lines = []
        for record in raw:
            role = next((tag[5:] for tag in record.tags if tag.startswith("role:")), "unknown")
            lines.append(f"{role}: {record.content}")
        summary = "\n".join(lines)
        if len(summary) > self.max_summary_chars:
            summary = summary[: self.max_summary_chars].rstrip() + "\n[summary truncated]"
        return self.memory.remember(
            "semantic",
            summary,
            tags=(self.SUMMARY_TAG, f"session:{session_id}", *((
                f"project:{project_id}",
            ) if project_id else ())),
            session_id=session_id,
            project_id=project_id,
            task_id=task_id,
            source=f"compaction:session:{session_id}",
        )


__all__ = ["AstraConversationCompactor", "ConversationMessage"]
