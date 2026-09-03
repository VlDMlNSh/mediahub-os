"""P0-08 inert plugin proposal boundary.

A proposal is data only. It is not a command, authorization decision, state
mutation primitive, persistence request, or execution instruction.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from mediahub_runtime.plugin_capabilities import CapabilityRequest
from mediahub_runtime.plugin_resources import ResourceLimitError, bounded_value_size


class PluginProposalError(ValueError):
    """Raised when an inert proposal is malformed or exceeds bounds."""


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

    @property
    def is_inert(self) -> bool:
        return True

    def to_observation(self) -> dict[str, Any]:
        return {
            "plugin_id": self.plugin_id,
            "capability": self.request.capability,
            "operation": self.request.operation,
            "payload": dict(self.payload),
        }

    def __getattr__(self, name: str) -> Any:
        if name in {
            "execute", "commit", "authorize", "grant", "state_authority",
            "persistence", "filesystem", "network", "subprocess",
        }:
            raise AttributeError(name)
        raise AttributeError(name)
