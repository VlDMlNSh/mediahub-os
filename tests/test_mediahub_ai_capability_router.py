import pytest
from ops.mediahub_ai_capability_router import AIProvider, providers_for, qualify_gemini
from ops.mediahub_gemini_task_policy import GeminiTaskKind


def test_gemini_is_qualified_for_all_declared_development_tasks():
    for kind in GeminiTaskKind:
        assert qualify_gemini(kind)


def test_provider_selection_is_health_gated():
    healthy = frozenset({AIProvider.OMNIROUTE, AIProvider.LOCAL_QWEN})
    assert providers_for("architecture", healthy=healthy) == (AIProvider.OMNIROUTE,)


def test_local_fallback_is_available_for_bounded_coding():
    healthy = frozenset({AIProvider.LOCAL_QWEN})
    assert providers_for("code_generation", healthy=healthy) == (AIProvider.LOCAL_QWEN,)


def test_unknown_task_is_denied():
    with pytest.raises(ValueError):
        providers_for("production_deploy", healthy=frozenset(AIProvider))
