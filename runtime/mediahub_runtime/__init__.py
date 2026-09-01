"""MediaHub OS runtime foundation."""

from .authorization import AuthorizationContext, AuthorizationDecision, AuthorizationPolicy
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

__all__ = [
    "AuthorizationContext",
    "AuthorizationDecision",
    "AuthorizationPolicy",
    "AuthorizationDenied",
    "ExpiredProposal",
    "Generation",
    "GenerationMismatch",
    "InvalidStateTransition",
    "LifecycleState",
    "LifecycleStateMachine",
    "Proposal",
    "ProposalAuthority",
    "RuntimeInvariantError",
    "validate_generation_compatibility",
]
