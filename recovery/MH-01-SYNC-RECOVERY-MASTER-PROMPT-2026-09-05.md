# MEDIAHUB OS 11.x LTS / MEDIAHUB iOS
# MH-01 SYNC & RECOVERY MASTER PROMPT

Date: 2026-09-05
Repository: VlDMlNSh/mediahub-os
Branch: recovery/full-functional-spec

## 0. PURPOSE

This prompt is the controlled recovery/synchronization instruction for the MH-01 historical architecture contour.

Goal: recover, synchronize and reconcile all available MH-01 evidence with the canonical MediaHub architecture without inventing missing facts, deleting historical evidence, or changing canonical truth unilaterally.

Current state: MH-01 is ACCOUNTED / RECONSTRUCTED / HISTORICAL-CORPUS-EVIDENCE-GAPPED.

This prompt does NOT accept the Master Architecture and does NOT authorize production implementation.

## 1. AUTHORITY ORDER

Use evidence in this order:
1. GitHub repository and immutable commit history.
2. Canonical recovery control point and redistribution master prompt.
3. specification/capability-registry.yaml
4. specification/contract-registry.yaml
5. specification/invariant-registry.yaml
6. specification/decision-registry.yaml
7. specification/dependency-graph.yaml
8. architecture/master-mediahub-architecture-reconstruction-2026-09-05.md
9. development/implementation-map.yaml
10. MH-01 historical material supplied by the user or recovered from authoritative sources.

If sources conflict, preserve both provenance records, identify the contradiction, and escalate to central reconciliation. Never silently overwrite evidence.

## 2. NON-NEGOTIABLE ANTI-LOSS RULES

- UNKNOWN != LOST.
- EVIDENCE_GAP != LOST.
- NOT_FOUND_IN_CURRENT_SEARCH != NEVER_EXISTED.
- DEFERRED != REJECTED.
- NOT_IMPLEMENTED != REMOVED.
- No capability may be deleted because MH-01 evidence is missing.
- Historical evidence must be preserved with source and commit SHA.
- Canonical ownership is unique; cross-domain references are allowed.
- MH-01 has no unilateral authority over canonical registries.

## 3. CANONICAL BASELINE

Protect the current baseline:
- 58 canonical capabilities.
- 51 canonical domains.
- 58/58 explicit capability ownership.
- 36 contract families.
- 30 protected invariants.
- DEC-001…DEC-012 accepted.
- DEC-A-001…DEC-A-004 remain DRAFT.
- Master Architecture remains DRAFT / NOT ACCEPTED.
- Production implementation remains BLOCKED.

The recovery pass must prove preservation of the 58/58 capability baseline after synchronization.

## 4. MH-01 RECOVERY OBJECTIVE

Recover the historical MH-01 contour as completely as evidence permits.

Search and reconcile:
- historical requirements;
- architecture principles and boundaries;
- domain/component ownership;
- capability mappings;
- contracts and interfaces;
- invariants;
- decisions and rejected alternatives;
- dependencies;
- implementation boundaries;
- tests and verification;
- acceptance/release evidence;
- references to other MH contours;
- historical files, commits, branches, tags and migration artifacts where accessible.

Do not assume that absence from the current branch means historical absence.

## 5. SYNCHRONIZATION PROTOCOL

For every recovered MH-01 artifact:

EVIDENCE -> IDENTIFY SOURCE -> RECORD PATH/COMMIT SHA -> CLASSIFY -> MAP -> CONTRADICTION CHECK -> ANTI-LOSS CHECK -> CENTRAL REGISTRY IMPACT -> VERIFICATION -> ACCEPTANCE STATUS.

Every material item must receive one of:
- RETAIN
- REMAP
- RECONCILE
- REPLACE (only when canonical authority explicitly requires it)
- RETIRE (only with explicit evidence and approval)
- UNKNOWN / EVIDENCE_GAP

Never use RETIRE or REPLACE merely because an item is absent from the current implementation.

## 6. REQUIRED TRACEABILITY

Build and verify:
FUNCTION -> REQUIREMENT -> CONTRACT -> ARCHITECTURE -> IMPLEMENTATION BOUNDARY -> TEST -> ACCEPTANCE.

For each recovered item record:
- evidence source;
- provenance;
- canonical mapping;
- historical status;
- current status;
- contradiction, if any;
- dependency impact;
- security/authority impact;
- variant impact;
- verification evidence;
- confidence.

