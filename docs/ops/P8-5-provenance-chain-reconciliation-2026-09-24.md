# P8.5 — Provenance chain reconciliation

Status: PROVENANCE_RECONCILIATION / P8.5 NOT CLOSED

## Scope

This record traces the existing provenance identifiers across request/proposal, recovery evidence and AI adapter result boundaries. It does not create a persistence mechanism or infer a complete request→artifact→result→evidence journal where the repository does not demonstrate one.

## Deterministic findings

- `request_id`, `workload_id`, `source_sha` and `provider` are validated and bound at the native execution proposal boundary.
- Recovery evidence is required to be verified and provenance-matching before proposal admission.
- Cluster recovery evidence carries request/workload/source provenance into native execution admission.
- The AI adapter exposes source provenance in its result contract.
- A single persistent, independently verifiable chain linking request → produced artifact → execution result → evidence is not established by these surfaces alone.

## Closure

P8.5 remains OPEN. Full closure requires an existing or explicitly authorized provenance record that links every lifecycle hop without adding hidden persistence or bypassing authority boundaries.

## Source evidence

### ops/mediahub_native_execution.py
SHA256: db7e67d988bb19a2c0b88bdf29ccda4a7b578df92e08da1f001f346213400a5a
- L13: provider: str
- L18: provider: str
- L27: if not all(isinstance(value, str) for value in (self.provider, self.endpoint, self.model)):
- L31: if not isinstance(self.credential.provider, str) or not isinstance(self.credential.path, str):
- L33: if self.provider != self.credential.provider:
- L34: raise PermissionError("credential provider mismatch")
- L43: request_id: str
- L44: workload_id: str
- L45: source_sha: str
- L46: provider: str
- L49: if not all(isinstance(value, str) for value in (self.request_id, self.workload_id, self.source_sha, self.provider)):
- L51: if not all((self.request_id, self.workload_id, self.source_sha, self.provider)):
- L59: observed_source_sha: str
- L71: raise PermissionError("verified recovery evidence is required")
- L72: if not isinstance(self.observed_source_sha, str) or not self.observed_source_sha:
- L74: if self.observed_source_sha != self.proposal.source_sha:
- L94: if self.proposal.provider != self.target.provider:
- L95: raise PermissionError("proposal provider does not match execution target")
- L133: observed_source_sha: str
- L140: if not isinstance(self.observed_source_sha, str) or not self.observed_source_sha:
- L143: if self.observed_source_sha != self.request.proposal.source_sha:
- L148: self, request: BoundedExecutionRequest, status: str, observed_source_sha: str,
- L150: verification = ExecutionVerification(request, status, observed_source_sha)
- L156: self._targets = {t.provider: t for t in targets}
- L160: def target(self, provider: str) -> ExecutionTarget:
- L161: if not isinstance(provider, str) or not provider:
- L162: raise PermissionError("malformed provider identity")
- L164: return self._targets[provider]
- L166: raise PermissionError(f"provider not qualified: {provider}") from exc
- L169: self, request_id: str, workload_id: str, source_sha: str, provider: str

### ops/mediahub_cluster_failover.py
SHA256: 4fe575b2f632d374d78c509c0fa95fce05e2d901a5f1d0b9e1bb7ade5b285596
- L1: """Admission-aware Local Cluster failover and deterministic recovery evidence."""
- L31: workload_id: str
- L32: request_id: str
- L33: source_sha: str
- L40: evidence_id: str
- L59: self._evidence: dict[str, RecoveryEvidence] = {}
- L72: current = self._lifecycle.record(workload.workload_id)
- L75: if current.identity.source_sha != workload.source_sha:
- L77: if current.identity.request_id == "":
- L82: old_reservation = self._resources.reserved(workload.workload_id)
- L86: workload.workload_id,
- L93: decision = self._lifecycle.failover(workload.workload_id, failure)
- L97: workload.workload_id,
- L102: record = self._lifecycle.reassign(workload.workload_id, new_assignment_id, new_node_id)
- L106: evidence = self._record_evidence(current.identity, record, failure)
- L107: self._evidence[workload.workload_id] = evidence
- L108: return evidence
- L110: def evidence(self, workload_id: str) -> RecoveryEvidence | None:
- L111: return self._evidence.get(workload_id)
- L113: def verify_and_recover(self, workload_id: str) -> RecoveryEvidence:
- L114: evidence = self._evidence.get(workload_id)
- L115: if evidence is None:
- L116: raise FailoverDenied("recovery evidence is required")
- L117: if self._lifecycle.record(workload_id).state is not LifecycleState.REASSIGNED:
- L119: self._lifecycle.transition(workload_id, LifecycleState.VERIFIED)
- L120: self._lifecycle.transition(workload_id, LifecycleState.RECOVERED)
- L122: evidence.workload_id, evidence.request_id, evidence.source_sha,
- L123: evidence.previous_assignment_id, evidence.previous_node_id,
- L124: evidence.replacement_assignment_id, evidence.replacement_node_id,
- L125: evidence.failure, True, evidence.evidence_id,

