# MH-24 Batch 04 — Atom-Level Crosswalk Batch 05 (B1 §12 Smart Home Automation)

- Date: 2026-10-12
- Branch: `docs/mediahub-chat-tree-map-20261012`
- Status: **DOCUMENTARY DRAFT / OPEN — NOT APPROVED; NOT A CANONICAL BACKLOG**
- Scope: 19 literal-source traceability rows (B1-12-01…B1-12-19) plus one derived control (B1-12-D01), using existing Audit 01 row IDs.
- B1: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` @ `main`, SHA `9df4892ed0734050ac79732603d15bb414717310`.
- B2: `docs/checkpoints/mediahub-functional-baseline-2.0.md` @ `main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Audit 01 SHA `d0938f14ed4110545118f075175dee3be412097b`; Proposal 02 SHA `7e737c8add9e3453062e9fc459790e7010e55689`; parent-level crosswalk SHA `f9e66b7adde7afeaf6a7fb6ef1a867dee07c1b34`; Product Owner Decision Record SHA `9117098e22c26708d48ca8ba5954669faa209d68`.

## 1. Mapping interpretation and overlap rules

- Use only the approved mapping statuses `MAPPED`, `CONFLICT`, `NO_DIRECT_COUNTERPART`, and `NOT_REVIEWED`.
- Explicit relation → `MAPPED` means only explicit documentary coverage. It does not mean implementation, testing, qualification or production readiness.
- Partial or derived relation → `NOT_REVIEWED`; the approved vocabulary has no `PARTIAL` status.
- Audit 01 marks the energy/security automation rows as `NOT-LOCATED` in the reviewed B2 clauses. They use `NO_DIRECT_COUNTERPART` only within that reviewed scope, not as a global statement that no related project document exists.
- **AUTO4-02 stays a historical cross-link to AUTO4-01.j/.k**, not a second normative copy of energy/security categories. Both Audit 01 atom IDs are retained; no historical source is rewritten.
- B1 line 204 is one literal comma-separated list. B1 line 206 is one compound paragraph/sentence group containing AI assistance, non-authority and controlled mechanisms. The atom rows are traceability subdivisions, not added literal source sentences.
- B1-12-D01 remains separately D-coded and unapproved; it is not a verbatim source requirement.
- No stable child IDs are minted. Owner approval covers schema/status vocabulary only, not these mappings or proposed criteria.

## 2. Batch summary

| Metric | Result |
|---|---:|
| Audit 01 source/control rows | 20 |
| Draft atom rows | 20 |
| Literal-source traceability rows | 19 |
| Derived-control rows | 1 |
| MAPPED | 1 |
| NOT_REVIEWED | 17 |
| NO_DIRECT_COUNTERPART | 2 |
| CONFLICT | 0 |
| Final child IDs minted | 0 |
| Runtime tests / qualification / deployment | Not run |

## 3. Atom-level records — 12 fields each

### B1-12-01 — AUTO4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-01/B1-12-01 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support automations.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 sets Smart Home authority/lifecycle but does not fully define the automation object model and semantics.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: accepted automation contract identifies lifecycle, owner, state transitions, authorization and unsupported outcomes.
- **Required evidence:** Automation schema/lifecycle contract and later conformance evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-05 Smart Home; MH-06 runtime; MH-17 device protocols.
- **Verification method:** Compare B1 literal list item with B2 §14; review the accepted automation contract when available.
- **Change history:** Audit 01 atom B1-12-01; historical parent/cross-link AUTO4-01 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. One item in the single literal list at B1 line 204; not a separate source sentence.

### B1-12-02 — AUTO4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-01/B1-12-02 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support scenarios.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not distinguish scenario, scene and automation semantics.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: the domain contract defines how scenarios relate to scenes/automations, including identity and lifecycle.
- **Required evidence:** Scenario/scene/automation vocabulary and accepted behavior matrix.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-05; MH-06; MH-17.
- **Verification method:** Source comparison and independent semantic review of scenario definitions.
- **Change history:** Audit 01 atom B1-12-02; historical parent/cross-link AUTO4-01 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. One item in the single literal list at B1 line 204.

### B1-12-03 — AUTO4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-01/B1-12-03 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support scenes.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 gives HA Core operational authority but does not detail scene schema, versioning or activation behavior.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: scene identity, contents, version/lifecycle and execution authority are defined.
- **Required evidence:** Scene contract and accepted HA ownership/command-path specification.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-05; MH-17; MH-03 authority boundary.
- **Verification method:** Source comparison; review scene contract when accepted.
- **Change history:** Audit 01 atom B1-12-03; historical parent/cross-link AUTO4-01 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. One item in the single literal list at B1 line 204.

