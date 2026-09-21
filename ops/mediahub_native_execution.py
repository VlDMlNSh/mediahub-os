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
        if not isinstance(self.credential, CredentialRef):
            raise PermissionError("malformed execution credential reference")
        if not all(isinstance(value, str) for value in (self.provider, self.endpoint, self.model)):
            raise PermissionError("malformed execution target")
        if not isinstance(self.protocol, Protocol):
            raise PermissionError("malformed execution protocol")
        if not isinstance(self.credential.provider, str) or not isinstance(self.credential.path, str):
            raise PermissionError("malformed execution credential reference")
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
        if not all(isinstance(value, str) for value in (self.request_id, self.workload_id, self.source_sha, self.provider)):
            raise PermissionError("malformed execution proposal")
        if not all((self.request_id, self.workload_id, self.source_sha, self.provider)):
            raise PermissionError("incomplete execution proposal")


@dataclass(frozen=True)
class ExecutionAdmission:
    proposal: ExecutionProposal
    authorized: bool
    observed_source_sha: str
    recovery_verified: bool

    def validate(self) -> None:
        if not isinstance(self.proposal, ExecutionProposal):
            raise PermissionError("malformed execution admission")
        if not isinstance(self.authorized, bool) or not isinstance(self.recovery_verified, bool):
            raise PermissionError("execution admission verification flags must be boolean")
        self.proposal.validate()
        if self.authorized is not True:
            raise PermissionError("execution authorization is required")
        if self.recovery_verified is not True:
            raise PermissionError("verified recovery evidence is required")
        if not isinstance(self.observed_source_sha, str) or not self.observed_source_sha:
            raise PermissionError("execution provenance is required")
        if self.observed_source_sha != self.proposal.source_sha:
            raise PermissionError("execution provenance does not match proposal")


@dataclass(frozen=True)
class BoundedExecutionRequest:
    proposal: ExecutionProposal
    target: ExecutionTarget
    timeout_seconds: int
    max_output_bytes: int

    def validate(self) -> None:
        if not isinstance(self.proposal, ExecutionProposal) or not isinstance(self.target, ExecutionTarget):
            raise PermissionError("malformed bounded execution request")
        if not isinstance(self.timeout_seconds, int) or isinstance(self.timeout_seconds, bool):
            raise PermissionError("execution timeout must be an integer")
        if not isinstance(self.max_output_bytes, int) or isinstance(self.max_output_bytes, bool):
            raise PermissionError("execution output limit must be an integer")
        self.proposal.validate()
        self.target.validate()
        if self.proposal.provider != self.target.provider:
            raise PermissionError("proposal provider does not match execution target")
        if not 1 <= self.timeout_seconds <= 900:
            raise ValueError("execution timeout is outside the bounded policy")
        if not 1 <= self.max_output_bytes <= 1_048_576:
            raise ValueError("execution output limit is outside the bounded policy")

class BoundedExecutionAdapter:
    def admit_verified(
        self, admission: ExecutionAdmission, target: ExecutionTarget,
        timeout_seconds: int = 60, max_output_bytes: int = 1_048_576,
    ) -> BoundedExecutionRequest:
        if not isinstance(admission, ExecutionAdmission):
            raise PermissionError("malformed execution admission")
        admission.validate()
        return self.admit(admission.proposal, target, timeout_seconds, max_output_bytes)

    def admit(
        self, proposal: ExecutionProposal, target: ExecutionTarget,
        timeout_seconds: int = 60, max_output_bytes: int = 1_048_576,
    ) -> BoundedExecutionRequest:
        request = BoundedExecutionRequest(proposal, target, timeout_seconds, max_output_bytes)
        request.validate()
        return request

    def execute(self, request: BoundedExecutionRequest) -> None:
        raise PermissionError("execution is not permitted at the admission boundary")

    def prepare_headers(self, request: BoundedExecutionRequest) -> Mapping[str, str]:
        raise PermissionError("secret access is not permitted at the admission boundary")

    def prepare_network(self, request: BoundedExecutionRequest) -> None:
        raise PermissionError("network access is not permitted at the admission boundary")


@dataclass(frozen=True)
class ExecutionVerification:
    request: BoundedExecutionRequest
    status: str
    observed_source_sha: str

    def validate(self) -> None:
        if not isinstance(self.request, BoundedExecutionRequest):
            raise PermissionError("malformed verification request")
        if not isinstance(self.status, str) or self.status not in {"COMPLETED", "FAILED"}:
            raise PermissionError("unsupported verification status")
        if not isinstance(self.observed_source_sha, str) or not self.observed_source_sha:
            raise PermissionError("malformed verification provenance")
        self.request.validate()
        if self.observed_source_sha != self.request.proposal.source_sha:
            raise PermissionError("verification provenance does not match proposal")

class VerificationBoundary:
    def verify(
        self, request: BoundedExecutionRequest, status: str, observed_source_sha: str,
    ) -> ExecutionVerification:
        verification = ExecutionVerification(request, status, observed_source_sha)
        verification.validate()
        return verification

class NativeExecutionContract:
    def __init__(self, targets: tuple[ExecutionTarget, ...] = ()) -> None:
        self._targets = {t.provider: t for t in targets}
        for target in targets:
            target.validate()

    def target(self, provider: str) -> ExecutionTarget:
        if not isinstance(provider, str) or not provider:
            raise PermissionError("malformed provider identity")
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


    def prepare_recovery_proposal(self, evidence: object, provider: str) -> ExecutionProposal:
        verified = getattr(evidence, "verified", None)
        request_id = getattr(evidence, "request_id", None)
        workload_id = getattr(evidence, "workload_id", None)
        source_sha = getattr(evidence, "source_sha", None)
        if verified is not True:
            raise PermissionError("verified recovery evidence is required")
        if not all(isinstance(value, str) for value in (request_id, workload_id, source_sha, provider)):
            raise PermissionError("malformed recovery evidence")
        return self.prepare_proposal(request_id, workload_id, source_sha, provider)
    def prepare_headers(self, target: ExecutionTarget, secret: str) -> Mapping[str, str]:
        target.validate()
        if not isinstance(secret, str) or not secret:
            raise PermissionError("missing provider credential")
        if target.provider == "openai":
            return {"authorization": f"Bearer {secret}", "content-type": "application/json"}
        if target.provider == "anthropic":
            return {"x-api-key": secret, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        raise PermissionError(f"unsupported native provider: {target.provider}")
