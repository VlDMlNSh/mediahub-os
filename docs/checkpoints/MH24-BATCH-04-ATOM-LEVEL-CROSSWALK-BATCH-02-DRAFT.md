# MH-24 Batch 04 — Atom-Level Crosswalk Batch 02 (B1 §4 Home Assistant Core)

- Date: 2026-10-12
- Branch: `docs/mediahub-chat-tree-map-20261012`
- Status: **DOCUMENTARY DRAFT / OPEN — NOT APPROVED; NOT A CANONICAL BACKLOG**
- Scope: 19 source-atom rows from B1 §4 lines 85–98, based on existing Audit 01 IDs B1-04-01…B1-04-19. Existing Audit 01 labels are references, not final child Requirement IDs.
- B1 source: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` @ `main`, SHA `9df4892ed0734050ac79732603d15bb414717310`.
- B2 current functional reference: `docs/checkpoints/mediahub-functional-baseline-2.0.md` @ `main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Other sources: Audit 01 SHA `d0938f14ed4110545118f075175dee3be412097b`; Proposal 02 SHA `7e737c8add9e3453062e9fc459790e7010e55689`; Product Owner Decision Record SHA `9117098e22c26708d48ca8ba5954669faa209d68`.

## 1. Interpretation and constraints

- Mapping statuses use only the owner-approved values `MAPPED`, `CONFLICT`, `NO_DIRECT_COUNTERPART`, `NOT_REVIEWED`.
- Audit 01 partial or mixed `EXPLICIT/PARTIAL` relations are represented as `NOT_REVIEWED`; the approved vocabulary has no `PARTIAL` status.
- `MAPPED` is documentary explicit coverage only, not implementation, test, qualification or production evidence.
- B1 lines 87, 92 and 94 contain list/compound sentences. Splitting them into rows is a traceability operation, not a claim that each row is a separate source sentence.
- Cross-links across historical parent IDs are preserved; no final child IDs are minted. UI4-04 remains HOLD / CROSS-LINK-ONLY elsewhere.
- Acceptance criteria in these rows are proposed and not approved. The decision record approves only the field schema/status vocabulary and does not accept the crosswalk as a whole.

## 2. Batch summary

| Metric | Result |
|---|---:|
| Scope | B1 §4, lines 85–98 |
| Audit 01 atoms | 19 |
| Draft atom rows | 19 |
| MAPPED | 2 |
| NOT_REVIEWED | 17 |
| CONFLICT | 0 |
| NO_DIRECT_COUNTERPART | 0 |
| Final child Requirement IDs minted | 0 |
| Runtime tests / qualification / deployment | Not run |

## 3. Atom-level records — 12 fields each

### B1-04-01 — HA4-01 / HA4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-01 / HA4-06/B1-04-01 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 85 — LITERAL B1 SOURCE. Home Assistant Core является единым источником истины именно для домена Smart Home.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: EXPLICIT/PARTIAL, B2 §§3–4/14. B2 §3 names HA Core as Smart Home operational/device-state authority and MediaHub State Authority as platform authority; B2 §14 repeats the Smart Home authority. The source atom’s authority scope still requires one accepted authority table and detailed scope boundary.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: the authority table clearly separates HA Core operational/device state in Smart Home from platform canonical state owned by MediaHub State Authority.
- **Required evidence:** Exact B1 §4 line 85; B2 §§3–4/14; accepted authority-scope table plus interface/conflict semantics.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03 State Authority; MH-05 Smart Home; MH-17 device/protocol; MH-09 UI boundary.
- **Verification method:** Compare the exact source line and B2 authority rows; independent review of an accepted authority table. No runtime verification performed.
- **Change history:** Audit 01 atom B1-04-01; historical parent/cross-links HA4-01 / HA4-06 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Audit 01 atom preserved; historical parents HA4-01 and HA4-06 retained as cross-links; stable child ID deferred.

