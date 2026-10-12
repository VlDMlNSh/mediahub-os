# MH-24 Batch 04 — Atom-Level Crosswalk Batch 06 (B1 §15 Local AI)

- **Date:** 2026-10-12
- **Branch:** `docs/mediahub-chat-tree-map-20261012`
- **Status:** **DOCUMENTARY DRAFT / OPEN — NOT APPROVED; NOT A CANONICAL BACKLOG**
- **Scope:** all 18 Audit 01 §15 labels: 16 literal-source traceability rows and two D-coded derived controls.
- **B1 source:** `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` @ `main`, blob SHA `9df4892ed0734050ac79732603d15bb414717310`, §15 lines 232, 235–249.
- **B2 reference:** `docs/checkpoints/mediahub-functional-baseline-2.0.md` @ `main`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §§2.1, 3, 5–7, 14–18.
- **Audit source:** `docs/checkpoints/MH24-B1-SECTIONS-03-06-12-15-17-CLAUSE-COVERAGE-AUDIT-01.md` @ `docs/mediahub-chat-tree-map-20261012`, blob SHA `d0938f14ed4110545118f075175dee3be412097b`.
- **Normalization proposal:** `docs/checkpoints/MH24-BATCH-04-NORMALIZATION-PROPOSAL-02.md` @ `docs/mediahub-chat-tree-map-20261012`, blob SHA `7e737c8add9e3453062e9fc459790e7010e55689`.
- **Field schema:** 1. Requirement ID; 2. Owner; 3. Source atom/classification; 4. B2 mapping status; 5. Canonical contract path/ref; 6. Acceptance criteria; 7. Required evidence; 8. Lifecycle status; 9. Reviewer/approval reference; 10. Dependencies; 11. Verification method; 12. Change history.
- **Owner decision:** Product Owner Decision Record SHA `9117098e22c26708d48ca8ba5954669faa209d68`; schema/status vocabulary only.

## 1. Scope and source interpretation

B1 §15 defines Local AI execution placement (line 232), enumerated capabilities (lines 235–247), and an advisory/proposal-producing non-authority rule (line 249). Per-capability records are traceability subdivisions, not additional B1 sentences. The umbrella phrase “local intelligent processing” overlaps enumerated capabilities and needs an owner decision before any distinct canonical requirement is created.

The approved mapping vocabulary is `MAPPED`, `CONFLICT`, `NO_DIRECT_COUNTERPART`, `NOT_REVIEWED`. Explicit documentary coverage maps to `MAPPED`; partial and derived relationships remain `NOT_REVIEWED`. Mapping does not imply implementation, tests, qualification or production readiness. No semantic `CONFLICT` is asserted here.

**Confirmed cross-reference defect:** Audit 01 atom `B1-15-13` links document assistance to B2 §19. Directly fetched B2 defines §16 as “Documents and Knowledge” and §19 as “Update / Recovery / Migration”. The correct B2 review target for this atom is §§16/18. This is a citation/traceability defect in Audit 01, not a B1↔B2 semantic conflict. Audit 01 remains unchanged; this working batch records the corrected B2 pointer and preserves its historical source.

## 2. Batch summary

| Metric | Count |
|---|---:|
| Audit 01 §15 labels | 18 |
| Literal-source traceability rows | 16 |
| Derived-control rows | 2 |
| MAPPED | 2 |
| NOT_REVIEWED | 16 |
| NO_DIRECT_COUNTERPART | 0 |
| CONFLICT | 0 |
| Stable child IDs minted | 0 |
| Runtime tests / qualification / deployment | Not run |

## 3. Atom-level records — 12 approved fields per record

### B1-15-01 — LAI4-01

