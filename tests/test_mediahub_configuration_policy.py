import pytest

from ops.mediahub_configuration_policy import (
    ActivationState,
    ConfigurationActivation,
    ConfigurationVersion,
    Decision,
    PolicyClass,
    PolicyConflict,
    PolicyEngine,
    PolicyInput,
    PolicyRule,
    PolicyVersion,
    Scope,
    resolve_configuration_conflict,
)


def policy(pid, version=1, scope=Scope.USER, cls=PolicyClass.USER):
    return PolicyVersion(
        policy_id=pid,
        version=version,
        policy_class=cls,
        scope=scope,
        owner="owner",
        applicability="always",
        dependencies=frozenset(),
        effective_at="2026-01-01T00:00:00Z",
        expires_at=None,
        provenance="test-provenance",
        approval_state="approved",
        qualification_state="qualified",
    )


def request(**overrides):
    values = dict(
        actor="user",
        identity="identity",
        device="device",
        capability="control",
        resource="resource",
        target="target",
        action="write",
        context="normal",
        timestamp="2026-01-01T00:00:00Z",
        data_classification="non-sensitive",
        risk="low",
        current_state="ready",
        authorized=True,
    )
    values.update(overrides)
    return PolicyInput(**values)


def test_policy_evaluation_is_deterministic_and_non_mutating():
    engine = PolicyEngine((
        PolicyRule(policy("user-1"), Decision.ALLOW, required_capability="control"),
    ))
    before = engine.simulate(request())
    after = engine.evaluate(request())
    assert before == after
    assert before.decision is Decision.ALLOW


def test_authorization_and_policy_are_separate():
    engine = PolicyEngine((
        PolicyRule(policy("user-1"), Decision.ALLOW, required_capability="control"),
    ))
    result = engine.evaluate(request(authorized=False))
    assert result.decision is Decision.REQUIRE_AUTHORIZATION


def test_security_deny_overrides_user_allow():
    engine = PolicyEngine((
        PolicyRule(policy("user-allow"), Decision.ALLOW, required_capability="control"),
        PolicyRule(
            policy("security-deny", scope=Scope.SECURITY, cls=PolicyClass.SECURITY),
            Decision.DENY,
            required_capability="control",
            reason="mandatory security boundary",
        ),
    ))
    assert engine.evaluate(request()).decision is Decision.DENY


def test_critical_deny_overrides_lower_scope_critical_allow():
    engine = PolicyEngine((
        PolicyRule(
            policy("security-deny", scope=Scope.SECURITY, cls=PolicyClass.SECURITY),
            Decision.DENY,
        ),
        PolicyRule(
            policy("safety-allow", scope=Scope.SESSION, cls=PolicyClass.SAFETY),
            Decision.ALLOW,
        ),
    ))
    assert engine.evaluate(request()).decision is Decision.DENY


def test_critical_conflict_fails_closed():
    engine = PolicyEngine((
        PolicyRule(policy("security-allow", cls=PolicyClass.SECURITY), Decision.ALLOW),
        PolicyRule(policy("security-deny", cls=PolicyClass.SECURITY), Decision.DENY),
    ))
    assert engine.evaluate(request()).decision is Decision.DENY


def test_mixed_critical_non_allow_decisions_fail_closed():
    engine = PolicyEngine((
        PolicyRule(policy("security-deny", cls=PolicyClass.SECURITY), Decision.DENY),
        PolicyRule(policy("safety-quarantine", cls=PolicyClass.SAFETY), Decision.QUARANTINE),
    ))
    assert engine.evaluate(request()).decision is Decision.DENY


def test_unresolved_noncritical_conflict_is_not_last_write_wins():
    engine = PolicyEngine((
        PolicyRule(policy("a", version=1), Decision.ALLOW),
        PolicyRule(policy("b", version=1), Decision.REQUIRE_CONFIRMATION),
    ))
    with pytest.raises(PolicyConflict):
        engine.evaluate(request())


def test_configuration_activation_requires_qualification_and_integrity():
    with pytest.raises(ValueError):
        ConfigurationActivation("cfg", 2, ActivationState.CURRENT, False, True, 1).validate()
    ConfigurationActivation("cfg", 2, ActivationState.CURRENT, True, True, 1).validate()


def test_configuration_conflict_requires_ownership_compatibility():
    def cfg(owner, version, scope=Scope.USER):
        return ConfigurationVersion(
            "cfg", version, 1, owner, scope, "2026-01-01T00:00:00Z",
            "prov", "valid", "compatible", "allowed", f"digest-{version}",
        )

    with pytest.raises(ValueError):
        resolve_configuration_conflict((cfg("a", 1), cfg("b", 2)))
    selected = resolve_configuration_conflict((cfg("a", 1), cfg("a", 2)))
    assert selected.version == 2


def test_expired_policy_metadata_is_rejected():
    with pytest.raises(ValueError):
        PolicyVersion(
            "p", 1, PolicyClass.SECURITY, Scope.SECURITY, "owner", "always",
            frozenset(), "2026-01-02", "2026-01-01", "prov", "approved", "qualified",
        ).validate()


def test_no_policy_does_not_become_permissive():
    engine = PolicyEngine(())
    assert engine.evaluate(request()).decision is Decision.DEFER
