import unittest


class StubProvider:
    def __init__(self, provider_id, availability):
        self.provider_id = provider_id
        self.availability = availability


class ProviderSelector:
    """Minimal deterministic selector contract test fixture.

    Runtime implementation is intentionally kept outside State Authority and
    credentials are not part of the selector input.
    """

    def __init__(self, providers, fallback_provider_id):
        self.providers = providers
        self.fallback_provider_id = fallback_provider_id

    def select(self):
        for provider in self.providers:
            if provider.availability == "available":
                return provider.provider_id
        fallback = next(
            provider
            for provider in self.providers
            if provider.provider_id == self.fallback_provider_id
        )
        if fallback.availability == "available":
            return fallback.provider_id
        raise RuntimeError("NO_PROVIDER_AVAILABLE")


class ProviderSelectorContractTests(unittest.TestCase):
    def test_primary_is_selected_when_available(self):
        selector = ProviderSelector(
            [
                StubProvider("openai-api", "available"),
                StubProvider("anthropic", "available"),
                StubProvider("openrouter-free", "available"),
            ],
            "openrouter-free",
        )
        self.assertEqual(selector.select(), "openai-api")

    def test_fallback_is_selected_when_primary_unavailable(self):
        selector = ProviderSelector(
            [
                StubProvider("openai-api", "unavailable"),
                StubProvider("anthropic", "unavailable"),
                StubProvider("openrouter-free", "available"),
            ],
            "openrouter-free",
        )
        self.assertEqual(selector.select(), "openrouter-free")

    def test_fail_closed_when_all_providers_are_unavailable(self):
        selector = ProviderSelector(
            [
                StubProvider("openai-api", "unavailable"),
                StubProvider("anthropic", "unavailable"),
                StubProvider("openrouter-free", "unavailable"),
            ],
            "openrouter-free",
        )
        with self.assertRaisesRegex(RuntimeError, "^NO_PROVIDER_AVAILABLE$"):
            selector.select()

    def test_unknown_provider_state_is_not_selected(self):
        selector = ProviderSelector(
            [
                StubProvider("openai-api", "unknown"),
                StubProvider("openrouter-free", "available"),
            ],
            "openrouter-free",
        )
        self.assertEqual(selector.select(), "openrouter-free")

    def test_selector_has_no_credential_or_endpoint_input(self):
        selector = ProviderSelector(
            [StubProvider("openai-api", "available")],
            "openrouter-free",
        )
        self.assertEqual(selector.select(), "openai-api")
        self.assertFalse(hasattr(selector, "api_key"))
        self.assertFalse(hasattr(selector, "endpoint"))


if __name__ == "__main__":
    unittest.main()
