"""Bounded, transient P0-07 configuration and policy domain primitives.

This module is deliberately limited to value semantics and deterministic
validation. It does not persist, execute, resolve credentials, access the
network, or mutate State Authority.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


DOCUMENT_MAX_BYTES = 256 * 1024
REQUEST_MAX_BYTES = 256 * 1024
RESPONSE_MAX_BYTES = 256 * 1024
MAX_DEPTH = 8
MAX_NODES = 512
MAX_COLLECTION_ELEMENTS = 128
MAX_STRING_BYTES = 4096
MAX_IDENTIFIER_BYTES = 128
MAX_OBJECT_KEY_BYTES = 128
MAX_OBJECT_KEYS = 64
MAX_POLICY_RULES = 64
MAX_NAMESPACE_SCHEMA_BYTES = 128

_SECRET_KEY_MARKERS = frozenset(
    {
        "password",
        "passwd",
        "secret",
        "token",
        "access_token",
        "refresh_token",
        "api_key",
        "apikey",
        "credential",
        "credentials",
        "private_key",
        "raw_secret",
    }
)


class ConfigurationPolicyError(ValueError):
    """Base class for bounded configuration/policy validation failures."""


class InvalidConfigurationPolicy(ConfigurationPolicyError):
    """Raised when a configuration or policy violates the domain boundary."""


def _fail(message: str) -> None:
    raise InvalidConfigurationPolicy(message)


def _validate_string(value: str, *, label: str, limit: int = MAX_STRING_BYTES) -> None:
    if type(value) is not str or not value:
        _fail(f"{label} must be a non-empty string")
    if len(value.encode("utf-8")) > limit:
        _fail(f"{label} exceeds allowed length")


def _secret_key(key: str) -> bool:
    normalized = key.casefold().replace("-", "_")
    parts = normalized.split("_")
    for marker in _SECRET_KEY_MARKERS:
        marker_parts = marker.split("_")
        if normalized == marker:
            return True
        if len(parts) >= len(marker_parts):
            for index in range(len(parts) - len(marker_parts) + 1):
                if parts[index : index + len(marker_parts)] == marker_parts:
                    return True
    return False


def _freeze_and_validate(value: Any, *, depth: int, nodes: list[int]) -> Any:
    if depth > MAX_DEPTH:
        _fail("value exceeds maximum depth")
    nodes[0] += 1
    if nodes[0] > MAX_NODES:
        _fail("value exceeds maximum node count")

    value_type = type(value)
    if value_type is str:
        if len(value.encode("utf-8")) > MAX_STRING_BYTES:
            _fail("string exceeds allowed length")
        return value
    if value_type is bool or value is None or value_type is int:
        return value
    if value_type is float:
        if not math.isfinite(value):
            _fail("non-finite numeric values are not allowed")
        return value
    if value_type is list:
        if len(value) > MAX_COLLECTION_ELEMENTS:
            _fail("collection exceeds allowed element count")
        return tuple(_freeze_and_validate(item, depth=depth + 1, nodes=nodes) for item in value)
    if value_type is tuple:
        if len(value) > MAX_COLLECTION_ELEMENTS:
            _fail("collection exceeds allowed element count")
        return tuple(_freeze_and_validate(item, depth=depth + 1, nodes=nodes) for item in value)
    if value_type is dict:
        if len(value) > MAX_OBJECT_KEYS:
            _fail("object exceeds allowed key count")
        frozen = {}
        for key, item in value.items():
            if type(key) is not str:
                _fail("object keys must be strings")
            if len(key.encode("utf-8")) > MAX_OBJECT_KEY_BYTES:
                _fail("object key exceeds allowed length")
            if _secret_key(key):
                _fail("credential or secret material is not permitted")
            frozen[key] = _freeze_and_validate(item, depth=depth + 1, nodes=nodes)
        return MappingProxyType(frozen)
    _fail("unsupported value type")


def _plain(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _plain(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_plain(item) for item in value]
    return value


def _document_size(value: Any) -> int:
    try:
        encoded = json.dumps(
            _plain(value),
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError):
        _fail("document is not JSON-compatible")
    if len(encoded) > DOCUMENT_MAX_BYTES:
        _fail("document exceeds allowed size")
    return len(encoded)


@dataclass(frozen=True)
class Configuration:
    """Device-local transient configuration document with immutable values."""

    identity: str
    namespace: str
    schema_version: str
    scope: str
    metadata: Mapping[str, Any]
    value: Any

    def __post_init__(self) -> None:
        _validate_string(self.identity, label="identity", limit=MAX_IDENTIFIER_BYTES)
        _validate_string(self.namespace, label="namespace", limit=MAX_NAMESPACE_SCHEMA_BYTES)
        _validate_string(self.schema_version, label="schema_version", limit=MAX_NAMESPACE_SCHEMA_BYTES)
        _validate_string(self.scope, label="scope", limit=MAX_IDENTIFIER_BYTES)
        if self.scope != "device-local":
            _fail("only device-local scope is authorized")
        if type(self.metadata) is not dict:
            _fail("metadata must be a plain object")
        nodes = [0]
        frozen_metadata = _freeze_and_validate(self.metadata, depth=0, nodes=nodes)
        frozen_value = _freeze_and_validate(self.value, depth=0, nodes=nodes)
        object.__setattr__(self, "metadata", frozen_metadata)
        object.__setattr__(self, "value", frozen_value)
        _document_size(
            {
                "identity": self.identity,
                "namespace": self.namespace,
                "schema_version": self.schema_version,
                "scope": self.scope,
                "metadata": frozen_metadata,
                "value": frozen_value,
            }
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity,
            "namespace": self.namespace,
            "schema_version": self.schema_version,
            "scope": self.scope,
            "metadata": _plain(self.metadata),
            "value": _plain(self.value),
        }


@dataclass(frozen=True)
class PolicyRule:
    """Declarative rule envelope; execution semantics are intentionally absent."""

    effect: str
    operation: str
    resource: str

    def __post_init__(self) -> None:
        _validate_string(self.effect, label="rule.effect", limit=MAX_IDENTIFIER_BYTES)
        _validate_string(self.operation, label="rule.operation", limit=MAX_IDENTIFIER_BYTES)
        _validate_string(self.resource, label="rule.resource", limit=MAX_IDENTIFIER_BYTES)
        if self.effect not in {"ALLOW", "DENY"}:
            _fail("rule.effect must be ALLOW or DENY")


@dataclass(frozen=True)
class Policy:
    """Device-local transient policy document with bounded declarative rules."""

    identity: str
    namespace: str
    version: str
    scope: str
    rules: tuple[PolicyRule, ...]

    def __post_init__(self) -> None:
        _validate_string(self.identity, label="identity", limit=MAX_IDENTIFIER_BYTES)
        _validate_string(self.namespace, label="namespace", limit=MAX_NAMESPACE_SCHEMA_BYTES)
        _validate_string(self.version, label="version", limit=MAX_IDENTIFIER_BYTES)
        _validate_string(self.scope, label="scope", limit=MAX_IDENTIFIER_BYTES)
        if self.scope != "device-local":
            _fail("only device-local scope is authorized")
        if type(self.rules) is not tuple:
            _fail("rules must be an immutable tuple")
        if len(self.rules) > MAX_POLICY_RULES:
            _fail("policy exceeds allowed rule count")
        for rule in self.rules:
            if type(rule) is not PolicyRule:
                _fail("policy rules must be PolicyRule instances")
        _document_size(
            {
                "identity": self.identity,
                "namespace": self.namespace,
                "version": self.version,
                "scope": self.scope,
                "rules": [
                    {"effect": r.effect, "operation": r.operation, "resource": r.resource}
                    for r in self.rules
                ],
            }
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "identity": self.identity,
            "namespace": self.namespace,
            "version": self.version,
            "scope": self.scope,
            "rules": [
                {"effect": r.effect, "operation": r.operation, "resource": r.resource}
                for r in self.rules
            ],
        }


def validate_configuration(configuration: Configuration) -> Configuration:
    """Validate and return an already bounded configuration."""
    if type(configuration) is not Configuration:
        _fail("configuration must be a Configuration instance")
    return configuration


def validate_policy(policy: Policy) -> Policy:
    """Validate and return an already bounded policy."""
    if type(policy) is not Policy:
        _fail("policy must be a Policy instance")
    return policy