"""Fail-closed model registry for autonomous development lanes.

Model identifiers are configuration, not hard-coded CLI truth. Retired or
explicitly denied identifiers cannot enter an execution target.
"""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class ModelRecord:
    provider: str
    model: str
    enabled: bool = True

class ModelRegistry:
    def __init__(self, records: tuple[ModelRecord, ...] = ()) -> None:
        self._records = {(r.provider, r.model): r for r in records}

    def require(self, provider: str, model: str) -> ModelRecord:
        record = self._records.get((provider, model))
        if record is None or not record.enabled:
            raise PermissionError(f"model not qualified: {provider}/{model}")
        return record

    def providers(self) -> tuple[str, ...]:
        return tuple(sorted({r.provider for r in self._records.values() if r.enabled}))
