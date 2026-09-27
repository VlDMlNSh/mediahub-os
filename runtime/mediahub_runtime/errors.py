"""Typed runtime foundation errors."""


class RuntimeInvariantError(Exception):
    """Base class for deterministic runtime invariant failures."""


class InvalidStateTransition(RuntimeInvariantError):
    """Raised when a lifecycle transition is not explicitly permitted."""


class GenerationMismatch(RuntimeInvariantError):
    """Raised when runtime generation components are incompatible."""


class AuthorizationDenied(RuntimeInvariantError):
    """Raised when an operation is not explicitly authorized."""


class ExpiredProposal(RuntimeInvariantError):
    """Raised when an AI proposal is no longer valid."""
