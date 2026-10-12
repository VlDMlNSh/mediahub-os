# MH-24 Batch 04 — Atom-Level Crosswalk Batch 03 (B1 §5 MediaHub User Interface)

- Date: 2026-10-12
- Branch: `docs/mediahub-chat-tree-map-20261012`
- Status: **DOCUMENTARY DRAFT / OPEN — NOT APPROVED; NOT A CANONICAL BACKLOG**
- Scope: 10 Audit 01 atom labels B1-05-01…B1-05-10, B1 §5 source lines 104, 107–114 and 116.
- B1 source: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` @ `main`, SHA `9df4892ed0734050ac79732603d15bb414717310`.
- B2 reference: `docs/checkpoints/mediahub-functional-baseline-2.0.md` @ `main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Audit 01 SHA `d0938f14ed4110545118f075175dee3be412097b`; Proposal 02 SHA `7e737c8add9e3453062e9fc459790e7010e55689`; Product Owner Decision Record SHA `9117098e22c26708d48ca8ba5954669faa209d68`.

## 1. Interpretation / UI4-04 hold

- Status vocabulary remains `MAPPED`, `CONFLICT`, `NO_DIRECT_COUNTERPART`, `NOT_REVIEWED`.
- Audit 01 marks the exact style/visual requirements in rows B1-05-02/03/04/05/07/08 as `NOT-LOCATED` in the reviewed B2 clauses. They are labelled `NO_DIRECT_COUNTERPART` here only for that reviewed scope; this is not a claim of global absence from every possible domain document.
- Mixed/partial relations remain `NOT_REVIEWED`. Explicit source coverage is not inferred from general architectural similarity.
- **UI4-04 remains HOLD / CROSS-LINK-ONLY.** Although B1 line 114 contains literal wording about hiding complexity behind a unified interface, Proposal 02 places it under UI4-02.f; the owner explicitly prohibited creating a duplicate UI4-04 requirement until a unique residual obligation is established. This draft therefore preserves the literal anchor as a cross-link/overlap record, does not mint a child ID and does not present it as a newly approved atom.
- Historical IDs and parent/cross-link lineage are preserved. The existing Audit 01 labels are not final Requirement IDs; no final child IDs are minted.
- The 12-field schema is approved; this atom-level mapping, acceptance criteria and domain ownership are not thereby approved.

## 2. Batch summary

| Metric | Result |
|---|---:|
| Audit 01 source/control rows | 10 |
| Draft rows | 10 |
| MAPPED | 0 |
| NOT_REVIEWED | 4 |
| NO_DIRECT_COUNTERPART | 6 |
| CONFLICT | 0 |
| UI4-04 lifecycle | HOLD / CROSS-LINK-ONLY |
| Stable child IDs minted | 0 |
| Runtime tests / qualification / deployment | Not run |

## 3. Atom-level records — 12 fields each

### B1-05-01 — UI4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/UI4-01/B1-05-01 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 104 — MediaHub provides one unified user-facing visual environment.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §2.3. B2 §2.3 describes the MediaHub application roles and separation but is not a complete UI surface/route inventory.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: an accepted UI surface inventory defines the unified user-facing environment, included surfaces and exceptions.
- **Required evidence:** B1 line 104; B2 §2.3; accepted MH-09 design/route acceptance and surface inventory.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** MH-09 UI; MH-05 Smart Home integration; mobile product boundary.
- **Verification method:** Exact B1/B2 source comparison and independent review of the UI surface inventory.
- **Change history:** Audit 01 atom B1-05-01; historical parent/cross-links UI4-01 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

### B1-05-02 — UI4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/UI4-02/B1-05-02 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 107 — Literal list item: minimalist interface.
- **B2 mapping status:** NO_DIRECT_COUNTERPART. Audit 01 relation: NOT-LOCATED in reviewed B2 clauses. Audit 01 did not locate a direct counterpart for this visual design detail in the reviewed B2 clauses. This is scoped to the reviewed B2 text, not a claim of global absence.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: owner-approved design rubric/tokens define how minimalism is reviewed without rewriting B1.
- **Required evidence:** B1 line 107; B2 clauses reviewed in Audit 01; owner-approved design reference/rubric still required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** MH-09 UI; visual design system; accessibility constraints.
- **Verification method:** Verify B1 anchor and Audit 01 NOT-LOCATED classification; separately review the design rubric if/when approved.
- **Change history:** Audit 01 atom B1-05-02; historical parent/cross-links UI4-02 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

