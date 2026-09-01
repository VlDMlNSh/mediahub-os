"""MediaHub OS runtime foundation."""

from .authorization import AuthorizationContext, AuthorizationDecision, AuthorizationPolicy
from .diagnostics import DiagnosticEvent, make_event, sanitize_fields
from .errors import (
    AuthorizationDenied,
    ExpiredProposal,
    GenerationMismatch,
    InvalidStateTransition,
    RuntimeInvariantError,
)
from .generation import Generation, validate_generation_compatibility
from .lifecycle import LifecycleState, LifecycleStateMachine
from .proposals import Proposal, ProposalAuthority
from .state import StateAuthority

__all__ = [
    "AuthorizationContext",
    "AuthorizationDecision",
    "AuthorizationPolicy",
    "AuthorizationDenied",
    "DiagnosticEvent",
    "ExpiredProposal",
    "Generation",
    "GenerationMismatch",
    "InvalidStateTransition",
    "LifecycleState",
    "LifecycleStateMachine",
    "Proposal",
    "ProposalAuthority",
    "RuntimeInvariantError",
    "StateAuthority",
    "make_event",
    "sanitize_fields",
    "validate_generation_compatibility",
]
