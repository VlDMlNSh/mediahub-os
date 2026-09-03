"""P0-07 inert AI proposal and plugin capability boundary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from .authorization import AuthorizationContext
from .configuration_policy_authorization import P0_07_CAPABILITIES
from .proposals import Proposal, ProposalAuthority


@dataclass(frozen=True)
class InertProposal:
    """Validated proposal data with no execution or mutation semantics."""

    proposal: Proposal
    context: AuthorizationContext

    def __post_init__(self) -> None:
        if type(self.proposal) is not Proposal:
            raise ValueError("invalid proposal")
        if type(self.context) is not AuthorizationContext:
            raise ValueError("invalid authorization context")
        if self.proposal.requested_action not in P0_07_CAPABILITIES:
            raise PermissionError("proposal action denied")


@dataclass(frozen=True)
class PluginCapabilityGrant:
    """Explicit device-local plugin grant; validation only, no grant mutation."""

    plugin_id: str
    capability: str

    def __post_init__(self) -> None:
        if type(self.plugin_id) is not str or not self.plugin_id:
            raise ValueError("plugin identifier must be non-empty")
        if len(self.plugin_id.encode("utf-8")) > 128:
            raise ValueError("plugin identifier exceeds allowed length")
        if self.capability not in P0_07_CAPABILITIES:
            raise ValueError("capability is not authorized by P0-07")


class ProposalPluginBoundary:
    """Convert approved proposal data into inert data and validate plugin grants."""

    def __init__(self, authority: ProposalAuthority | None = None) -> None:
        self._authority = authority or ProposalAuthority()

    def accept_proposal(
        self,
        proposal: Proposal,
        context: AuthorizationContext,
        *,
        now: datetime | None = None,
    ) -> InertProposal:
        validated = self._authority.validate(proposal, now=now or datetime.now(timezone.utc))
        return InertProposal(validated, context)

    def validate_plugin_grant(self, grant: PluginCapabilityGrant) -> PluginCapabilityGrant:
        if type(grant) is not PluginCapabilityGrant:
            raise ValueError("invalid plugin grant")
        return grant
