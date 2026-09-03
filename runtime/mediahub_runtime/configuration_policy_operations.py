"""P0-07 operation dispatch boundary.

This module authorizes and validates requests only. It does not publish state,
persist data, resolve credentials, access the network, or execute external work.
Actual mutation remains mediated by the existing P0-05 -> P0-04 path.
"""

from __future__ import annotations

from dataclasses import dataclass

from .authorization import AuthorizationContext
from .configuration_policy import Configuration, Policy, validate_configuration, validate_policy
from .configuration_policy_authorization import ConfigurationPolicyAuthorization, P0_07_CAPABILITIES
from .policy_evaluator import PolicyDecision, evaluate_policy


_RESOURCE_TYPES = frozenset({"configuration", "policy"})


@dataclass(frozen=True)
class ConfigurationPolicyOperationRequest:
    """Bounded inert operation request."""

    resource_type: str
    operation: str
    resource: str
    context: AuthorizationContext
    payload: Configuration | Policy | None = None

    def __post_init__(self) -> None:
        if type(self.resource_type) is not str or self.resource_type not in _RESOURCE_TYPES:
            raise ValueError("unsupported resource type")
        if type(self.operation) is not str or not self.operation:
            raise ValueError("operation must be non-empty")
        if type(self.resource) is not str or not self.resource:
            raise ValueError("resource must be non-empty")
        if type(self.context) is not AuthorizationContext:
            raise ValueError("context must be AuthorizationContext")
        if self.context.capability not in P0_07_CAPABILITIES:
            raise ValueError("capability is not authorized by P0-07")
        if self.payload is not None:
            if self.resource_type == "configuration" and type(self.payload) is not Configuration:
                raise ValueError("configuration operation requires Configuration payload")
            if self.resource_type == "policy" and type(self.payload) is not Policy:
                raise ValueError("policy operation requires Policy payload")


@dataclass(frozen=True)
class ConfigurationPolicyOperationDecision:
    """Bounded authorization/evaluation result; contains no executable action."""

    authorized: bool
    policy: PolicyDecision
    reason: str


class ConfigurationPolicyOperationBoundary:
    """Validate P0-07 operation requests without becoming an authority."""

    def __init__(self, authorization: ConfigurationPolicyAuthorization, policy: Policy) -> None:
        if type(authorization) is not ConfigurationPolicyAuthorization:
            raise ValueError("invalid P0-07 authorization")
        if type(policy) is not Policy:
            raise ValueError("invalid P0-07 policy")
        self._authorization = authorization
        self._policy = policy

    def decide(self, request: ConfigurationPolicyOperationRequest) -> ConfigurationPolicyOperationDecision:
        if type(request) is not ConfigurationPolicyOperationRequest:
            return ConfigurationPolicyOperationDecision(
                False, PolicyDecision(False, "malformed request"), "malformed request"
            )

        try:
            if request.resource_type == "configuration" and request.payload is not None:
                validate_configuration(request.payload)
            elif request.resource_type == "policy" and request.payload is not None:
                validate_policy(request.payload)
        except Exception:
            return ConfigurationPolicyOperationDecision(
                False, PolicyDecision(False, "malformed payload"), "malformed payload"
            )

        if not self._authorization.decide(request.context, request.operation):
            return ConfigurationPolicyOperationDecision(
                False, PolicyDecision(False, "capability denied"), "capability denied"
            )

        policy_decision = evaluate_policy(
            self._policy,
            operation=request.operation,
            resource=request.resource,
        )
        if not policy_decision.allowed:
            return ConfigurationPolicyOperationDecision(False, policy_decision, policy_decision.reason)

        return ConfigurationPolicyOperationDecision(True, policy_decision, "authorized")

    def authorize(self, request: ConfigurationPolicyOperationRequest) -> None:
        decision = self.decide(request)
        if not decision.authorized:
            raise PermissionError("P0-07 operation denied")
