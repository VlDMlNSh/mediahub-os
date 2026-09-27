"""Explicit destination allowlist for MediaHub autonomous development."""
from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse


class EgressDenied(PermissionError):
    """Raised when an external destination is not explicitly approved."""


@dataclass(frozen=True)
class EgressPolicy:
    destinations: frozenset[str]
    max_destinations: int = 16

    def __post_init__(self) -> None:
        if not isinstance(self.destinations, frozenset) or any(not isinstance(destination, str) for destination in self.destinations):
            raise EgressDenied("malformed egress destinations")
        if not isinstance(self.max_destinations, int) or isinstance(self.max_destinations, bool) or self.max_destinations < 0:
            raise EgressDenied("invalid egress destination limit")

@dataclass
class EgressController:
    policy: EgressPolicy
    authorized: bool = False
    revoked: bool = False

    def authorize(self) -> None:
        if self.revoked:
            raise EgressDenied("egress controller is revoked")
        if len(self.policy.destinations) > self.policy.max_destinations:
            raise EgressDenied("egress policy is too broad")
        for destination in self.policy.destinations:
            self._validate_destination(destination)
        self.authorized = True

    def revoke(self) -> None:
        self.authorized = False
        self.revoked = True

    def admit(self, destination: str) -> None:
        if not self.authorized or self.revoked:
            raise EgressDenied("egress is not authorized")
        self._validate_destination(destination)
        if destination not in self.policy.destinations:
            raise EgressDenied("destination is not allowlisted")

    @staticmethod
    def _validate_destination(destination: str) -> None:
        parsed = urlparse(destination)
        if parsed.scheme != "https" or not parsed.hostname:
            raise EgressDenied("only HTTPS destinations with a hostname are allowed")
        if parsed.username or parsed.password:
            raise EgressDenied("userinfo in destination is forbidden")
        if parsed.query or parsed.fragment:
            raise EgressDenied("query and fragment are forbidden in policy destinations")
