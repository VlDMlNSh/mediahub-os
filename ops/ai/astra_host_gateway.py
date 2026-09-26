"""MH-21 bounded Astra-to-host proposal boundary.

This module admits a host execution *proposal* only. It never executes a
command, resolves credentials, mutates State Authority, or grants device
authority. Host reachability and enrollment are not authorization.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class HostGatewayDenied(PermissionError):
    """Raised when a host execution proposal cannot be admitted."""


class HostTrust(StrEnum):
    UNKNOWN = "UNKNOWN"
    VERIFIED = "VERIFIED"
    ENROLLED = "ENROLLED"
    AUTHORIZED = "AUTHORIZED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    QUARANTINED = "QUARANTINED"
    REVOKED = "REVOKED"


@dataclass(frozen=True)
class HostExecutionProposal:
    request_id: str
    host_id: str
    workload_id: str
    source_sha: str
    command: str
    timeout_seconds: int
    output_limit_bytes: int
    trust: HostTrust
    authorization_id: str
    capabilities: frozenset[str]


class AstraHostGateway:
    """Translate an approved Astra task into a bounded, non-executing proposal."""

    MAX_TIMEOUT_SECONDS = 900
    MAX_OUTPUT_BYTES = 1_048_576
    REQUIRED_CAPABILITY = "host.execute"

    @classmethod
    def propose(
        cls,
        *,
        request_id: str,
        host_id: str,
        workload_id: str,
        source_sha: str,
        expected_source_sha: str,
        command: str,
        timeout_seconds: int,
        output_limit_bytes: int,
        trust: HostTrust,
        authorization_id: str,
        capabilities: frozenset[str],
    ) -> HostExecutionProposal:
        values = (
            request_id, host_id, workload_id, source_sha,
            expected_source_sha, command, authorization_id,
        )
        if any(
            not isinstance(value, str) or not value or value.strip() != value
            for value in values
        ):
            raise HostGatewayDenied("host proposal identity is invalid")
        if source_sha != expected_source_sha:
            raise HostGatewayDenied("host proposal provenance does not match task")
        if trust is not HostTrust.ACTIVE:
            raise HostGatewayDenied("host is not active and explicitly authorized")
        if not isinstance(capabilities, frozenset):
            raise HostGatewayDenied("host capabilities are invalid")
        if cls.REQUIRED_CAPABILITY not in capabilities:
            raise HostGatewayDenied("required host capability is absent")
        if not isinstance(timeout_seconds, int) or isinstance(timeout_seconds, bool):
            raise HostGatewayDenied("timeout is invalid")
        if not 1 <= timeout_seconds <= cls.MAX_TIMEOUT_SECONDS:
            raise HostGatewayDenied("timeout exceeds host policy")
        if not isinstance(output_limit_bytes, int) or isinstance(output_limit_bytes, bool):
            raise HostGatewayDenied("output limit is invalid")
        if not 1 <= output_limit_bytes <= cls.MAX_OUTPUT_BYTES:
            raise HostGatewayDenied("output limit exceeds host policy")
        if len(command.encode("utf-8")) > 64 * 1024:
            raise HostGatewayDenied("command exceeds bounded size")
        return HostExecutionProposal(
            request_id=request_id,
            host_id=host_id,
            workload_id=workload_id,
            source_sha=source_sha,
            command=command,
            timeout_seconds=timeout_seconds,
            output_limit_bytes=output_limit_bytes,
            trust=trust,
            authorization_id=authorization_id,
            capabilities=capabilities,
        )
