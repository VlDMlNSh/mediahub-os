import pytest

from ops.mediahub_gemini_task_policy import (
    CAPABILITIES,
    GeminiTaskKind,
    capability_for,
    execution_authority,
)


def test_gemini_covers_bounded_development_task_classes():
    assert {c.kind for c in CAPABILITIES} == set(GeminiTaskKind)
    assert len(CAPABILITIES) >= 10


@pytest.mark.parametrize("kind", list(GeminiTaskKind))
def test_gemini_tasks_are_advisory_only(kind):
    capability = capability_for(kind)
    assert capability.operation == "generateContent"
    assert execution_authority(kind) == "advisory-proposal-only"
    assert capability.requires_human_gate is False


def test_unknown_task_kind_is_denied():
    with pytest.raises(PermissionError):
        capability_for("production_deploy")
