# MH-24 Batch 04 — Product Owner Decision Record 01

**Decision date:** 2026-10-12  
**Status:** OWNER DECISIONS RECORDED — PARTIAL GOVERNANCE RESOLUTION; NOT A CANONICAL BACKLOG APPROVAL.  
**Decision source:** Explicit product-owner response in the MediaHub OS project conversation on 2026-10-12.  
**Repository/ref:** `VlDMlNSh/mediahub-os` / `docs/mediahub-chat-tree-map-20261012`.

## 1. Source basis checked before recording

| Source | Ref | Blob SHA | Purpose |
|---|---|---|---|
| `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md` | `docs/mediahub-chat-tree-map-20261012` | `eeba60329772e0033a027c1410075a046fbc6b43` | Current navigation and latest MH-24 checkpoint |
| `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md` | `docs/mediahub-chat-tree-map-20261012` | `f86014d81a2db1b5246b4fc2600812340f1c7d22` | Mandatory protocol and B1/B2 separation |
| `docs/checkpoints/MH24-BATCH-04-DECISION-TRIAGE-01.md` | `docs/mediahub-chat-tree-map-20261012` | `2113f4e378d8d7a439b36cf987833f80d56f8411` | Open owner questions and precedence policy |
| `docs/checkpoints/MH24-BATCH-04-NORMALIZATION-PROPOSAL-02.md` | `docs/mediahub-chat-tree-map-20261012` | `7e737c8add9e3453062e9fc459790e7010e55689` | Proposed atomization and source anchors |
| `docs/checkpoints/MH24-BATCH-04-OWNER-GOVERNANCE-DECISION-REGISTER-01.md` | `docs/mediahub-chat-tree-map-20261012` | `a1bd98aa461859bf173725703723ec8dff73cce5` | GOV-MH24-01…14 and exit criteria |

## 2. Explicit decisions supplied by the product owner

### D-01 — Accountable approver (triage A1; GOV-MH24-01)

**Decision:** The user confirms they are the accountable product owner and may approve product decisions for this normalization.  
**Effect:** Record subsequent explicit choices from this owner as product-owner decisions. This does not bypass independent review, domain-specific evidence, or separate release/production permissions.

### D-02 — UI4-04 disposition (triage B1; GOV-MH24-04)

**Decision:** Keep UI4-04 in `HOLD` / cross-link-only until sufficient evidence establishes a unique, non-duplicative residual requirement.  
**Constraints:** Do not invent a literal source span, create a stable child ID, or duplicate UI4-01/02 obligations while the evidence is absent.

### D-03 — Child-ID scheme (triage C1; GOV-MH24-11)

**Decision:** Approve the proposed lineage pattern `MH24-B04-SA4-02-a` (workstream + historical parent + child). Preserve historical/legacy IDs.  
**Required precondition before assigning final IDs:** Perform and record collision checks against existing IDs, including the separate Audit 01 register; maintain explicit parent-child lineage. Until that check is evidenced, proposed child suffixes remain provisional in working artifacts.

### D-04 — B1↔B2 mapping status vocabulary (triage D1; GOV-MH24-12)

**Decision:** Approve the mapping statuses:
- `MAPPED`
- `CONFLICT`
- `NO_DIRECT_COUNTERPART`
- `NOT_REVIEWED`

**Interpretation:** Baseline 2.0 is the current functional reference; Baseline 1.0 remains the literal historical source for edition 1.0. This approves the vocabulary and precedence framing, **not** the mapping of any individual atom. Each mapping must have exact source references and evidence; no equivalence is inferred automatically.

### D-05 — Required canonical-atom evidence schema (triage E2; GOV-MH24-13)

**Decision:** Approve the eight proposed minimum fields and the four additions. The required schema is:
1. `Requirement ID`
2. `Owner`
3. `Source atom / classification` (literal or derived, with source anchor/rationale)
4. `B2 mapping status`
5. `Canonical contract path/ref`
6. `Acceptance criteria`
7. `Required evidence`
8. `Lifecycle status`
9. `Reviewer / approval reference`
10. `Dependencies`
11. `Verification method`
12. `Change history`

Unknown or unverified values must remain explicitly unknown/open; they must not be inferred to make a record appear complete.

## 3. Decisions' scope and limits

These decisions resolve the owner-choice portions of GOV-MH24-01, GOV-MH24-04, GOV-MH24-11, GOV-MH24-12, and GOV-MH24-13 only to the extent described above. They do **not** implicitly approve all of Normalization Proposal 02 or resolve every GOV-MH24 row.

Still requiring documentary resolution, evidence, or explicit decision as applicable:
- shared literal atom ownership and cross-link semantics (GOV-MH24-02);
- distinct HA Core Smart Home authority and MediaHub platform State Authority scopes (GOV-MH24-03);
- literal-versus-derived AI automation/audit controls (GOV-MH24-07);
- shared cloud gate decomposition and derived fallback/continuity controls (GOV-MH24-10);
- domain-owner confirmations and acceptance/evidence details in other rows;
- the historical “47” statement versus 48 verified unique IDs, which must remain preserved as provenance unless a separate erratum is authorized (GOV-MH24-14).

The evidence-based recommendations recorded in Decision Triage 01 are not converted into owner approvals by this record.

## 4. Required next steps

1. Update the working governance register to reference these five explicit decisions without rewriting its historical question record.
2. Perform a collision check for the approved child-ID scheme and record the checked ID inventory/source SHA.
3. Build a field-complete, source-anchored crosswalk proposal using the approved 12-field schema and the four B1/B2 mapping statuses.
4. Keep UI4-04 on HOLD unless unique residual evidence is produced.
5. Run an independent documentary diff/review before any canonical backlog or matrix update.
6. Do not edit either baseline or merge into `main` without separate authorization.

**Current outcome:** Five owner choices recorded. Proposal 02 remains a proposal pending the remaining atom-level dispositions, collision-check evidence, complete crosswalk, and independent review. No baseline, canonical backlog, traceability matrix, implementation, test, qualification, deployment, infrastructure, or production state is changed by this record.
