# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS
# MASTER DEVELOPMENT HANDOFF — CLEAN DEVELOPMENT CHAT

Date: 2026-09-05
Repository: VlDMlNSh/mediahub-os
Baseline branch: recovery/full-functional-spec
Status: DEVELOPMENT BASELINE / PRODUCTION BLOCKED

## 0. PURPOSE

This document starts a clean development chat from the recovered MediaHub master baseline. Historical MH-01…MH-23 are projections/scopes of ONE system, not 23 independent architectures.

GitHub is the persistent source of truth. Do not reconstruct architecture from memory and do not silently replace canonical contracts with legacy code behavior.

## 1. NON-NEGOTIABLE BASELINE

- 58 canonical capabilities; 58/58 owned.
- 51 canonical domains.
- 36 contract families.
- 30 protected invariants.
- DEC-001…DEC-012 accepted.
- DEC-A-001…DEC-A-004 remain draft/proposed unless explicitly accepted later.
- No capability is identified as LOST, REMOVED or DROPPED.
- UNKNOWN/EVIDENCE_GAP/DEFERRED/NOT_IMPLEMENTED are not capability loss.
- Master Architecture remains DRAFT / NOT ACCEPTED until explicit human acceptance.
- Production implementation is BLOCKED until Master Architecture acceptance and scoped implementation authorization.

## 2. AUTHORITATIVE FILES — READ FIRST

Read these before implementation planning:

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

## 3. FIRST CHAT ACTION — NO CODE

Perform, in one initial pass:

A. Verify repository and branch.
B. Verify exact HEAD and clean/dirty state where observable.
C. Read all canonical registries above.
D. Reconcile capability ownership against contracts and implementation map.
E. Reconcile dependency graph against implementation boundaries.
F. Identify accepted versus proposed architecture decisions.
G. Identify evidence gaps and blockers.
H. Inspect existing implementation only as evidence; code is not automatically architectural authority.
I. Produce DEVELOPMENT BASELINE REPORT.

Do not create production implementation merely because a capability exists in the registry.

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

Then list:
- open contracts;
- unresolved dependencies;
- evidence gaps;
- governance blockers;
- implementation candidates;
- first candidate and why it is dependency-safe;
- exact decisions/authorizations still required.

## 5. ONE AUTHORITY RULE

Canonical mutation path:

Input → Boundary → Authorization → State Authority → Canonical State → Observation → Evidence

State Authority is the sole canonical mutation authority.

Forbidden:
- second State Authority;
- AI → physical mutation;
- Graph/Digital Twin → physical mutation;
- Projection/Cache → canonical mutation;
- Telemetry/Health/Readiness → canonical mutation;
- persistence/database/cache becoming shadow canonical state;
- plugin/automation/cloud bypass around authorization or State Authority.

## 6. SECURITY INVARIANTS

Discovery ≠ Trust
Presence ≠ Authentication
Authentication ≠ Authorization
Physical Connection ≠ Authorization
Health ≠ Trust
Readiness ≠ Trust
Liveness ≠ Trust
Remote Access ≠ Increased Authorization

No implementation may use these observations as substitutes for authorization.

## 7. STORAGE INVARIANTS

Maintain three logical canonical storage domains:
1. System Storage
2. Surveillance Recording Storage
3. Personal Media Library Storage

Do not collapse them for implementation convenience.

## 8. LOCAL-FIRST / CLOUD BOUNDARY

Local MediaHub is the primary runtime.
Local Assistant is the primary assistant path.
Cloud Development is privileged infrastructure, not an ordinary-user workspace.

Never equate Local MediaHub Cluster with Cloud Development Cluster.

## 9. CONTRACT-FIRST IMPLEMENTATION

For every implementation unit establish:

Capability → Owner → Contract → Invariants → Dependencies → Verification → Acceptance

If any prerequisite is unresolved, STOP and classify the blocker. Do not invent a substitute authority or silently change the contract.

## 10. IMPLEMENTATION AUTHORIZATION RULE

Architecture acceptance and implementation authorization are separate gates.

Current MH-06 precedent is mandatory:
- Health/Readiness semantic contract: GOVERNANCE ACCEPTED through ADR-001.
- Implementation authorization: NOT GRANTED unless a separate explicit governance decision authorizes it.

The same separation applies to all other capabilities.

## 11. MASTER ARCHITECTURE GATE

Current master architecture:
DRAFT / NOT ACCEPTED

Therefore no production implementation may be declared accepted, frozen, qualified or deployment-authorized.

If a human governance decision explicitly accepts the Master Architecture, record:
- exact decision text;
- date;
- authority;
- GitHub issue/ADR/reference;
- exact relevant commit SHA.

Until then, implementation remains planning/evidence only.

## 12. IMPLEMENTATION ORDER

Use canonical dependency order, not historical MH numbering:

A. Canonical foundation:
State Authority, Runtime, Lifecycle, Configuration, Persistence, Storage, Security, Identity, IPC, Events, Observability, Recovery.

B. Device/Integration:
Device lifecycle, Discovery, Presence, Compatibility, Protocols, Firmware, Health, Diagnostics, Backpressure, Offline behavior.

C. Media/Surveillance:
Media lifecycle, Surveillance recording, Personal Media, Ingestion, Indexing, Retention, Export, Migration.

D. Intelligence:
Knowledge Graph, Digital Twin, Search, RAG, AI, Local Assistant, Semantic projections, Provenance.

E. Automation:
Automation, Scheduling, Policy, Triggers, Verification, Safety boundaries.

F. Product/Appliance:
Installer, Recovery, Update, Backup, Restore, Migration, Variants, Qualification, Acceptance.