## 7. SECURITY / AUTHORITY PRESERVATION

Preserve these semantics during reconstruction:
- Discovery != Trust.
- Presence != Authentication.
- Authentication != Authorization.
- Physical connection != Authorization.
- Health != Trust.
- Readiness != Trust.
- Liveness != Trust.
- Remote access != increased authorization.

No recovered MH-01 artifact may create an undocumented authority bypass.

## 8. STATE AUTHORITY

MediaHub remains the single user-facing Smart Home model.

State Authority remains canonical and centralized by contract.

Knowledge, AI, Digital Twin, search, telemetry, projections, caches or historical models must not silently become State Authority.

No historical MH-01 material may authorize:
- Graph -> Device bypass;
- AI -> physical mutation bypass;
- Digital Twin -> Device bypass;
- projection/cache -> canonical state mutation.

## 9. LOCAL / CLOUD AND STORAGE BOUNDARIES

Preserve:
- Local MediaHub as primary runtime.
- Local Assistant first.
- Cloud Development as controlled privileged infrastructure, not ordinary-user workspace.
- Local MediaHub Cluster != Cloud Development Cluster.
- System Storage != Surveillance Recording Storage != Personal Media Library Storage.

Do not infer physical storage implementation without evidence.

## 10. RECOVERY / DATA SAFETY

Recovery work must be additive and reversible.

Before changing any recovered artifact:
1. preserve original evidence;
2. record source and SHA;
3. create a normalized reconstruction separately;
4. compare original vs normalized form;
5. record all transformations;
6. verify no canonical capability or invariant was lost;
7. leave unresolved ambiguity explicitly marked.

No destructive migration, deletion, overwrite, or irreversible transformation is authorized by this prompt.

## 11. REQUIRED OUTPUTS FROM MH-01 CHAT

Produce, if evidence permits:
1. MH-01 Evidence Inventory.
2. MH-01 Historical Scope Reconstruction.
3. MH-01 Requirement Mapping.
4. MH-01 Capability Mapping against CAP-001…CAP-058.
5. MH-01 Contract Mapping against CTR-001…CTR-036.
6. MH-01 Invariant Mapping against INV-001…INV-030.
7. MH-01 Decision Mapping against DEC-001…DEC-012 and DEC-A-001…004.
8. MH-01 Dependency Impact.
9. MH-01 Contradiction Register.
10. MH-01 Missing Evidence Register.
11. MH-01 Traceability Matrix.
12. MH-01 Anti-Loss Verification.
13. MH-01 Proposed Registry Changes — proposals only unless centrally accepted.
14. Updated MH-01 Reverse Master Prompt with exact evidence and SHAs.
15. Final MH-01 reconciliation status.

## 12. ACCEPTABLE FINAL STATES

Use precise status semantics:

A. RECONCILED / EVIDENCE-COMPLETE
Only when the historical evidence required for the claimed scope is actually available and verified.

B. RECONCILED / EVIDENCE-GAPPED
When the available evidence permits a reliable canonical reconciliation but some historical corpus or implementation evidence remains missing.

C. UNKNOWN / EVIDENCE-GAP
When insufficient evidence exists to reconstruct the historical contour reliably.

Never promote B or C to A without new evidence.

## 13. CENTRAL ACCEPTANCE GATE

MH-01 completion is not Master Architecture acceptance.

The final authority sequence is:
MH-01 result -> central MH-01…MH-23 reconciliation -> contradiction/dependency/security/anti-loss verification -> human acceptance -> only then architecture acceptance and production authorization.

Until that sequence completes:
- Master Architecture = DRAFT / NOT ACCEPTED.
- Production implementation = BLOCKED.

## 14. FINAL COMMAND

Recover MH-01 completely where evidence exists.
Synchronize recovered evidence with the canonical registries without silent mutation.
Preserve every capability, invariant, contract and historical artifact.
Record every gap explicitly.
Do not invent missing architecture.
Do not convert absence of evidence into evidence of absence.
Return the strongest evidence-backed reconciliation possible and stop at the exact boundary of what can be proven.

ONE MEDIAHUB.
ONE CANONICAL ARCHITECTURE.
MH-01 HISTORICAL EVIDENCE PRESERVED.
ZERO FUNCTION LOSS.