### B1-05-03 — UI4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/UI4-02/B1-05-03 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 108 — Literal list item: predominantly grey styling.
- **B2 mapping status:** NO_DIRECT_COUNTERPART. Audit 01 relation: NOT-LOCATED in reviewed B2 clauses. Audit 01 did not locate a direct counterpart for this color/styling detail in the reviewed B2 clauses. Scope is limited to the reviewed text.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: an owner-approved theme token/reference specifies predominant grey use and permitted variants.
- **Required evidence:** B1 line 108; reviewed B2 clauses; approved color tokens/reference set not yet identified.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** MH-09 UI; visual design system; accessibility/contrast requirements.
- **Verification method:** Verify exact source anchor and Audit 01 status; later review the approved theme reference.
- **Change history:** Audit 01 atom B1-05-03; historical parent/cross-links UI4-02 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

### B1-05-04 — UI4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/UI4-02/B1-05-04 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 109 — Literal list item: intuitive navigation.
- **B2 mapping status:** NO_DIRECT_COUNTERPART. Audit 01 relation: NOT-LOCATED in reviewed B2 clauses. Audit 01 did not locate a direct counterpart for this navigation-quality requirement in the reviewed B2 clauses. This does not establish global absence.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: an owner-approved usability/navigation rubric defines reviewable acceptance criteria.
- **Required evidence:** B1 line 109; reviewed B2 clauses; approved navigation rubric and route inventory.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** MH-09 UI; navigation matrix; accessibility and user flows.
- **Verification method:** Verify source anchor and Audit 01 classification; later independently review navigation criteria.
- **Change history:** Audit 01 atom B1-05-04; historical parent/cross-links UI4-02 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

### B1-05-05 — UI4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/UI4-02/B1-05-05 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 110 — Literal list item: minimize visual complexity.
- **B2 mapping status:** NO_DIRECT_COUNTERPART. Audit 01 relation: NOT-LOCATED in reviewed B2 clauses. Audit 01 did not locate a direct counterpart for this detail in the reviewed B2 clauses. It remains a literal B1 design requirement with no direct B2 match identified in that reviewed scope.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: an owner-approved visual complexity rubric defines measurable or reviewable criteria.
- **Required evidence:** B1 line 110; reviewed B2 clauses; accepted UX rubric/reference set.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** MH-09 UI; visual design system; navigation matrix.
- **Verification method:** Verify source anchor and Audit 01 classification; later inspect approved UX acceptance rubric.
- **Change history:** Audit 01 atom B1-05-05; historical parent/cross-links UI4-02 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

### B1-05-06 — UI4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/UI4-01/B1-05-06 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 111 — Literal list item: unified control system.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §2.3. The reviewed B2 mobile/app boundary is related but does not fully define the scope of a unified control system or all component surface exceptions.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: the accepted UI inventory defines which functions/surfaces belong to the unified control system and lists approved exceptions.
- **Required evidence:** B1 line 111; B2 §2.3; accepted UI capability/route inventory and MH-09 acceptance.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** MH-09 UI; MH-05 Smart Home; media/documents/knowledge domain interfaces.
- **Verification method:** Source comparison and independent review of the UI function/route inventory.
- **Change history:** Audit 01 atom B1-05-06; historical parent/cross-links UI4-01 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

### B1-05-07 — UI4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/UI4-03/B1-05-07 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 112 — Literal list item: UX should feel as close as possible to Apple macOS.
- **B2 mapping status:** NO_DIRECT_COUNTERPART. Audit 01 relation: NOT-LOCATED in reviewed B2 clauses. Audit 01 did not locate a direct B2 counterpart for the macOS-like UX target in the reviewed clauses. This classification does not add a new legal or visual constraint beyond B1.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: the product owner defines an interpretation/reference rubric while preserving MediaHub's distinct identity and applicable platform rules.
- **Required evidence:** B1 line 112; reviewed B2 clauses; owner decision and reviewable reference set still needed.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** MH-09 UI; visual design system; Apple platform adaptation requirements.
- **Verification method:** Verify anchor and Audit 01 NOT-LOCATED classification; later review the approved rubric.
- **Change history:** Audit 01 atom B1-05-07; historical parent/cross-links UI4-03 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