- **Requirement ID:** `PROVISIONAL/LAI4-01/B1-15-01` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 232 — LITERAL: Local AI runs directly in MediaHub Core / the local system.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §§2.1/18. B2 names a Local AI tier and local-user domain but does not pin the exact locality, offline behavior or runtime placement.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define local execution boundary, data paths and behavior when cloud/network is unavailable.
- **Required evidence:** Approved locality profile, data-flow map and offline-mode acceptance cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-02; MH-06; MH-10; MH-13; MH-21.
- **Verification method:** Compare B1 line 232 with B2 §§2.1/18 and the future accepted local-AI contract.
- **Change history:** Audit 01 B1-15-01 / LAI4-01 preserved; no stable child ID.

### B1-15-02 — LAI4-02

- **Requirement ID:** `PROVISIONAL/LAI4-02/B1-15-02` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 235 — LITERAL: Provide local inference.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §18. B2 names Local AI but does not state a complete supported-model/runtime/resource matrix.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define target model families, runtime interfaces, memory/latency budgets and offline behavior per hardware profile.
- **Required evidence:** Pinned runtime/model matrix, per-profile measurements and model qualification evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-06; MH-10; MH-15; MH-21; MH-22.
- **Verification method:** Compare B1 line 235 with B2 §18 and exact-version platform support.
- **Change history:** Audit 01 B1-15-02 / LAI4-02 preserved; candidates remain non-selected absent evidence.

### B1-15-03 — LAI4-02

- **Requirement ID:** `PROVISIONAL/LAI4-02/B1-15-03` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 236 — LITERAL: Provide natural-language interaction.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §18. Supported modalities/languages and interaction-level failure semantics are not defined in the reviewed clause.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define supported modalities/languages, explicit capability profile and behavior on low-confidence or unsupported inputs.
- **Required evidence:** Interface contract, locale/modality matrix and uncertainty/unsupported-input cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-09; MH-10; MH-06; MH-13.
- **Verification method:** Compare B1 line 236 with B2 §18 and future UI/API acceptance criteria.
- **Change history:** Audit 01 B1-15-03 / LAI4-02 preserved.

### B1-15-04 — LAI4-03

- **Requirement ID:** `PROVISIONAL/LAI4-03/B1-15-04` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 237 — LITERAL: Provide analysis.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §18. B2 permits analysis within policy but does not define workload scope, source provenance or correctness criteria.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define analysis classes, inputs, source provenance, uncertainty and boundaries against authoritative facts.
- **Required evidence:** Versioned analysis contract, provenance schema and unknown/stale-data cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-10; MH-11; MH-19; MH-13.
- **Verification method:** Compare B1 line 237 with B2 §18 and future analysis contract.
- **Change history:** Audit 01 B1-15-04 / LAI4-03 preserved; umbrella remains underspecified.

### B1-15-05 — LAI4-03

- **Requirement ID:** `PROVISIONAL/LAI4-03/B1-15-05` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 238 — LITERAL: Provide user assistance.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §18. B2 permits AI assistance but does not fully define supported workflows, user-safety limits or escalation boundaries.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define allowed assistance classes and distinguish advice, proposal, executable command and committed result.
- **Required evidence:** Assistance catalogue, role/policy matrix, uncertainty and denial cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-09; MH-10; MH-12; MH-13.
- **Verification method:** Compare B1 line 238 with B2 §18 and accepted product/UI policy.
- **Change history:** Audit 01 B1-15-05 / LAI4-03 preserved.

### B1-15-06 — LAI4-04

- **Requirement ID:** `PROVISIONAL/LAI4-04/B1-15-06` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 239 — LITERAL: Assist the user in creating automations.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §§14/18. B2 defines Smart Home and AI authority boundaries but not a complete automation proposal contract.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: AI output is a proposal; owning domain validates it and policy authorizes effects.
- **Required evidence:** Proposal schema, approval/denial path, non-bypass evidence and negative direct-mutation cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-05; MH-10; MH-17; MH-03.
- **Verification method:** Compare B1 line 239 with B2 §§14/18 and future accepted automation contract.
- **Change history:** Audit 01 B1-15-06 / LAI4-04 preserved; no AI authority granted.