### B1-12-04 — AUTO4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-01/B1-12-04 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support triggers.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not fully specify trigger source, ordering, duplication, debounce or retry semantics.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: trigger evaluation, event source, de-duplication and failure semantics are versioned and explicit.
- **Required evidence:** Trigger/event schema and retry/ordering contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-05; MH-06; MH-11 observability; MH-17.
- **Verification method:** Source comparison and trigger/event contract review.
- **Change history:** Audit 01 atom B1-12-04; historical parent/cross-link AUTO4-01 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. One item in the single literal list at B1 line 204.

### B1-12-05 — AUTO4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-01/B1-12-05 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support conditions.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 does not detail condition evaluation, unknown values or error handling.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: condition results define true/false/unknown/error semantics and their impact on execution.
- **Required evidence:** Condition-evaluation contract and negative/unknown-case criteria.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-05; MH-06; MH-07 policy.
- **Verification method:** Source comparison and review of condition semantics.
- **Change history:** Audit 01 atom B1-12-05; historical parent/cross-link AUTO4-01 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. One item in the single literal list at B1 line 204.

### B1-12-06 — AUTO4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-01/B1-12-06 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support actions.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 establishes authority boundaries but not each action’s permission, execution and uncertain-outcome model.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: actions declare capability/permissions and explicit allow/deny/unknown outcomes through the approved authority path.
- **Required evidence:** Action command contract and authorization policy/evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-03; MH-04; MH-05; MH-07; MH-17.
- **Verification method:** Source comparison and action-contract review; no action executed.
- **Change history:** Audit 01 atom B1-12-06; historical parent/cross-link AUTO4-01 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. One item in the single literal list at B1 line 204.

### B1-12-07 — AUTO4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-01/B1-12-07 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support schedules.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not define schedule timezone, recurrence, missed-run or clock-change behavior.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: schedule semantics explicitly define timezone, recurrence, missed runs and duplicate suppression.
- **Required evidence:** Schedule contract and clock/timezone acceptance cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-05; MH-06; MH-17.
- **Verification method:** Source comparison and schedule-contract review.
- **Change history:** Audit 01 atom B1-12-07; historical parent/cross-link AUTO4-01 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. One item in the single literal list at B1 line 204.

### B1-12-08 — AUTO4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-01/B1-12-08 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support events.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 does not specify event source/schema, ordering or retention for automation events.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: event schema, source identity, delivery assumptions and retention boundaries are explicit.
- **Required evidence:** Event contract, provenance and retention decision.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-05; MH-06; MH-11; MH-13 privacy.
- **Verification method:** Source comparison and event-contract review.
- **Change history:** Audit 01 atom B1-12-08; historical parent/cross-link AUTO4-01 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. One item in the single literal list at B1 line 204.

### B1-12-09 — AUTO4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-01/B1-12-09 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support presence workflows.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not specify presence sources, confidence, stale/unknown states or privacy constraints.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: presence-source provenance, confidence/freshness and privacy/retention semantics are specified.
- **Required evidence:** Presence-source and confidence contract; privacy classification.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-05; MH-13 privacy; MH-17 devices.
- **Verification method:** Source comparison and privacy/state semantics review.
- **Change history:** Audit 01 atom B1-12-09; historical parent/cross-link AUTO4-01 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. One item in the single literal list at B1 line 204.

### B1-12-10 — AUTO4-02 ↔ AUTO4-01.j

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-02 ↔ AUTO4-01.j/B1-12-10 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support energy automation; traceability cross-link to AUTO4-01.j.
- **B2 mapping status:** NO_DIRECT_COUNTERPART. Audit 01 relation: NOT-LOCATED in reviewed B2 clauses. Audit 01 did not locate a direct counterpart for the explicit energy-automation category in the reviewed B2 clauses. This scope does not prove absence from all project documents.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: owner decides required energy-automation categories; define domain/safety/consent boundaries without creating a duplicate category beside AUTO4-01.j.
- **Required evidence:** Owner/domain scope decision and capability matrix; safety criteria as applicable.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** AUTO4-01.j; MH-04; MH-05; MH-17.
- **Verification method:** Verify B1 anchor and Audit 01 classification; review scope decision. Do not duplicate normative category.
- **Change history:** Audit 01 atom B1-12-10; historical parent/cross-link AUTO4-02 ↔ AUTO4-01.j preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Historical AUTO4-02 is retained as cross-link, not a second copy of the literal category.

