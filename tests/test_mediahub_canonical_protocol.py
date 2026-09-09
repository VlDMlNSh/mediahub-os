import pytest

from ops.mediahub_canonical_protocol import (
    Capability,
    CapabilityMatrix,
    FailureClass,
    Protocol,
)


def test_unknown_capability_is_denied():
    matrix = CapabilityMatrix(
        (Capability("continuum", "claude-sonnet-4-5", Protocol.OPENAI_RESPONSES, "responses"),)
    )
    assert not matrix.supports("continuum", "unknown", Protocol.OPENAI_RESPONSES, "responses")
    with pytest.raises(PermissionError):
        matrix.require("continuum", "unknown", Protocol.OPENAI_RESPONSES, "responses")


def test_wildcard_model_is_explicitly_qualified():
    matrix = CapabilityMatrix(
        (Capability("openrouter", "*", Protocol.OPENAI_CHAT, "chat.completions"),)
    )
    assert matrix.supports("openrouter", "model-x", Protocol.OPENAI_CHAT, "chat.completions")


def test_protocols_are_distinct():
    matrix = CapabilityMatrix(
        (Capability("opper", "model-x", Protocol.OPENAI_CHAT, "chat.completions"),)
    )
    assert matrix.supports("opper", "model-x", Protocol.OPENAI_CHAT, "chat.completions")
    assert not matrix.supports("opper", "model-x", Protocol.OPENAI_RESPONSES, "responses")


def test_failure_classification_enum_is_closed():
    assert FailureClass.POLICY_BLOCKED.value == "policy_blocked"
    assert FailureClass.TRANSIENT.value == "transient"
    assert FailureClass.PERMANENT.value == "permanent"
