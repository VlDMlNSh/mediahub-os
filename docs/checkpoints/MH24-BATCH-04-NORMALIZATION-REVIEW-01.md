# MH-24 Batch 04 Normalization Proposal — Independent Review 01

**Date:** 2026-10-12  
**Status:** INDEPENDENT DOCUMENTARY REVIEW / OPEN — proposal remains NOT APPROVED.  
**Scope:** Read-only review of normalization proposal 01 against the literal Baseline 1.0 source, historical Batch 04, Audit 01 and Audit 02. No canonical backlog, baseline, matrix, IDs, governance state, implementation or qualification is changed.

## 1. Sources actually read

| Source | Ref | Blob SHA | Review use |
|---|---|---|---|
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | `docs/mediahub-chat-tree-map-20261012` | `d774550f820c7c70b31870427e3b013358f6432b` | Current navigation and latest checkpoint |
| `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` | `docs/mediahub-chat-tree-map-20261012` | `f86014d81a2db1b5246b4fc2600812340f1c7d22` | Required process / limits |
| `docs/checkpoints/MH24-BATCH-04-NORMALIZATION-PROPOSAL-01.md` | `docs/mediahub-chat-tree-map-20261012` | `f883f0e69316bf001391606d6a9f5c853a8e8262` | Proposal under review |
| `docs/checkpoints/MH24-ATOMIC-TRACEABILITY-BACKLOG-04.md` | `docs/mediahub-chat-tree-map-20261012` | `26163e6f60b44e997560212bf7de9900210b7ed3` | Historical IDs and source anchors |
| `docs/checkpoints/MH24-B1-SECTIONS-03-06-12-15-17-CLAUSE-COVERAGE-AUDIT-01.md` | `docs/mediahub-chat-tree-map-20261012` | `d0938f14ed4110545118f075175dee3be412097b` | Clause/control register |
| `docs/checkpoints/MH24-B1-SECTIONS-03-06-12-15-17-CLAUSE-COVERAGE-AUDIT-02.md` | `docs/mediahub-chat-tree-map-20261012` | `8b1f02eb07e153be825e39ec7a0289b0105d6156` | Independent structural validation |
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Literal normative source |

## 2. Review outcome

**Result: HISTORICAL INVENTORY PRESERVED; PROPOSAL NEEDS SOURCE-SPAN CORRECTIONS AND OVERLAP REVIEW BEFORE OWNER/GOVERNANCE REVIEW.**

Confirmed:
- Historical Batch 04 contains 48 unique IDs; its concluding sentence incorrectly says 47.
- Proposal 01 lists all 48 historical IDs and keeps them proposed/open.
- B1 has the eight reviewed sections at the recorded headings: §§3, 4, 5, 6, 12, 15, 16 and 17.
- The proposal explicitly distinguishes derived controls from literal B1 wording and does not claim Audit 01's 153 IDs are 153 independent requirements.
- No baseline/matrix/backlog edits, status upgrades, tests, qualification, installation, infrastructure change or merge to `main` occurred.

## 3. Concrete corrections required

