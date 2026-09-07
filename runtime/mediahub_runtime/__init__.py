"""MediaHub runtime foundation."""

from .event_projection import CanonicalEvent, ProjectionError, project_runtime_event, validate_canonical_event
from .evidence import EvidenceError, build_evidence_record
from .state_authority import (
    AuthorizationContext,
    Command,
    Event,
    StateAuthority,
    StateAuthorityError,
    AuthorizationDenied,
    ConflictDetected,
    DuplicateCommand,
    InvalidCommand,
    AuthorityUnavailable,
)

__all__ = [
    "AuthorizationContext",
    "Command",
    "Event",
    "StateAuthority",
    "StateAuthorityError",
    "AuthorizationDenied",
    "ConflictDetected",
    "DuplicateCommand",
    "InvalidCommand",
    "AuthorityUnavailable",
    "CanonicalEvent",
    "ProjectionError",
    "project_runtime_event",
    "validate_canonical_event",
    "EvidenceError",
    "build_evidence_record",
]
