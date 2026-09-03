"""P0-08 plugin authorization seam.

This module composes plugin declaration validation with the existing explicit
runtime authorization policy. It creates no authority, grant, transaction,
persistence, execution, or mutation primitive.
"""

from __future__ import annotations

from dataclasses import dataclass

from .authorization import AuthorizationContext, AuthorizationPolicy
from .plugin_capabilities import CapabilityDeclaration, CapabilityRequest


@dataclass(frozen=True)
class PluginAuthorizationDecision:
    allowed: bool
    reason: str


class PluginAuthorization:
    """Fail-closed authorization for plugin requests."""

    def __init__(self, policy: AuthorizationPolicy) -> None:
        if type(policy) is not AuthorizationPolicy:
            raise TypeError("policy must be AuthorizationPolicy")
        self._policy = policy

    def decide(
        self,
        declaration: CapabilityDeclaration,
        request: CapabilityRequest,
        context: AuthorizationContext,
    ) -> PluginAuthorizationDecision:
        if type(declaration) is not CapabilityDeclaration:
            return PluginAuthorizationDecision(False, "invalid declaration")
        if type(request) is not CapabilityRequest:
            return PluginAuthorizationDecision(False, "invalid request")
        if type(context) is not AuthorizationContext:
            return PluginAuthorizationDecision(False, "invalid authorization context")

        if not request.is_declared_by(declaration):
            return PluginAuthorizationDecision(False, "capability not declared")
        if context.principal != request.plugin_id:
            return PluginAuthorizationDecision(False, "principal identity mismatch")
        if context.capability != request.capability:
            return PluginAuthorizationDecision(False, "capability context mismatch")

        decision = self._policy.decide(context, request.operation)
        if not decision.allowed:
            return PluginAuthorizationDecision(False, "explicit authorization denied")
        return PluginAuthorizationDecision(True, "explicit authorization granted")

    def require(
        self,
        declaration: CapabilityDeclaration,
        request: CapabilityRequest,
        context: AuthorizationContext,
    ) -> PluginAuthorizationDecision:
        decision = self.decide(declaration, request, context)
        if not decision.allowed:
            raise PermissionError(decision.reason)
        return decision