### B1-04-02 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-02 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: integrations. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 states the operational authority and lifecycle for Smart Home devices but does not individually specify ownership/contract semantics for integrations.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: an integration ownership row defines its lifecycle, authority, errors and relation to HA Core.
- **Required evidence:** Exact B1 §4 line 87; B2 §14; accepted Smart Home capability/ownership matrix.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-05; MH-17; MH-03 authority boundary.
- **Verification method:** Compare the literal list item and B2 §14; verify the accepted per-capability ownership row when available.
- **Change history:** Audit 01 atom B1-04-02; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-03 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-03 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: devices. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 discusses Smart Home device-state authority and duplicate-discovery ownership, but not the complete device identity/schema contract.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: each Smart Home device has a documented identity/ownership mapping to HA Core and MediaHub references.
- **Required evidence:** Exact B1 §4 line 87; B2 §14; device identity and ownership mapping.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-05; MH-17; MH-03; identity/trust contracts.
- **Verification method:** Source comparison and independent review of device identity/ownership mapping.
- **Change history:** Audit 01 atom B1-04-03; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-04 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-04 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: entities. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. The reviewed B2 clause does not separately define HA entity identifiers and their mapping to MediaHub’s domain/state model.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: HA entities have explicit identifiers, ownership semantics and a defined mapping to MediaHub representations.
- **Required evidence:** Exact B1 §4 line 87; B2 §14; entity mapping schema and ownership rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-05; MH-17; MH-03; MH-14 persistence boundary.
- **Verification method:** Source comparison and independent review of entity schema/mapping.
- **Change history:** Audit 01 atom B1-04-04; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-05 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-05 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: states. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 distinguishes Smart Home operational/device state from platform canonical state but does not fully define each HA-state-to-platform-reference boundary.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: state ownership and any platform-level references are separately defined so HA device state cannot be confused with platform canonical state.
- **Required evidence:** Exact B1 §4 line 87; B2 §§3–4/14; state semantics and mapping contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03; MH-05; MH-17; state vocabulary.
- **Verification method:** Compare source and B2 authority clauses; independent state-semantics review.
- **Change history:** Audit 01 atom B1-04-05; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-06 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-06 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: events. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not individually define event schemas, delivery, retention or ordering semantics for HA events.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: event names/payloads, delivery behavior, ordering guarantees and authority implications are documented for the integration boundary.
- **Required evidence:** Exact B1 §4 line 87; B2 §14; event/API contract and retention policy.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-05; MH-06 runtime services; MH-11 observability; MH-17.
- **Verification method:** Source comparison and review of a versioned event contract.
- **Change history:** Audit 01 atom B1-04-06; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-07 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-07 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: services. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not individually define the HA service-invocation contract or its policy/authorization boundary.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: service calls use an explicitly bounded command path with identity, policy and outcome semantics.
- **Required evidence:** Exact B1 §4 line 87; B2 §14; accepted service/API and authorization contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03; MH-04; MH-05; MH-07; MH-17.
- **Verification method:** Source comparison and service-contract review; no service was invoked.
- **Change history:** Audit 01 atom B1-04-07; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-08 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-08 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: triggers. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. The reviewed B2 clause does not define trigger semantics, ordering, duplicate delivery or recovery.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: trigger sources, conditions, de-duplication and retry behavior are explicitly specified for supported workflows.
- **Required evidence:** Exact B1 §4 line 87; B2 §14; trigger semantics and failure/recovery contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-05; MH-06; MH-17; MH-22 qualification.
- **Verification method:** Source comparison and trigger-contract review; no trigger executed.
- **Change history:** Audit 01 atom B1-04-08; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-09 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-09 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: conditions. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not define condition evaluation semantics or unknown-condition behavior.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: condition evaluation has explicit semantics for true, false and unknown/error outcomes.
- **Required evidence:** Exact B1 §4 line 87; B2 §14; condition-evaluation contract and failure cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-05; MH-06; MH-17; policy/safety semantics.
- **Verification method:** Source comparison and condition-contract review.
- **Change history:** Audit 01 atom B1-04-09; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-10 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-10 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: actions. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2’s no-bypass rule and HA operational authority do not by themselves define action admission, authorization or unknown execution outcomes.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: action execution is routed through the accepted authority/policy path with defined allow/deny/unknown result semantics.
- **Required evidence:** Exact B1 §4 line 87; B2 §§3–4/14/18; action command contract and negative-path evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03; MH-04; MH-05; MH-17.
- **Verification method:** Source comparison and action-contract review; no action executed.
- **Change history:** Audit 01 atom B1-04-10; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-11 — HA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02/B1-04-11 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: scenes. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. The reviewed B2 clause does not separately define scene schema, versioning, owner or lifecycle.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: scenes have a documented identity, ownership, version/lifecycle and authorized execution path.
- **Required evidence:** Exact B1 §4 line 87; B2 §14; accepted scene schema/lifecycle contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-05; MH-17; MH-14; MH-16.
- **Verification method:** Source comparison and scene-contract review.
- **Change history:** Audit 01 atom B1-04-11; historical parent/cross-links HA4-02 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; parent HA4-02 preserved; final child ID not minted.

