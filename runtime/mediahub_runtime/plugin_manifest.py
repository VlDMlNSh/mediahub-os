"""P0-08 plugin manifest contract.

The manifest is declarative metadata only. It is never an authorization grant,
execution directive, persistence request, or capability escalation mechanism.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping


MAX_PLUGIN_ID_BYTES = 128
MAX_DISPLAY_NAME_BYTES = 256
MAX_VERSION_BYTES = 64
MAX_API_VERSION_BYTES = 64
MAX_CAPABILITIES = 64
MAX_METADATA_KEYS = 32
MAX_METADATA_VALUE_BYTES = 256

_ALLOWED_KEYS = frozenset(
    {
        "schema_version",
        "plugin_id",
        "display_name",
        "plugin_version",
        "api_version",
        "declared_capabilities",
        "resource_limits",
        "metadata",
    }
)

_FORBIDDEN_TERMS = frozenset(
    {
        "credential",
        "credentials",
        "secret",
        "token",
        "password",
        "filesystem",
        "network",
        "shell",
        "command",
        "executable",
        "callback",
        "script",
        "code",
        "native_library",
        "persistence",
        "database",
    }
)


class PluginManifestError(ValueError):
    """Raised when a manifest violates the P0-08 security contract."""


def _bounded_text(value: Any, name: str, limit: int) -> str:
    if type(value) is not str or not value or len(value.encode("utf-8")) > limit:
        raise PluginManifestError(f"invalid {name}")
    return value


def _validate_identifier(value: str, name: str) -> str:
    if any(ch.isspace() for ch in value) or any(ch in value for ch in "/\\"):
        raise PluginManifestError(f"invalid {name}")
    return value


def _validate_capability(value: Any) -> str:
    capability = _bounded_text(value, "capability", MAX_API_VERSION_BYTES)
    parts = capability.split(".")
    if len(parts) != 2 or not all(parts) or "*" in capability:
        raise PluginManifestError("invalid capability")
    if any(ch.isspace() for ch in capability) or any(term in capability.lower() for term in _FORBIDDEN_TERMS):
        raise PluginManifestError("forbidden capability")
    return capability


def _validate_metadata(value: Any) -> Mapping[str, str]:
    if type(value) is not dict or len(value) > MAX_METADATA_KEYS:
        raise PluginManifestError("invalid metadata")
    result: dict[str, str] = {}
    for key, item in value.items():
        key = _bounded_text(key, "metadata key", 128)
        if any(term in key.lower() for term in _FORBIDDEN_TERMS):
            raise PluginManifestError("forbidden metadata key")
        item = _bounded_text(item, "metadata value", MAX_METADATA_VALUE_BYTES)
        result[key] = item
    return MappingProxyType(result)


@dataclass(frozen=True)
class PluginManifest:
    schema_version: str
    plugin_id: str
    display_name: str
    plugin_version: str
    api_version: str
    declared_capabilities: frozenset[str]
    resource_limits: Mapping[str, int]
    metadata: Mapping[str, str]

    @classmethod
    def from_mapping(cls, raw: Mapping[str, Any]) -> "PluginManifest":
        if type(raw) is not dict:
            raise PluginManifestError("manifest must be a plain mapping")
        if set(raw) != _ALLOWED_KEYS:
            raise PluginManifestError("manifest keys must exactly match the schema")

        schema_version = _bounded_text(raw["schema_version"], "schema_version", MAX_VERSION_BYTES)
        plugin_id = _validate_identifier(_bounded_text(raw["plugin_id"], "plugin_id", MAX_PLUGIN_ID_BYTES), "plugin_id")
        display_name = _bounded_text(raw["display_name"], "display_name", MAX_DISPLAY_NAME_BYTES)
        plugin_version = _bounded_text(raw["plugin_version"], "plugin_version", MAX_VERSION_BYTES)
        api_version = _bounded_text(raw["api_version"], "api_version", MAX_API_VERSION_BYTES)

        capabilities = raw["declared_capabilities"]
        if type(capabilities) is not list or not 0 <= len(capabilities) <= MAX_CAPABILITIES:
            raise PluginManifestError("invalid declared_capabilities")
        validated = frozenset(_validate_capability(item) for item in capabilities)
        if len(validated) != len(capabilities):
            raise PluginManifestError("duplicate declared capability")

        limits = raw["resource_limits"]
        if type(limits) is not dict or any(type(k) is not str or type(v) is not int or v < 0 for k, v in limits.items()):
            raise PluginManifestError("invalid resource_limits")
        if any(any(term in k.lower() for term in _FORBIDDEN_TERMS) for k in limits):
            raise PluginManifestError("forbidden resource limit")
        if len(limits) > 32:
            raise PluginManifestError("too many resource limits")

        return cls(
            schema_version=schema_version,
            plugin_id=plugin_id,
            display_name=display_name,
            plugin_version=plugin_version,
            api_version=api_version,
            declared_capabilities=validated,
            resource_limits=MappingProxyType(dict(limits)),
            metadata=_validate_metadata(raw["metadata"]),
        )