### B1-12-11 — AUTO4-02 ↔ AUTO4-01.k

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-02 ↔ AUTO4-01.k/B1-12-11 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 204 — LITERAL: support security automation; traceability cross-link to AUTO4-01.k.
- **B2 mapping status:** NO_DIRECT_COUNTERPART. Audit 01 relation: NOT-LOCATED in reviewed B2 clauses. Audit 01 did not locate a direct counterpart for the explicit security-automation category in the reviewed B2 clauses. This scope does not prove global absence.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: define supported security-automation classes, authorization and fail-safe behavior with explicit safety boundaries.
- **Required evidence:** Owner/domain scope decision, safety class matrix and fail-safe acceptance criteria.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** AUTO4-01.k; MH-04 security; MH-05; MH-12; MH-17.
- **Verification method:** Verify anchor and Audit 01 classification; review owner-approved scope/safety decision.
- **Change history:** Audit 01 atom B1-12-11; historical parent/cross-link AUTO4-02 ↔ AUTO4-01.k preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Historical AUTO4-02 is retained as cross-link, not a second copy of the literal category.

### B1-12-12 — AUTO4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-03/B1-12-12 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 206 — LITERAL: AI may help create automations.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §§14/18. B2 §18 permits AI assistance within policy and §14 gives the domain authority, but the automation-proposal schema/review flow is not fully specified.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: AI outputs a proposal with scope, affected primitives, rationale and validation result; execution remains separately authorized.
- **Required evidence:** Proposal schema, preview/reject flow and authority-path evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-03; MH-04; MH-05; MH-10; MH-17.
- **Verification method:** Compare B1 line 206 with B2 §§14/18; review accepted AI proposal/command contract.
- **Change history:** Audit 01 atom B1-12-12; historical parent/cross-link AUTO4-03 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Traceability subdivision of one compound B1 paragraph, not a separate source sentence.

### B1-12-13 — AUTO4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-03/B1-12-13 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 206 — LITERAL: AI may help change automations.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §§14/18. B2 §18 allows assistance but does not define change diff/preview and authorization for automation edits.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: edits expose a diff/impact preview, validation result and explicit authorized commit path.
- **Required evidence:** Change proposal/diff contract and review evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-03; MH-04; MH-05; MH-10; MH-17.
- **Verification method:** Source comparison; review proposed change workflow. No automation modified.
- **Change history:** Audit 01 atom B1-12-13; historical parent/cross-link AUTO4-03 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Traceability subdivision of one compound B1 paragraph, not a separate source sentence.

### B1-12-14 — AUTO4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-03/B1-12-14 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 206 — LITERAL: AI may explain automation operation.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §18. B2 §18 covers explanation at a broad level, but source provenance/uncertainty and access filtering are not fully specified for automation explanations.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: explanations distinguish observed state, inferred causes and unknowns, with access-filtered sources where relevant.
- **Required evidence:** Explanation provenance/uncertainty contract and access-control review.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-05; MH-10; MH-11; MH-13.
- **Verification method:** Source comparison and explanation-contract review.
- **Change history:** Audit 01 atom B1-12-14; historical parent/cross-link AUTO4-03 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Traceability subdivision of one compound B1 paragraph.

### B1-12-15 — AUTO4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-03/B1-12-15 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 206 — LITERAL: AI may create instructions.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §18. B2 §18 permits artifact creation within policy but does not detail instructions’ scope, source quality or safe-use boundary.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: instructions carry source/provenance and do not claim unverified behavior as fact.
- **Required evidence:** Instruction artifact schema and source-quality rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-10; MH-11; MH-13; relevant device/domain owners.
- **Verification method:** Source comparison; review accepted instruction/provenance schema.
- **Change history:** Audit 01 atom B1-12-15; historical parent/cross-link AUTO4-03 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Traceability subdivision of one compound B1 paragraph.

### B1-12-16 — AUTO4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-03/B1-12-16 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 206 — LITERAL: AI may add devices.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §§14/18. B2 §14 defines a qualified device lifecycle; AI-assisted onboarding proposal and permission path are not fully defined by the cited clauses.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: AI can propose onboarding only through discovery→identity→trust→capability→authorization and the accepted user/policy gate.
- **Required evidence:** Device onboarding contract and authorized proposal/command-path evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-03; MH-04; MH-05; MH-10; MH-17.
- **Verification method:** Compare with B2 §14 lifecycle; review the accepted onboarding and AI control-path contract.
- **Change history:** Audit 01 atom B1-12-16; historical parent/cross-link AUTO4-03 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Traceability subdivision of one compound B1 paragraph.

