"""MediaHub OS runtime foundation."""

from .authorization import AuthorizationContext, AuthorizationDecision, AuthorizationPolicy
from .consumer_boundary import ConsumerBoundary, ConsumerBoundaryError, ConsumerTransaction, OperationRequest
from .diagnostics import DiagnosticEvent, make_event, sanitize_fields
from .errors import (
    AuthorizationDenied,
    ExpiredProposal,
    GenerationMismatch,
    InvalidStateTransition,
    RuntimeInvariantError,
)
from .generation import Generation, validate_generation_compatibility
from .in_memory_state import (
    CanonicalState,
    Checkpoint,
    InMemoryStateAuthority,
    IntegrityFailure,
    InvalidCheckpoint,
    InvalidTransaction,
    MalformedState,
    SelfTestFailure,
    StaleTransaction,
    Transaction,
)
from .lifecycle import LifecycleState, LifecycleStateMachine
from .proposals import Proposal, ProposalAuthority
from .state import StateAuthority

__all__ = [
    "AuthorizationContext",
    "AuthorizationDecision",
    "AuthorizationPolicy",
    "AuthorizationDenied",
    "CanonicalState",
    "Checkpoint",
    "ConsumerBoundary",
    "ConsumerBoundaryError",
    "ConsumerTransaction",
    "DiagnosticEvent",
    "ExpiredProposal",
    "Generation",
    "GenerationMismatch",
    "InMemoryStateAuthority",
    "IntegrityFailure",
    "InvalidCheckpoint",
    "InvalidStateTransition",
    "InvalidTransaction",
    "LifecycleState",
    "LifecycleStateMachine",
    "MalformedState",
    "OperationRequest",
    "Proposal",
    "ProposalAuthority",
    "RuntimeInvariantError",
    "SelfTestFailure",
    "StaleTransaction",
    "StateAuthority",
    "Transaction",
    "make_event",
    "sanitize_fields",
    "validate_generation_compatibility",
]
