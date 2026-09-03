"""P0-07 operation/capability authorization boundary.

The boundary is an explicit allow-list. It introduces no authority and no
mutation primitive; callers remain subject to the existing P0-05/P0-04 path.
"""

from __future__ import annotations

from dataclasses import dataclass

from .authorization import AuthorizationContext


P0_07_CAPABILITIES = frozenset(
    {
        "configuration.read",
        "configuration.validate",
        "configuration.propose",
        "configuration.update",
        "configuration.replace",
        "configuration.reset",
        "configuration.delete",
        "policy.read",
        "policy.validate",
        "policy.propose",
        "policy.update",
        "policy.replace",
        "policy.reset",
        "policy.delete",
    }
)

P0_07_OPERATIONS = frozenset({
    "read",
    "validate",
    "propose",
    "update",
    "replace",
    "reset",
    "delete",
})


@dataclass(frozen=True)
class ConfigurationPolicyAuthorization:
    """Explicit device-local P0-07 capability grant set; default deny."""

    grants: frozenset[tuple[str, str, str]] = frozenset()

    def __post_init__(self) -> None:
        if type(self.grants) is not frozenset:
            raise ValueError("grants must be an immutable frozenset")
        for grant in self.grants:
            if type(grant) is not tuple or len(grant) != 3:
                raise ValueError("grant must be a (principal, capability, operation) tuple")
            principal, capability, operation = grant
            if type(principal) is not str or not principal:
                raise ValueError("grant principal must be non-empty")
            if capability not in P0_07_CAPABILITIES:
                raise ValueError("capability is not authorized by P0-07")
            if operation not in P0_07_OPERATIONS:
                raise ValueError("operation is not authorized by P0-07")
            if capability.rsplit(".", 1)[-1] != operation and operation != "read":
                raise ValueError("capability and operation do not match")

    def decide(self, context: AuthorizationContext, operation: str) -> bool:
        if type(context) is not AuthorizationContext:
            return False
        if type(operation) is not str or operation not in P0_07_OPERATIONS:
            return False
        if context.capability not in P0_07_CAPABILITIES:
            return False
        return (context.principal, context.capability, operation) in self.grants

    def require(self, context: AuthorizationContext, operation: str) -> None:
        if not self.decide(context, operation):
            raise PermissionError("P0-07 authorization denied")