### ops/ai/ai_adapter.py
SHA256: ff3261a2e5386e350d0b0372d46e2c8c5d93d37da0eec2f866631d9e2f021272
- L53: def provenance(self, request: ProviderRequest, source_sha: str) -> dict[str, str]:
- L54: if not source_sha or not request.task_id:
- L58: "source_sha": source_sha,
- L59: "adapter": "mediahub.provider-neutral.v1",

### tests/test_mediahub_native_execution.py
SHA256: 51ed0d00794c90dc88311aefe2d3b4977ca499a058031cad6fa1a65a0bd40082
- L15: def target(provider="openai"):
- L16: return ExecutionTarget(provider, "https://api.example.test/v1", Protocol.OPENAI_RESPONSES if provider == "openai" else Protocol.ANTHROPIC_MESSAGES, "test-model", CredentialRef(provider, "/credential"))
- L35: def test_credential_provider_mismatch_denied():
- L50: assert proposal.request_id == "req-1"
- L51: assert proposal.workload_id == "work-1"
- L52: assert proposal.source_sha == "sha-1"
- L53: assert proposal.provider == "openai"
- L62: def test_target_rejects_malformed_provider_identity():
- L63: with pytest.raises(PermissionError, match="malformed provider identity"):
- L69: with pytest.raises(PermissionError, match="missing provider credential"):
- L73: def test_recovery_evidence_admits_verified_execution_proposal():
- L76: evidence = SimpleNamespace(verified=True, request_id="req-r", workload_id="work-r", source_sha="sha-r")
- L77: proposal = NativeExecutionContract().prepare_recovery_proposal(evidence, "openai")
- L78: assert proposal.request_id == "req-r"
- L79: assert proposal.workload_id == "work-r"
- L80: assert proposal.source_sha == "sha-r"
- L81: assert proposal.provider == "openai"
- L84: def test_unverified_recovery_evidence_fails_closed():
- L87: evidence = SimpleNamespace(verified=False, request_id="req-r", workload_id="work-r", source_sha="sha-r")
- L89: NativeExecutionContract().prepare_recovery_proposal(evidence, "openai")
- L92: def test_recovery_evidence_missing_identity_fails_closed():
- L95: for evidence in (
- L96: SimpleNamespace(verified=True, request_id="", workload_id="work-r", source_sha="sha-r"),
- L97: SimpleNamespace(verified=True, request_id="req-r", workload_id="", source_sha="sha-r"),
- L98: SimpleNamespace(verified=True, request_id="req-r", workload_id="work-r", source_sha=""),
- L101: NativeExecutionContract().prepare_recovery_proposal(evidence, "openai")
- L109: assert request.target.provider == "openai"
- L114: def test_bounded_execution_adapter_rejects_provider_mismatch():
- L161: def test_verification_boundary_accepts_matching_completed_evidence():
- L166: assert verification.observed_source_sha == "sha-v"

### tests/test_mediahub_cluster_failover.py
SHA256: 3eb108824af203c8f13e0148c29f399c806dc820497b8476970650ec9feabbe2
- L57: evidence = coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
- L58: assert evidence.verified is False
- L59: assert evidence.source_sha == "sha-work"
- L64: def test_verify_and_recover_records_deterministic_evidence():
- L67: second = coordinator.evidence("w1")
- L71: assert recovered.evidence_id == first.evidence_id
- L139: def test_request_identity_is_preserved_and_boundary_has_no_bypass():
- L141: evidence = coordinator.failover(workload, FailureClass.NODE_FAILED, "a2", "node-b")
- L142: assert evidence.request_id == "req-1"
- L177: failover.failover(workload.__class__(workload.workload_id, workload.workload_class, True, 128, 0, "sha"), FailureClass.NODE_FAILED, "a2", "node-b")

### tests/security/test_ai_adapter.py
SHA256: 006a86b1f16ecb3a5f24b715ae9be5200369558cf62a14b45a3e59bca1acda30
- L48: result = adapter.provenance(ProviderRequest(task_id="t1"), "abc123")
- L49: assert result["task_id"] == "t1"
- L50: assert result["source_sha"] == "abc123"
- L51: assert result["adapter"] == "mediahub.provider-neutral.v1"