### B1-05-08 — UI4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/UI4-03/B1-05-08 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 113 — Literal list item: a distinct MediaHub visual identity.
- **B2 mapping status:** NO_DIRECT_COUNTERPART. Audit 01 relation: NOT-LOCATED in reviewed B2 clauses. Audit 01 did not locate a direct counterpart for the distinct visual identity requirement in the reviewed B2 clauses.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: an approved brand/reference specification defines the distinct MediaHub identity.
- **Required evidence:** B1 line 113; reviewed B2 clauses; owner-approved visual identity/reference specification.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** MH-09 UI; visual design system; brand assets.
- **Verification method:** Verify source anchor and Audit 01 classification; independently review the approved identity reference when available.
- **Change history:** Audit 01 atom B1-05-08; historical parent/cross-links UI4-03 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

### B1-05-09 — UI4-04

- **Requirement ID (provisional; stable child ID not minted):** HOLD/UI4-04/CROSS-LINK-ONLY — no stable Requirement ID minted
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 114 — Literal B1 wording exists: technical complexity is hidden behind a unified interface. However the historical UI4-04 record remains HOLD / CROSS-LINK-ONLY because Proposal 02 places this wording under UI4-02.f and no unique residual obligation has been approved for a separate UI4-04 requirement.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §§2–3; owner-directed duplicate/uniqueness hold. Do not assign a separate normative atom/child ID to UI4-04. Cross-link the historical UI4-04 record to UI4-02.f and keep the potential presentation/authority-boundary control distinct only if later approved as a derived control.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** HOLD — not an acceptance criterion for a new requirement. Required next decision is evidence of a unique non-duplicative residual requirement; until then, retain cross-link-only.
- **Required evidence:** B1 line 114; Proposal 02 §6.1 and §6.2; Product Owner Decision Record D-02; evidence of uniqueness is currently absent.
- **Lifecycle status:** HOLD / CROSS-LINK-ONLY
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** UI4-02.f; UI4-01; MH-09 UI; authority/read-model/command contracts only if a derived control is separately approved.
- **Verification method:** Check literal anchor, cross-link/overlap register and explicit D-02 hold. Do not mint a stable child ID or claim unique requirement.
- **Change history:** Audit 01 atom B1-05-09; historical parent/cross-links UI4-04 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

### B1-05-10 — UI4-01 / HA4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/UI4-01 / HA4-04/B1-05-10 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §5 line 116 — The user must not switch among fragmented component interfaces.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §2.3. Proposal 02 assigns line 116 to UI4-01 as a cross-link supporting the unified visual environment, not to a separate new normative copy. B2 §2.3 is only partial coverage in Audit 01.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f; Proposal 02 @ docs/mediahub-chat-tree-map-20261012 SHA 7e737c8add9e3453062e9fc459790e7010e55689. No accepted MH-09 domain contract is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: an accepted UI route/surface inventory identifies where the unified MediaHub interface is used and lists explicit exceptions.
- **Required evidence:** B1 line 116; B2 §2.3; Proposal 02 overlap register; accepted MH-09 UI surface/route evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; D-02 explicitly holds UI4-04 until uniqueness is evidenced; schema/status vocabulary approved, not this mapping.
- **Dependencies:** UI4-01; HA4-04; MH-09 UI; MH-05 Smart Home.
- **Verification method:** Compare literal source and overlap register; review the accepted interface inventory when available.
- **Change history:** Audit 01 atom B1-05-10; historical parent/cross-links UI4-01 / HA4-04 preserved. Proposal 02 §6.1/§6.2 used for source ownership/overlap. No stable child ID minted; no canonical backlog promotion.

## 4. Next review gates

- [ ] Verify each source anchor against B1 SHA and Audit 01 classification.
- [ ] Review whether B2 §2.3 has any directly applicable UI-specific requirements beyond the current partial mapping.
- [ ] Preserve no-direct-counterpart scope narrowly; do not infer global absence.
- [ ] Keep UI4-04 on HOLD unless unique residual evidence and an explicit owner decision permit a distinct requirement.
- [ ] Do not create stable child IDs until a full repository/current-branch collision review.
- [ ] Do not update the canonical backlog or main traceability matrix from this draft.

## 5. Non-actions

B1, B2, main, the historical backlog, parent-level crosswalk and prior Batch-01/02 artifacts were not modified by this draft. No tests, qualification, installation, deployment, infrastructure/live-host operation or merge was performed.
