"""Provider-neutral execution contract for cloud development lanes."""
from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from urllib.parse import urlparse

from ops.mediahub_canonical_protocol import Protocol


@dataclass(frozen=True)
class CredentialRef:
    provider: str
    path: str

@dataclass(frozen=True)
class ExecutionTarget:
    provider: str
    endpoint: str
    protocol: Protocol
    model: str
    credential: CredentialRef

    def validate(self) -> None:
        if self.provider != self.credential.provider:
            raise PermissionError("credential provider mismatch")
        if urlparse(self.endpoint).scheme != "https":
            raise PermissionError("execution endpoint must use HTTPS")
        if not self.model or not self.endpoint or not self.credential.path:
            raise ValueError("incomplete execution target")


@dataclass(frozen=True)
class ExecutionProposal:
    request_id: str
    workload_id: str
    source_sha: str
    provider: str

    def validate(self) -> None:
        if not all((self.request_id, self.workload_id, self.source_sha, self.provider)):
            raise PermissionError("incomplete execution proposal")

class NativeExecutionContract:
    def __init__(self, targets: tuple[ExecutionTarget, ...] = ()) -> None:
        self._targets = {t.provider: t for t in targets}
        for target in targets:
            target.validate()

    def target(self, provider: str) -> ExecutionTarget:
        try:
            return self._targets[provider]
        except KeyError as exc:
            raise PermissionError(f"provider not qualified: {provider}") from exc

    def prepare_proposal(
        self, request_id: str, workload_id: str, source_sha: str, provider: str
    ) -> ExecutionProposal:
        proposal = ExecutionProposal(request_id, workload_id, source_sha, provider)
        proposal.validate()
        return proposal

    def prepare_headers(self, target: ExecutionTarget, secret: str) -> Mapping[str, str]:
        target.validate()
        if not secret:
            raise PermissionError("missing provider credential")
        if target.provider == "openai":
            return {"authorization": f"Bearer {secret}", "content-type": "application/json"}
        if target.provider == "anthropic":
            return {"x-api-key": secret, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        raise PermissionError(f"unsupported native provider: {target.provider}")
