"""Provider-neutral, fail-closed boundary for development AI workers."""
from __future__ import annotations

from dataclasses import dataclass, field

FORBIDDEN = frozenset({"production", "secrets", "state-authority", "host-filesystem"})


class AdapterDenied(PermissionError):
    """Raised when an AI request cannot be admitted safely."""


@dataclass(frozen=True)
class ProviderRequest:
    task_id: str
    capabilities: frozenset[str] = frozenset()
    egress: frozenset[str] = frozenset()
    timeout_seconds: int = 60
    data: str = ""


@dataclass
class AIAdapter:
    authorized: bool = False
    revoked: bool = False
    allowed_egress: frozenset[str] = frozenset()
    max_timeout_seconds: int = 900
    audit_events: list[dict[str, str]] = field(default_factory=list)

    def authorize(self, allowed_egress: frozenset[str] = frozenset()) -> None:
        if self.revoked:
            raise AdapterDenied("adapter is revoked")
        self.allowed_egress = allowed_egress
        self.authorized = True
        self.audit_events.append({"event": "authorized"})

    def revoke(self) -> None:
        self.revoked = True
        self.authorized = False
        self.audit_events.append({"event": "revoked"})

    def admit(self, request: ProviderRequest) -> None:
        if not request.task_id or not self.authorized or self.revoked:
            raise AdapterDenied("request is not authorized")
        if request.capabilities & FORBIDDEN:
            raise AdapterDenied("forbidden capability")
        if request.egress - self.allowed_egress:
            raise AdapterDenied("egress is not allowlisted")
        if not 1 <= request.timeout_seconds <= self.max_timeout_seconds:
            raise AdapterDenied("timeout is outside the bounded policy")
        self.audit_events.append({"event": "admitted", "task_id": request.task_id})

    def provenance(self, request: ProviderRequest, source_sha: str) -> dict[str, str]:
        if not source_sha or not request.task_id:
            raise AdapterDenied("provenance is incomplete")
        return {
            "task_id": request.task_id,
            "source_sha": source_sha,
            "adapter": "mediahub.provider-neutral.v1",
        }