### B1-04-12 — HA4-02 / HA4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-02 / HA4-05/B1-04-12 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 87 — LITERAL B1 SOURCE. List item: Smart Home automations. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 establishes HA Core operational authority and AI no-bypass, but the full automation lifecycle and AI-created change protocol are not completely specified by this clause.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: automation state and execution remain under HA Core; AI-originated changes use a controlled, auditable proposal/authorization path.
- **Required evidence:** Exact B1 §4 line 87; B2 §§14/18; accepted automation lifecycle and AI proposal/command contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03; MH-04; MH-05; MH-10; MH-17.
- **Verification method:** Source comparison and automation contract review; no automations changed.
- **Change history:** Audit 01 atom B1-04-12; historical parent/cross-links HA4-02 / HA4-05 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Literal list item split from one comma-separated source line; shared parent HA4-02/HA4-05 lineage retained; final child ID not minted.

### B1-04-13 — HA4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-03/B1-04-13 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 90 — LITERAL B1 SOURCE. Ordered chain: Physical Devices → Home Assistant Integrations → Home Assistant Core → MediaHub Smart Home Layer → MediaHub API → MediaHub UI.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 expresses the authority/lifecycle boundary but does not reproduce the full ordered six-stage path or an interface contract for each edge.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: preserve the ordered flow and define the input/output, authority, error and acknowledgement semantics for each edge.
- **Required evidence:** Exact B1 §4 line 90; B2 §14; versioned sequence/edge contracts.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03; MH-05; MH-09; MH-17; API contracts.
- **Verification method:** Compare literal chain and B2 §14; independently review every edge contract.
- **Change history:** Audit 01 atom B1-04-13; historical parent/cross-links HA4-03 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Source line split into edge-level traceability only; these are not additional B1 sentences; parent HA4-03 preserved; final child ID not minted.

### B1-04-14 — HA4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-04/B1-04-14 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 92 — LITERAL B1 SOURCE. Home Assistant Core’s standard visual interface is not the MediaHub user interface. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §2.3. The reviewed B2 user/mobile surface description is not a full component-UI exclusion contract; the exact HA UI/MediaHub UI boundary remains partial.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: MediaHub’s accepted UI boundary identifies where the HA standard UI may appear, if anywhere, without treating it as the MediaHub UI.
- **Required evidence:** Exact B1 §4 line 92; B2 §2.3; accepted MH-09/UI boundary and surface/route inventory.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-09; MH-05; MH-17; UI/navigation contract.
- **Verification method:** Source comparison and independent UI boundary/route review; no UI tested.
- **Change history:** Audit 01 atom B1-04-14; historical parent/cross-links HA4-04 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. One of two traceability atoms from the compound B1 line 92; parent HA4-04 preserved; final child ID not minted.

### B1-04-15 — HA4-04 / UI4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-04 / UI4-01/B1-04-15 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 92 — LITERAL B1 SOURCE. The user interacts with Smart Home through the unified MediaHub UI. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §2.3. B2 §2.3 is related but does not provide the complete route/surface inventory proving all Smart Home interactions use the unified MediaHub UI.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: the accepted UI surface/route inventory identifies the MediaHub UI as the user-facing Smart Home interaction surface and documents exceptions.
- **Required evidence:** Exact B1 §4 line 92; B2 §2.3; accepted UI surface/route inventory and MH-09 acceptance.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-09; MH-05; MH-17; UI/navigation contract.
- **Verification method:** Source comparison and independent route/surface review; no UI tested.
- **Change history:** Audit 01 atom B1-04-15; historical parent/cross-links HA4-04 / UI4-01 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. One of two traceability atoms from the compound B1 line 92; cross-link UI4-01 preserved to avoid duplicate normative copies; final child ID not minted.

### B1-04-16 — HA4-05 / AUTO4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-05 / AUTO4-04/B1-04-16 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 94 — LITERAL B1 SOURCE. AI must not bypass Home Assistant Core when creating automations. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** MAPPED. Audit 01 relation: EXPLICIT, B2 §§14/18. B2 §14 states that AI and external ecosystems do not bypass HA Core; §18 carries the AI authority/no-bypass boundary.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: the documented AI automation command path does not bypass HA Core. This is documentary coverage only; implementation conformance remains open.
- **Required evidence:** Exact B1 §4 line 94; B2 §§14/18; future command-path and bypass-negative evidence under separate authorization.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03; MH-04; MH-05; MH-10; MH-17.
- **Verification method:** Compare literal source to B2 §§14/18; independent review of command-path contract; no runtime tests performed.
- **Change history:** Audit 01 atom B1-04-16; historical parent/cross-links HA4-05 / AUTO4-04 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Traceability subdivision of one B1 sentence and linked to AUTO4-04; parent IDs preserved; final child ID not minted.

