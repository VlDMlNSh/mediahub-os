from ops.mediahub_free_model_catalog import (
    FREE_MODEL_CANDIDATES,
    FreeTier,
    candidates,
    providers,
)


def test_catalog_is_discovery_only_and_contains_no_openrouter():
    assert FREE_MODEL_CANDIDATES
    assert all(item.provider != "openrouter" for item in FREE_MODEL_CANDIDATES)
    assert all(item.endpoint.startswith("https://") for item in FREE_MODEL_CANDIDATES)


def test_gemini_free_models_are_present():
    models = {item.model for item in candidates("google-gemini")}
    assert models == {"gemini-2.5-flash", "gemini-2.5-flash-lite"}


def test_free_tier_labels_distinguish_access_classes():
    assert any(item.free_tier is FreeTier.PERPETUAL for item in FREE_MODEL_CANDIDATES)
    assert any(item.free_tier is FreeTier.DAILY_ALLOCATION for item in FREE_MODEL_CANDIDATES)
    assert any(item.free_tier is FreeTier.INTRODUCTORY for item in FREE_MODEL_CANDIDATES)


def test_provider_list_is_stable_and_unique():
    listed = providers()
    assert listed == tuple(sorted(set(listed)))
