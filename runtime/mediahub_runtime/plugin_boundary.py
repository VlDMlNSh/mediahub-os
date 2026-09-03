"""P0-08 controlled plugin boundary.

The boundary accepts only inert, bounded data. It never exposes State Authority,
transaction, persistence, filesystem, process, network, or credential handles.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .plugin_capabilities import CapabilityDeclaration, CapabilityRequest, PluginCapabilityError
from .plugin_manifest import PluginManifest, PluginManifestError


MAX_REQUEST_BYTES = 256 * 1024
MAX_RESPONSE_BYTES = 256 * 1024
MAX_PAYLOAD_DEPTH = 8
MAX_PAYLOAD_NODES = 512
MAX_STRING_BYTES = 4096
MAX_OBJECT_KEYS = 64


class PluginBoundaryError(ValueError):
    """Raised when plugin input violates the controlled boundary."""


@dataclass(frozen=True)
class PluginRequest:
    plugin_id: str
    capability: str
    operation: str
    payload: Any


@dataclass(frozen=True)
class PluginObservation:
    plugin_id: str
    operation: str
    payload: Any


class PluginBoundary:
    """Validate plugin declarations and inert requests without executing them."""

    def validate_manifest(self, raw: Mapping[str, Any]) -> PluginManifest:
        try:
            return PluginManifest.from_mapping(raw)
        except PluginManifestError as exc:
            raise PluginBoundaryError("manifest_rejected") from exc

    def declare_capabilities(self, manifest: PluginManifest) -> CapabilityDeclaration:
        try:
            return CapabilityDeclaration.from_manifest(manifest)
        except PluginCapabilityError as exc:
            raise PluginBoundaryError("capability_declaration_rejected") from exc

    def validate_request(self, declaration: CapabilityDeclaration, request: PluginRequest) -> PluginRequest:
        if not isinstance(request, PluginRequest):
            raise PluginBoundaryError("request_rejected")
        try:
            capability_request = CapabilityRequest(
                request.plugin_id,
                request.capability,
                request.operation,
            )
        except PluginCapabilityError as exc:
            raise PluginBoundaryError("request_rejected") from exc
        if not capability_request.is_declared_by(declaration):
            raise PluginBoundaryError("capability_not_declared")
        payload = _bounded_copy(request.payload)
        return PluginRequest(request.plugin_id, request.capability, request.operation, payload)

    def observation(self, plugin_id: str, operation: str, payload: Any) -> PluginObservation:
        if type(plugin_id) is not str or not plugin_id:
            raise PluginBoundaryError("observation_rejected")
        if type(operation) is not str or not operation:
            raise PluginBoundaryError("observation_rejected")
        return PluginObservation(plugin_id, operation, _bounded_copy(payload))


def _bounded_copy(value: Any, depth: int = 0, budget: list[int] | None = None) -> Any:
    budget = [0] if budget is None else budget
    budget[0] += 1
    if budget[0] > MAX_PAYLOAD_NODES or depth > MAX_PAYLOAD_DEPTH:
        raise PluginBoundaryError("payload_limit_exceeded")
    if value is None or type(value) is bool or type(value) is int:
        return value
    if type(value) is float:
        if value != value or value in (float("inf"), float("-inf")):
            raise PluginBoundaryError("payload_rejected")
        return value
    if type(value) is str:
        if len(value.encode("utf-8")) > MAX_STRING_BYTES:
            raise PluginBoundaryError("payload_limit_exceeded")
        return value
    if type(value) is list:
        return [_bounded_copy(item, depth + 1, budget) for item in value]
    if type(value) is tuple:
        return tuple(_bounded_copy(item, depth + 1, budget) for item in value)
    if type(value) is dict:
        if len(value) > MAX_OBJECT_KEYS:
            raise PluginBoundaryError("payload_limit_exceeded")
        result = {}
        for key, item in value.items():
            if type(key) is not str or len(key.encode("utf-8")) > 128:
                raise PluginBoundaryError("payload_rejected")
            result[key] = _bounded_copy(item, depth + 1, budget)
        return result
    raise PluginBoundaryError("payload_rejected")