### B1-04-17 — HA4-05 / AUTO4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-05 / AUTO4-04/B1-04-17 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 94 — LITERAL B1 SOURCE. AI must not bypass MediaHub Smart Home Layer when creating automations. Traceability subdivision of a shared list/compound sentence, not an additional literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: EXPLICIT/PARTIAL, B2 §§14/18. The B2 no-bypass rule explicitly names HA Core but does not fully specify the MediaHub Smart Home Layer as a separate enforcement boundary; keep mapping open.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: the AI automation path explicitly traverses MediaHub Smart Home Layer and cannot invoke lower-level HA actions around it.
- **Required evidence:** Exact B1 §4 line 94; B2 §§14/18; accepted Smart Home layer/API contract and later bypass-negative evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03; MH-04; MH-05; MH-10; MH-17.
- **Verification method:** Source comparison and review of the accepted layer/API contract; runtime negatives require separate authorization.
- **Change history:** Audit 01 atom B1-04-17; historical parent/cross-links HA4-05 / AUTO4-04 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Traceability subdivision of one B1 sentence; shared lineage with HA4-05/AUTO4-04 preserved; final child ID not minted.

### B1-04-18 — HA4-01 / HA4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-01 / HA4-06/B1-04-18 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 97 — LITERAL B1 SOURCE. Home Assistant Core — authority for the Smart Home domain.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: EXPLICIT/PARTIAL, B2 §§3–4/14. B2 explicitly assigns HA Core Smart Home operational/device-state authority, but the full domain-scope conflict boundary with platform authority is still awaiting accepted authority-table evidence.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§2.3/3/4/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Smart Home operational/device state is assigned to HA Core, and the boundary to MediaHub platform identity/lifecycle/policy/state is explicit.
- **Required evidence:** Exact B1 §4 line 97; B2 §§3–4/14; accepted authority-scope table and cross-domain conflict semantics.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03; MH-05; MH-17; policy and identity/trust contracts.
- **Verification method:** Source comparison plus independent scope/conflict-table review.
- **Change history:** Audit 01 atom B1-04-18; historical parent/cross-links HA4-01 / HA4-06 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Historical parents HA4-01/HA4-06 preserved; distinct authority statement; stable child ID deferred.

### B1-04-19 — HA4-06 / SA4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/HA4-06 / SA4-01/B1-04-19 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §4 line 98 — LITERAL B1 SOURCE. MediaHub State Authority — canonical authority of MediaHub platform state.
- **B2 mapping status:** MAPPED. Audit 01 relation: EXPLICIT, B2 §3. B2 §3 explicitly identifies MediaHub State Authority as the canonical authority for platform canonical state.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3/14/18; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level HA/UI contract is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: the accepted authority model identifies MediaHub State Authority as canonical authority for platform state; this is documentary coverage only.
- **Required evidence:** Exact B1 §4 line 98; B2 §3 authority table; cross-domain authority table must retain the distinct HA scope.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; approval covers schema/status vocabulary only, not this atom mapping. Independent semantic review/owner disposition remains open.
- **Dependencies:** MH-03; MH-05; MH-17; State Authority contract.
- **Verification method:** Compare exact source line and B2 §3; independent reviewer confirms the platform-state mapping and Smart Home scope separation.
- **Change history:** Audit 01 atom B1-04-19; historical parent/cross-links HA4-06 / SA4-01 preserved; Proposal 02 §6.1 source-anchor treatment consulted. Documentary mapping draft only; no canonical backlog, baseline, main matrix or runtime changed. Historical parent HA4-06 and shared SA4-01 link preserved; final child ID deferred.

## 4. Next review gates

- [ ] Independently compare all 19 rows with exact B1 anchors and Audit 01.
- [ ] Reconfirm per-atom B2 clauses without substituting a general domain relationship for exact mapping.
- [ ] Keep mixed/partial mappings `NOT_REVIEWED` until their complete meaning is explicitly supported.
- [ ] Review derived criteria separately from literal B1 text; do not promote a proposed criterion to a canonical contract by copying it here.
- [ ] Preserve the distinction between HA Core's Smart Home operational/device-state authority and MediaHub State Authority's canonical platform-state authority.
- [ ] Do not assign final child IDs before complete cross-branch/repository collision review and owner approval.
- [ ] Do not merge into the parent-level crosswalk or canonical backlog before independent review and separate governance disposition.

## 5. Non-actions

B1, B2, main, historical Batch 04 backlog, the parent-level crosswalk, and the existing atom-level Batch-01 draft/review were not modified by this artifact. No tests, qualification, installation, deployment, infrastructure/live-host operation or merge was performed.
