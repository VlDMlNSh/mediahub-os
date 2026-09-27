"""MediaHub runtime foundation."""

from .event_projection import (
    CanonicalEvent,
    ProjectionError,
    project_runtime_event,
    validate_canonical_event,
)
from .evidence import EvidenceError, build_evidence_record
from .state_authority import (
    AuthorityUnavailable,
    AuthorizationContext,
    AuthorizationDenied,
    Command,
    ConflictDetected,
    DuplicateCommand,
    Event,
    InvalidCommand,
    StateAuthority,
    StateAuthorityError,
)

__all__ = [
    "AuthorityUnavailable",
    "AuthorizationContext",
    "AuthorizationDenied",
    "CanonicalEvent",
    "Command",
    "ConflictDetected",
    "DuplicateCommand",
    "Event",
    "EvidenceError",
    "InvalidCommand",
    "ProjectionError",
    "StateAuthority",
    "StateAuthorityError",
    "build_evidence_record",
    "project_runtime_event",
    "validate_canonical_event",
]
