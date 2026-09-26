"""Canonical, credential-free Astra Cloud -> MH-21 host envelope.

The envelope is a transport-neutral proposal record. It is intentionally not
an execution API and cannot mutate State Authority or resolve credentials.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass


class HostEnvelopeDenied(PermissionError):
    """Raised when an Astra host envelope is invalid."""


@dataclass(frozen=True)
class AstraHostEnvelope:
    version: int
    request_id: str
    session_id: str
    conversation_id: str
    generation: int
    host_id: str
    workload_id: str
    source_sha: str
    command: str
    timeout_seconds: int
    output_limit_bytes: int
    authorization_id: str
    capabilities: frozenset[str]

    def __post_init__(self) -> None:
        if self.version != 1:
            raise HostEnvelopeDenied("unsupported envelope version")
        strings = (
            self.request_id, self.session_id, self.conversation_id,
            self.host_id, self.workload_id, self.source_sha,
            self.command, self.authorization_id,
        )
        if any(not isinstance(value, str) or not value or value.strip() != value for value in strings):
            raise HostEnvelopeDenied("envelope identity is invalid")
        if not isinstance(self.generation, int) or isinstance(self.generation, bool) or self.generation < 1:
            raise HostEnvelopeDenied("generation is invalid")
        if not 1 <= self.timeout_seconds <= 900:
            raise HostEnvelopeDenied("timeout is outside the bounded policy")
        if not 1 <= self.output_limit_bytes <= 1_048_576:
            raise HostEnvelopeDenied("output limit is outside the bounded policy")
        if len(self.command.encode("utf-8")) > 64 * 1024:
            raise HostEnvelopeDenied("command exceeds bounded size")
        if not isinstance(self.capabilities, frozenset) or "host.execute" not in self.capabilities:
            raise HostEnvelopeDenied("host execution capability is required")
        if any(not isinstance(capability, str) or not capability for capability in self.capabilities):
            raise HostEnvelopeDenied("capability set is invalid")

    def canonical_payload(self) -> str:
        data = asdict(self)
        data["capabilities"] = sorted(self.capabilities)
        return json.dumps(data, sort_keys=True, separators=(",", ":"))

    def fingerprint(self) -> str:
        return hashlib.sha256(self.canonical_payload().encode("utf-8")).hexdigest()

    def without_credentials(self) -> dict:
        """Return the complete transport payload; credentials are not representable."""
        return json.loads(self.canonical_payload())
