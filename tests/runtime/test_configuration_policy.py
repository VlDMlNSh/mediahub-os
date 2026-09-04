import math

import pytest

from mediahub_runtime.configuration_policy import (
    Configuration,
    InvalidConfigurationPolicy,
    Policy,
    PolicyRule,
    MAX_COLLECTION_ELEMENTS,
    MAX_DEPTH,
    MAX_NODES,
    MAX_OBJECT_KEYS,
    MAX_POLICY_RULES,
    MAX_STRING_BYTES,
)


def make_config(value):
    return Configuration(
        identity="runtime",
        namespace="mediahub.runtime",
        schema_version="1",
        scope="device-local",
        metadata={},
        value=value,
    )


def make_policy(rules):
    return Policy(
        identity="runtime",
        namespace="mediahub.runtime",
        version="1",
        scope="device-local",
        rules=tuple(rules),
    )


def test_configuration_is_value_immutable():
    config = make_config({"nested": [1, 2]})
    assert config.value["nested"] == (1, 2)
    with pytest.raises(TypeError):
        config.value["nested"] = ()
    with pytest.raises(AttributeError):
        config.value["nested"].append(3)


def test_subclasses_are_rejected():
    class ValueDict(dict):
        pass

    with pytest.raises(InvalidConfigurationPolicy):
        make_config(ValueDict(foo="bar"))


def test_non_finite_numbers_are_rejected():
    for value in (math.nan, math.inf, -math.inf):
        with pytest.raises(InvalidConfigurationPolicy):
            make_config(value)


def test_secret_and_credential_keys_are_rejected():
    for key in (
        "password",
        "api_key",
        "access-token",
        "my_secret",
        "my_api_key",
        "service_access_token",
        "user_private_key",
        "raw_secret_value",
    ):
        with pytest.raises(InvalidConfigurationPolicy):
            make_config({key: "value"})


def test_secret_markers_are_detected_as_contiguous_tokens():
    for key in ("my-api-key", "service-refresh-token", "stored-private-key"):
        with pytest.raises(InvalidConfigurationPolicy):
            make_config({key: "value"})


def test_non_secret_similar_keys_remain_allowed():
    config = make_config({"tokenizer": "value", "secretary": "value", "credentialing": "value"})
    assert config.value["tokenizer"] == "value"


def test_collection_and_object_bounds_are_enforced():
    with pytest.raises(InvalidConfigurationPolicy):
        make_config(list(range(MAX_COLLECTION_ELEMENTS + 1)))
    with pytest.raises(InvalidConfigurationPolicy):
        make_config({str(i): i for i in range(MAX_OBJECT_KEYS + 1)})


def test_string_bound_is_enforced():
    with pytest.raises(InvalidConfigurationPolicy):
        make_config("x" * (MAX_STRING_BYTES + 1))


def test_node_and_depth_bounds_are_enforced():
    too_deep = 1
    for _ in range(MAX_DEPTH + 1):
        too_deep = [too_deep]
    with pytest.raises(InvalidConfigurationPolicy):
        make_config(too_deep)
    with pytest.raises(InvalidConfigurationPolicy):
        make_config([list(range(MAX_NODES))])


def test_scope_is_device_local_only():
    with pytest.raises(InvalidConfigurationPolicy):
        Configuration("runtime", "mediahub.runtime", "1", "project", {}, {})


def test_policy_rule_effect_is_explicit():
    assert PolicyRule("ALLOW", "configuration.read", "runtime")
    assert PolicyRule("DENY", "configuration.update", "runtime")
    with pytest.raises(InvalidConfigurationPolicy):
        PolicyRule("MAYBE", "configuration.read", "runtime")


def test_policy_rule_count_is_bounded():
    rules = [PolicyRule("DENY", "configuration.read", "runtime") for _ in range(MAX_POLICY_RULES + 1)]
    with pytest.raises(InvalidConfigurationPolicy):
        make_policy(rules)


def test_policy_requires_immutable_rule_collection():
    with pytest.raises(InvalidConfigurationPolicy):
        Policy("runtime", "mediahub.runtime", "1", "device-local", [])
