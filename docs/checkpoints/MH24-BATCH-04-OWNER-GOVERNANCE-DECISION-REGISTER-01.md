# MH-24 Batch 04 — Owner/Governance Decision Register 01

**Date:** 2026-10-12  
**Status:** OPEN — DECISIONS REQUIRED; NOT AN APPROVAL RECORD.  
**Purpose:** Enumerate unresolved owner/governance choices before Proposal 02 can be converted into a canonical atomic traceability backlog. This register records questions and safe default recommendations; it does not answer on behalf of the product owner.

## 1. Source basis

| Source | Ref | Blob SHA |
|---|---|---|
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | `docs/mediahub-chat-tree-map-20261012` | `46d7755b17375b379d1e947ec7bd95748bae038a` |
| `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` | `docs/mediahub-chat-tree-map-20261012` | `f86014d81a2db1b5246b4fc2600812340f1c7d22` |
| `docs/checkpoints/MH24-BATCH-04-NORMALIZATION-PROPOSAL-02.md` | `docs/mediahub-chat-tree-map-20261012` | `7e737c8add9e3453062e9fc459790e7010e55689` |
| `docs/checkpoints/MH24-BATCH-04-NORMALIZATION-VALIDATION-02.md` | `docs/mediahub-chat-tree-map-20261012` | `e21137d8ac230a9ff28f616adcb840e234e5c965` |
| `docs/checkpoints/MH24-BATCH-04-NORMALIZATION-REVIEW-01.md` | `docs/mediahub-chat-tree-map-20261012` | `373530821ae8dcbcf84e953f42e047e99f7810a8` |
| `docs/checkpoints/MH24-ATOMIC-TRACEABILITY-BACKLOG-04.md` | `docs/mediahub-chat-tree-map-20261012` | `26163e6f60b44e997560212bf7de9900210b7ed3` |
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` |

## 2. Decision log

No decisions have been supplied or inferred. Every row below remains OPEN.

| Decision ID | Question requiring explicit decision | Evidence / affected items | Safe default pending decision | Decision authority / evidence required |
|---|---|---|---|---|
| GOV-MH24-01 | Who is the accountable owner for approving the normalized Batch 04 crosswalk and its child-level taxonomy? | Proposal 02 §§2, 5–6; Validation 02 §6 | Keep proposal and all child suffixes provisional; do not update canonical backlog. | Named product/domain owner; dated decision referencing this register and the approved revision. |
| GOV-MH24-02 | Which exact literal B1 atom is the single normative requirement for user configuration ownership at line 68 and resource lifecycle at line 69 when each is referenced by both SA4-02 and SA4-03? | SA4-02.c / SA4-03.a; SA4-02.d / SA4-03.b | One normative atom per B1 line; preserve both historical IDs as provenance/cross-links, not duplicate obligations. | State Authority/domain owner confirms canonical owner path and legacy cross-link semantics. |
| GOV-MH24-03 | How should HA Core Smart Home authority and MediaHub platform State Authority be represented without implying competing or interchangeable authorities? | HA4-01, HA4-06; B1 lines 85, 97–98 | Maintain two distinct domain-scoped authority claims and cross-link them; no authority escalation inferred. | Architecture/security owner confirms scope statement and canonical contract references. |
| GOV-MH24-04 | Does UI4-04 represent a unique residual requirement, or should it remain a legacy cross-link / explicitly D-coded derived control? | UI4-01/02/03/04; B1 lines 104, 107–116; Review 01 R04 | HOLD UI4-04; do not assign a literal source span or stable child ID until a non-duplicative obligation is provided. | UI/domain owner provides exact residual wording, source rationale, or explicit derived-control acceptance. |
| GOV-MH24-05 | Which historical item owns vendor-neutral extensibility, and how is it cross-linked to device exposure in unified UI without duplicating obligations? | SH4-01.b / SH4-07 at B1 line 136; SH4-06.c at line 134 | One canonical vendor-neutral atom at line 136 and a separate UI-exposure atom at line 134; cross-link only. | Smart Home/UI owners approve canonical ownership and links. |
| GOV-MH24-06 | Are energy/security automation categories represented once as literal atoms with AUTO4-02 serving only as a historical cross-link? | AUTO4-01.j/.k and AUTO4-02; B1 line 204 | Treat line 204 as one literal source list; avoid counting AUTO4-02 as a second normative copy. | Automation owner confirms inventory semantics and canonical ID mapping. |
| GOV-MH24-07 | Which parts of the AI-assisted automation sentence are literal capabilities versus derived audit/result-record controls? | AUTO4-03/04/05; B1 line 206 | Keep the sentence as the literal source; label audit schema, mandatory result record, and extra fail-closed behavior as D-coded unless independently sourced. | AI/automation/security owner approves derived-control rationale and required evidence. |
| GOV-MH24-08 | How should LAI4-01/03/04/05/06/07 be cross-linked so that local execution, capability labels, domain support, and advisory boundary remain distinct and non-duplicative? | B1 lines 232, 235–249; LAI4-05.a–f; LAI4-06 cross-links | Preserve six literal capability atoms at lines 242–247; LAI4-06 remains cross-link-only for lines 244–246; keep line 249 as a distinct advisory boundary. | Local AI/domain owner approves atom map, cross-links, and contract ownership. |
| GOV-MH24-09 | Which cluster AI controls are literal B1 requirements, and which are derived acceptance controls? | CLAI4-01/03/04/05; B1 lines 255–267 | Keep trusted-cluster and gateway statements literal; node admission, resource/failure behavior, qualification profiles remain D-coded unless a precise B1 source is cited. | Cluster AI/security owner approves each derived control and its acceptance/evidence requirements. |
| GOV-MH24-10 | How should the single cloud-compute gate at line 291 be decomposed for traceability without multiplying one compound gate into multiple independent normative requirements? | CDAI4-04 / CDAI4-05; B1 line 291 | Use a shared source-gate identifier and child condition references; provider allowlist/fallback and local continuity remain derived controls. | Cloud/security/privacy owner approves gate model, egress/residency requirements, and canonical contract links. |
| GOV-MH24-11 | What stable child-ID scheme should be adopted, considering collision risk with Audit 01's separate 153-row register? | Proposal 02 §2 and §6.3; Audit 01/02 | Do not mint stable child IDs yet; keep proposed suffixes visibly provisional and maintain legacy parent IDs unchanged. | Governance owner approves namespace, lineage rules, collision checks, and migration approach. |
| GOV-MH24-12 | What exact B2 mapping and reconciliation disposition applies to each approved B1 atom? | Proposal 02 §§4–5; map §20.22; Baseline 1.0 SHA above and current Baseline 2.0 on `main` | Do not infer B2 acceptance from B1 anchoring; keep baselines separate until explicit reconciliation. | Baseline/governance owner supplies exact B2 clause refs, conflict disposition, and approval evidence. |
| GOV-MH24-13 | Which canonical contract, acceptance criteria, implementation evidence, and qualification evidence fields are mandatory per normalized item? | Proposal 02 §§2, 5; Validation 02 §§4–6 | Keep these fields distinct; blank/unknown is preferable to inferred values. Do not promote status. | Domain owner defines required evidence schema and acceptance authority per item. |
| GOV-MH24-14 | How is the historical “47 records” sentence handled against the verified set of 48 unique IDs? | Historical Batch 04; Validation 02 §2 | Preserve historical artifact unchanged; report 48 unique IDs in new documents and record discrepancy as provenance. | Documentation owner decides whether a separate erratum is warranted; never silently rewrite historical evidence. |

## 3. Mandatory fields for recording a decision

For every resolved row, record:
- decision ID and exact question resolved;
- decision value and rationale;
- accountable owner / approving role;
- date and approval evidence reference;
- affected historical IDs and proposed child atoms;
- exact B1 source line(s) and literal-versus-derived classification;
- B2 mapping or explicit “not reconciled” status;
- canonical contract path/ref;
- acceptance criteria and required evidence;
- resulting status and any supersession links.

A conversation-level preference or an unreferenced statement is not sufficient evidence to mark the decision approved. If the product owner explicitly decides an item, record that decision in a separate decision artifact and preserve this register's history.

## 4. Exit criteria before canonical backlog update

The canonical backlog must remain unchanged until all applicable conditions are met:
1. Every row above is either explicitly decided or formally marked not applicable by the accountable owner.
2. Each literal atom has an exact B1 anchor; each derived control is D-coded with rationale.
3. Every shared source atom has one normative owner and secondary links rather than duplicate normative records.
4. Stable child-ID syntax and lineage to the 48 legacy IDs are approved and collision-checked against the separate 153-row register.
5. B1/B2 mapping status is explicit and unresolved conflicts remain visible.
6. Owner, contract, acceptance criteria, and evidence requirements are defined.
7. An independent reviewer reads the proposed canonical diff before any backlog update.

## 5. Current disposition

- Register status at original creation: **OPEN — NO OWNER DECISIONS RECORDED**; see §6 for subsequent owner decisions.
- Proposal 02: **OPEN / NOT APPROVED**.
- Historical Batch 04: unchanged; 48 unique historical IDs preserved.
- Baseline 1.0, Baseline 2.0, and traceability matrix: unchanged.
- Canonical backlog and stable child IDs: unchanged / not created.
- No tests, qualification, installation, deployment, infrastructure/production action, or merge to `main` was performed.


## 6. Subsequent product-owner decisions — 2026-10-12

This section is a dated status addendum. It preserves the original questions and safe defaults above rather than rewriting their historical record.

**Decision artifact:** `docs/checkpoints/MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md`  
**Ref:** `docs/mediahub-chat-tree-map-20261012`  
**Blob SHA (read-back):** `9117098e22c26708d48ca8ba5954669faa209d68`  
**Decision record status:** OWNER DECISIONS RECORDED — PARTIAL GOVERNANCE RESOLUTION; NOT A CANONICAL BACKLOG APPROVAL.

| Register row | Current recorded decision | Remaining condition |
|---|---|---|
| GOV-MH24-01 | Resolved for this normalization: user confirms accountable product-owner authority. | Does not waive independent review or separate release/production permissions. |
| GOV-MH24-04 | UI4-04 stays HOLD/cross-link-only pending evidence of a unique residual requirement. | No literal span or stable child ID until supported. |
| GOV-MH24-11 | Child-ID lineage pattern `MH24-B04-SA4-02-a` approved; legacy IDs preserved. | Final ID assignment awaits documented collision checks against existing inventory, including Audit 01. |
| GOV-MH24-12 | Mapping vocabulary approved: `MAPPED / CONFLICT / NO_DIRECT_COUNTERPART / NOT_REVIEWED`; B2 current functional reference, B1 literal historical source. | Atom-by-atom mapping and any conflict disposition require exact references/evidence; no equivalence is inferred. |
| GOV-MH24-13 | Twelve-field canonical-atom schema approved: Requirement ID, Owner, Source atom/classification, B2 mapping status, Canonical contract path/ref, Acceptance criteria, Required evidence, Lifecycle status, Reviewer/approval reference, Dependencies, Verification method, Change history. | Populate each field from evidence; unknown values remain explicitly unknown/open. |

GOV-MH24-02, 03, 05, 06, 07, 08, 09, 10, and 14 are not approved or closed by this addendum. Recommendations in Decision Triage 01 remain recommendations unless separately recorded as explicit decisions with evidence.

**Current disposition after addendum:** five owner-choice areas have recorded decisions; Proposal 02 remains OPEN / NOT APPROVED; canonical backlog and traceability matrix remain unchanged; no final child IDs have been assigned; Baseline 1.0 and Baseline 2.0 remain unchanged. The next gates are collision-check evidence, atom-level crosswalk completion, resolution of remaining applicable register rows, and independent documentary review. No tests, qualification, installation, deployment, infrastructure/production action, or merge to `main` was performed.
