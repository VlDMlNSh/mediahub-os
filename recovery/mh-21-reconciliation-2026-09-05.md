# MH-21 RECONCILIATION — 2026-09-05

Status: RECONCILED WITH AVAILABLE EVIDENCE / NOT ACCEPTED / NOT FROZEN / PRODUCTION BLOCKED

## 1. MH identifier
MH-21 — Hybrid Cloud / Distributed AI.

## 2. Historical scope
Historical contour represented by the current MH-21 architecture chat and its synchronized GitHub artifacts: hybrid cloud, distributed AI, local-first execution, cloud development, remote providers/models, external compute, RAG, distributed agents/tools, network/VPN/egress, cloud credentials, privacy/security, resource/cost governance, offline/degraded operation, observability/audit, provider lifecycle/quarantine, update/recovery and interactions with UI/plugins/media/devices/energy/knowledge graph/automation.

This result does not claim recovery of inaccessible historical MH-21 material beyond the evidence surface actually available in this chat and repository.

## 3. Source evidence and provenance

Authoritative control sources read from `recovery/full-functional-spec`:
- `recovery/forensic-control-point-2026-09-05.md`
- `recovery/MASTER-PROMPT-NEW-CHAT-MH01-23-REDISTRIBUTION-FINAL-2026-09-05.md`
- `recovery/mh01-23-redistribution-projection-matrix-2026-09-05.yaml`
- `specification/capability-registry.yaml`
- `specification/contract-registry.yaml`
- `specification/invariant-registry.yaml`
- `specification/decision-registry.yaml`
- `specification/dependency-graph.yaml`
- `architecture/master-mediahub-architecture-reconstruction-2026-09-05.md`
- `development/implementation-map.yaml`
- `recovery/mh01-23-redistribution-execution-status-2026-09-05.md`

MH-21 evidence surface also includes the existing synchronized architecture records: cloud boundary, external compute contract, provider contract/trust, data egress, local-first, cloud failure, model routing/qualification, RAG security, agent distribution, agent-to-agent, remote execution, resource/cost governance, privacy, observability, audit, offline mode, security invariants, dependency/decision/contradiction/unknown/acceptance registers.

The forensic control point states 58 capabilities, 36 contracts, protected invariants, DEC-001…DEC-012 accepted, DEC-A-001…DEC-A-004 draft, terminal verification partial, Master Architecture draft/not accepted and production blocked. fileciteturn96file0L2-L2

## 4. CAP mapping

Primary MH-21 mappings:
- CAP-024 — local MediaHub cluster coordinated compute/failover.
- CAP-025 — distributed compute and AI processing.
- CAP-026 — privileged cloud development compute/assistant.
- CAP-027 — trusted-source content generation.
- CAP-028 — parameterized website generation.
- CAP-038 — Knowledge Graph interaction.
- CAP-039 — privacy/data governance.
- CAP-040 — security/trust/authentication/authorization/secure remote access.
- CAP-048 — resource quotas/priority/cluster workload governance.
- CAP-050 — simulation/verification/acceptance.

Cross-cutting references are legitimate relationships, not duplicate ownership. CAP ownership remains canonical and unique in the registry. The registry defines CAP-025 as distributed compute/AI, CAP-026 as privileged cloud development, and CAP-040 as security/remote access. fileciteturn97file0L2-L2

## 5. Requirement mapping

R21-01: Hybrid cloud must remain compute, not authority.
R21-02: Local runtime and Local Assistant are primary/first where feasible.
R21-03: Cloud Development is privileged and separated from ordinary-user access.
R21-04: External data transfer requires classification, privacy/security policy and authorization.
R21-05: Remote results, RAG context and agent proposals are data, not authority.
R21-06: Distributed agents cannot self-authorize or inherit/delegate capabilities implicitly.
R21-07: Remote execution is bounded by identity, capability, data, time, resources, credentials and output.
R21-08: Cloud failure cannot disable critical local operation.
R21-09: Provider/model selection and fallback require explicit policy and qualification.
R21-10: External compute is observable, auditable, cost/resource bounded and revocable.
R21-11: Offline and degraded modes preserve local critical behavior.
R21-12: Technology selection remains evidence/ADR gated.

