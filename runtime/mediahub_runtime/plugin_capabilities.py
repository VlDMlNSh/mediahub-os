"""P0-08 capability declaration/request model.

Declaration, request, and effective authorization are deliberately separate.
A plugin declaration never grants authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from .plugin_manifest import PluginManifestError, _validate_capability

MAX_REQUEST_CAPABILITIES = 64
MAX_PLUGIN_ID_BYTES = 128


class PluginCapabilityError(ValueError):
    """Raised when a plugin capability contract is violated."""


def _plugin_id(value: object) -> str:
    if type(value) is not str or not value or len(value.encode("utf-8")) > MAX_PLUGIN_ID_BYTES:
        raise PluginCapabilityError("invalid plugin_id")
    return value


@dataclass(frozen=True)
class CapabilityDeclaration:
    plugin_id: str
    capabilities: FrozenSet[str]

    @classmethod
    def from_manifest(cls, manifest: object) -> "CapabilityDeclaration":
        from .plugin_manifest import PluginManifest

        if type(manifest) is not PluginManifest:
            raise PluginCapabilityError("manifest type is invalid")
        return cls(manifest.plugin_id, frozenset(manifest.declared_capabilities))

    def __post_init__(self) -> None:
        _plugin_id(self.plugin_id)
        if type(self.capabilities) is not frozenset or len(self.capabilities) > MAX_REQUEST_CAPABILITIES:
            raise PluginCapabilityError("invalid capability declaration")
        for capability in self.capabilities:
            try:
                if _validate_capability(capability) != capability:
                    raise PluginCapabilityError("invalid capability")
            except PluginManifestError as exc:
                raise PluginCapabilityError(str(exc)) from exc


@dataclass(frozen=True)
class CapabilityRequest:
    plugin_id: str
    capability: str
    operation: str

    def __post_init__(self) -> None:
        _plugin_id(self.plugin_id)
        try:
            canonical = _validate_capability(self.capability)
        except PluginManifestError as exc:
            raise PluginCapabilityError(str(exc)) from exc
        if canonical != self.capability:
            raise PluginCapabilityError("invalid capability")
        if type(self.operation) is not str or not self.operation:
            raise PluginCapabilityError("invalid operation")
        if capability_operation(self.capability) != self.operation:
            raise PluginCapabilityError("capability and operation do not match")

    def is_declared_by(self, declaration: CapabilityDeclaration) -> bool:
        if type(declaration) is not CapabilityDeclaration:
            return False
        return declaration.plugin_id == self.plugin_id and self.capability in declaration.capabilities


def capability_operation(capability: str) -> str:
    try:
        canonical = _validate_capability(capability)
    except PluginManifestError as exc:
        raise PluginCapabilityError(str(exc)) from exc
    return canonical.rsplit(".", 1)[1]
