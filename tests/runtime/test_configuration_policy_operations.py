from mediahub_runtime.authorization import AuthorizationContext
from mediahub_runtime.configuration_policy import Policy, PolicyRule
from mediahub_runtime.configuration_policy_authorization import ConfigurationPolicyAuthorization
from mediahub_runtime.configuration_policy_operations import (
    ConfigurationPolicyOperationBoundary,
    ConfigurationPolicyOperationRequest,
)


def make_policy(*rules):
    return Policy(
        identity="runtime",
        namespace="mediahub.runtime",
        version="1",
        scope="device-local",
        rules=tuple(rules),
    )


def make_boundary(*rules):
    authorization = ConfigurationPolicyAuthorization(
        grants=frozenset({("system", "configuration.read", "read")})
    )
    return ConfigurationPolicyOperationBoundary(authorization, make_policy(*rules))


def request(operation="read", capability="configuration.read", resource="runtime"):
    return ConfigurationPolicyOperationRequest(
        resource_type="configuration",
        operation=operation,
        resource=resource,
        context=AuthorizationContext("system", capability),
    )


def test_operation_requires_explicit_capability_grant_and_policy_allow():
    boundary = make_boundary(
        PolicyRule("ALLOW", "configuration.read", "runtime")
    )
    decision = boundary.decide(request())
    assert decision.authorized is True
    assert decision.reason == "authorized"


def test_missing_capability_grant_is_denied():
    boundary = ConfigurationPolicyOperationBoundary(
        ConfigurationPolicyAuthorization(),
        make_policy(PolicyRule("ALLOW", "configuration.read", "runtime")),
    )
    decision = boundary.decide(request())
    assert decision.authorized is False
    assert decision.reason == "capability denied"


def test_policy_deny_is_fail_closed():
    boundary = make_boundary(
        PolicyRule("DENY", "configuration.read", "runtime")
    )
    decision = boundary.decide(request())
    assert decision.authorized is False
    assert decision.reason == "explicit deny"


def test_unsupported_operation_is_denied():
    boundary = make_boundary(PolicyRule("ALLOW", "configuration.read", "runtime"))
    decision = boundary.decide(request(operation="update"))
    assert decision.authorized is False


def test_malformed_request_is_denied():
    boundary = make_boundary(PolicyRule("ALLOW", "configuration.read", "runtime"))
    decision = boundary.decide(object())
    assert decision.authorized is False
    assert decision.reason == "malformed request"


def test_decision_is_inert_and_does_not_mutate_policy():
    policy = make_policy(PolicyRule("ALLOW", "configuration.read", "runtime"))
    boundary = ConfigurationPolicyOperationBoundary(
        ConfigurationPolicyAuthorization(
            grants=frozenset({("system", "configuration.read", "read")})
        ),
        policy,
    )
    before = policy.as_dict()
    boundary.decide(request())
    assert policy.as_dict() == before