### B1-15-07 — LAI4-04

- **Requirement ID:** `PROVISIONAL/LAI4-04/B1-15-07` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 240 — LITERAL: Assist with equipment configuration.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §§14/18. B2 establishes authority boundaries but does not define supported configuration primitives or confirmation policy.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define configuration assistance as a bounded proposal with capability validation and owning-domain authorization.
- **Required evidence:** Schema, policy evidence, rejection/rollback cases and supported-device matrix.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-05; MH-17; MH-04; MH-10.
- **Verification method:** Compare B1 line 240 with B2 §§14/18 and device/configuration contracts.
- **Change history:** Audit 01 B1-15-07 / LAI4-04 preserved; consequential changes remain gated.

### B1-15-08 — LAI4-05

- **Requirement ID:** `PROVISIONAL/LAI4-05/B1-15-08` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 241 — LITERAL: Create instructions.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §18. AI may create artifacts within policy, but the reviewed clause does not define instruction-source quality or applicability.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Instructions identify sources, applicability/version assumptions and uncertainty; they are not authorization.
- **Required evidence:** Source-link coverage, version/applicability checks and unsupported-step examples.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-10; MH-13; MH-19.
- **Verification method:** Compare B1 line 241 with B2 §18 and future knowledge/provenance contract.
- **Change history:** Audit 01 B1-15-08 / LAI4-05 preserved.

### B1-15-09 — LAI4-05

- **Requirement ID:** `PROVISIONAL/LAI4-05/B1-15-09` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 242 — LITERAL: Provide search.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §§16/18. B2 includes search of verified sources, but corpus scope, access filtering, freshness and local index contract remain incomplete.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Search respects source permissions, data classification, freshness and provenance; retrieval does not create authority.
- **Required evidence:** Search contract, corpus/index inventory, permission-denial, freshness and provenance evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-10; MH-13; MH-19; MH-14.
- **Verification method:** Compare B1 line 242 with B2 §§16/18 and accepted search/index contract.
- **Change history:** Audit 01 B1-15-09 / LAI4-05 preserved.

### B1-15-10 — LAI4-05

- **Requirement ID:** `PROVISIONAL/LAI4-05/B1-15-10` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 243 — LITERAL: Work with data locally.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §§5/7/18. Data classes exist in B2, but this clause does not specify supported data classes, retention, locality proof or tool boundaries.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define data allowed locally, working-copy locations, logging and retention limits.
- **Required evidence:** Data-flow/locality map, data-class rules, retention policy and egress-denial evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-10; MH-13; MH-21; MH-12.
- **Verification method:** Compare B1 line 243 with B2 §§5/7/18 and verify each data class against runtime boundaries.
- **Change history:** Audit 01 B1-15-10 / LAI4-05 preserved; local does not mean unrestricted.

### B1-15-11 — LAI4-06

- **Requirement ID:** `PROVISIONAL/LAI4-06/B1-15-11` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 244 — LITERAL: Support Smart Home.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §14. B2 reserves Smart Home operational authority to HA Core and does not detail every AI-assisted workflow.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: AI may explain/propose within policy; device-state operations remain under HA Core and product policy.
- **Required evidence:** Cross-domain command/proposal contract, authority review and bypass-denial cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-05; MH-10; MH-17; MH-03.
- **Verification method:** Compare B1 line 244 with B2 §14 and accepted HA integration contract.
- **Change history:** Audit 01 B1-15-11 / LAI4-06 preserved as a cross-link, not a duplicate domain requirement.

### B1-15-12 — LAI4-06

