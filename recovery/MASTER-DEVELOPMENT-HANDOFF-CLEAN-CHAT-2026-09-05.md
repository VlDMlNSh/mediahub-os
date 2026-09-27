# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS
# MASTER DEVELOPMENT HANDOFF — CLEAN DEVELOPMENT CHAT

Date: 2026-09-05
Repository: VlDMlNSh/mediahub-os
Baseline branch: recovery/full-functional-spec
Status: DEVELOPMENT BASELINE / PRODUCTION BLOCKED

## 0. PURPOSE
This document starts a clean development chat from the recovered MediaHub master baseline. Historical MH-01…MH-23 are projections/scopes of ONE system, not 23 independent architectures. GitHub is the persistent source of truth.

## 1. NON-NEGOTIABLE BASELINE
- 58 canonical capabilities; 58/58 owned.
- 51 canonical domains.
- 36 contract families.
- 30 protected invariants.
- DEC-001…DEC-012 accepted.
- DEC-A-001…DEC-A-004 remain draft/proposed unless explicitly accepted.
- No capability is identified as LOST, REMOVED or DROPPED.
- UNKNOWN/EVIDENCE_GAP/DEFERRED/NOT_IMPLEMENTED are not capability loss.
- Master Architecture remains DRAFT / NOT ACCEPTED until explicit human acceptance.
- Production implementation is BLOCKED until Master Architecture acceptance and scoped implementation authorization.

## 2. READ FIRST
Read before implementation planning:
1. recovery/forensic-control-point-2026-09-05.md
2. recovery/MASTER-PROMPT-NEW-CHAT-MH01-23-REDISTRIBUTION-FINAL-2026-09-05.md
3. recovery/mh01-23-redistribution-projection-matrix-2026-09-05.yaml
4. specification/capability-registry.yaml
5. specification/contract-registry.yaml
6. specification/invariant-registry.yaml
7. specification/decision-registry.yaml
8. specification/dependency-graph.yaml
9. architecture/master-mediahub-architecture-reconstruction-2026-09-05.md
10. development/implementation-map.yaml
Also inspect relevant recovery/reconciliation artifacts named by the forensic control point.

## 3. FIRST ACTION — NO CODE
Perform one initial baseline pass:
A. Verify repository, branch, exact HEAD and working-tree state where observable.
B. Read canonical registries.
C. Reconcile capability ownership, contracts, invariants, dependencies and implementation boundaries.
D. Identify accepted versus proposed decisions.
E. Identify evidence gaps, contradictions and blockers.
F. Inspect implementation only as evidence; code is not automatically architecture authority.
G. Produce DEVELOPMENT BASELINE REPORT.
Do not create production implementation merely because a capability exists in a registry.

## 4. REQUIRED BASELINE REPORT
Return:
MEDIAHUB DEVELOPMENT BASELINE
Repository:
Branch:
HEAD:
Working tree:
Canonical capabilities: 58/58
Canonical domains: 51
Capability ownership: 58/58
Contracts: 36
Invariants: 30
Accepted decisions: DEC-001…DEC-012
Draft decisions: DEC-A-001…DEC-A-004
Historical scopes: MH-01…MH-23 accounted
Capability loss: NONE IDENTIFIED
Historical evidence: PARTIALLY GAPPED
Master Architecture: DRAFT / NOT ACCEPTED
Production: BLOCKED

Then list open contracts, unresolved dependencies, evidence gaps, governance blockers, implementation candidates and the exact decisions/authorizations required.

## 5. ONE AUTHORITY RULE
Canonical path:
Input → Boundary → Authorization → State Authority → Canonical State → Observation → Evidence
State Authority is the sole canonical mutation authority.
Forbidden: second State Authority; AI/Graph/Digital Twin physical mutation; Projection/Cache canonical mutation; Telemetry/Health/Readiness canonical mutation; shadow persistence authority; plugin/automation/cloud bypass around authorization or State Authority.

## 6. SECURITY
Discovery ≠ Trust
Presence ≠ Authentication
Authentication ≠ Authorization
Physical Connection ≠ Authorization
Health ≠ Trust
Readiness ≠ Trust
Liveness ≠ Trust
Remote Access ≠ Increased Authorization
No implementation may use these observations as authorization substitutes.

## 7. STORAGE
Preserve three logical canonical domains:
1. System Storage
2. Surveillance Recording Storage
3. Personal Media Library Storage
Never collapse them for implementation convenience.

## 8. LOCAL/CLOUD
Local MediaHub is primary runtime. Local Assistant is primary assistant path. Cloud Development is privileged infrastructure, not ordinary-user workspace. Local MediaHub Cluster ≠ Cloud Development Cluster.

## 9. CONTRACT-FIRST
For every implementation unit:
Capability → Owner → Contract → Invariants → Dependencies → Verification → Acceptance
If a prerequisite is unresolved, STOP and classify the blocker. Never invent substitute authority or silently change the contract.

## 10. GATES
Architecture acceptance and implementation authorization are separate gates. Current MH-06 precedent: Health/Readiness semantic contract is governance accepted, but implementation authorization requires a separate explicit governance decision. Apply the same separation everywhere.

Current Master Architecture: DRAFT / NOT ACCEPTED. No production implementation may be declared accepted, frozen, qualified or deployment-authorized until the applicable gates are satisfied.

