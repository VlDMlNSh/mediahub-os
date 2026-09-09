import pytest

from ops.mediahub_canonical_protocol import Capability, Protocol, ProviderAdapter
from ops.mediahub_provider_registry import ProviderRecord, ProviderRegistry


class DummyAdapter(ProviderAdapter):
    provider = "dummy"

    def capabilities(self):
        return (Capability("dummy", "model", Protocol.OPENAI_CHAT, "chat.completions"),)

    def encode(self, request):
        raise NotImplementedError

    def decode_response(self, request, payload):
        raise NotImplementedError

    def decode_failure(self, request, status_code, payload):
        raise NotImplementedError


def record(endpoint="https://provider.example/v1"):
    adapter = DummyAdapter()
    return ProviderRecord("dummy", adapter, endpoint, adapter.capabilities())


def test_registry_requires_https():
    registry = ProviderRegistry()
    with pytest.raises(ValueError):
        registry.register(record("http://provider.example/v1"))


def test_registry_rejects_duplicate_provider():
    registry = ProviderRegistry()
    registry.register(record())
    with pytest.raises(ValueError):
        registry.register(record())


def test_registry_requires_identity_match():
    registry = ProviderRegistry()
    adapter = DummyAdapter()
    bad = ProviderRecord("other", adapter, "https://provider.example/v1", adapter.capabilities())
    with pytest.raises(ValueError):
        registry.register(bad)