## 6. Contract mapping

Primary contracts:
- CTR-017 cluster — distributed workload/membership/failover boundary.
- CTR-018 cloud-development-boundary — privileged cloud development, egress, minimization, residency, audit and metering.
- CTR-019 assistant-escalation — local-first assistant with controlled cloud escalation.
- CTR-026 privacy — classification, processing, disclosure and egress.
- CTR-035 resource-governance — workload admission, quotas and limits.
- CTR-036 verification-acceptance — evidence and acceptance authority.

Supporting contracts:
CTR-001 state-authority, CTR-002 consumer-boundary, CTR-003 identity/auth, CTR-004 trust, CTR-006 command, CTR-016 network, CTR-020 health, CTR-021 readiness, CTR-022 diagnostics, CTR-023 recovery, CTR-024 update, CTR-033 telemetry, CTR-034 search-knowledge.

The canonical contract registry explicitly defines CTR-018 and CTR-019 as the cloud-development and assistant-escalation surfaces. fileciteturn98file0L2-L2

## 7. Invariant mapping

Directly affected:
- INV-002 security by design.
- INV-005 authentication != authorization.
- INV-006 remote access does not increase authorization.
- INV-007 ordinary user has no Cloud Development access.
- INV-008 local-first.
- INV-009 offline-first where possible.
- INV-017 local cluster is one coordinated system.
- INV-021 security is system-level/cross-cutting.
- INV-024 health/readiness/liveness/trust/authorization remain distinct.
- INV-026 historical evidence preserved.
- INV-029 Cloud Development Cluster distinct from Local MediaHub Cluster.

The invariant registry confirms these baseline constraints. fileciteturn99file0L2-L2

Additional MH-21 architectural invariants are proposed: cloud/AI/agents are not authority; network/VPN/mTLS/API keys are not business authorization; remote results/RAG context are data; arbitrary egress/fallback are forbidden; remote execution is bounded and revocable; cloud failure cannot disable local critical control.

## 8. Decision mapping

Accepted baseline decisions implicated:
- DEC-005 local-first/offline-first.
- DEC-006 Cloud Development privileged internal infrastructure.
- DEC-007 Local MediaHub Cluster is one coordinated user-facing system.
- DEC-009 security is system-level invariant.
- DEC-012 deferred detail remains preserved, not rejected.

Architecture proposals implicated but NOT accepted:
- DEC-A-003 separate Local MediaHub Cluster and Cloud Development trust/control planes.
- DEC-A-001 capability-centric contract-driven architecture.
- DEC-A-002 explicit authority/security boundaries.

The decision registry marks DEC-A-001…DEC-A-004 as DRAFT. fileciteturn100file0L2-L2

## 9. Architecture / boundary mapping

Canonical projection:
Local Request → classification → privacy/security policy → authorization → workload placement → external compute adapter → remote compute → untrusted result → validation → provenance → policy → authorization → Consumer Boundary → State Authority.

Forbidden direct paths:
- Cloud → State Authority.
- Cloud → critical Device.
- Agent → State Authority.
- Agent → critical Device without local authorization chain.
- RAG context → authority.

The synchronized cloud-boundary artifact explicitly records the controlled bridge and forbidden direct paths. fileciteturn120file0L2-L2

## 10. Classification of material items