| Finding | Proposal entry | Evidence / issue | Required correction |
|---|---|---|---|
| R01 — missing literal UI atom in cited span | UI4-02, §5 lines 108–111, 114 | B1 line 107 is “минималистичный интерфейс”; current proposed span starts at line 108 while child atom UI4-02.a is “minimal”. | Extend source span to include line 107. Keep each visual requirement individually anchored: 107–111 and 114, with 112–113 reserved for macOS-like UX and distinct identity. |
| R02 — unrelated source line bundled into discovery anchor | SH4-03, §6 lines 126 and 136 | Line 126 states automatic equipment discovery; line 136 states vendor-neutral compatibility objective. Line 136 does not substantiate discovery or discovery≠trust. | Anchor the literal discovery atom to line 126 only. Keep “discovery does not imply trust/enrollment” as a separately D-coded control; cross-link SH4-01/07 only for vendor-neutral compatibility. |
| R03 — source span too broad and overlapping | SA4-03, §3 lines 65–75 | The proposed children are user-configuration ownership and resource lifecycle, specifically B1 lines 68–69; lines 65–75 also cover unrelated state, authorization, consistency, provenance, audit, recovery and migration obligations. | Narrow literal anchors to lines 68–69 and cross-link SA4-02.c/.d; do not claim lines 65–75 as direct source for just these two atoms. |
| R04 — composite/overlapping UI anchor needs a boundary | UI4-04, §5 lines 104–116 | The range spans UI4-01, visual language and navigation requirements, so it cannot itself identify a non-duplicative “remaining” obligation. | Do not treat the full range as a new literal requirement. Specify the exact residual clause, or mark UI4-04 as a derived presentation/authority-boundary control and cross-link source clauses without duplicating UI4-01/02. |
| R05 — source-atom granularity is not yet stable | HA4-01, LAI4-01, LAI4-03, CDAI4-01 and CDAI4-04 | Some entries intentionally cite multiple separated lines/clauses or divide a compound sentence into children; current table does not always say which child maps to which exact phrase. | Add child-level source spans (and D-code where needed), not only parent-level spans. This is a precision issue, not proof that the underlying requirement is absent. |
| R06 — stale map provenance in proposal input table | Proposal §1, map row | Proposal cites map SHA `57b1ecebef504dfabaca57248cd32c8b37a4bc90`, whereas the current map read before this review is SHA `d774550f820c7c70b31870427e3b013358f6432b`. | Preserve the old SHA as historical “map version used when proposal was drafted”; do not label it current. A later revision should record both proposal-time and review-time map versions. |

## 4. Cross-record overlap requiring owner/governance disposition

These are not automatically defects; the proposal itself says cross-links are preferred. They must be explicitly resolved before canonical child IDs are minted:

1. **SA4-02 ↔ SA4-03:** system/object state vs user configurations/resource lifecycle. Make the parent-child relationship and exact source atoms explicit.
2. **HA4-01 ↔ HA4-06:** HA Core authority and distinct platform State Authority scope. Keep one authority-scope contract cross-linked rather than duplicate obligations.
3. **UI4-01 ↔ UI4-02 ↔ UI4-04:** unified interface, visual/design criteria and hiding backend complexity. Identify the residual obligation for UI4-04 or keep it derived.
4. **SH4-01 ↔ SH4-07 ↔ SH4-06.c:** vendor-neutral extensibility vs device exposure through unified UI. Do not count the same UI exposure obligation twice.
5. **AUTO4-01.j/.k ↔ AUTO4-02:** energy/security are both inventory atoms and separately important functional categories. Use cross-links rather than duplicated normative text.
6. **AUTO4-04 ↔ AUTO4-05:** controlled MediaHub/HA mechanism is literal B1; mandatory audit/result schema is a derived acceptance control unless sourced to another exact clause.
7. **LAI4-01 ↔ LAI4-07 and LAI4-03 ↔ LAI4-05:** AI runtime/location, advisory boundary, analysis/help, search/data and local intelligent processing need exact per-child spans to avoid overlapping capability claims.
8. **CLAI4-01/03 ↔ CLAI4-04/05:** trusted-cluster/gateway wording is literal; node admission, capability, resource/failure behavior and qualification profiles are derived controls unless separately sourced.
9. **CDAI4-04 ↔ CDAI4-05 ↔ CDAI4-07:** the single B1 sentence at line 291 already includes requester, insufficiency, policy, confidentiality, authorization and residency/egress. Separate these as traceable conditions without multiplying the same gate; provider allowlist/fallback and local continuity remain derived unless sourced elsewhere.

## 5. Constraints and status

- This review does not approve proposal 01 and does not create canonical child IDs.
- All historical IDs and all related records remain OPEN.
- Baseline 1.0 remains the literal source under review. Baseline 2.0 and the MH-24 matrix status conflict remain unresolved.
- No changes were made to Baseline 1.0, Baseline 2.0, the traceability matrix or original Batch 04.
- No tests/qualification, software installation, deployment, infrastructure or production action was performed. No merge to `main` occurred.

## 6. Next safe step

Revise proposal 01 in a new version only after preserving this review as evidence; correct R01–R06, produce child-level exact source anchors, and prepare an owner/governance decision list for the overlap items. Keep all suffixes provisional until explicit approval. Do not update the canonical backlog or baselines without that approval.
