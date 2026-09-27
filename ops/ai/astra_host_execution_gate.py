"""MH-21 explicit execution authorization gate.

Converts an admitted Astra host envelope into the existing bounded native
execution contract only when independent authorization and recovery evidence
are explicitly verified. This module never executes, reads secrets, or mutates
State Authority.
"""
from __future__ import annotations

from dataclasses import dataclass

from ops.ai.astra_host_envelope import AstraHostEnvelope
from ops.mediahub_native_execution import (
    BoundedExecutionAdapter,
    BoundedExecutionRequest,
    ExecutionAdmission,
    ExecutionProposal,
    ExecutionTarget,
)


class HostExecutionGateDenied(PermissionError):
    """Raised when explicit remote-execution authorization is absent or invalid."""


@dataclass(frozen=True)
class HostExecutionAdmission:
    proposal: ExecutionProposal
    bounded_request: BoundedExecutionRequest


class AstraHostExecutionGate:
    """Explicit gate between PREPARED admission and the native execution contract."""

    def __init__(self, adapter: BoundedExecutionAdapter | None = None) -> None:
        self._adapter = adapter or BoundedExecutionAdapter()

    def admit(
        self,
        envelope: AstraHostEnvelope,
        target: ExecutionTarget,
        *,
        authorized: bool,
        recovery_verified: bool,
        observed_source_sha: str,
    ) -> HostExecutionAdmission:
        if not isinstance(envelope, AstraHostEnvelope):
            raise HostExecutionGateDenied("invalid host envelope")
        if not isinstance(target, ExecutionTarget):
            raise HostExecutionGateDenied("invalid execution target")
        proposal = ExecutionProposal(
            request_id=envelope.request_id,
            workload_id=envelope.workload_id,
            source_sha=envelope.source_sha,
            provider=target.provider,
        )
        admission = ExecutionAdmission(
            proposal=proposal,
            authorized=authorized,
            observed_source_sha=observed_source_sha,
            recovery_verified=recovery_verified,
        )
        try:
            bounded = self._adapter.admit_verified(
                admission,
                target,
                timeout_seconds=envelope.timeout_seconds,
                max_output_bytes=envelope.output_limit_bytes,
            )
        except (PermissionError, ValueError, TypeError) as exc:
            raise HostExecutionGateDenied("remote execution admission failed closed") from exc
        return HostExecutionAdmission(proposal, bounded)
