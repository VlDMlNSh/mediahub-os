"""Controlled P0-05 consumer boundary around the frozen State Authority."""

from copy import deepcopy
from dataclasses import dataclass

from .authorization import AuthorizationContext
from .errors import AuthorizationDenied, GenerationMismatch, RuntimeInvariantError
from .in_memory_state import InvalidCheckpoint, InvalidTransaction, StaleTransaction
from .proposals import ProposalAuthority


class ConsumerBoundaryError(RuntimeError):
    """Stable, sanitized error exposed by the consumer boundary."""

    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class OperationRequest:
    """Inert consumer intent; it carries no executable capability."""

    operation: str
    context: AuthorizationContext


@dataclass(frozen=True)
class ConsumerTransaction:
    """Opaque consumer handle; the authority transaction is never exposed."""

    _authority_transaction: object


class ConsumerBoundary:
    """Narrow facade preserving State Authority exclusivity and fail-closed access."""

    _SANITIZED = {
        AuthorizationDenied: "authorization_denied",
        GenerationMismatch: "stale_generation",
        StaleTransaction: "stale_transaction",
        InvalidTransaction: "invalid_transaction",
        InvalidCheckpoint: "invalid_checkpoint",
        RuntimeInvariantError: "operation_rejected",
    }

    def __init__(self, authority, proposal_authority=None):
        self._authority = authority
        self._proposal_authority = proposal_authority or ProposalAuthority()

    @staticmethod
    def request(operation, context):
        if not isinstance(operation, str) or not operation:
            raise ConsumerBoundaryError("invalid_request")
        if not isinstance(context, AuthorizationContext):
            raise ConsumerBoundaryError("authorization_denied")
        return OperationRequest(operation, context)

    def read(self, key=None):
        return self._authority.read(key)

    def begin(self, request, payload=None):
        self._require_operation(request, "begin")
        try:
            tx = self._authority.begin(request.context, deepcopy(payload) if payload is not None else None)
            return ConsumerTransaction(tx)
        except Exception as exc:
            raise self._sanitize(exc) from exc

    def update(self, transaction, payload):
        tx = self._unwrap(transaction)
        try:
            tx.set_payload(deepcopy(payload))
        except Exception as exc:
            raise self._sanitize(exc) from exc

    def commit(self, request, transaction):
        self._require_operation(request, "commit")
        tx = self._unwrap(transaction)
        try:
            return self._authority.commit(tx)
        except Exception as exc:
            raise self._sanitize(exc) from exc

    def abort(self, request, transaction):
        self._require_operation(request, "abort")
        tx = self._unwrap(transaction)
        try:
            return self._authority.abort(tx)
        except Exception as exc:
            raise self._sanitize(exc) from exc

    def snapshot(self, request):
        self._require_operation(request, "snapshot")
        try:
            return self._authority.snapshot(request.context)
        except Exception as exc:
            raise self._sanitize(exc) from exc

    def restore(self, request, checkpoint):
        self._require_operation(request, "restore")
        try:
            return self._authority.restore(checkpoint, request.context)
        except Exception as exc:
            raise self._sanitize(exc) from exc

    def validate_proposal(self, proposal, now=None):
        """Validate inert proposal data without executing or mutating state."""
        try:
            return self._proposal_authority.validate(proposal, now)
        except Exception as exc:
            raise ConsumerBoundaryError("proposal_rejected") from exc

    @staticmethod
    def _require_operation(request, operation):
        if not isinstance(request, OperationRequest) or request.operation != operation:
            raise ConsumerBoundaryError("invalid_request")

    @staticmethod
    def _unwrap(transaction):
        if not isinstance(transaction, ConsumerTransaction):
            raise ConsumerBoundaryError("invalid_transaction")
        return transaction._authority_transaction

    @classmethod
    def _sanitize(cls, exc):
        for error_type, code in cls._SANITIZED.items():
            if isinstance(exc, error_type):
                return ConsumerBoundaryError(code)
        return ConsumerBoundaryError("operation_rejected")