| Material | Classification | Reason |
|---|---|---|
| External compute is not authority | RETAIN | Direct canonical MH-21 principle; consistent with P0 boundaries |
| Local-first/cloud escalation | RETAIN | Consistent with DEC-005 and CTR-019 |
| Cloud Development separation | RETAIN | Consistent with DEC-006 / INV-007 / INV-029 |
| Distributed compute without distributed authority | RETAIN | Preserves CTR-001/state authority |
| Provider-neutral adapter boundary | RETAIN | Prevents canonical provider coupling |
| Default-deny egress | RETAIN as PROPOSED CONTROL | Requires enforcement evidence |
| RAG untrusted-data model | RETAIN as PROPOSED CONTROL | Security boundary; no authority from documents |
| Agent capability isolation | RETAIN as PROPOSED CONTROL | Requires runtime verification |
| Remote execution boundary | RETAIN as PROPOSED / NOT AUTHORIZED | No unrestricted shell/filesystem/device/master-secret access |
| Specific technology choices | UNKNOWN / EVIDENCE-BLOCKED | No sufficient qualification evidence |
| Production cloud runtime readiness | UNKNOWN | No runtime qualification evidence |
| Absence of cloud→device bypass | UNKNOWN | No complete runtime proof |
| Historical material not visible in current corpus | UNKNOWN | Anti-loss rule prohibits inference |
| Intentional retirement of MH-21 capability | RETIRE NOT JUSTIFIED | No authoritative retirement evidence |

The external compute contract defines a bounded workload and states that completion never grants mutation authority. fileciteturn118file0L2-L2

## 11. Contradictions

C21-001: `remote/local/hybrid` is compute placement, not trust/authorization — RESOLVED architecturally.

C21-002: configured provider/adapter endpoint is not permission; egress policy decides eligibility — RESOLVED architecturally.

C21-003: AI output is data and cannot be interpreted as authority — CONTROL REQUIRED.

C21-004: code-search absence cannot prove runtime absence — UNKNOWN / REQUIRES VERIFICATION.

These are already recorded in the MH-21 contradiction register. fileciteturn108file0L2-L2

## 12. Missing evidence / search scope

Searched/read:
- canonical control point;
- canonical registries;
- projection matrix;
- master architecture draft;
- implementation map;
- MH-21 architecture records and registers available on the target branch;
- current MH-21 chat evidence retained in the project context.

Still missing/insufficient:
actual deployed provider contracts; retention/training behavior; regions; network/VPN topology; remote worker/GPU deployment; concrete agent/RAG runtimes; provider credentials; production routing; enforced egress; model qualification; SBOM/provenance; resource/cost limits; provider guarantees; complete cloud→device and cloud→State Authority runtime traces; chaos results; local hardware capacity.

The Unknown Register independently records these evidence gaps. fileciteturn107file0L2-L2

## 13. Dangling references

No canonical registry endpoint was identified as dangling within the fetched dependency/contract/capability surfaces.

Potential runtime dangling references remain UNKNOWN where implementation evidence is absent: provider endpoints, worker identities, agent runtimes, RAG/vector runtime, egress enforcement and cloud→device/cloud→State Authority paths.

## 14. Stale references

No authoritative stale reference was established. Technology names such as Docker/Compose/Kubernetes/WireGuard/Tailscale/Ollama/vLLM/llama.cpp and specific providers remain candidates, not canonical selections.

## 15. Proposed technical decisions

TD21-001: adopt a provider-neutral external-compute adapter contract.
TD21-002: enforce default-deny external egress with classification/purpose/destination/policy/authorization.
TD21-003: require model/provider qualification and explicit approved fallback sets.
TD21-004: require separate agent identities and explicit bounded capability delegation.
TD21-005: require bounded remote execution with no unrestricted shell/filesystem/device/State Authority/master-secret access.
TD21-006: require provider lifecycle states including quarantine/revocation.
TD21-007: require cost/resource/iteration/time/concurrency bounds and safe termination.
TD21-008: require offline/emergency-offline preservation of critical local control.
TD21-009: require end-to-end audit/provenance for external workloads and outcomes.

All remain PROPOSED / OPEN until evidence, alternatives, constraints, contract impact, invariant impact, verification criteria and acceptance authority are supplied.

## 16. Contract impacts

Potential impacts: CTR-018, CTR-019, CTR-026, CTR-035 and CTR-036; supporting impacts to CTR-003, CTR-004, CTR-016, CTR-017, CTR-033 and CTR-034.

No canonical contract registry was changed by MH-21.

## 17. Invariant impacts

