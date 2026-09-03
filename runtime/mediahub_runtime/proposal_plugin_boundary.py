"""P0-07 inert AI proposal and capability-scoped plugin boundary."""

from __future__ import annotations

from dataclasses import dataclass

from .authorization import AuthorizationContext
from .configuration_policy import MAX_IDENTIFIER_BYTES, Proposal
from .configuration_policy_authorization import P0_07_CAPABILITIES


_ALLOWED_RESOURCE_TYPES = frozenset({"configuration", "policy"})


def _valid_identifier(value: str) -> bool:
    return type(value) is str and bool(value) and len(value.encode("utf-8")) <= MAX_IDENTIFIER_BYTES


@dataclass(frozen=True)
class InertProposal:
    """A proposal is data only; it contains no executable operation."""

    proposal: Proposal
    context: AuthorizationContext

    def __post_init__(self) -> None:
        if type(self.proposal) is not Proposal:
            raise ValueError("invalid proposal")
        if type(self.context) is not AuthorizationContext:
            raise ValueError("invalid context")


@dataclass(frozen=True)
class PluginCapabilityGrant:
    """Explicit device-local capability grant; no wildcard or escalation."""

    plugin_id: str
    capability: str

    def __post_init__(self) -> None:
        if not _valid_identifier(self.plugin_id):
            raise ValueError("invalid plugin identifier")
        if self.capability not in P0_07_CAPABILITIES:
            raise ValueError("capability is not authorized by P0-07")


class ProposalPluginBoundary:
    """Accept proposals and plugin grants as bounded inert data only."""

    def accept_proposal(self, proposal: Proposal, context: AuthorizationContext) -> InertProposal:
        candidate = InertProposal(proposal, context)
        if proposal.requested_action not in P0_07_CAPABILITIES:
            raise PermissionError("proposal action denied")
        if proposal.expires_at <= 0:
            raise ValueError("proposal is expired")
        return candidate

    def validate_plugin_grant(self, grant: PluginCapabilityGrant) -> PluginCapabilityGrant:
        if type(grant) is not PluginCapabilityGrant:
            raise ValueError("invalid plugin grant")
        return grant

    def execute_proposal(self, proposal: InertProposal) -> None:
        """Deliberately absent mutation/execution path."""
        raise PermissionError("proposal execution is not permitted")

    def grant_capability(self, grant: PluginCapabilityGrant) -> None:
        """Deliberately absent dynamic grant mutation path."""
        raise PermissionError("dynamic plugin grants are not permitted")
