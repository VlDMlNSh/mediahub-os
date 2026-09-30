# MH-20 — Architecture Audit — 2026-09-30

Status: **AUDIT COMPLETE / MH-20 NOT CLOSED**

Audit mode: evidence-based reconciliation of existing architecture. No new product architecture is introduced.

## 1. Audit Scope

Audited the existing MediaHub OS / MediaHub iOS architecture represented by MH-01…MH-19, the repository contracts, dependency/implementation maps, security reconciliation records, Smart Home/AI/cloud boundaries, and current qualification evidence.

The audit uses the canonical MH-01…MH-23 map supplied for MH-20. Section 24 Resource Management remains a section, not MH-24.

## 2. Baseline

Repository: `VlDMlNSh/mediahub-os`

Authoritative branch: `engineering/mh21-sandbox-lifecycle-20260910`

Observed branch HEAD: `91f841b1b00f412e218892732c645cae0f1935d8`

Observed HEAD tree: `11fd15ba8a28b03dcfd885ac715aa3cdfed520d9`

R4: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`

R4 tree: `2279612908135418b2b5448d598274ea6741deaa`

R4 ancestry: PASS. GitHub compare reports HEAD 698 commits ahead and 0 behind R4, with R4 as merge base.

Master Architecture remains not accepted by the repository governance records inspected.

## 3. Architecture Map

The intended map is MH-01 charter → MH-02 boundaries → MH-03 runtime → MH-04 security → MH-05 consumer boundary → MH-06 runtime services → MH-07 configuration/policy → MH-08 plugins → MH-09 UI → MH-10 AI → MH-11 observability → MH-12 security analysis → MH-13 privacy → MH-14 persistence → MH-15 OS/appliance → MH-16 update/recovery → MH-17 device/protocol → MH-18 media → MH-19 knowledge graph → MH-20 architecture audit → MH-21 hybrid cloud → MH-22 qualification → MH-23 migration.

The repository artifact `architecture/MH-01-to-MH-23-interface-contract.md` currently assigns MH-20 to “Automation/Energy/Self-Healing”. This conflicts with the canonical MH-20 audit scope and is the primary architecture-register contradiction.

## 4. Authority Audit

**Result: PARTIAL / reconciliation required.**

The architecture consistently distinguishes State Authority from runtime, persistence, cache, AI and cloud. Smart Home authority is separately represented through Home Assistant.

Required canonical layering:

- MediaHub State Authority: canonical platform identity/lifecycle/cross-domain state and governed mutation semantics.
- Home Assistant Core: sole Smart Home operational/device-state authority.
- Knowledge Graph: derived/provenance-bound knowledge, never authority.
- AI: proposal/inference only.
- Cloud: external/non-authoritative.
- UI/cache/observability: non-authoritative.

The State Authority vs HA distinction is technically resolvable without changing product intent, but the contract must explicitly state the domain-specific authority boundary.

## 5. Boundary Audit

**Result: PARTIAL.**

The dependency graph explicitly models local runtime vs cloud development, ordinary user vs engineering/installer, discovery vs trust, trust vs authentication, authentication vs authorization, surveillance vs personal media storage, local cluster vs cloud development cluster, and user runtime vs privileged cloud development.

The missing closure evidence is exhaustive end-to-end data/command/secret/event flow coverage for every production path.

## 6. Trust Audit

**Result: PARTIAL.**

Core trust principles are coherent: discovery does not grant trust, reachability does not grant authorization, capabilities cannot self-expand, unknown states fail closed/quarantine.

Concrete enrollment, attestation, revocation and requalification remain under-specified for several node/device classes.

## 7. Security Audit

**Result: PARTIAL / NOT CLOSED.**

The existing MH-12 security analysis records unresolved cross-contract authorization issues C-01…C-05 and open gaps for mobile authorization, production egress inventory, CPRG qualification, key/root-of-trust profile, durable State Authority/HA security, provenance, SBOM/dependency provenance, node admission, physical/HIGH_SPEED controls, Developer Fabric isolation, recovery and incident evidence.

P9.1–P9.7 records explicitly remain open.

## 8. Privacy Audit

**Result: PARTIAL.**

The architecture defines privacy-by-default, local-first processing and controlled egress. Developer/User separation is explicit.

The audit cannot mark the zero-user-data Developer Fabric invariant as fully qualified because concrete production-path evidence is incomplete. Static secret/dependency review also remains open.

## 9. Local First Audit

**Result: PASS at architectural principle / PARTIAL at qualification.**

The traceability matrix requires local primary operation, no mandatory cloud dependency, deterministic critical paths and cloud non-authority.

Qualification remains incomplete for concrete degraded modes across every product capability.

## 10. State Authority Audit

**Result: PARTIAL / P0 dependency.**

The State Authority contract and negative tests are present for the accepted in-memory scope. The architecture prohibits shadow authority in runtime/cache/persistence.

Durable distributed authority, leader election/failover, epoch semantics, quorum/split-brain handling, rollback and production recovery are not closed by the inspected evidence.

Critical ambiguity must remain fail-closed; Last-Write-Wins must not be the universal conflict resolver for critical state.

## 11. Smart Home Audit

**Result: PARTIAL.**

The declared model is:

User/AI → MediaHub policy/authorization → Home Assistant Core → device → verification/state.

Existing P6 records state that HA authority is declared but the operational HA mutation adapter and runtime end-to-end proof are absent. Voice provider adapters and voice-specific consent/provenance/replay contracts are also absent.

No direct AI → device or AI → HA bypass is accepted.

## 12. Network Audit

**Result: PARTIAL.**

The repository contains explicit egress admission and fail-closed endpoint validation. P9.3 remains open because the evidence does not prove that every production-relevant egress path is covered.

Network reachability, VPN and localhost remain non-authoritative.

## 13. Device / Protocol Audit

**Result: PARTIAL.**

The dependency/implementation maps distinguish device onboarding, management, protocol integration, capability and command paths.

Required lifecycle remains:

Discover → Identify → Authenticate → Capability → Trust → Qualify → Policy Admission → Integrate → Operate → Observe → Update → Revoke/Remove.

Protocol-specific qualification for Matter, HomeKit, AirPlay, ONVIF, RTSP, MQTT, HTTP/WebSocket, SMB/NFS, USB/BLE and industrial protocols is not established by the inspected repository evidence.

## 14. Media Audit

**Result: PARTIAL.**

Logical media/storage ownership exists in the dependency and implementation maps. Personal Media Library and surveillance storage are separately modeled.

Canonical media authority, multi-node storage semantics, DRM compliance, camera retention/deletion, distributed playback, transcoding/resource admission and recovery are not fully qualified.

Media must remain non-authoritative outside its domain.

## 15. Documents Audit

**Result: PARTIAL.**

Document/data/search/knowledge components exist and are separated from State Authority.

The required provenance chain, malicious-document handling, prompt-injection containment, rebuildability and export/import semantics require explicit qualification.

## 16. Knowledge Graph Audit

**Result: PARTIAL / important invariant.**

Knowledge Graph is modeled as a knowledge/derived-data component.

Invariant: Knowledge ≠ Authority.

The graph must never authorize, grant capability, mutate physical state, bypass policy or bypass State Authority. Provenance, temporal semantics, confidence, poisoning resistance, entity merge/split and rebuildability remain qualification requirements.

## 17. Digital Twin / Engineering Audit

**Result: PARTIAL.**

Engineering and Digital Twin are separated from physical execution.

Required path:

Twin/Engineering → model/proposal → policy/authorization → domain authority → execution → verification.

No direct AI/Twin/Engineering → physical device path is accepted.

Installed/configured/desired/observed/actual/planned/failed/historical state semantics require final cross-domain reconciliation.

## 18. AI Audit

**Result: PARTIAL / invariant preserved.**

AI is non-authoritative. The repository contains local AI/provider/cloud-development boundaries, deny-by-default execution admission and negative tests.

Remaining gaps include complete provenance from request through artifact/result/evidence, model qualification, model update/rollback, prompt-injection resistance, data minimization and production admission.

## 19. Developer Compute Fabric Audit

**Result: PARTIAL / P0/P1 dependency.**

Developer and user domains are architecturally separated.

Invariant:

Compute Resource Sharing ≠ User Data Sharing.

No evidence inspected authorizes Developer Cloud access to user media, documents, recordings, credentials, secrets or operational authority.

However, production qualification of zero-user-data access, dynamic primary development node, high-speed transport, resource leases, scheduler isolation and recovery is incomplete.

## 20. Resource Management — Section 24

**Result: UNDER-SPECIFIED.**

The implementation map contains `resource_governance` for quotas, priority and workload admission, and the dependency graph links cluster/assistant workloads to resource governance.

The full Section 24 architecture is not closed by the inspected evidence for CPU/GPU/NPU/RAM/remote-memory/storage/network/thermal/power/energy, reservation/lease/admission/isolation/rescheduling and failure recovery.

No MH-24 is introduced.

## 21. Persistence Audit

**Result: PARTIAL.**

Persistence is explicitly not authority. Recovery is a separate boundary.

Durable State Authority, replicas, journal, immutable/offline recovery points, key separation, RPO/RTO, ransomware recovery, node replacement and cluster reconstruction remain qualification gates.

Backup copies must not become alternative authority.

## 22. Observability Audit

**Result: PARTIAL.**

Observability/diagnostics are explicitly separated from mutation authority.

Required flow remains:

Observe → Detect → Diagnose → Propose → Authorize → Remediate → Verify → Audit.

Automated remediation must re-enter policy/authorization. Evidence preservation and incident timeline completeness remain open.

## 23. API / Event / Contract Audit

**Result: PARTIAL.**

Contract-driven boundaries, events and State Authority command authorization are present.

Open areas: exhaustive public API inventory, version compatibility, idempotency, replay protection, correlation, timeout/retry/compensation semantics and complete external-event source qualification.

## 24. Update Audit

**Result: PARTIAL.**

Update architecture contains signing/provenance, compatibility, downgrade protection, rollback and recovery principles.

Node bootstrap/admission, identity enrollment, revocation and requalification are not closed for every node class.

## 25. Backup / Recovery Audit

**Result: PARTIAL / production-blocking.**

Recovery is a separate privileged security boundary and tamper-evidence tests exist.

Durable backup/restore, cross-node disaster recovery, immutable/offline recovery points and destructive-failure qualification are not proven.

## 26. OSS / Supply Chain Audit

**Result: PARTIAL / P1.**

The architecture recognizes provenance, licensing and dependency security.

P9.2 remains open: repository review recorded two secret-keyword locations with values omitted and no complete transitive dependency/license provenance from repository manifests alone.

Open source is not treated as automatically trusted.

## 27. Qualification / Release Audit

**Result: BLOCKED.**

Architecture qualification is explicitly distinct from production authorization.

The evidence chain is not yet sufficient for production admission because State Authority durability/HA, mobile auth, egress, CPRG, Developer Fabric isolation, recovery, supply-chain provenance and several cross-domain contracts remain open.

## 28. Failure Model Audit

**Result: PARTIAL.**

The architecture recognizes node, authority, network, storage, AI, HA, device, protocol, plugin, API, cloud, CPRG, Developer Fabric, power/thermal, update, credential, malicious device/document/plugin/model failures.

A single exhaustive matrix with detection, containment, degraded mode, authority behavior, failover, recovery, verification and audit for every listed failure class is not yet closed.

## 29. Cross-Domain Workflow Audit

**Result: PARTIAL.**

The intended governed paths are consistent:

- Smart Home: User/AI → MediaHub policy → HA Core → device.
- Media: User → API/policy → Media → device/storage → verification.
- Engineering/Twin: proposal → policy → domain authority → execution.
- Knowledge: source → validation → knowledge → context → AI.
- AI: input → classification → context → model → proposal → policy → authority.
- Developer: corporate input → Developer Domain/Fabric → qualified artifact → release.

The remaining risk is hidden bypass paths not covered by exhaustive runtime evidence.

## 30. Scalability Audit

**Result: PARTIAL.**

Single-node, multi-node and heterogeneous-cluster concepts exist.

Bottlenecks/SPOFs requiring explicit closure include State Authority leadership/failover, CPRG, egress control, storage indexing, Knowledge Graph rebuild, AI resource admission and high-speed transport.

## 31. Implementability Audit

**Result: PARTIAL.**

The architecture explicitly allows platform-specific implementation on Mac mini, mini-PC/Linux, Raspberry Pi and iOS/iPadOS/mobile endpoints.

A single implementation is not required across platforms.

Concrete Apple platform restrictions, hardware security capabilities, thermal/power envelopes and per-variant qualification remain outside complete evidence.

## 32. Migration Readiness

**Result: PARTIAL / MH-23 prerequisite set required.**

Before MH-23, the following must have explicit preservation rules: identity, State Authority state, policy, contracts, media, documents, Knowledge Graph provenance, Digital Twin state, models, node/cluster identity, storage topology, hardware capability changes, recovery points and rollback.

Full migration architecture remains delegated to MH-23.

## 33. Cloud Boundary

**Result: PARTIAL / strong invariant.**

User Cloud and Developer Cloud are distinct trust domains.

Developer Cloud must never receive user files, documents, media, camera recordings, Knowledge Graph, operational history, credentials or secrets.

Remote access, backup, notifications and optional approved AI remain separate user-cloud functions subject to policy.

The remaining gap is production qualification of every egress path.

## 34. Contradiction Register

### C-MH20-001 — MH-20 scope collision
Affected: MH-01 interface contract, MH-20, all downstream routing.

Type: CONTRADICTION.

Severity: P0.

Evidence: `architecture/MH-01-to-MH-23-interface-contract.md` assigns MH-20 to “Automation/Energy/Self-Healing”, while the canonical MH map assigns MH-20 to Architecture Audit.

Resolution: update the interface/routing artifact to make MH-20 Architecture Audit. Preserve Automation/Energy/Self-Healing only as a domain capability, not MH-20.

User decision: No; this is a governance/consistency correction implied by the supplied canonical map.

Status: OPEN.

### C-MH20-002 — State Authority vs Smart Home authority wording
Affected: MH-01, MH-04, MH-17, MH-20.

Type: BOUNDARY CLARIFICATION.

Severity: P1.

Evidence: State Authority is described as sole canonical mutation authority while Smart Home is separately assigned to HA Core.

Resolution: explicitly define State Authority as canonical platform authority and HA Core as sole Smart Home operational/device-state authority.

User decision: No.

Status: RESOLUTION PROPOSED.

### C-MH20-003 — Historical decision status mismatch
Affected: MH-01, MH-20.

Type: GOVERNANCE / PROVENANCE.

Severity: P1.

Evidence: MH-01 decision log labels AI, Cloud and Local First entries PROPOSED while the current project baseline treats them as inherited decisions/invariants.

Resolution: do not rewrite history; create reconciliation records that distinguish historical proposal status from current inherited canonical status.

User decision: No.

Status: OPEN.

### C-MH20-004 — Branch provenance embedded in security artifact is stale
Affected: MH-12, MH-20, evidence chain.

Type: PROVENANCE.

Severity: P1.

Evidence: branch HEAD is 91f841b…, while MH-12 artifact names ea7177e… as current authoritative commit.

Resolution: future evidence must bind to the exact commit under audit.

User decision: No.

Status: OPEN.

### C-MH20-005 — Architecture maps not yet closure-grade
Affected: dependency graph, implementation map, MH-20.

Type: COMPLETENESS.

Severity: P1.

Evidence: dependency graph status IN_PROGRESS; implementation map status DRAFT_BOUNDARIES_ONLY.

Resolution: reconcile ownership/edges/contracts before architecture freeze.

User decision: No.

Status: OPEN.

### C-MH20-006 — Smart Home runtime qualification gap
Affected: MH-17, MH-20, P6.

Type: UNQUALIFIED IMPLEMENTATION.

Severity: P1.

Evidence: P6.4 declares HA authority but reports operational mutation adapter and end-to-end runtime proof absent.

Resolution: later bounded implementation/qualification; no architecture bypass.

Status: OPEN.

## 35. Gap Register

| ID | Domain | Category | Priority | Gap | Closure criterion |
|---|---|---|---|---|---|
| G-MH20-001 | MH mapping | Inconsistent | P0 | MH-20 domain mapping collision | canonical map and interface contract agree |
| G-MH20-002 | State Authority | Under-specified | P0 | durable/distributed authority and failover | explicit epoch/quorum/split-brain/recovery contract + evidence |
| G-MH20-003 | Smart Home | Unqualified | P1 | HA mutation path | qualified MediaHub→HA→device path |
| G-MH20-004 | Mobile | Missing | P1 | session/authz/offline revocation contract | P5.2 closure evidence |
| G-MH20-005 | Network | Unqualified | P1 | exhaustive production egress inventory | all egress paths classified and tested |
| G-MH20-006 | CPRG | Unqualified | P1 | registration/data-plane separation evidence | lifecycle and negative tests |
| G-MH20-007 | Developer Fabric | Security-sensitive | P1 | zero-user-data production proof | independent boundary evidence |
| G-MH20-008 | Recovery | Production-blocking | P1 | durable backup/restore/DR qualification | restore/RPO/RTO/destructive-failure evidence |
| G-MH20-009 | Supply chain | Production-blocking | P1 | transitive provenance/SBOM/license evidence | reproducible inventory and advisory evidence |
| G-MH20-010 | Resource Mgmt | Under-specified | P1 | Section 24 complete resource model | CPU/GPU/NPU/RAM/storage/network/thermal/power admission model |
| G-MH20-011 | Failure model | Missing | P1 | exhaustive failure matrix | detection→containment→recovery→audit for all critical failures |
| G-MH20-012 | API/events | Unqualified | P2 | exhaustive replay/idempotency/API inventory | contract-level evidence |
| G-MH20-013 | Migration | Migration-sensitive | P1 | preservation prerequisites | MH-23 input contract complete |
| G-MH20-014 | Knowledge | Security-sensitive | P1 | graph poisoning/provenance/rebuild closure | deterministic provenance and rebuild evidence |

## 36. Risk Register

| Risk | Asset/Boundary | Likelihood | Impact | Current control | Residual concern | Status |
|---|---|---|---|---|---|---|
| R-MH20-001 authority ambiguity | State Authority/HA | Medium | Critical | layered authority principles | wording can create conflicting mutation assumptions | Open |
| R-MH20-002 hidden egress | Network/Cloud | Medium | Critical | deny-by-default egress | incomplete production inventory | Open |
| R-MH20-003 Developer data crossing | Developer/User | Low-Medium | Critical | domain separation | production proof incomplete | Open |
| R-MH20-004 recovery authority bypass | Recovery/State | Low-Medium | Critical | separate recovery boundary | durable recovery qualification incomplete | Open |
| R-MH20-005 graph poisoning | Knowledge/AI | Medium | High | provenance and validation principles | rebuild/poisoning tests incomplete | Open |
| R-MH20-006 HA bypass | Smart Home | Low-Medium | Critical | HA authority invariant | runtime adapter proof absent | Open |
| R-MH20-007 supply-chain compromise | OSS/build | Medium | High | provenance/SBOM policy | transitive provenance incomplete | Open |
| R-MH20-008 migration state loss | Migration/State | Medium | Critical | migration domain exists | exact preservation/rollback contract incomplete | Open |

## 37. Invariant Register

1. State Authority = canonical platform authority.
2. HA Core = sole Smart Home operational/device-state authority.
3. AI ≠ Authority.
4. Knowledge ≠ Authority.
5. Cloud ≠ Authority.
6. Developer Domain ≠ User Domain.
7. Developer Cloud has zero user-data access.
8. User Compute Contribution is not part of the accepted architecture.
9. Unknown device = DENY/QUARANTINE.
10. Critical ambiguity = FAIL CLOSED.
11. Smart Home mutations pass through HA Core.
12. Security/Identity/Policy cannot be bypassed by adapters.
13. Local First is preserved.
14. Critical functions do not acquire hidden mandatory cloud dependencies.
15. Registration capability ≠ data-plane access.
16. Compute sharing ≠ user-data sharing.
17. Desired ≠ Observed.
18. Cached ≠ Canonical.
19. Discovery ≠ Trust.
20. Protocol ≠ Authority.
21. Hardware capability ≠ device identity.
22. Production admission requires qualification.
23. Recovery sources must be trusted and verified.
24. Resource Management is Section 24, not MH-24.

## 38. Decision Register

- D-MH20-001: **A — Already Consistent:** AI remains non-authoritative.
- D-MH20-002: **A — Already Consistent:** Cloud remains non-authoritative.
- D-MH20-003: **A — Already Consistent:** Knowledge remains non-authoritative.
- D-MH20-004: **C — Engineering Resolution:** distinguish platform authority from Smart Home operational authority.
- D-MH20-005: **C — Engineering Resolution:** bind audit evidence to exact GitHub commit/tree.
- D-MH20-006: **D — Architectural Correction:** correct MH-20 mapping collision in the interface contract.
- D-MH20-007: **C — Engineering Resolution:** complete dependency/implementation traceability before freeze.
- D-MH20-008: **D — Architectural Correction candidate:** complete Section 24 resource-management contract if no existing authoritative artifact covers it.
- D-MH20-009: **E — User Decision Required:** none at this audit checkpoint; unresolved product-level decisions are already represented in historical architecture and must not be silently invented here.

## 39. Required Corrections

1. Correct MH-20 routing/domain mapping.
2. Add an explicit layered authority statement: State Authority governs platform-level canonical semantics; HA Core governs Smart Home operational/device state.
3. Reconcile stale evidence commit references.
4. Complete dependency graph and implementation-map reconciliation.
5. Produce explicit Section 24 Resource Management closure artifact if existing Section 24 evidence is not authoritative.
6. Close mobile authentication, egress, CPRG, Developer Fabric, durable recovery and supply-chain qualification prerequisites before production admission.
7. Build one failure matrix covering all critical failure classes.
8. Preserve all historical decisions; corrections must be additive reconciliation records.

## 40. Dependencies for MH-21

MH-21 must receive:

- exact User Cloud vs Developer Cloud boundary;
- Developer Cloud zero-user-data invariant;
- controlled egress and residency policy;
- cloud trust domain;
- optional cloud AI semantics;
- remote access/backup/notification boundaries;
- API Gateway and Security/Egress Gateway separation;
- CPRG registration-only boundary;
- registration capability ≠ data-plane access;
- no cloud State Authority authority;
- fail-closed cloud failure semantics.

## 41. Dependencies for MH-22

MH-22 must receive:

- qualification hierarchy;
- hardware/software/security/cluster/device/protocol/AI qualification;
- production admission rules;
- artifact and provenance requirements;
- SBOM/license/dependency evidence;
- recovery qualification;
- fault injection;
- interoperability/performance evidence;
- explicit separation between qualification and production authorization.

## 42. Dependencies for MH-23

MH-23 must receive:

- State Authority migration semantics;
- identity/node/cluster migration;
- storage/media/document/knowledge migration;
- Digital Twin and AI/model migration;
- policy/API compatibility;
- hardware replacement;
- topology changes;
- rollback and recovery-point requirements.

## 43. Audit Closure Criteria

MH-20 is **NOT CLOSED**.

Closure requires, at minimum:

- MH-20 mapping contradiction resolved;
- State Authority/HA layered authority contract explicit;
- no unresolved P0 contradictions;
- dependency/implementation traceability reconciled;
- Developer/User boundary evidence preserved;
- State Authority recovery model reconciled;
- CPRG and egress boundaries qualified;
- Section 24 resource-management requirements explicitly owned;
- failure/recovery prerequisites recorded;
- MH-21/22/23 input requirements accepted as downstream constraints;
- final consistency pass against the exact GitHub HEAD/tree;
- no unsupported claims of production qualification.

## 44. Audit Decision Model Summary

A — Already Consistent: major invariants remain coherent.

B — Clarification Required: authority wording and provenance terminology require clarification.

C — Engineering Resolution: traceability/evidence binding and layered boundary wording can be resolved without changing product intent.

D — Architectural Correction: MH-20 mapping must be corrected.

E — User Decision Required: none newly required by this audit. Existing historical product decisions must not be reopened merely because MH-20 found implementation gaps.

## 45. Final Reconciliation

The audit confirms that the core architectural direction remains coherent: Local First, State-Authority-Centric, Domain-Authority-Aware, Identity-Centric, Policy-Controlled, Capability-Driven, Zero-Trust-Oriented, Privacy-Preserving, Developer/User Isolated, AI/Knowledge/Cloud Non-Authoritative, Recoverable, Observable and qualification-backed.

The architecture is not yet closure-grade because several boundaries are specified but not fully qualified, and one explicit repository mapping contradiction assigns the wrong meaning to MH-20.

No historical MH-01…MH-19 decision is silently replaced.

No MH-24 is created.

No production authorization is implied.

## 46. Evidence / Provenance

GitHub-confirmed evidence used for this audit includes:

- current branch ref: `91f841b1b00f412e218892732c645cae0f1935d8`;
- current tree: `11fd15ba8a28b03dcfd885ac715aa3cdfed520d9`;
- R4 commit: `471f709f5633feab7aeb62dd3ea52effad6d2bc4`;
- R4 tree: `2279612908135418b2b5448d598274ea6741deaa`;
- `architecture/MH-01-to-MH-23-interface-contract.md`;
- `architecture/MH-01-decision-log.md`;
- `architecture/MH-01-contradiction-register.md`;
- `architecture/MH-01-traceability-matrix.md`;
- `specification/dependency-graph.yaml`;
- `development/implementation-map.yaml`;
- MH-03 contradiction register;
- MH-12 security analysis;
- P9.1–P9.7 security reconciliation records;
- P6.1–P6.5 voice/Smart Home reconciliation records;
- R4 ancestry compare.

This artifact is evidence of audit findings, not architecture acceptance.
