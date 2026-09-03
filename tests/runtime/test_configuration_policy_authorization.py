import pytest

from mediahub_runtime.authorization import AuthorizationContext
from mediahub_runtime.configuration_policy_authorization import (
    P0_07_CAPABILITIES,
    ConfigurationPolicyAuthorization,
)


def test_exact_p0_07_capability_inventory_is_present():
    assert len(P0_07_CAPABILITIES) == 14
    assert "configuration.update" in P0_07_CAPABILITIES
    assert "policy.delete" in P0_07_CAPABILITIES


def test_default_deny():
    auth = ConfigurationPolicyAuthorization()
    context = AuthorizationContext("runtime", "configuration.read")
    assert auth.decide(context, "read") is False
    with pytest.raises(PermissionError):
        auth.require(context, "read")


def test_explicit_grant_allows_only_matching_operation():
    auth = ConfigurationPolicyAuthorization(
        frozenset({("runtime", "configuration.read", "read")})
    )
    context = AuthorizationContext("runtime", "configuration.read")
    assert auth.decide(context, "read") is True
    assert auth.decide(context, "update") is False


def test_unknown_capability_is_rejected():
    with pytest.raises(ValueError):
        ConfigurationPolicyAuthorization(
            frozenset({("runtime", "configuration.*", "read")})
        )


def test_cross_operation_capability_is_rejected():
    with pytest.raises(ValueError):
        ConfigurationPolicyAuthorization(
            frozenset({("runtime", "configuration.update", "read")})
        )


def test_non_p0_07_operation_is_denied():
    auth = ConfigurationPolicyAuthorization(
        frozenset({("runtime", "configuration.read", "read")})
    )
    context = AuthorizationContext("runtime", "configuration.read")
    assert auth.decide(context, "execute") is False
