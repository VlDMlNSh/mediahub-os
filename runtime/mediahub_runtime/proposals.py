"""Non-executable AI proposal boundary."""

from dataclasses import dataclass
from datetime import datetime, timezone

from .errors import ExpiredProposal


MAX_PROPOSAL_ID_BYTES = 128
MAX_ACTION_BYTES = 128
MAX_TARGET_BYTES = 128
MAX_GENERATION_BYTES = 128


@dataclass(frozen=True)
class Proposal:
    proposal_id: str
    requested_action: str
    target: str
    confidence: float
    generation: str
    expires_at: datetime

    def __post_init__(self):
        for name, value, limit in (
            ("proposal_id", self.proposal_id, MAX_PROPOSAL_ID_BYTES),
            ("requested_action", self.requested_action, MAX_ACTION_BYTES),
            ("target", self.target, MAX_TARGET_BYTES),
            ("generation", self.generation, MAX_GENERATION_BYTES),
        ):
            if type(value) is not str or not value:
                raise ValueError("proposal identifiers and action fields must be non-empty strings")
            if len(value.encode("utf-8")) > limit:
                raise ValueError("proposal field exceeds allowed length")
        if type(self.confidence) is not float or not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be a finite value between 0 and 1")
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
