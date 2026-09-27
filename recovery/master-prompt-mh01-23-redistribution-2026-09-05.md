# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS
# MASTER PROMPT — MH-01…MH-23 ARCHITECTURE REDISTRIBUTION & RECONCILIATION

Date: 2026-09-05
Source control point: recovery/forensic-control-point-2026-09-05.md
Source branch: recovery/full-functional-spec
Status: TRANSITION MASTER PROMPT — NOT AN ACCEPTANCE EVENT

## 0. PURPOSE

This chat is the direct successor to the forensic recovery/reconstruction chat. Its purpose is to project the protected canonical MediaHub baseline into the already-created MH-01…MH-23 architecture chats and reconcile their historical material with the reconstructed Master Architecture.

This is NOT a new architecture-design chat, NOT a production-development chat, and NOT an authority transfer to MH-01…MH-23.

## 1. STARTING CONTROL POINT

The mandatory source of truth is the latest committed forensic control point plus the canonical registries in this branch.

Current baseline:
- 58 canonical capabilities CAP-001…CAP-058.
- 51 canonical domains.
- 58/58 explicit capability owners.
- 36 contract families CTR-001…CTR-036.
- 30 protected invariants INV-001…INV-030.
- accepted product decisions DEC-001…DEC-012.
- architecture proposal decisions DEC-A-001…DEC-A-004 remain DRAFT until explicitly reconciled/accepted.
- terminal capability verification: VERIFIED=0, ACCEPTED=0; evidence is partial.
- Master Architecture: DRAFT / NOT ACCEPTED.
- technical decision closure: OPEN / EVIDENCE-BLOCKED where exact implementation evidence is unavailable.
- production implementation: BLOCKED.

Canonical files:
- specification/capability-registry.yaml
- specification/contract-registry.yaml
- specification/invariant-registry.yaml
- specification/decision-registry.yaml
- specification/dependency-graph.yaml
- architecture/master-mediahub-architecture-reconstruction-2026-09-05.md
- development/implementation-map.yaml
- recovery/forensic-control-point-2026-09-05.md

## 2. AUTHORITY HIERARCHY

MASTER CONTROL POINT
  > CANONICAL REGISTRIES / ACCEPTED DECISIONS / INVARIANTS / CONTRACTS
  > MASTER ARCHITECTURE PROJECTION
  > MH-01…MH-23 SCOPED ARCHITECTURE RECONCILIATIONS
  > DEVELOPMENT IMPLEMENTATION

A local MH chat may identify evidence, contradictions, gaps and proposals, but cannot unilaterally alter canonical truth.

## 3. NON-NEGOTIABLE PRESERVATION

1. No capability may be removed because historical evidence is incomplete.
2. UNKNOWN / EVIDENCE_GAP is never FUNCTION_LOSS.
3. DEFERRED is never rejection.
4. Historical material must remain preserved with provenance.
5. The functional baseline survives P0–P8; P0–P8 are historical decomposition only.
6. MediaHub directly records supported surveillance streams; a separate NVR is not a prerequisite where MediaHub can provide recording.
7. Dahua, Hikvision and Ajax evidence must not be lost.
8. KINCONY/KCS USB→firmware→network onboarding must not be lost.
9. Personal Media Library and Surveillance Recording Storage remain separate logical domains.
10. Home Assistant remains internal integration/automation infrastructure; MediaHub remains the user-facing Smart Home model.
11. Health, Readiness, Liveness, Trust, Authentication and Authorization remain distinct semantics.
12. Local MediaHub Cluster and Cloud Development Cluster remain separate trust/control domains.
13. Ordinary users never receive direct Cloud Development access.
14. Product-variant differences remain explicit.
15. Physical connection, discovery, presence or health never grants authorization.
16. Internal implementation details must not leak into the ordinary user model.

## 4. REQUIRED MH CHAT OPERATION

For each MH-01…MH-23:

A. Load the canonical baseline first.
B. Identify the historical scope of that MH chat.
C. Extract all historical capabilities, requirements, contracts, invariants, decisions, boundaries, tests and acceptance evidence.
D. Map each historical item to CAP / CTR / INV / DEC or mark it UNKNOWN/EVIDENCE_GAP.
E. Detect contradictions with canonical baseline.
F. Detect duplicated ownership versus legitimate cross-domain relationships.
G. Detect missing owners and dangling references.
H. Identify technical decisions that require evidence rather than assumption.
I. Preserve historical alternatives even when not selected.
J. Produce a structured Reverse Master Prompt.

## 5. REQUIRED CLASSIFICATION FOR HISTORICAL MATERIAL

Every material item must be classified as one of:
- RETAIN — still canonical and applicable.
- REMAP — same semantic requirement under a new canonical boundary.
- RECONCILE — valid but requires conflict resolution.
- REPLACE — superseded by an explicitly accepted canonical decision, while historical evidence remains preserved.
- RETIRE — only with authoritative evidence of intentional retirement.
- UNKNOWN — insufficient evidence.

Never use RETIRE or LOST merely because an item cannot currently be found.

