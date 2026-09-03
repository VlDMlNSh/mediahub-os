"""P0-08 inert plugin proposal boundary.

A proposal is data only. It is not a command, authorization decision, state
mutation primitive, persistence request, or execution instruction.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Mapping

from mediahub_runtime.plugin_capabilities import CapabilityRequest
from mediahub_runtime.plugin_resources import ResourceLimitError, bounded_value_size


class PluginProposalError(ValueError):
    """Raised when an inert proposal is malformed or exceeds bounds."""


def _freeze(value: Any) -> Any:
    if type(value) is dict:
        return MappingProxyType({key: _freeze(child) for key, child in value.items()})
    if type(value) is list:
        return tuple(_freeze(child) for child in value)
    if type(value) is tuple:
        return tuple(_freeze(child) for child in value)
    return value


@dataclass(frozen=True)
class InertPluginProposal:
    plugin_id: str
    request: CapabilityRequest
    payload: Mapping[str, Any]

    def __post_init__(self) -> None:
        if type(self.plugin_id) is not str or not self.plugin_id:
            raise PluginProposalError("invalid plugin identity")
        if self.plugin_id != self.request.plugin_id:
            raise PluginProposalError("proposal identity mismatch")
        if type(self.payload) is not dict:
            raise PluginProposalError("proposal payload must be a plain mapping")
        try:
            bounded_value_size(self.payload, max_depth=8, max_nodes=512)
        except ResourceLimitError as exc:
            raise PluginProposalError(str(exc)) from exc
        object.__setattr__(self, "payload", _freeze(self.payload))

    @property
    def is_inert(self) -> bool:
        return True

    def to_observation(self) -> dict[str, Any]:
        return {
            "plugin_id": self.plugin_id,
            "capability": self.request.capability,
            "operation": self.request.operation,
            "payload": _thaw(self.payload),
        }


def _thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _thaw(child) for key, child in value.items()}
    if type(value) is tuple:
        return [_thaw(child) for child in value]
    return value
