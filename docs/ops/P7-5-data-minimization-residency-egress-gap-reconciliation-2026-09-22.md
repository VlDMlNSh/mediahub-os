# P7.5 — Data minimization, residency/policy and egress boundary

Status: DISCOVERY_RECONCILIATION / P7.5 NOT CLOSED

## Scope

This artifact records deterministic repository evidence for existing Cloud Development AI data-minimization, residency/policy and egress requirements. It does not infer provider guarantees, regions, retention periods or external runtime behavior.

## Deterministic classification

- Existing policy/contract declarations: PRESENT where recorded below.
- Existing generic PolicyEngine/EgressController implementation and tests: PRESENT in the inspected repository surfaces.
- Human-Clone-specific acceptance of minimization, residency/policy and egress: NOT ESTABLISHED by this reconciliation alone.
- Overall P7.5 status: PARTIAL — generic controls are evidenced, but subsystem-specific acceptance is not demonstrated here.

## Source evidence

### specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md
SHA256: 9cab7f0518208ecaeae8f605785a9e25eb9ed1ae9db420b19898fe83059dc18a
- 7: **Change policy:** baseline 1.0 immutable; изменения только через новую версию и governance-проход.
- 126: local resources и при policy, privacy, authorization, residency и egress controls.
- 129: Эскалация определяется latency, privacy, capability, resources, data classification, criticality,
- 130: user policy, cost и network. Ни один AI tier не получает mutation authority автоматически.
- 182: Cloud boundary: authorization, minimization, residency, egress control, audit, metering,
- 216: cloud boundary и egress control.
- 263: Implementation → unit/integration/negative-path tests → security → regression → provenance

### specification/contract-registry.yaml
SHA256: b49e4abf80ea4f73982a2297ebae68b56a6034cad58aeaa11179c25f24e253e4
- 40: required_semantics: immutable identity, source, causal chain, ordering, deduplication, retention, replay policy
- 64: scope: camera discovery, live, direct recording, archive, playback, search and export
- 65: required_semantics: stream identity, transport, recording policy, timestamps, retention handoff, integrity, privacy, export authorization
- 95: required_semantics: privileged identity, workload authorization, egress control, data minimization, residency, audit, metering, isolation
- 100: required_semantics: local attempt, escalation criteria, user/data authorization, sensitive-data policy, provider/model qualification, audit, fallback
- 115: required_semantics: evidence collection, correlation, reproducibility, privacy, access control and export
- 134: scope: data minimization, access, processing and disclosure controls
- 135: required_semantics: classification, purpose, retention, residency, processing, export/egress, policy and audit

### docs/architecture/MH-13-privacy-data-governance.md
SHA256: 786508c524ed445edf3d34eddf4f367690cdaaae115bbab83d28ff06a0c23335
- 38: ### 2.1 Data classification
- 40: Privacy-aware classification is required before applicable downstream operations, especially external egress. Exact historical classification levels are UNKNOWN / REQUIRES VERIFICATION.
- 44: Data use is purpose-bound to an authorized purpose. Exact historical purpose vocabulary and policy representation are UNKNOWN / REQUIRES VERIFICATION.
- 46: ### 2.3 Data minimization
- 48: Collection, processing, retention and transfer are minimized relative to the authorized purpose. Minimization and redaction are required controls for sensitive/private data.
- 72: No provider is implicitly trusted by this reconstruction. Exact provider contracts, regions, deletion guarantees, training-use terms and residency rules remain UNKNOWN / REQUIRES VERIFICATION.
- 80: AI has no privacy authority. AI routing MUST NOT weaken MH-13 restrictions. AI processing is subject to classification, purpose, minimization, authorization and external-transfer controls.
- 117: 6. Minimization applies to collection, processing and transfer.

### docs/architecture/MH-21-data-residency.md
SHA256: 0f69bf472d258082f8766d9b607a04fd37bd41877c8b6b5b3ba55a6ad6a423eb
- 1: # MH-21 Data Residency

### ops/mediahub_policy_engine.py
SHA256: e7847976a2f9ef0d3c2155ce2e17a639b236ce94216528db4e3815f108cc05d9
- 1: """Deterministic policy engine for autonomous development requests."""
- 7: class PolicyDenied(PermissionError):
- 8: """Raised when a request violates explicit MediaHub policy."""
- 12: class DevelopmentPolicy:
- 21: class PolicyRequest:
- 31: class PolicyDecision:
- 41: class PolicyEngine:
- 42: def __init__(self, policy: DevelopmentPolicy):

### ops/mediahub_egress_controller.py
SHA256: 89d9d3dc73b974ee0ba2bdd66840c81d3f3e8304cb74d25c8b8dd5e83aef9c27
- 1: """Explicit destination allowlist for MediaHub autonomous development."""
- 8: class EgressDenied(PermissionError):
- 13: class EgressPolicy:
- 19: raise EgressDenied("malformed egress destinations")
- 21: raise EgressDenied("invalid egress destination limit")
- 24: class EgressController:
- 25: policy: EgressPolicy
- 31: raise EgressDenied("egress controller is revoked")

### tests/test_mediahub_policy_engine.py
SHA256: 08fe09af64f9d2c566e7d5ea4663ff6fe3c2c125069a01cc0e822cdbcca78337
- 3: from ops.mediahub_policy_engine import (
- 4: DevelopmentPolicy,
- 5: PolicyDenied,
- 6: PolicyEngine,
- 7: PolicyRequest,
- 13: return PolicyEngine(DevelopmentPolicy(
- 24: return PolicyRequest(**values)
- 32: def test_provider_protocol_and_data_class_are_allowlists(engine):

### tests/test_mediahub_egress_controller.py
SHA256: 79c668785a557224d54141991750cfa058db7f37566ef5025569e3d174674a46
- 3: from ops.mediahub_egress_controller import EgressController, EgressDenied, EgressPolicy
- 6: def test_egress_is_fail_closed():
- 7: controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
- 8: with pytest.raises(EgressDenied):
- 12: def test_allowlisted_destination_is_admitted():
- 13: controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
- 19: controller = EgressController(EgressPolicy(frozenset({"https://api.example.com"})))
- 22: with pytest.raises(EgressDenied):
