from ops import astra_first_cycle


def test_local_generation_budget_is_large_enough_for_complete_test_function():
    assert astra_first_cycle.LOCAL_GENERATION_MAX_TOKENS >= 256
