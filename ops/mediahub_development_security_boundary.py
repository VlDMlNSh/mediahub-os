"""Composed fail-closed security boundary for cloud development lanes."""
from __future__ import annotations

from dataclasses import dataclass

from ops.mediahub_credential_broker import CredentialBroker, CredentialDenied
from ops.mediahub_egress_controller import EgressController, EgressDenied
from ops.mediahub_policy_engine import PolicyEngine, PolicyRequest


class DevelopmentBoundaryDenied(PermissionError):
    """Raised when any security boundary denies a development task."""


@dataclass
class DevelopmentSecurityBoundary:
    policy: PolicyEngine
    egress: EgressController
    credentials: CredentialBroker

    def authorize(self) -> None:
        try:
            self.egress.authorize()
            self.credentials.authorize()
        except (EgressDenied, CredentialDenied) as exc:
            raise DevelopmentBoundaryDenied(str(exc)) from exc

    def revoke(self) -> None:
        self.policy.revoke()
        self.egress.revoke()
        self.credentials.revoke()

    def admit(self, request: PolicyRequest, destinations: frozenset[str]) -> None:
        try:
            self.policy.require(request)
            for destination in destinations:
                self.egress.admit(destination)
            self.credentials.resolve(request.provider)
        except (PermissionError, OSError) as exc:
            raise DevelopmentBoundaryDenied(str(exc)) from exc

    def credential_ref(self, provider: str):
        try:
            return self.credentials.resolve(provider)
        except (CredentialDenied, OSError) as exc:
            raise DevelopmentBoundaryDenied(str(exc)) from exc
