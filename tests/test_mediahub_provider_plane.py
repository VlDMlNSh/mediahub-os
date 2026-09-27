import pytest

from ops.mediahub_provider_plane import (
    ProviderHealth,
    choose_provider,
    credentials_present,
    secret_names,
)


HEALTHY = {"openai": ProviderHealth.HEALTHY, "anthropic": ProviderHealth.HEALTHY,
           "local-qwen": ProviderHealth.HEALTHY, "groq": ProviderHealth.HEALTHY}


def test_provider_selection_requires_credential_presence():
    d = choose_provider("code_generation", healthy=HEALTHY)
    assert d.provider == "local-qwen"
    assert d.candidates[0] == "local-qwen"


def test_credential_names_are_metadata_only():
    assert secret_names("openai") == ("OPENAI_API_KEY",)
    assert credentials_present("openai", frozenset()) is False
    assert credentials_present("openai", frozenset({"OPENAI_API_KEY"})) is True


def test_external_provider_is_selected_when_trusted_and_credential_ready():
    d = choose_provider(
        "code_generation",
        healthy=HEALTHY,
        credential_names=frozenset({"OPENAI_API_KEY"}),
    )
    assert d.provider == "openai"
    assert d.candidates == ("openai", "local-qwen")


def test_external_pr_blocks_credential_bearing_providers():
    d = choose_provider(
        "code_generation",
        healthy=HEALTHY,
        credential_names=frozenset({"OPENAI_API_KEY"}),
        external_pr=True,
    )
    assert d.provider == "local-qwen"
    assert d.candidates == ("local-qwen",)


def test_unhealthy_provider_is_skipped():
    health = dict(HEALTHY)
    health["openai"] = ProviderHealth.DOWN
    d = choose_provider("code_generation", healthy=health, credential_names=frozenset({"OPENAI_API_KEY"}))
    assert d.provider == "local-qwen"


def test_unknown_capability_fails_closed():
    d = choose_provider("production_deploy", healthy=HEALTHY, credential_names=frozenset({"OPENAI_API_KEY"}))
    assert d.provider is None
    assert d.reason == "no qualified credential-safe provider"


def test_unknown_provider_secret_lookup_fails_closed():
    with pytest.raises(KeyError):
        secret_names("unknown")