- **Requirement ID:** `PROVISIONAL/LAI4-06/B1-15-12` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 245 — LITERAL: Manage/support the media system.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §15. B2 §15 covers media scope but not the exact AI-assisted media operation set or authorization path.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define AI-supported media operations separately from authorized execution and vendor/DRM limits.
- **Required evidence:** Media-operation contract, capability/rights matrix and denied/unsupported-operation cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-18; MH-10; MH-12; MH-21.
- **Verification method:** Compare B1 line 245 with B2 §15; cross-link §16 only if a specific data/knowledge feature is involved.
- **Change history:** Audit 01 B1-15-12 / LAI4-06 preserved; B2 §15 is the direct Media scope.

### B1-15-13 — LAI4-06

- **Requirement ID:** `PROVISIONAL/LAI4-06/B1-15-13` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 246 — LITERAL: Assist with documents.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §§16/18. Audit 01 incorrectly points this atom to B2 §19. Pinned B2 defines §16 as Documents and Knowledge and §19 as Update / Recovery / Migration. The appropriate review target is §§16/18; detailed document-AI permissions remain open.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define document access, permission filtering, retrieval provenance and labeling of derived outputs.
- **Required evidence:** Document-AI contract, data-class/permission matrix, provenance, denial cases and retention/egress evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-10; MH-13; MH-16; MH-19; MH-21.
- **Verification method:** Verify B2 section headings and compare B1 line 246; update derived working references only, preserve Audit 01.
- **Change history:** Audit 01 B1-15-13 / LAI4-06 preserved; citation defect recorded, historical Audit 01 not rewritten.

### B1-15-14 — LAI4-02 / LAI4-05

- **Requirement ID:** `PROVISIONAL/LAI4-02 / LAI4-05/B1-15-14` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 247 — LITERAL: Provide local intelligent processing.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: PARTIAL, B2 §18. This umbrella phrase overlaps enumerated features and has no separate workload boundary.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Owner defines a distinct residual scope or cross-links this phrase to enumerated capabilities; avoid duplicate normative requirements.
- **Required evidence:** Owner disposition and overlap map connecting claimed function to enumerated capabilities.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-10; MH-06; MH-13.
- **Verification method:** Compare literal line 247 with lines 235–246; determine whether unique residual behavior exists.
- **Change history:** Audit 01 B1-15-14 / LAI4-02 and LAI4-05 preserved as historical dual links.

### B1-15-15 — LAI4-07

- **Requirement ID:** `PROVISIONAL/LAI4-07/B1-15-15` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 249 — LITERAL: AI acts in an advisory / proposal-producing model.
- **B2 mapping status:** `MAPPED`; Audit 01 relation: EXPLICIT, B2 §§3/18. B2 explicitly constrains AI to policy-governed advisory/proposal/analysis capabilities and disallows direct authority bypass; this is documentary mapping only.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Proposed criterion: outputs are distinguishable from commands and committed state changes; criterion not approved.
- **Required evidence:** Output-type schema and independent negative evidence that advisory output alone does not mutate canonical state.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-03; MH-10; MH-12; MH-17.
- **Verification method:** Compare B1 line 249 with B2 §§3/18; runtime conformance requires future independent evidence.
- **Change history:** Audit 01 B1-15-15 / LAI4-07 preserved; MAPPED is not implementation/qualification.

### B1-15-16 — LAI4-07

- **Requirement ID:** `PROVISIONAL/LAI4-07/B1-15-16` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 249 — LITERAL: AI is not State Authority.
- **B2 mapping status:** `MAPPED`; Audit 01 relation: EXPLICIT, B2 §§3/18. B2 explicitly states AI cannot obtain canonical state authority or security bypass; this is documentary mapping only.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Proposed criterion: AI/provider/tools cannot directly mutate canonical state except through an owning authority’s authorized path; criterion not approved.
- **Required evidence:** Authority-boundary contract and independent negative tests against direct/indirect bypass.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-03; MH-10; MH-12; MH-17; MH-21.
- **Verification method:** Compare B1 line 249 with B2 §§3/18; require independent runtime evidence later.
- **Change history:** Audit 01 B1-15-16 / LAI4-07 preserved; no operational state inferred.

