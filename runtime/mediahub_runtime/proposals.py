"""Non-executable AI proposal boundary."""

from dataclasses import dataclass
from datetime import datetime, timezone

from .errors import ExpiredProposal


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    requested_action: str
    target: str
    confidence: float
    generation: str
    expires_at: datetime

    def __post_init__(self):
        if (
            not self.proposal_id
            or not self.requested_action
            or not self.target
            or not self.generation
        ):
            raise ValueError("proposal identifiers and action fields must be non-empty")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0 and 1")
        if self.expires_at.tzinfo is None:
            raise ValueError("expires_at must be timezone-aware")

    def is_expired(self, now=None):
        now = now or datetime.now(timezone.utc)
        return now >= self.expires_at


class ProposalAuthority:
    """Validates proposals but deliberately exposes no execution primitive."""

    def validate(self, proposal, now=None):
        if not isinstance(proposal, Proposal):
            raise TypeError("proposal must be a Proposal instance")
        if proposal.is_expired(now):
            raise ExpiredProposal(proposal.proposal_id)
        return proposal
