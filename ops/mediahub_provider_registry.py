"""MediaHub-native provider registry.

The registry is deliberately provider-neutral. It stores qualified adapter
metadata and rejects duplicate provider registrations. Runtime authority,
credentials, policy and egress remain outside this registry.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from ops.mediahub_canonical_protocol import Capability, ProviderAdapter


@dataclass(frozen=True)
class ProviderRecord:
    provider: str
    adapter: ProviderAdapter
    endpoint: str
    capabilities: tuple[Capability, ...]
    enabled: bool = True
    metadata: Mapping[str, str] = MappingProxyType({})


class ProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, ProviderRecord] = {}

    def register(self, record: ProviderRecord) -> None:
        if not record.provider or record.provider != record.adapter.provider:
            raise ValueError("provider identity must match adapter identity")
        if not record.endpoint.startswith("https://"):
            raise ValueError("provider endpoint must use HTTPS")
        if record.provider in self._providers:
            raise ValueError(f"provider already registered: {record.provider}")
        self._providers[record.provider] = record

    def get(self, provider: str) -> ProviderRecord:
        try:
            return self._providers[provider]
        except KeyError as exc:
            raise KeyError(f"provider not registered: {provider}") from exc

    def enabled(self) -> tuple[ProviderRecord, ...]:
        return tuple(record for record in self._providers.values() if record.enabled)

    def capabilities(self, provider: str) -> tuple[Capability, ...]:
        return self.get(provider).capabilities
