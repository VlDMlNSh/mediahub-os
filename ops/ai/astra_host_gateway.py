"""MH-21 host execution proposal boundary for Astra.
This module prepares, but does not perform, host execution. Host trust and
authorization are explicit; enrollment is not inferred from reachability.
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


class AstraHostGateway:
    """Translate an approved Astra task into a bounded host proposal."""

    MAX_TIMEOUT_SECONDS = 900
    MAX_OUTPUT_BYTES = 1_048_576

    @classmethod
    def propose(cls, *, request_id: str, host_id: str, workload_id: str,
                source_sha: str, command: str, timeout_seconds: int,
                output_limit_bytes: int, trust: HostTrust,
                authorization_id: str) -> HostExecutionProposal:
        values = (request_id, host_id, workload_id, source_sha, command, authorization_id)
        if any(not isinstance(value, str) or not value or value.strip() != value for value in values):
            raise HostGatewayDenied("host proposal identity is invalid")
        if trust is not HostTrust.AUTHORIZED:
            raise HostGatewayDenied("host is not explicitly authorized")
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
            request_id, host_id, workload_id, source_sha, command,
            timeout_seconds, output_limit_bytes, trust, authorization_id,
        )
