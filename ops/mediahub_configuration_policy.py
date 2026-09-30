"""MH-7 configuration and policy contracts.

This module is deliberately authority-neutral: it models configuration/policy
artifacts and deterministic evaluation without becoming State Authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import FrozenSet


class Decision(str, Enum):
    ALLOW = "allow"
    DENY = "deny"
    REQUIRE_AUTHORIZATION = "require_additional_authorization"
    REQUIRE_CONFIRMATION = "require_confirmation"
    QUARANTINE = "quarantine"
    DEFER = "defer"
    DEGRADED = "degraded"


class PolicyClass(str, Enum):
    SECURITY = "security"
    SAFETY = "safety"
    SYSTEM = "system"
    PRIVACY = "privacy"
    DATA = "data"
    NETWORK = "network"
    IDENTITY = "identity"
    DEVICE = "device"
    SMART_HOME = "smart_home"
    MEDIA = "media"
    AI = "ai"
    ENGINEERING = "engineering"
    INTEGRATION = "integration"
    RESOURCE = "resource"
    UPDATE = "update"
    RECOVERY = "recovery"
    USER = "user"
    DEVELOPER = "developer"


class Scope(str, Enum):
    PLATFORM = "platform"
    SECURITY = "security"
    SYSTEM = "system"
    CLUSTER = "cluster"
    NODE = "node"
    DOMAIN = "domain"
    SERVICE = "service"
    WORKLOAD = "workload"
    INTEGRATION = "integration"
    USER = "user"
    DEVICE = "device"
    SESSION = "session"


class ActivationState(str, Enum):
    CURRENT = "current"
    PENDING = "pending"
    DEGRADED = "degraded"
    STALE = "stale"
    INCOMPATIBLE = "incompatible"
    QUARANTINED = "quarantined"


_SCOPE_RANK = {scope: rank for rank, scope in enumerate(Scope)}
_CRITICAL_CLASSES = frozenset({PolicyClass.SECURITY, PolicyClass.SAFETY})


@dataclass(frozen=True)
class ConfigurationVersion:
    config_id: str
    version: int
    schema_version: int
    owner: str
    scope: Scope
    timestamp: str
    provenance: str
    validation_state: str
    compatibility_state: str
    policy_state: str
    value_digest: str

    def validate(self) -> None:
        if self.version < 1 or self.schema_version < 1:
            raise ValueError("configuration version must be positive")
        if not all(
            isinstance(value, str) and value
            for value in (
                self.config_id, self.owner, self.timestamp, self.provenance,
                self.validation_state, self.compatibility_state,
                self.policy_state, self.value_digest,
            )
        ):
            raise ValueError("configuration metadata is incomplete")


@dataclass(frozen=True)
class PolicyVersion:
    policy_id: str
    version: int
    policy_class: PolicyClass
    scope: Scope
    owner: str
    applicability: str
    dependencies: FrozenSet[str]
    effective_at: str
    expires_at: str | None
    provenance: str
    approval_state: str
    qualification_state: str

    def validate(self) -> None:
        if self.version < 1:
            raise ValueError("policy version must be positive")
        if not self.owner or not self.applicability or not self.effective_at:
            raise ValueError("policy metadata is incomplete")
        if not self.provenance or not self.approval_state or not self.qualification_state:
            raise ValueError("policy provenance/qualification metadata is required")
        if self.expires_at is not None and self.expires_at <= self.effective_at:
            raise ValueError("policy expiry must be after effective time")


@dataclass(frozen=True)
class PolicyInput:
    actor: str
    identity: str
    device: str
    capability: str
    resource: str
    target: str
    action: str
    context: str
    timestamp: str
    data_classification: str
    risk: str
    current_state: str
    authorized: bool = False
    observed_state_fresh: bool = True


@dataclass(frozen=True)
class PolicyRule:
    policy: PolicyVersion
    decision: Decision
    required_capability: str | None = None
    required_context: str | None = None
    reason: str = ""

    def matches(self, request: PolicyInput) -> bool:
        if self.required_capability and request.capability != self.required_capability:
            return False
        if self.required_context and request.context != self.required_context:
            return False
        return True


@dataclass(frozen=True)
class PolicyDecision:
    decision: Decision
    policy_id: str
    policy_version: int
    scope: Scope
    policy_class: PolicyClass
    reason: str
    provenance: str

    @property
    def allowed(self) -> bool:
        return self.decision is Decision.ALLOW


class PolicyConflict(ValueError):
    """Raised when critical rules cannot be resolved deterministically."""


class PolicyEngine:
    """Pure, deterministic evaluator; it does not mutate canonical state."""

    def __init__(self, rules: tuple[PolicyRule, ...]) -> None:
        for rule in rules:
            rule.policy.validate()
        self._rules = tuple(rules)

    def evaluate(self, request: PolicyInput) -> PolicyDecision:
        matches = [rule for rule in self._rules if rule.matches(request)]
        if not matches:
            return PolicyDecision(
                Decision.DEFER, "", 0, Scope.SESSION, PolicyClass.SYSTEM,
                "no applicable policy", "",
            )

        # Security/safety are never relaxed by a lower scope.
        critical = [
            rule for rule in matches if rule.policy.policy_class in _CRITICAL_CLASSES
        ]
        if any(rule.decision is not Decision.ALLOW for rule in critical):
            selected = max(critical, key=self._sort_key)
            return self._decision(selected)

        # Explicit deny wins over allow at the same effective precedence.
        ordered = sorted(matches, key=self._sort_key, reverse=True)
        top_rank = self._sort_key(ordered[0])[:3]
        top = [rule for rule in ordered if self._sort_key(rule)[:3] == top_rank]
        decisions = {rule.decision for rule in top}
        if len(decisions) > 1:
            if any(rule.policy.policy_class in _CRITICAL_CLASSES for rule in top):
                raise PolicyConflict("unresolved critical policy conflict")
            if Decision.DENY in decisions:
                selected = next(rule for rule in top if rule.decision is Decision.DENY)
            else:
                raise PolicyConflict("unresolved policy conflict")
        else:
            selected = top[0]

        if selected.decision is Decision.ALLOW and not request.authorized:
            return PolicyDecision(
                Decision.REQUIRE_AUTHORIZATION,
                selected.policy.policy_id,
                selected.policy.version,
                selected.policy.scope,
                selected.policy.policy_class,
                "authorization is required before policy allows action",
                selected.policy.provenance,
            )
        return self._decision(selected)

    @staticmethod
    def _sort_key(rule: PolicyRule) -> tuple[int, int, int]:
        # Scope is primary; policy version and class provide deterministic tie breaks.
        return (
            _SCOPE_RANK[rule.policy.scope],
            rule.policy.version,
            1 if rule.policy.policy_class in _CRITICAL_CLASSES else 0,
        )

    @staticmethod
    def _decision(rule: PolicyRule) -> PolicyDecision:
        return PolicyDecision(
            rule.decision,
            rule.policy.policy_id,
            rule.policy.version,
            rule.policy.scope,
            rule.policy.policy_class,
            rule.reason or rule.decision.value,
            rule.policy.provenance,
        )

    def simulate(self, request: PolicyInput) -> PolicyDecision:
        """Evaluate without activation or canonical-state mutation."""
        return self.evaluate(request)


@dataclass(frozen=True)
class ConfigurationChange:
    request_id: str
    actor: str
    identity: str
    scope: Scope
    previous: ConfigurationVersion | None
    proposed: ConfigurationVersion
    reason: str
    authorization: str
    policy_decision: Decision
    target: str
    provenance: str

    def validate(self) -> None:
        self.proposed.validate()
        if self.previous and self.previous.config_id != self.proposed.config_id:
            raise ValueError("configuration identity cannot change during update")
        if not all(
            isinstance(value, str) and value
            for value in (
                self.request_id, self.actor, self.identity, self.reason,
                self.authorization, self.target, self.provenance,
            )
        ):
            raise ValueError("configuration audit metadata is incomplete")


@dataclass(frozen=True)
class ConfigurationActivation:
    config_id: str
    version: int
    state: ActivationState
    qualified: bool
    integrity_verified: bool
    rollback_version: int | None

    def validate(self) -> None:
        if self.version < 1:
            raise ValueError("activation version must be positive")
        if self.state is ActivationState.CURRENT and not (
            self.qualified and self.integrity_verified
        ):
            raise ValueError("current configuration must be qualified and integrity verified")
        if self.rollback_version is not None and self.rollback_version >= self.version:
            raise ValueError("rollback version must precede active version")


def resolve_configuration_conflict(
    candidates: tuple[ConfigurationVersion, ...],
) -> ConfigurationVersion:
    """Resolve only when ownership/scope/version make the result deterministic."""
    if not candidates:
        raise ValueError("no configuration candidates")
    for candidate in candidates:
        candidate.validate()
    owners = {candidate.owner for candidate in candidates}
    scopes = {candidate.scope for candidate in candidates}
    if len(owners) > 1 and len(scopes) == 1:
        raise ValueError("configuration ownership conflict")
    return max(candidates, key=lambda c: (_SCOPE_RANK[c.scope], c.version))