## 11. IMPLEMENTATION ORDER
Use canonical dependency order, not historical MH numbering:
A. Canonical foundation — State Authority, Runtime, Lifecycle, Configuration, Persistence, Storage, Security, Identity, IPC, Events, Observability, Recovery.
B. Device/Integration — lifecycle, discovery, presence, compatibility, protocols, firmware, health, diagnostics, backpressure, offline behavior.
C. Media/Surveillance — lifecycle, recording, personal media, ingestion, indexing, retention, export, migration.
D. Intelligence — Knowledge Graph, Digital Twin, Search, RAG, AI, Local Assistant, semantic projections, provenance.
E. Automation — Automation, Scheduling, Policy, Triggers, Verification, Safety.
F. Product/Appliance — Installer, Recovery, Update, Backup, Restore, Migration, Variants, Qualification, Acceptance.

## 12. VERIFICATION
Required chain:
Architecture Scope → Authorization Check → Implementation → Test → Observation → Evidence → Architectural Impact Check → Reverse Master Prompt
Every implementation must cover applicable functional, authority, security, privacy, persistence, recovery/failure, offline, resource, observability, migration/rollback/compatibility and acceptance evidence.
If architecture impact appears: STOP → classify → request architecture decision.

## 13. ANTI-LOSS
Before every merge inspect capability-registry.yaml, contract-registry.yaml, invariant-registry.yaml, decision-registry.yaml, dependency-graph.yaml and implementation-map.yaml.
Explicitly answer: “What canonical capability, contract, invariant or authority boundary changes because of this commit?” If none, state NONE. Semantic changes require registry/decision impact and acceptance authority.

## 14. UNKNOWN / PROVENANCE
Never invent, delete evidence, mark LOST without evidence, silently replace, promote UNKNOWN to VERIFIED or PROPOSED to ACCEPTED. Use UNKNOWN / EVIDENCE_GAP / EVIDENCE_BLOCKED / DEFERRED / REQUIRES_VERIFICATION. Preserve source, path, commit SHA, classification, confidence/evidence status and canonical mapping.

## 15. GIT
Preserve forensic history and documents. Do not rewrite history for cleanliness. Do not delete obsolete evidence; classify it HISTORICAL / SUPERSEDED / RECONCILED / DEPRECATED / EVIDENCE-GAP. Recovery material must not be silently mixed into production implementation.

## 16. DEVELOPMENT ARTIFACTS
For authorized implementation create/update as applicable: implementation branch, tests, evidence packet, verification record, Reverse Master Prompt and governance acceptance request.
Evidence packet: STATUS, TASK, AUTHORIZATION, ARCHITECTURAL DEPENDENCIES, CURRENT SHA, BRANCH, PR, CHANGED FILES, IMPLEMENTATION, TESTS, COMMANDS, RESULTS, ENVIRONMENT, OBSERVED BEHAVIOR, EVIDENCE, ARCHITECTURAL CONFORMANCE, AUTHORITY/SECURITY/PRIVACY/PERSISTENCE/MIGRATION/RECOVERY IMPACTS, UNKNOWNs, CONTRADICTIONS, BLOCKERS, REQUESTED DECISION.

## 17. MH-06 SPECIAL CONTROL
Health = observation-only: UNKNOWN, HEALTHY, DEGRADED, FAILED, QUARANTINED.
Readiness = operation-scoped derived verdict: UNKNOWN, NOT_READY, READY, DEGRADED, QUARANTINED.
UNKNOWN ≠ READY. P0-06 LifecycleState.READY ≠ MH-06 Readiness.READY.
Precedence: QUARANTINED → invalid/incompatible generation/integrity → unavailable State Authority → lifecycle incompatible → failed/unknown critical dependency → resource constraint → permitted optional degradation → all required observations healthy.
Readiness never replaces Authorization or State Authority.
Current MH-06 implementation authorization remains NOT GRANTED unless explicit governance evidence appears.

## 18. CLEAN-CHAT MODE
After baseline:
- Master Architecture not accepted → architecture-readiness / planning only.
- Architecture accepted but scoped authorization absent → implementation STOPPED.
- Explicit scoped authorization present → verify exact scope/baseline, then implement only that scope.
- Architecture impact discovered → STOP and return to governance.

## 19. FIRST IMPLEMENTATION TARGET
Do not choose by MH number. Choose by canonical dependency graph. A capability is eligible only when owner, contract, invariants, dependencies, security, persistence semantics (if applicable), verification criteria and implementation authorization are ready. Otherwise produce a blocker/decision request, not code.

## 20. FINAL COMMAND
Start from this exact control point. Read the authoritative artifacts. Verify Git state. Produce DEVELOPMENT BASELINE REPORT. Reconcile implementation candidates against the canonical dependency graph. Do not reconstruct architecture from memory, treat evidence gaps as lost functionality, create a second architecture, or write production code before applicable gates.

Proceed through:
RECOVERED ARCHITECTURE
→ CANONICAL BASELINE
→ ARCHITECTURE ACCEPTANCE
→ SCOPED IMPLEMENTATION AUTHORIZATION
→ CONTRACT-FIRST IMPLEMENTATION
→ TESTED
→ VERIFIED
→ IMPLEMENTATION GOVERNANCE ACCEPTANCE
→ PRODUCTION QUALIFICATION

Production remains BLOCKED until all required gates are explicitly satisfied.
