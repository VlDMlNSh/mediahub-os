from mediahub_runtime.configuration_policy import Policy, PolicyRule
from mediahub_runtime.policy_evaluator import PolicyDecision, evaluate_policy


def make_policy(*rules):
    return Policy(
        identity="runtime",
        namespace="mediahub.runtime",
        version="1",
        scope="device-local",
        rules=tuple(rules),
    )


def test_no_match_is_denied_by_default():
    decision = evaluate_policy(make_policy(), operation="configuration.read", resource="runtime")
    assert decision == PolicyDecision(False, "no matching rule")


def test_explicit_allow_is_allowed():
    policy = make_policy(PolicyRule("ALLOW", "configuration.read", "runtime"))
    assert evaluate_policy(policy, operation="configuration.read", resource="runtime") == PolicyDecision(
        True, "explicit allow"
    )


def test_explicit_deny_overrides_allow():
    policy = make_policy(
        PolicyRule("ALLOW", "configuration.read", "runtime"),
        PolicyRule("DENY", "configuration.read", "runtime"),
    )
    assert evaluate_policy(policy, operation="configuration.read", resource="runtime") == PolicyDecision(
        False, "conflicting matching effects"
    )


def test_explicit_deny_is_denied():
    policy = make_policy(PolicyRule("DENY", "configuration.update", "runtime"))
    assert evaluate_policy(policy, operation="configuration.update", resource="runtime") == PolicyDecision(
        False, "explicit deny"
    )


def test_duplicate_same_effect_is_deterministic():
    policy = make_policy(
        PolicyRule("ALLOW", "configuration.read", "runtime"),
        PolicyRule("ALLOW", "configuration.read", "runtime"),
    )
    assert evaluate_policy(policy, operation="configuration.read", resource="runtime").allowed is True


def test_operation_and_resource_are_exact_matches():
    policy = make_policy(PolicyRule("ALLOW", "configuration.read", "runtime"))
    assert evaluate_policy(policy, operation="configuration.read.extra", resource="runtime").allowed is False
    assert evaluate_policy(policy, operation="configuration.read", resource="runtime.child").allowed is False


def test_malformed_request_is_denied():
    policy = make_policy(PolicyRule("ALLOW", "configuration.read", "runtime"))
    assert evaluate_policy(policy, operation="", resource="runtime").allowed is False
    assert evaluate_policy(policy, operation="configuration.read", resource="").allowed is False
    assert evaluate_policy(object(), operation="configuration.read", resource="runtime").allowed is False


def test_wildcard_text_does_not_match():
    policy = make_policy(PolicyRule("ALLOW", "configuration.*", "runtime"))
    assert evaluate_policy(policy, operation="configuration.read", resource="runtime").allowed is False


def test_evaluation_is_value_only():
    policy = make_policy(PolicyRule("ALLOW", "configuration.read", "runtime"))
    before = policy.as_dict()
    evaluate_policy(policy, operation="configuration.read", resource="runtime")
    assert policy.as_dict() == before