### B1-12-17 — AUTO4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-04/B1-12-17 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 206 — LITERAL: AI does not receive independent authority.
- **B2 mapping status:** MAPPED. Audit 01 relation: EXPLICIT, B2 §§3/14/18. B2 §§3/14/18 expressly preserve canonical platform authority and Smart Home boundaries and deny AI physical/canonical authority or security bypass. This is documentary mapping only.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: no AI component has independent authority to commit canonical platform or Smart Home state outside the authoritative controlled paths.
- **Required evidence:** B2 §§3/14/18 plus accepted tool/API authority-boundary contract; eventual bypass-negative evidence requires separate authorization.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-03 State Authority; MH-04 security; MH-05 Smart Home; MH-10 AI; MH-12 security analysis.
- **Verification method:** Check exact B1 anchor and B2 clauses; review authority boundary; runtime bypass tests are not performed here.
- **Change history:** Audit 01 atom B1-12-17; historical parent/cross-link AUTO4-04 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Only this atom receives MAPPED because Audit 01 marks the B2 relation EXPLICIT; no implementation/qualification is implied.

### B1-12-18 — AUTO4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-05/B1-12-18 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 206 — LITERAL: all changes pass through controlled MediaHub mechanisms.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 provides domain lifecycle/authority but the exact command path, mediation points and outcomes are not fully specified in the cited clause.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: all AI-initiated changes traverse a versioned MediaHub-controlled command path with explicit identity, policy decision and result semantics.
- **Required evidence:** Accepted MediaHub command/API contract and later path-trace evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-03; MH-04; MH-05; MH-06; MH-10.
- **Verification method:** Source comparison and accepted command-path contract review; no command was issued.
- **Change history:** Audit 01 atom B1-12-18; historical parent/cross-link AUTO4-05 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Traceability subdivision of one compound B1 paragraph.

### B1-12-19 — AUTO4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-05/B1-12-19 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 206 — LITERAL: all changes pass through controlled Home Assistant mechanisms.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 says AI/external ecosystems do not bypass HA Core, but the full HA command route and interaction with the MediaHub Smart Home layer remain OPEN.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: consequential Smart Home changes traverse the accepted MediaHub/HA route and preserve HA Core’s operational authority.
- **Required evidence:** Accepted HA command-path and cross-domain authority contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-03; MH-04; MH-05; MH-10; MH-17.
- **Verification method:** Compare source with B2 §14; review command route/authority contract; no action executed.
- **Change history:** Audit 01 atom B1-12-19; historical parent/cross-link AUTO4-05 preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Traceability subdivision of one compound B1 paragraph.

### B1-12-D01 — AUTO4-05 (derived cross-link)

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/AUTO4-05 (derived cross-link)/B1-12-D01 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §12 line 206 — DERIVED CONTROL: require a separately verifiable auditable result for each change.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: DERIVED, Audit 01 D01. Audit 01 explicitly says B1’s controlled-mechanisms wording does not itself require an audit-result schema. This is a derived acceptance control, not literal B1 wording.
- **Canonical contract path/ref:** B1 @ main SHA 9df4892ed0734050ac79732603d15bb414717310; B2 @ main SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §§14/18; related contract not accepted/identified for this atom.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: define result/evidence schema (decision, actor, outcome, provenance and correlation) only after explicit owner/governance approval.
- **Required evidence:** Owner-approved derived-control decision, audit schema, retention/data classification and later authorized evidence.
- **Lifecycle status:** DRAFT / DERIVED CONTROL / OWNER APPROVAL OPEN
- **Reviewer / approval reference:** Product Owner Decision Record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approves 12-field schema and status vocabulary only, not this mapping or acceptance criteria.
- **Dependencies:** MH-03; MH-11 observability; MH-12 security; MH-13 privacy; MH-22 qualification gates.
- **Verification method:** Verify literal/derived distinction against Audit 01; obtain owner decision before adding to canonical requirements. No runtime test performed.
- **Change history:** Audit 01 atom B1-12-D01; historical parent/cross-link AUTO4-05 (derived cross-link) preserved; Proposal 02 §6.1/§6.2 consulted. No final child ID minted. Preserve D-coded identity and link to AUTO4-05; do not count as an extra literal B1 requirement.

## 4. Review gates

- [ ] Re-fetch B1/B2/Audit 01/Proposal 02/owner decision at the pinned refs before review.
- [ ] Compare all 20 IDs with the Audit 01 §12 register.
- [ ] Verify literal anchors at B1 lines 204 and 206 and confirm row source text is not inventing extra source sentences.
- [ ] Confirm statuses from Audit 01 relation, including the explicit-only MAPPED row and two reviewed-scope NO_DIRECT_COUNTERPART rows.
- [ ] Preserve AUTO4-02 as cross-link only; do not duplicate AUTO4-01.j/.k.
- [ ] Keep B1-12-D01 derived and separate unless owner/governance explicitly accepts it.
- [ ] Do not mint final child IDs or update the canonical backlog/main matrix before complete collision review and independent owner/governance acceptance.

## 5. Non-actions

B1, B2, `main`, the historical backlog, parent-level crosswalk and previous atom batches were not modified. No tests, qualification, installation, deployment, infrastructure/live-host operation or merge was performed.
