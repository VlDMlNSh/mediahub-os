"""P0-05 controlled consumer boundary around the frozen State Authority."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .authorization import AuthorizationContext
from .errors import AuthorizationDenied, RuntimeInvariantError
from .state import StateAuthority


@dataclass(frozen=True)
class OperationRequest:
    """Inert consumer intent; never executable by itself."""

    operation: str
    payload: Any = None


class ConsumerBoundary:
    """Narrow facade that prevents consumers from bypassing State Authority."""

    _ALLOWED_OPERATIONS = frozenset({"begin", "snapshot", "restore"})

    def __init__(self, authority: StateAuthority) -> None:
        self._authority = authority

    def read(self):
        return self._authority.read()

    def request(self, request: OperationRequest, authorization: AuthorizationContext):
        if not isinstance(request, OperationRequest):
            raise RuntimeInvariantError("invalid operation request")
        if request.operation not in self._ALLOWED_OPERATIONS:
            raise AuthorizationDenied("operation not permitted")
        if request.operation == "begin":
            return self._authority.begin(authorization)
        if request.operation == "snapshot":
            return self._authority.snapshot(authorization)
        if request.operation == "restore":
            checkpoint = request.payload
            return self._authority.restore(checkpoint, authorization)
        raise AuthorizationDenied("operation not permitted")