## 6. REQUIRED TRACEABILITY

Every reconstructed material requirement should be traced as far as evidence permits:

FUNCTION → REQUIREMENT → CONTRACT → ARCHITECTURE → IMPLEMENTATION BOUNDARY → TEST → ACCEPTANCE

A missing downstream artifact is a GAP, not proof that the upstream function is absent.

## 7. TECHNICAL DECISION RULE

No implementation-specific choice may be promoted merely because it is conventional or plausible.

For every proposed closure record:

EVIDENCE → ALTERNATIVES → CONSTRAINTS → DECISION → CONTRACT UPDATE → INVARIANT IMPACT → VERIFICATION CRITERIA → ACCEPTANCE AUTHORITY

If evidence is absent, retain OPEN / EVIDENCE-BLOCKED.

## 8. MASTER ARCHITECTURE BOUNDARY MODEL

The reconstructed candidate architecture is capability-centric and contract-driven. It contains, at minimum:
- State Authority.
- Security / Identity / Trust.
- Consumer Boundary.
- Smart Home & Device Plane.
- Automation & Scheduling Plane.
- Surveillance Plane.
- Media Plane.
- Energy & Engineering Plane.
- Network Plane.
- Cluster Plane.
- Assistant & Knowledge Plane.
- Lifecycle Plane.
- Logical System / Surveillance / Personal Media storage domains.
- Separate Local MediaHub and Cloud Development trust/control domains.
- Ordinary, Advanced/Engineering, Installer, Professional Engineering and privileged developer/operator surfaces.

This boundary model is a candidate Master Architecture until explicit acceptance.

## 9. MH PROJECTION RULE

MH-01…MH-23 are NOT independent products.

Each MH chat receives:
- its scoped canonical capabilities;
- relevant contracts;
- relevant invariants;
- relevant accepted decisions;
- relevant dependency/security boundaries;
- relevant historical evidence;
- explicit open questions.

Cross-cutting concerns may appear in several MH projections, but canonical ownership remains unique.

## 10. REVERSE MASTER PROMPT — REQUIRED OUTPUT

Each MH chat must return a structured report containing:

1. MH identifier and historical scope.
2. Source evidence and provenance.
3. CAP mapping.
4. Requirement mapping.
5. Contract mapping.
6. Invariant mapping.
7. Decision mapping.
8. Architecture/boundary mapping.
9. Historical items classified RETAIN/REMAP/RECONCILE/REPLACE/RETIRE/UNKNOWN.
10. Contradictions.
11. Missing evidence.
12. Dangling/stale references.
13. Proposed technical decisions, if any.
14. Contract impacts.
15. Invariant impacts.
16. Verification requirements.
17. Acceptance evidence and authority.
18. Items that must remain OPEN.
19. Explicit anti-loss confirmation.
20. Suggested canonical registry changes, but NOT direct authority to apply them.

## 11. CENTRAL RECONCILIATION

Do not update canonical registries from one MH result in isolation.

After MH-01…MH-23 responses are collected, reconcile them centrally:
- cross-MH duplicates;
- conflicting ownership;
- contradictory requirements;
- technical decision alternatives;
- invariant impacts;
- contract changes;
- dependency graph changes;
- verification and acceptance gaps.

Only the central reconciliation may propose canonical registry changes.

## 12. ACCEPTANCE GATE

The end of redistribution does NOT mean architecture acceptance.

Before Master Architecture can become ACCEPTED, the central reconciliation must establish:
- no unresolved functional loss claim;
- all 58 capabilities retained and semantically accounted for;
- technical decisions closed only where evidence/authority exists;
- contracts reconciled;
- invariants preserved;
- dependency and authority boundaries coherent;
- verification criteria complete enough for the intended acceptance stage;
- acceptance authority explicitly identified;
- critical unknowns dispositioned.

Then, and only then, request explicit human acceptance of Master Architecture.

## 13. PRODUCTION GATE

Production implementation remains blocked until the applicable architecture, contract, verification and acceptance gates are explicitly satisfied.

No MH chat may begin production coding as part of this redistribution operation.

## 14. FIRST ACTION IN THE SUCCESSOR CHAT

1. Read this Master Prompt.
2. Fetch and verify the current forensic control point.
3. Fetch the canonical registries.
4. Confirm the 58-capability baseline.
5. Build the MH-01…MH-23 projection matrix.
6. Begin with historical evidence reconciliation, not code.
7. Preserve the control point and GitHub provenance after every material pass.

## 15. TERMINAL HANDOFF CONDITION

The successor chat may declare the redistribution phase complete only after all MH-01…MH-23 have either:
- returned a reconciled response, or
- been explicitly marked UNKNOWN / EVIDENCE_GAP with documented search scope.

A missing MH corpus is never silently treated as empty.

## 16. FINAL CONTROL STATEMENT

The objective is not to make 23 chats independently correct.

The objective is to make 23 historical architecture contours consistent projections of ONE MediaHub architecture while preserving every accepted function, invariant, decision, historical evidence item and unresolved technical question.

The canonical product remains one MediaHub system.
