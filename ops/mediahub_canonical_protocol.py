"""MediaHub-native canonical protocol contracts.

This module deliberately contains no provider-specific HTTP client logic.
Provider adapters translate to/from these contracts after policy/capability
qualification. Unknown capabilities are treated as unsupported by design.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Mapping


class Protocol(str, Enum):
    OPENAI_RESPONSES = "openai.responses"
    OPENAI_CHAT = "openai.chat.completions"
    ANTHROPIC_MESSAGES = "anthropic.messages"


class FailureClass(str, Enum):
    SUCCESS = "success"
    POLICY_BLOCKED = "policy_blocked"
    TRANSIENT = "transient"
    PERMANENT = "permanent"


@dataclass(frozen=True)
class CanonicalRequest:
    request_id: str
    model: str
    protocol: Protocol
    input: Any
    timeout_seconds: float
    policy_context: Mapping[str, str] = field(default_factory=dict)
    generation: Mapping[str, Any] = field(default_factory=dict)
    tools: tuple[Mapping[str, Any], ...] = ()
    metadata: Mapping[str, str] = field(default_factory=dict)
    provider_extensions: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class CanonicalResponse:
    request_id: str
    provider: str
    model: str
    output: Any
    finish_reason: str | None = None
    usage: Mapping[str, Any] = field(default_factory=dict)
    elapsed_ms: int | None = None
    provenance: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class CanonicalFailure:
    request_id: str
    provider: str
    failure_class: FailureClass
    message: str
    status_code: int | None = None
    retry_after_seconds: float | None = None
    retryable: bool = False
    policy_blocked: bool = False
    provenance: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class Capability:
    provider: str
    model_pattern: str
    protocol: Protocol
    operation: str


class CapabilityMatrix:
    """Explicit allow-list: absence of a capability means DENY."""

    def __init__(self, capabilities: tuple[Capability, ...] = ()) -> None:
        self._capabilities = frozenset(capabilities)

    def supports(self, provider: str, model: str, protocol: Protocol, operation: str) -> bool:
        return any(
            c.provider == provider
            and c.protocol == protocol
            and c.operation == operation
            and (c.model_pattern == "*" or c.model_pattern == model)
            for c in self._capabilities
        )

    def require(self, provider: str, model: str, protocol: Protocol, operation: str) -> None:
        if not self.supports(provider, model, protocol, operation):
            raise PermissionError(
                f"capability not qualified: {provider}/{model}/{protocol.value}/{operation}"
            )


class ProviderAdapter:
    """Minimal native adapter boundary; adapters must not bypass policy/egress."""

    provider: str

    def capabilities(self) -> tuple[Capability, ...]:
        raise NotImplementedError

    def encode(self, request: CanonicalRequest) -> tuple[str, Mapping[str, str], bytes]:
        raise NotImplementedError

    def decode_response(self, request: CanonicalRequest, payload: bytes) -> CanonicalResponse:
        raise NotImplementedError

    def decode_failure(self, request: CanonicalRequest, status_code: int | None, payload: bytes) -> CanonicalFailure:
        raise NotImplementedError
