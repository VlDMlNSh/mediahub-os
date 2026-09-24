"""Immutable task/evidence lineage primitives for MediaHub."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any


class LineageError(RuntimeError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def canonical_json(value: Any) -> bytes:
    try:
        return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise LineageError("non_canonical_value") from exc


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value)).hexdigest()


@dataclass(frozen=True)
class TaskEvidenceLineage:
    request_id: str
    contract_sha256: str
    evidence_sha256: str
    lineage_sha256: str

    @classmethod
    def create(cls, request_id: str, contract: dict, evidence: dict) -> "TaskEvidenceLineage":
        if not isinstance(request_id, str) or not request_id:
            raise LineageError("invalid_request_id")
        contract_hash = sha256_json(contract)
        evidence_hash = sha256_json(evidence)
        lineage_hash = hashlib.sha256(
            f"{request_id}\n{contract_hash}\n{evidence_hash}".encode("ascii")
        ).hexdigest()
        return cls(request_id, contract_hash, evidence_hash, lineage_hash)

    def verify(self, contract: dict, evidence: dict) -> bool:
        expected = TaskEvidenceLineage.create(self.request_id, contract, evidence)
        return self == expected

    def as_dict(self) -> dict[str, str]:
        return {
            "request_id": self.request_id,
            "contract_sha256": self.contract_sha256,
            "evidence_sha256": self.evidence_sha256,
            "lineage_sha256": self.lineage_sha256,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TaskEvidenceLineage":
        if not isinstance(data, dict):
            raise LineageError("invalid_lineage")
        values = tuple(data.get(k) for k in ("request_id", "contract_sha256", "evidence_sha256", "lineage_sha256"))
        if any(not isinstance(v, str) or not v for v in values):
            raise LineageError("invalid_lineage")
        if any(len(v) != 64 for v in values[1:]):
            raise LineageError("invalid_lineage")
        return cls(*values)
