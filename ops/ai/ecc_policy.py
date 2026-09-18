"""Fail-closed MediaHub policy boundary for bounded ECC advisory roles."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ECCDenied(PermissionError):
    """Raised when an ECC request exceeds the advisory policy boundary."""


class ECCRole(StrEnum):
    EXPLORER = "explorer"
    REVIEWER = "reviewer"
    DOCS_RESEARCHER = "docs-researcher"
    VERIFICATION_LOOP = "verification-loop"


FORBIDDEN_CAPABILITIES = frozenset(
    {
        "state-authority",
        "production",
        "release",
        "secrets",
        "credential-access",
        "network-write",
    }
)


@dataclass(frozen=True)
class ECCRequest:
    task_id: str
    role: ECCRole
    source_sha: str
    capabilities: frozenset[str] = frozenset()
    scope: str = "advisory"


@dataclass(frozen=True)
class ECCAuthorization:
    task_id: str
    role: ECCRole
    source_sha: str
    capabilities: frozenset[str]
    scope: str = "advisory"


@dataclass
class ECCPolicy:
    """Admit only provenance-bound, advisory ECC work; never execute it."""

    audit_events: list[dict[str, str]] = field(default_factory=list)

    def admit(self, request: ECCRequest) -> ECCAuthorization:
        if not isinstance(request, ECCRequest):
            raise ECCDenied("malformed ECC request")
        if not all(isinstance(value, str) for value in (request.task_id, request.source_sha, request.scope)):
            raise ECCDenied("malformed ECC request fields")
        if not request.task_id or not request.source_sha:
            raise ECCDenied("ECC provenance is required")
        if request.scope != "advisory":
            raise ECCDenied("ECC scope must remain advisory")
        if not isinstance(request.role, ECCRole):
            raise ECCDenied("ECC role is not allowlisted")
        if not request.capabilities <= frozenset({"read-repo", "review", "docs", "verify"}):
            raise ECCDenied("ECC capability is not allowlisted")
        if request.capabilities & FORBIDDEN_CAPABILITIES:
            raise ECCDenied("ECC capability is forbidden")
        authorization = ECCAuthorization(
            request.task_id,
            request.role,
            request.source_sha,
            request.capabilities,
        )
        self.audit_events.append(
            {"event": "admitted", "task_id": request.task_id, "role": request.role.value}
        )
        return authorization
