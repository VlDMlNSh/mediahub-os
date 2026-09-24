"""Fail-closed authorization seam for privileged runtime mutations."""

from dataclasses import dataclass

from .errors import AuthorizationDenied


@dataclass(frozen=True)
class AuthorizationContext:
    principal: str
    capability: str


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str


class AuthorizationPolicy:
    """Explicit allow-list policy. Empty policy denies everything."""

    def __init__(self, grants=None):
        self._grants = frozenset(grants or ())

    def decide(self, context, operation):
        if not isinstance(context, AuthorizationContext):
            return AuthorizationDecision(False, "invalid authorization context")
        key = (context.principal, context.capability, operation)
        if key in self._grants:
            return AuthorizationDecision(True, "explicit grant")
        return AuthorizationDecision(False, "no explicit grant")

    def require(self, context, operation):
        decision = self.decide(context, operation)
        if not decision.allowed:
            raise AuthorizationDenied(decision.reason)
        return decision