Select the first actual implementation target only after checking owner, contract, dependency readiness, security readiness, persistence readiness and verification readiness.

## 13. TEST / EVIDENCE GATE

Every implementation must provide evidence for:
- functional correctness;
- authority boundary;
- security;
- privacy;
- persistence;
- recovery/failure behavior;
- offline behavior where applicable;
- resource governance;
- observability;
- migration/rollback/compatibility where applicable;
- acceptance traceability.

Required chain:
Architecture Scope → Authorization Check → Implementation → Test → Observation → Evidence → Architectural Impact Check → Reverse Master Prompt

If architectural impact appears:
STOP → classify → request architecture decision → do not silently implement.

## 14. ANTI-LOSS GATE

Before every merge inspect:
- capability-registry.yaml
- contract-registry.yaml
- invariant-registry.yaml
- decision-registry.yaml
- dependency-graph.yaml
- implementation-map.yaml

Explicitly answer:
“What canonical capability, contract, invariant or authority boundary changes because of this commit?”

If none, state NONE. If semantic contract changes, provide registry/decision impact and acceptance authority.

## 15. UNKNOWN / EVIDENCE GAP

Never:
- invent;
- delete evidence;
- mark LOST without evidence;
- silently replace;
- promote UNKNOWN to VERIFIED;
- promote PROPOSED to ACCEPTED.

Use explicit classifications:
UNKNOWN / EVIDENCE_GAP / EVIDENCE_BLOCKED / DEFERRED / REQUIRES_VERIFICATION.

## 16. GIT DISCIPLINE

Preserve forensic history and documents.
Do not rewrite history to make the repository appear cleaner.
Do not delete obsolete evidence; classify it HISTORICAL / SUPERSEDED / RECONCILED / DEPRECATED / EVIDENCE-GAP.

Recovery branches are evidence/reconciliation surfaces. Production implementation must use an explicitly authorized development branch.

## 17. REQUIRED DEVELOPMENT ARTIFACTS

For every authorized implementation create/update, as applicable:
- implementation branch;
- implementation evidence packet;
- tests;
- verification record;
- Reverse Master Prompt;
- governance acceptance request.

Evidence packet must include:
STATUS, TASK, AUTHORIZATION, ARCHITECTURAL DEPENDENCIES, CURRENT GIT SHA, BRANCH, PR, CHANGED FILES, IMPLEMENTATION, TESTS, COMMANDS, RESULTS, ENVIRONMENT, OBSERVED BEHAVIOR, EVIDENCE, ARCHITECTURAL CONFORMANCE, AUTHORITY IMPACT, SECURITY IMPACT, PRIVACY IMPACT, PERSISTENCE IMPACT, MIGRATION/RECOVERY IMPACT, UNKNOWNs, CONTRADICTIONS, BLOCKERS, REQUESTED DECISION.

## 18. PROHIBITIONS

Do not:
- implement 23 independent MH architectures;
- create duplicate owners;
- create a second State Authority;
- bypass P0-05/authorization boundaries where they apply;
- make AI authoritative;
- make Graph/Digital Twin authoritative;
- use health/readiness as trust or authorization;
- collapse storage domains;
- equate cloud development with user runtime;
- silently modify frozen baselines;
- declare CI verified without an actual run;
- declare local test success as production qualification;
- begin production implementation while acceptance is BLOCKED.

## 19. MH-06 SPECIAL CONTROL POINT

Accepted semantic contract:
Health = observation-only:
UNKNOWN, HEALTHY, DEGRADED, FAILED, QUARANTINED.

Readiness = operation-scoped derived verdict:
UNKNOWN, NOT_READY, READY, DEGRADED, QUARANTINED.

UNKNOWN ≠ READY.
P0-06 LifecycleState.READY ≠ MH-06 Readiness.READY.

Precedence:
1. QUARANTINED
2. invalid/incompatible generation or integrity
3. unavailable State Authority
4. lifecycle incompatible with operation
5. failed/unknown critical dependency
6. operation-specific resource constraint
7. optional dependency degradation
8. all required observations healthy

Readiness never replaces Authorization or State Authority.

Current implementation authorization for this contract is NOT GRANTED unless explicit governance evidence appears.

## 20. CLEAN-CHAT OPERATING MODE

The new chat must begin with the baseline report, not code.

After baseline:
- if Master Architecture is still not accepted: remain in architecture-readiness / implementation-planning mode;
- if Master Architecture becomes accepted but scoped authorization is absent: remain STOPPED for implementation;
- if explicit scoped authorization appears: verify its exact scope and baseline, then implement only that scope;
- if implementation reveals architecture impact: STOP and return to architecture governance.

## 21. FIRST IMPLEMENTATION TARGET RULE

Do not choose by MH number.
Choose by canonical dependency graph.

A target is eligible only when:
- capability owner is canonical;
- contract is accepted/ready;
- invariants are explicit;
- dependencies are ready or explicitly bounded;
- security boundary is ready;
- persistence semantics are ready if applicable;
- verification criteria exist;
- implementation authorization exists.

Otherwise the output is a blocker/decision request, not code.

## 22. FINAL COMMAND TO NEW DEVELOPMENT CHAT

Start from this exact control point.

Read the authoritative recovery and specification artifacts.
Verify Git state.
Produce DEVELOPMENT BASELINE REPORT.
Reconcile implementation candidates against the canonical dependency graph.
Do not reconstruct architecture from memory.
Do not treat evidence gaps as lost functionality.
Do not create a second architecture.
Do not write production code before the applicable architecture and implementation gates are satisfied.

Then proceed through:

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