### B1-15-D01 — LAI4-01 / LAI4-05

- **Requirement ID:** `PROVISIONAL/LAI4-01 / LAI4-05/B1-15-D01` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 232 — DERIVED CONTROL: Local AI must obey specified data-boundary and retention rules.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: DERIVED from B2 §§5/7/18 and privacy contracts; not a separate literal B1 §15 atom. This is a privacy/security derivation, not verbatim B1 wording; no approval is evidenced.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: If adopted, each workload declares data class, local/remote boundary, retention and allowed egress before execution.
- **Required evidence:** Approved data-flow/retention policy and evidence for forbidden data movement, logging and cache persistence.
- **Lifecycle status:** DERIVED / OPEN / NOT APPROVED.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-12; MH-13; MH-21; MH-10.
- **Verification method:** Review derivation against B2 §§5/7/18 and accepted privacy/security contracts; require owner decision.
- **Change history:** Audit 01 B1-15-D01 preserved as derived, not a literal atom.

### B1-15-D02 — LAI4-03

- **Requirement ID:** `PROVISIONAL/LAI4-03/B1-15-D02` (traceability label only; not a final stable child ID).
- **Owner:** TBD; domain implementation owner is not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §15 line 249 — DERIVED CONTROL: AI outputs should express uncertainty/provenance rather than be treated as canonical fact.
- **B2 mapping status:** `NOT_REVIEWED`; Audit 01 relation: DERIVED control linked to B2 §§3/16/18; not a distinct literal B1 §15 requirement. B1 gives advisory/non-authority principles but does not spell out a complete uncertainty schema.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. No accepted detailed Local AI implementation contract is asserted; B1-15-13 uses corrected working review target §§16/18 while preserving Audit 01’s historical §19 pointer.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: If adopted, outputs identify evidence/freshness and distinguish observation, inference, proposal and authoritative fact.
- **Required evidence:** Output schema, source-attribution checks, unknown-state examples and independent review.
- **Lifecycle status:** DERIVED / OPEN / NOT APPROVED.
- **Reviewer / approval reference:** Product Owner Decision Record @ `docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`; this approves the 12-field schema and mapping vocabulary only, not this crosswalk or its acceptance criteria.
- **Dependencies:** MH-10; MH-11; MH-13; MH-19.
- **Verification method:** Review derivation against B1 line 249, B2 §§3/16/18; do not call it verbatim source.
- **Change history:** Audit 01 B1-15-D02 preserved as derived, not literal.

## 4. Required independent review

1. Verify the 18 identifiers match Audit 01 §15: B1-15-01…B1-15-16 and B1-15-D01…D02.
2. Verify every record has all 12 approved fields in the approved order.
3. Check source anchors against B1 `main` SHA `9df4892ed0734050ac79732603d15bb414717310`, especially lines 232, 235–247 and 249; B1 is not to be rewritten.
4. Check B2 section numbers at the pinned SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`: §16 is Documents and Knowledge; §18 is AI architecture; §19 is Update/Recovery/Migration.
5. Confirm distribution `2 MAPPED / 16 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT`.
6. Confirm B1-15-13’s B2 §19 pointer mismatch remains documented and Audit 01 remains unchanged.
7. Confirm D01/D02 are labelled derived, not literal B1 requirements.
8. Preserve historical LAI4 parents and IDs; do not mint final child IDs.
9. Keep architecture, implementation, verification, qualification, release and production separate.
10. Do not update canonical backlog, main traceability matrix, B1/B2 or `main` from this draft.

## 5. Non-actions and disposition

This is a source-anchored documentary draft. It is not approval or a canonical backlog. No software was installed; no tests, qualification, soak, infrastructure/live-host operation, deployment or merge to `main` was executed.

**Disposition: OPEN / NOT APPROVED / REVIEW REQUIRED.**
