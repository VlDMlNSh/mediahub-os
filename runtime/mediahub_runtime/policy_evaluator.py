"""Deterministic, deny-by-default P0-07 policy evaluation."""

from __future__ import annotations

from dataclasses import dataclass

from .configuration_policy import (
    MAX_IDENTIFIER_BYTES,
    Policy,
    PolicyRule,
    validate_policy,
)


@dataclass(frozen=True)
class PolicyDecision:
    """Bounded policy result; evaluation never executes or mutates anything."""

    allowed: bool
    reason: str


def _valid_request_string(value: object) -> bool:
    return type(value) is str and bool(value) and len(value.encode("utf-8")) <= MAX_IDENTIFIER_BYTES


def evaluate_policy(policy: Policy, *, operation: str, resource: str) -> PolicyDecision:
    """Evaluate one exact operation/resource request using P0-07 precedence.

    Precedence is deterministic and fail-closed:
    malformed input -> DENY; explicit DENY -> DENY; conflicting matching
    effects -> DENY; explicit ALLOW without conflict -> ALLOW; no match -> DENY.
    No wildcard, priority, inheritance, merge, retry, or execution semantics
    are supported.
    """
    if type(policy) is not Policy:
        return PolicyDecision(False, "malformed policy")
    if not _valid_request_string(operation):
        return PolicyDecision(False, "malformed operation")
    if not _valid_request_string(resource):
        return PolicyDecision(False, "malformed resource")

    try:
        validate_policy(policy)
    except Exception:
        return PolicyDecision(False, "malformed policy")

    matches = tuple(
        rule
        for rule in policy.rules
        if type(rule) is PolicyRule
        and rule.operation == operation
        and rule.resource == resource
    )

    if not matches:
        return PolicyDecision(False, "no matching rule")

    effects = frozenset(rule.effect for rule in matches)
    if "DENY" in effects:
        if "ALLOW" in effects:
            return PolicyDecision(False, "conflicting matching effects")
        return PolicyDecision(False, "explicit deny")
    if effects == frozenset({"ALLOW"}):
        return PolicyDecision(True, "explicit allow")
    return PolicyDecision(False, "ambiguous policy")
