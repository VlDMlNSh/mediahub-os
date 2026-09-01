"""Deterministic in-memory State Authority implementation for P0-04."""

from dataclasses import dataclass, field
from types import MappingProxyType
import math
import threading

from .authorization import AuthorizationContext, AuthorizationPolicy
from .errors import AuthorizationDenied, GenerationMismatch, RuntimeInvariantError
from .generation import Generation
from .state import StateAuthority

_MAX_DEPTH = 8
_MAX_NODES = 512
_MAX_STRING = 4096
_MAX_KEY_LENGTH = 128
_MAX_KEYS = 64


class MalformedState(RuntimeInvariantError):
    """Raised when a state payload violates structural bounds."""


class IntegrityFailure(RuntimeInvariantError):
    """Raised when independent integrity validation rejects a payload."""


class InvalidTransaction(RuntimeInvariantError):
    """Raised when a transaction is not valid for the requested operation."""


class StaleTransaction(RuntimeInvariantError):
    """Raised when a transaction no longer targets the current canonical revision."""


class InvalidCheckpoint(RuntimeInvariantError):
    """Raised when a checkpoint is not an accepted immutable checkpoint."""


def _validate_value(value, depth=0, budget=None):
    budget = [0] if budget is None else budget
    budget[0] += 1
    if budget[0] > _MAX_NODES or depth > _MAX_DEPTH:
        raise MalformedState("state payload exceeds structural bounds")
    if value is None or isinstance(value, (bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise MalformedState("state payload contains non-finite number")
        return
    if isinstance(value, str):
        if len(value) > _MAX_STRING:
            raise MalformedState("state payload contains oversized string")
        return
    if isinstance(value, (list, tuple)):
        for item in value:
            _validate_value(item, depth + 1, budget)
        return
    if isinstance(value, dict):
        if len(value) > _MAX_KEYS:
            raise MalformedState("state payload contains too many keys")
        for key, item in value.items():
            if not isinstance(key, str) or len(key) > _MAX_KEY_LENGTH:
                raise MalformedState("state payload contains invalid key")
            _validate_value(item, depth + 1, budget)
        return
    raise MalformedState("state payload contains unsupported value type")


def _freeze(value):
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_freeze(item) for item in value)
    return value


def _thaw(value):
    if isinstance(value, MappingProxyType):
        return {key: _thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_thaw(item) for item in value]
    return value


@dataclass(frozen=True)
class CanonicalState:
    payload: object
    generation: Generation
    state_version: int
    integrity_valid: bool


@dataclass(frozen=True)
class Checkpoint:
    checkpoint_id: str
    payload: object
    generation: Generation
    state_version: int
    integrity_valid: bool = True
    _authority_token: object = field(default=None, repr=False, compare=False)


class Transaction:
    """Opaque transaction handle with an isolated candidate payload."""

    ACTIVE = "ACTIVE"
    COMMITTED = "COMMITTED"
    ABORTED = "ABORTED"

    def __init__(self, transaction_id, context, generation, state_version, candidate):
        self._transaction_id = transaction_id
        self._context = context
        self._generation = generation
        self._state_version = state_version
        self._candidate = candidate
        self._status = self.ACTIVE

    @property
    def transaction_id(self):
        return self._transaction_id

    @property
    def status(self):
        return self._status

    def set_payload(self, payload):
        if self._status != self.ACTIVE:
            raise InvalidTransaction("transaction is terminal")
        _validate_value(payload)
        self._candidate = payload

    def get_candidate(self):
        if self._status != self.ACTIVE:
            raise InvalidTransaction("transaction is terminal")
        return _thaw(_freeze(self._candidate))


class InMemoryStateAuthority(StateAuthority):
    """Persistence-free State Authority implementing the P0-03 contract."""

    OP_BEGIN = "begin"
    OP_COMMIT = "commit"
    OP_ABORT = "abort"
    OP_SNAPSHOT = "snapshot"
    OP_RESTORE = "restore"

    def __init__(self, generation, initial_payload=None, authorization_policy=None, integrity_validator=None):
        if not isinstance(generation, Generation):
            raise TypeError("generation must be a Generation")
        initial_payload = {} if initial_payload is None else initial_payload
        _validate_value(initial_payload)
        try:
            initial_version = int(generation.state_version)
        except (TypeError, ValueError) as exc:
            raise ValueError("generation.state_version must be an integer string") from exc
        if initial_version < 0:
            raise ValueError("generation.state_version must be non-negative")
        self._policy = authorization_policy or AuthorizationPolicy()
        self._integrity_validator = integrity_validator or (lambda payload, _generation: True)
        self._validate_integrity(initial_payload, generation)
        self._generation = generation
        self._state_version = initial_version
        self._canonical = CanonicalState(_freeze(initial_payload), generation, initial_version, True)
        self._transactions = {}
        self._next_transaction_id = 1
        self._next_checkpoint_id = 1
        self._authority_token = object()
        self._lock = threading.RLock()

    def _authorize(self, context, operation):
        if not isinstance(context, AuthorizationContext):
            raise AuthorizationDenied("invalid authorization context")
        return self._policy.require(context, operation)

    def _validate_integrity(self, payload, generation):
        try:
            valid = self._integrity_validator(payload, generation)
        except Exception as exc:
            raise IntegrityFailure("integrity validation failed") from exc
        if valid is not True:
            raise IntegrityFailure("integrity validation failed")

    def read(self, key=None):
        with self._lock:
            payload = _thaw(self._canonical.payload)
            if key is None:
                return CanonicalState(payload, self._canonical.generation, self._state_version, self._canonical.integrity_valid)
            if not isinstance(key, str) or not isinstance(payload, dict):
                raise KeyError(key)
            return payload[key]

    def begin(self, context, payload=None):
        with self._lock:
            self._authorize(context, self.OP_BEGIN)
            candidate = _thaw(self._canonical.payload) if payload is None else payload
            _validate_value(candidate)
            transaction_id = "tx-{}".format(self._next_transaction_id)
            self._next_transaction_id += 1
            tx = Transaction(transaction_id, context, self._generation, self._state_version, candidate)
            self._transactions[transaction_id] = tx
            return tx

    def commit(self, transaction):
        with self._lock:
            if not isinstance(transaction, Transaction):
                raise InvalidTransaction("invalid transaction")
            if self._transactions.get(transaction.transaction_id) is not transaction:
                raise InvalidTransaction("unknown transaction")
            if transaction.status != Transaction.ACTIVE:
                raise InvalidTransaction("transaction is terminal")
            self._authorize(transaction._context, self.OP_COMMIT)
            if transaction._generation.generation_id != self._generation.generation_id:
                raise GenerationMismatch("transaction generation is stale")
            if transaction._generation.binary_version != self._generation.binary_version:
                raise GenerationMismatch("transaction binary generation is incompatible")
            if transaction._generation.schema_version != self._generation.schema_version:
                raise GenerationMismatch("transaction schema is incompatible")
            if transaction._state_version != self._state_version:
                raise StaleTransaction("transaction targets stale canonical revision")
            candidate = transaction._candidate
            _validate_value(candidate)
            self._validate_integrity(candidate, self._generation)

            new_version = self._state_version + 1
            new_generation = Generation(
                self._generation.generation_id,
                self._generation.binary_version,
                self._generation.schema_version,
                str(new_version),
                self._generation.integrity_reference,
            )
            new_canonical = CanonicalState(_freeze(candidate), new_generation, new_version, True)
            self._canonical = new_canonical
            self._generation = new_generation
            self._state_version = new_version
            transaction._status = Transaction.COMMITTED
            self._transactions.pop(transaction.transaction_id, None)
            return self.read()

    def abort(self, transaction):
        with self._lock:
            if not isinstance(transaction, Transaction):
                raise InvalidTransaction("invalid transaction")
            if self._transactions.get(transaction.transaction_id) is not transaction:
                if transaction.status == Transaction.ABORTED:
                    return None
                raise InvalidTransaction("unknown transaction")
            if transaction.status != Transaction.ACTIVE:
                return None
            self._authorize(transaction._context, self.OP_ABORT)
            transaction._status = Transaction.ABORTED
            self._transactions.pop(transaction.transaction_id, None)
            return None

    def snapshot(self, context):
        with self._lock:
            self._authorize(context, self.OP_SNAPSHOT)
            state = self._canonical
            checkpoint = Checkpoint(
                checkpoint_id="cp-{}".format(self._next_checkpoint_id),
                payload=state.payload,
                generation=state.generation,
                state_version=state.state_version,
                integrity_valid=state.integrity_valid,
                _authority_token=self._authority_token,
            )
            self._next_checkpoint_id += 1
            return checkpoint

    def restore(self, snapshot_reference, context):
        with self._lock:
            self._authorize(context, self.OP_RESTORE)
            if not isinstance(snapshot_reference, Checkpoint) or snapshot_reference._authority_token is not self._authority_token:
                raise InvalidCheckpoint("checkpoint is not owned by this authority")
            if not snapshot_reference.integrity_valid:
                raise InvalidCheckpoint("checkpoint integrity is invalid")
            candidate = _thaw(snapshot_reference.payload)
            _validate_value(candidate)
            if snapshot_reference.generation.generation_id != self._generation.generation_id:
                raise GenerationMismatch("checkpoint generation is incompatible")
            if snapshot_reference.generation.binary_version != self._generation.binary_version:
                raise GenerationMismatch("checkpoint binary generation is incompatible")
            if snapshot_reference.generation.schema_version != self._generation.schema_version:
                raise GenerationMismatch("checkpoint schema is incompatible")
            self._validate_integrity(candidate, snapshot_reference.generation)

            new_version = self._state_version + 1
            new_generation = Generation(
                self._generation.generation_id,
                self._generation.binary_version,
                self._generation.schema_version,
                str(new_version),
                self._generation.integrity_reference,
            )
            self._canonical = CanonicalState(_freeze(candidate), new_generation, new_version, True)
            self._generation = new_generation
            self._state_version = new_version
            return self.read()
