"""MH-05 governed ingress to the canonical in-memory State Authority."""

import math
from dataclasses import dataclass

from .state_authority import (
    AuthorizationContext,
    AuthorizationDenied,
    AuthorityUnavailable,
    Command,
    ConflictDetected,
    DuplicateCommand,
    InvalidCommand,
)


class ConsumerBoundaryError(RuntimeError):
    """Stable, sanitized error exposed to consumers."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class ConsumerRequest:
    """Inert request metadata; it carries no mutation capability."""

    source_identity: str
    correlation_id: str
    authorization: AuthorizationContext


class ConsumerBoundary:
    """Single governed ingress; State Authority remains the only mutation owner."""

    _MAX_IDENTITY = 256
    _MAX_CORRELATION = 256
    _MAX_PATH = 32
    _MAX_VALUE_DEPTH = 8
    _MAX_VALUE_NODES = 512
    _MAX_STRING = 4096
    _MAX_KEYS = 64
    _MAX_KEY = 128

    def __init__(self, authority):
        if authority is None or not callable(getattr(authority, "execute", None)):
            raise TypeError("authority must expose execute")
        if not callable(getattr(authority, "read", None)):
            raise TypeError("authority must expose read")
        if not callable(getattr(authority, "restore", None)):
            raise TypeError("authority must expose restore")
        self._authority = authority

    @classmethod
    def request(cls, source_identity, correlation_id, authorization):
        if not cls._valid_id(source_identity, cls._MAX_IDENTITY):
            raise ConsumerBoundaryError("invalid_identity")
        if not cls._valid_id(correlation_id, cls._MAX_CORRELATION):
            raise ConsumerBoundaryError("invalid_correlation")
        if not isinstance(authorization, AuthorizationContext):
            raise ConsumerBoundaryError("authorization_denied")
        return ConsumerRequest(source_identity, correlation_id, authorization)

    def read(self):
        try:
            return self._authority.read()
        except AuthorityUnavailable as exc:
            raise ConsumerBoundaryError("authority_unavailable") from exc

    def restore(self, request, checkpoint):
        self._validate_request(request)
        try:
            return self._authority.restore(checkpoint, request.authorization)
        except AuthorizationDenied as exc:
            raise ConsumerBoundaryError("authorization_denied") from exc
        except InvalidCommand as exc:
            raise ConsumerBoundaryError("invalid_command") from exc
        except AuthorityUnavailable as exc:
            raise ConsumerBoundaryError("authority_unavailable") from exc
        except Exception as exc:
            raise ConsumerBoundaryError("operation_rejected") from exc

    def execute(self, request, operation, path, value=None, expected_generation=None, command_id=None):
        self._validate_request(request)
        if not isinstance(operation, str) or not operation:
            raise ConsumerBoundaryError("invalid_operation")
        if not isinstance(path, tuple) or not path or len(path) > self._MAX_PATH:
            raise ConsumerBoundaryError("invalid_path")
        if any(not isinstance(part, str) or not part or len(part) > self._MAX_KEY for part in path):
            raise ConsumerBoundaryError("invalid_path")
        if command_id is None:
            raise ConsumerBoundaryError("command_identity_required")
        if not self._valid_id(command_id, self._MAX_CORRELATION):
            raise ConsumerBoundaryError("command_identity_required")
        self._validate_value(value)
        command = Command(
            command_id=command_id,
            correlation_id=request.correlation_id,
            operation=operation,
            path=path,
            value=value,
            expected_generation=expected_generation,
            authorization=request.authorization,
            source_identity=request.source_identity,
        )
        try:
            return self._authority.execute(command)
        except AuthorizationDenied as exc:
            raise ConsumerBoundaryError("authorization_denied") from exc
        except ConflictDetected as exc:
            raise ConsumerBoundaryError("stale_generation") from exc
        except DuplicateCommand as exc:
            raise ConsumerBoundaryError("duplicate_command") from exc
        except InvalidCommand as exc:
            raise ConsumerBoundaryError("invalid_command") from exc
        except AuthorityUnavailable as exc:
            raise ConsumerBoundaryError("authority_unavailable") from exc
        except Exception as exc:
            raise ConsumerBoundaryError("operation_rejected") from exc

    @staticmethod
    def _validate_request(request):
        if not isinstance(request, ConsumerRequest):
            raise ConsumerBoundaryError("invalid_request")

    @staticmethod
    def _valid_id(value, maximum):
        return isinstance(value, str) and 0 < len(value) <= maximum and value.strip() == value

    @classmethod
    def _validate_value(cls, value, depth=0, budget=None):
        budget = [0] if budget is None else budget
        budget[0] += 1
        if budget[0] > cls._MAX_VALUE_NODES or depth > cls._MAX_VALUE_DEPTH:
            raise ConsumerBoundaryError("operation_rejected")
        if value is None or type(value) in (bool, int, str):
            if type(value) is str and len(value) > cls._MAX_STRING:
                raise ConsumerBoundaryError("operation_rejected")
            return
        if type(value) is float:
            if not math.isfinite(value):
                raise ConsumerBoundaryError("operation_rejected")
            return
        if type(value) in (list, tuple):
            for item in value:
                cls._validate_value(item, depth + 1, budget)
            return
        if type(value) is dict:
            if len(value) > cls._MAX_KEYS:
                raise ConsumerBoundaryError("operation_rejected")
            for key, item in value.items():
                if type(key) is not str or not key or len(key) > cls._MAX_KEY:
                    raise ConsumerBoundaryError("operation_rejected")
                cls._validate_value(item, depth + 1, budget)
            return
        raise ConsumerBoundaryError("operation_rejected")
