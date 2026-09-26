"""Fail-closed model registry for autonomous development lanes."""
from __future__ import annotations

from dataclasses import dataclass
from time import time


@dataclass(frozen=True)
class ModelRecord:
    provider: str
    model: str
    enabled: bool = True
    version: str = ""
    digest: str = ""
    capabilities: tuple[str, ...] = ()
    context: int | None = None
    ram_mb: int | None = None
    latency_ms: float | None = None
    qualification_status: str = "QUALIFIED"
    last_qualified_at: float | None = None
    failure_history: tuple[str, ...] = ()
    task_classes: tuple[str, ...] = ()

    @property
    def qualified(self) -> bool:
        return self.enabled and self.qualification_status == "QUALIFIED"


class ModelRegistry:
    def __init__(self, records: tuple[ModelRecord, ...] = ()) -> None:
        if not isinstance(records, tuple) or any(not isinstance(r, ModelRecord) for r in records):
            raise ValueError("malformed model registry records")
        for r in records:
            if not isinstance(r.provider, str) or not r.provider or not isinstance(r.model, str) or not r.model:
                raise ValueError("malformed model registry record")
            if not isinstance(r.enabled, bool) or (r.context is not None and r.context < 1):
                raise ValueError("malformed model registry record")
        self._records = {(r.provider, r.model): r for r in records}

    def require(self, provider: str, model: str, capability: str | None = None) -> ModelRecord:
        record = self._records.get((provider, model))
        if record is None or not record.qualified:
            raise PermissionError(f"model not qualified: {provider}/{model}")
        if capability is not None and capability not in record.capabilities:
            raise PermissionError(f"model capability not qualified: {provider}/{model}/{capability}")
        return record

    def register_qualification(self, record: ModelRecord, *, qualified: bool, now: float | None = None) -> ModelRecord:
        status = "QUALIFIED" if qualified else "NOT_QUALIFIED"
        updated = ModelRecord(
            provider=record.provider, model=record.model, enabled=record.enabled,
            version=record.version, digest=record.digest, capabilities=record.capabilities,
            context=record.context, ram_mb=record.ram_mb, latency_ms=record.latency_ms,
            qualification_status=status, last_qualified_at=time() if now is None else now,
            failure_history=record.failure_history, task_classes=record.task_classes,
        )
        self._records[(record.provider, record.model)] = updated
        return updated

    def providers(self) -> tuple[str, ...]:
        return tuple(sorted({r.provider for r in self._records.values() if r.enabled and r.qualified}))

    def records(self) -> tuple[ModelRecord, ...]:
        return tuple(self._records[key] for key in sorted(self._records))

    def candidates(self, capability: str, task_class: str | None = None) -> tuple[ModelRecord, ...]:
        rows = [r for r in self._records.values() if r.qualified and capability in r.capabilities]
        if task_class:
            rows = [r for r in rows if task_class in r.task_classes]
        return tuple(sorted(rows, key=lambda r: (r.latency_ms if r.latency_ms is not None else float("inf"), r.provider, r.model)))
