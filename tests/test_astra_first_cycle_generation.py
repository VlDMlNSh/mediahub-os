from ops import astra_first_cycle


def test_local_generation_budget_is_large_enough_for_complete_test_function():
    assert astra_first_cycle.LOCAL_GENERATION_MAX_TOKENS >= 256


def test_generated_patch_has_valid_git_and_unified_headers():
    patch = astra_first_cycle._build_unified_patch(
        "tests/x.py", "def old():\n    return 1\n", "def old():\n    return 1\n\n\ndef new_test():\n    assert True\n"
    )
    assert patch.startswith("diff --git a/tests/x.py b/tests/x.py\n")
    assert "--- a/tests/x.py\n" in patch
    assert "+++ b/tests/x.py\n" in patch


def test_local_generation_timeout_allows_slow_local_model():
    assert astra_first_cycle.LOCAL_MODEL_TIMEOUT_SECONDS >= 60


def test_local_generation_timeout_covers_coder_latency():
    assert astra_first_cycle.LOCAL_MODEL_TIMEOUT_SECONDS >= 120


def test_git_push_arguments_use_supported_git_push_syntax():
    assert "--ff-only" not in astra_first_cycle.GIT_PUSH_ARGS
    assert astra_first_cycle.GIT_PUSH_ARGS[0] == "origin"
