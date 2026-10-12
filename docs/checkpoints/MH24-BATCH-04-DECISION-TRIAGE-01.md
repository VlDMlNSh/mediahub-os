# MH-24 Batch 04 — Decision Triage 01

**Date:** 2026-10-12  
**Status:** WORKING TRIAGE / OPEN — NOT AN APPROVAL RECORD.  
**Scope:** Separate documentary discrepancies resolvable from latest evidence from owner decisions. No canonical backlog, matrix, or baseline is changed.

## 1. Current source snapshot

| Source | Ref | Blob SHA | Interpretation |
|---|---|---|---|
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | `docs/mediahub-chat-tree-map-20261012` | `7306207b93787a5b3478d5584bb1b3354c9bcdc9` | Current map; §20.24 is latest checkpoint |
| `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` | `docs/mediahub-chat-tree-map-20261012` | `f86014d81a2db1b5246b4fc2600812340f1c7d22` | Requires visible B1/B2 reconciliation; no silent substitution |
| `docs/checkpoints/MH24-BATCH-04-NORMALIZATION-PROPOSAL-02.md` | `docs/mediahub-chat-tree-map-20261012` | `7e737c8add9e3453062e9fc459790e7010e55689` | Latest proposal revision |
| `docs/checkpoints/MH24-BATCH-04-OWNER-GOVERNANCE-DECISION-REGISTER-01.md` | `docs/mediahub-chat-tree-map-20261012` | `a1bd98aa461859bf173725703723ec8dff73cce5` | Open questions |
| `docs/checkpoints/MH24-BATCH-04-OWNER-GOVERNANCE-REGISTER-REVIEW-01.md` | `docs/mediahub-chat-tree-map-20261012` | `ae9ff159117a08fceb9ea26e5cadd0dcafeb2105` | 14/14 questions traceable; no approval |
| `docs/checkpoints/mediahub-functional-baseline-2.0.md` | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Accepted canonical current functional reference |
| `docs/checkpoints/mediahub-mh24-traceability-matrix.md` | `main` | `8bdd364493ebbe2ef6f87400f80bc7eca8fb95c6` | Still labelled RECONCILIATION CANDIDATE |
| `docs/checkpoints/mediahub-mh24-reconciliation-report.md` | `main` | `d07d162ebaa57643a7bdd84d6fb13a1102b87bfc` | Records MH-24 CLOSED / B2 accepted |
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Fixed edition-1.0 passport and literal historical source |

## 2. Latest-edits precedence

Use the latest revision to correct a document's own content. Prefer the latest accepted canonical decision over an older provisional/candidate record for current functional meaning. Preserve older artifacts as provenance. A newer timestamp alone does not authorize changing a baseline. Baseline 2.0 is the current functional reference; Baseline 1.0 remains the immutable edition-1.0 source. Exact B1 atoms must not be presumed mapped to B2 without an explicit crosswalk.

## 3. Documentary dispositions recommended from latest evidence

| Register row | Recommended disposition | Basis |
|---|---|---|
| GOV-MH24-02 | One normative atom for B1 line 68 and one for line 69; SA4-02/SA4-03 IDs are provenance/cross-links, not duplicate obligations. | Proposal 02 §6.1 |
| GOV-MH24-03 | HA Core owns Smart Home scope; MediaHub State Authority owns platform state. Keep authority scopes distinct. | Proposal 02; accepted B2 §3 |
| GOV-MH24-05 | Vendor-neutral compatibility at B1 line 136; UI exposure at line 134 remains separate. | Proposal 02 §§6.1–6.2 |
| GOV-MH24-06 | B1 line 204 is one source list; energy/security child labels are cross-links, not duplicate requirements. | Proposal 02 §§6.1–6.2 |
| GOV-MH24-08 | Keep six literal capability anchors at B1 lines 242–247; LAI4-06 is cross-link-only for overlapping domain support. | Proposal 02 §6.1 |
| GOV-MH24-09 | Trusted-cluster placement and gateway are literal; node/resource/failure/qualification details remain derived unless another exact source is found. | Proposal 02 §§6.1–6.2 |
| GOV-MH24-14 | New documents report 48 unique historical IDs; preserve the historical “47” text unchanged. | Validation 02 |

These are evidence-based recommendations, not approval of Proposal 02.

## 4. Owner decisions still required

| ID | Question | Safe default |
|---|---|---|
| GOV-MH24-01 | Who is the accountable approver? | Do not infer an authorized role from repository evidence. |
| GOV-MH24-04 | Does UI4-04 have a unique residual requirement? | Keep HOLD/cross-link-only; no literal atom or stable ID. |
| GOV-MH24-07 | Approve separation of literal AI capabilities from derived audit/result-record controls? | Keep extra audit schema/result-record behavior D-coded pending contract/owner approval. |
| GOV-MH24-10 | Approve one shared source-gate model for B1 line 291? | Split conditions only for traceability; preserve one shared literal gate; derived fallback/continuity controls remain D-coded. |
| GOV-MH24-11 | Which stable child-ID namespace/lineage scheme? | Keep suffixes provisional; preserve legacy IDs and collision-check against Audit 01. |
| GOV-MH24-12 | What B1↔B2 mapping disposition applies to each atom? | Use statuses MAPPED / CONFLICT / NO_DIRECT_COUNTERPART / NOT_REVIEWED; B2 is current functional reference and B1 literal source, but do not infer equivalence. |
| GOV-MH24-13 | Which fields are mandatory for canonical atoms? | Minimum proposal: owner, source atom/classification, B2 mapping status, contract path/ref, acceptance criteria, evidence requirements, lifecycle status, approval/reviewer reference. |

## 5. Proposed policy

1. Latest accepted canonical decision governs current functional meaning; older records remain historical provenance.
2. Latest correction within a document wins over earlier versions of that document.
3. B2 is the current functional reference; B1 remains a literal edition-1.0 source. Crosswalk explicitly rather than silently reconciling.
4. A cross-link is not a second normative requirement.
5. Derived controls are D-coded with rationale, owner, contract, acceptance criteria, and evidence.
6. Do not create stable IDs, update canonical backlog/matrix, or amend either baseline until applicable owner decisions and independent diff review are complete.

## 6. Minimum questions to unblock the next stage

Please answer only these; other documentary discrepancies will be resolved using the latest accepted evidence:

**A. Approval role:** Are you the accountable product owner/approver for this normalization? (yes/no)

**B. UI4-04:** Approve HOLD/cross-link-only until a unique residual requirement is evidenced? (yes/no)

**C. Child IDs:** Approve pattern `MH24-B04-SA4-02-a` (workstream + historical parent + child), preserving legacy IDs and requiring collision checks? (yes/no; give alternative if no)

**D. B1/B2 mapping:** Approve statuses `MAPPED / CONFLICT / NO_DIRECT_COUNTERPART / NOT_REVIEWED`, with B2 current and B1 historical literal source? (yes/no)

**E. Evidence schema:** Approve the minimum fields in §4 for each canonical atom? (yes/no; identify additions)

## 7. Current state

Proposal 02 remains OPEN / NOT APPROVED. Owner decisions remain open. Canonical backlog, matrix, Baseline 1.0 and Baseline 2.0 remain unchanged. No tests, qualification, installation, deployment, infrastructure/production action, or merge to `main` was performed.
