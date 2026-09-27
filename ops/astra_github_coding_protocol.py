"""GitHub-native bounded execution identity and evidence validation for Astra.

This module is deliberately transport-agnostic: it validates the identity and
fencing contract before a worker is allowed to perform a side effect.
"""
from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from typing import Mapping


class ProtocolError(ValueError):
    pass


REQUIRED_IDENTITY = (
    "schema_version",
    "task_id",
    "execution_id",
    "generation",
    "lease_id",
    "owner_id",
    "operation_key",
    "target_sha",
    "created_at",
    "expires_at",
)


@dataclass(frozen=True)
class ExecutionIdentity:
    schema_version: int
    task_id: str
    execution_id: str
    generation: int
    lease_id: str
    owner_id: str
    operation_key: str
    target_sha: str
    created_at: str
    expires_at: str

    @classmethod
    def from_mapping(cls, value: Mapping[str, object]) -> "ExecutionIdentity":
        missing = [key for key in REQUIRED_IDENTITY if key not in value]
        if missing:
            raise ProtocolError(f"missing identity fields: {missing}")
        if value["schema_version"] != 1:
            raise ProtocolError("unsupported schema_version")
        if not isinstance(value["generation"], int) or value["generation"] < 1:
            raise ProtocolError("generation must be a positive integer")
        strings = (
            "task_id", "execution_id", "lease_id", "owner_id",
            "operation_key", "target_sha", "created_at", "expires_at",
        )
        if any(not isinstance(value[key], str) or not value[key] for key in strings):
            raise ProtocolError("identity string fields must be non-empty")
        if (
            len(value["target_sha"]) != 40
            or any(ch not in "0123456789abcdefABCDEF" for ch in value["target_sha"])
        ):
            raise ProtocolError("target_sha must be a 40-character hexadecimal SHA")
        return cls(**{key: value[key] for key in REQUIRED_IDENTITY})  # type: ignore[arg-type]


def validate_fence(
    identity: ExecutionIdentity,
    *,
    task_id: str,
    execution_id: str,
    generation: int,
    lease_id: str,
    owner_id: str,
    target_sha: str,
) -> None:
    actual = (
        identity.task_id, identity.execution_id, identity.generation,
        identity.lease_id, identity.owner_id, identity.target_sha,
    )
    expected = (
        task_id, execution_id, generation, lease_id, owner_id, target_sha,
    )
    if actual != expected:
        raise ProtocolError("execution fenced: identity does not match current lease")


def validate_operation_key(identity: ExecutionIdentity, operation_key: str) -> None:
    if identity.operation_key != operation_key:
        raise ProtocolError("operation_key mismatch")


@dataclass(frozen=True)
class EvidenceEnvelope:
    identity: ExecutionIdentity
    worker: str
    model: str
    provider: str
    changed_files: tuple[str, ...]
    tests: tuple[str, ...]
    security_results: tuple[str, ...]
    commit_sha: str
    remote_sha: str
    artifact_sha256: str
    terminal_status: str

    def validate(self) -> None:
        if not self.worker or not self.model or not self.provider:
            raise ProtocolError("worker/model/provider are required")
        if not self.changed_files:
            raise ProtocolError("changed_files cannot be empty")
        if not self.tests:
            raise ProtocolError("tests cannot be empty")
        if not self.security_results:
            raise ProtocolError("security_results cannot be empty")
        if not self.commit_sha or self.remote_sha != self.commit_sha:
            raise ProtocolError("commit_sha must equal verified remote_sha")
        if len(self.artifact_sha256) != 64:
            raise ProtocolError("artifact_sha256 must be a SHA-256 hex digest")
        try:
            int(self.artifact_sha256, 16)
        except ValueError as exc:
            raise ProtocolError("artifact_sha256 is not hexadecimal") from exc
        if self.terminal_status not in {"SUCCEEDED", "FAILED", "BLOCKED"}:
            raise ProtocolError("invalid terminal_status")

    def digest(self) -> str:
        self.validate()
        material = "|".join((
            self.identity.task_id,
            self.identity.execution_id,
            str(self.identity.generation),
            self.identity.lease_id,
            self.identity.owner_id,
            self.identity.operation_key,
            self.identity.target_sha,
            self.worker,
            self.model,
            self.provider,
            ",".join(self.changed_files),
            ",".join(self.tests),
            ",".join(self.security_results),
            self.commit_sha,
            self.remote_sha,
            self.artifact_sha256,
            self.terminal_status,
        )).encode()
        return sha256(material).hexdigest()


def accept_result(
    evidence: EvidenceEnvelope,
    *,
    current: EvidenceEnvelope | None = None,
) -> str:
    evidence.validate()
    digest = evidence.digest()
    if current is None:
        return digest
    current.validate()
    if current.digest() != digest:
        raise ProtocolError("duplicate execution_id has conflicting evidence")
    return digest
