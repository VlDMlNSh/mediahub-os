"""MediaHub OS runtime foundation."""

from .authorization import AuthorizationContext, AuthorizationDecision, AuthorizationPolicy
from .configuration_policy import (
    Configuration,
    ConfigurationPolicyError,
    InvalidConfigurationPolicy,
    Policy,
    PolicyRule,
    validate_configuration,
    validate_policy,
)
from .configuration_policy_authorization import P0_07_CAPABILITIES, ConfigurationPolicyAuthorization
from .configuration_policy_operations import (
    ConfigurationPolicyOperationBoundary,
    ConfigurationPolicyOperationDecision,
    ConfigurationPolicyOperationRequest,
)
from .consumer_boundary import ConsumerBoundary, ConsumerBoundaryError, ConsumerTransaction, OperationRequest
from .coordination_service import (
    CoordinationRequest,
    CoordinationResult,
    CoordinationServiceError,
    RuntimeCoordinationService,
)
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
from .lifecycle_service import LifecycleRequest, LifecycleService
from .policy_evaluator import PolicyDecision, evaluate_policy
from .proposals import Proposal, ProposalAuthority
from .state import StateAuthority

__all__ = [
    "AuthorizationContext",
    "AuthorizationDecision",
    "AuthorizationPolicy",
    "AuthorizationDenied",
    "CanonicalState",
    "Checkpoint",
    "Configuration",
    "ConfigurationPolicyAuthorization",
    "ConfigurationPolicyError",
    "ConfigurationPolicyOperationBoundary",
    "ConfigurationPolicyOperationDecision",
    "ConfigurationPolicyOperationRequest",
    "ConsumerBoundary",
    "ConsumerBoundaryError",
    "ConsumerTransaction",
    "CoordinationRequest",
    "CoordinationResult",
    "CoordinationServiceError",
    "DiagnosticEvent",
    "ExpiredProposal",
    "Generation",
    "GenerationMismatch",
    "InMemoryStateAuthority",
    "IntegrityFailure",
    "InvalidCheckpoint",
    "InvalidConfigurationPolicy",
    "InvalidStateTransition",
    "InvalidTransaction",
    "LifecycleRequest",
    "LifecycleService",
    "LifecycleState",
    "LifecycleStateMachine",
    "MalformedState",
    "OperationRequest",
    "P0_07_CAPABILITIES",
    "Policy",
    "PolicyDecision",
    "PolicyRule",
    "Proposal",
    "ProposalAuthority",
    "RuntimeCoordinationService",
    "RuntimeInvariantError",
    "SelfTestFailure",
    "StaleTransaction",
    "StateAuthority",
    "Transaction",
    "evaluate_policy",
    "make_event",
    "sanitize_fields",
    "validate_configuration",
    "validate_generation_compatibility",
    "validate_policy",
]