No protected INV-001…INV-030 was changed. MH-21 adds candidate enforcement detail beneath the protected baseline. Any future change affecting state authority, local-first, cloud separation, security, storage or user authority requires central reconciliation.

## 18. Dependency impacts

Primary dependencies: security_core, cluster_core, assistant_core, cloud_development, privacy_security, network_core, observability, resource_governance, knowledge_core and runtime_core. MH-21 is consumed by MH-22 qualification/operations and intersects MH-10, MH-11, MH-12, MH-13, MH-14, MH-15, MH-16, MH-19 and MH-20.

The dependency map describes MH-21 as dependent on these cross-domain contours and MH-22 as consumer of MH-21 qualification/operations artifacts. fileciteturn109file0L2-L2

## 19. Verification requirements

Required evidence:
1. End-to-end local→remote→local traces.
2. Explicit identity/auth/authorization evidence.
3. Data-classification/egress enforcement tests.
4. Provider/model qualification records.
5. RAG prompt-injection and authority-confusion tests.
6. Agent/tool capability isolation tests.
7. Cloud→device and cloud→State Authority negative-path tests.
8. Credential/secret non-exposure tests.
9. Provider outage/timeout/malformed-output/rate-limit tests.
10. Cost/resource exhaustion and runaway-agent tests.
11. Offline/degraded/emergency-offline tests.
12. Observability/audit completeness tests.
13. Supply-chain/provenance/SBOM evidence.
14. Chaos tests for DNS/TLS/network/provider/model/API failures.

## 20. Acceptance evidence

Current acceptance evidence is insufficient. The MH-21 acceptance criteria remain NOT SATISFIED. fileciteturn110file0L2-L2

Acceptance authority: central reconciliation + explicit human acceptance. MH-21 has no unilateral acceptance authority.

## 21. Items that must remain OPEN

- Exact provider/model/runtime selection.
- Exact cloud/VPN/network topology.
- Exact credentials and identity architecture.
- Exact data residency/retention/training behavior.
- Exact egress enforcement mechanism.
- Exact agent/RAG/vector runtime.
- Exact remote GPU/worker topology.
- Exact resource/cost limits.
- Exact qualification criteria and test evidence.
- Complete runtime proof of forbidden direct paths.
- Production cloud readiness.

## 22. Anti-loss confirmation

**PASS.** No capability was removed, retired or silently replaced. Unknown historical corpus remains UNKNOWN/EVIDENCE_GAP. The canonical baseline remains 58/58 preserved. The control point explicitly requires inaccessible scopes to remain UNKNOWN/EVIDENCE_GAP rather than being interpreted as loss. fileciteturn96file0L2-L2

## 23. Suggested canonical registry changes

1. Consider adding an explicit provider-neutral external-compute contract family after central review.
2. Consider extending CTR-018/CTR-019 with explicit egress, qualification, provenance and quarantine semantics.
3. Consider extending INV registry with explicit remote-compute non-authority invariants if central reconciliation determines they are globally canonical.
4. Consider adding decision entries for provider qualification, explicit fallback sets and remote-execution bounds.
5. Consider adding MH-21-specific verification cases to the canonical verification registry.

Each suggestion requires reason, evidence, affected CAP/CTR/INV/DEC, dependency impact, verification impact and explicit acceptance authority. None is applied by this MH chat.

## 24. Explicit authority statement

MH-21 has **NO UNILATERAL AUTHORITY** to modify capability, contract, invariant, decision, ownership or master-architecture canonical truth.

## 25. Final MH-21 result

**RECONCILIATION: COMPLETE FOR AVAILABLE EVIDENCE SURFACE.**

**HISTORICAL CORPUS: PARTIAL / NOT EXHAUSTIVELY RECOVERED.**

**FUNCTION LOSS: NONE ESTABLISHED.**

**CANONICAL REGISTRY CHANGES: NONE APPLIED.**

**MASTER ARCHITECTURE: DRAFT / NOT ACCEPTED.**

**PRODUCTION: BLOCKED.**
