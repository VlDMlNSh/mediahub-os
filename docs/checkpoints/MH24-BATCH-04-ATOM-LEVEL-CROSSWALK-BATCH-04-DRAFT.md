# MH-24 Batch 04 — Atom-Level Crosswalk Batch 04 (B1 §6 Smart Home)

- Date: 2026-10-12
- Branch: `docs/mediahub-chat-tree-map-20261012`
- Status: **DOCUMENTARY DRAFT / OPEN — NOT APPROVED; NOT A CANONICAL BACKLOG**
- B1 source: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` @ `main`, SHA `9df4892ed0734050ac79732603d15bb414717310`.
- B2 reference: `docs/checkpoints/mediahub-functional-baseline-2.0.md` @ `main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Supporting documents: Audit 01 SHA `d0938f14ed4110545118f075175dee3be412097b`; Proposal 02 SHA `7e737c8add9e3453062e9fc459790e7010e55689`; Product Owner Decision Record SHA `9117098e22c26708d48ca8ba5954669faa209d68`.

## 1. Scope, statuses and lineage exception

- This batch contains all 29 Audit 01 §6 source/control labels: 26 literal-source traceability items and three D-coded derived controls. D-coded rows must never be represented as verbatim B1 requirements.
- Approved mapping vocabulary: `MAPPED`, `CONFLICT`, `NO_DIRECT_COUNTERPART`, `NOT_REVIEWED`. B2 relations marked partial or derived remain `NOT_REVIEWED`; no implementation/qualification is implied.
- **Traceability finding:** Audit 01 links source line 134 (“expose device through unified MediaHub UI”) to legacy `SH4-07`. Later Proposal 02 §6.1/§6.2 assigns line 134 to `SH4-06.c` and maps the line-136 vendor-neutral compatibility sentence to shared `SH4-01.b / SH4-07.a`. Preserve the historical link and document the mismatch; do not silently rewrite Audit 01 or mint a final child ID. This is an ID/lineage discrepancy, not evidence of a B1↔B2 semantic conflict, so mapping status remains `NOT_REVIEWED`, not `CONFLICT`.
- One B1 sentence at line 136 is decomposed into two traceability components (maximum compatibility and no single-manufacturer restriction); it must not be counted as two separate source sentences.
- All owner approvals remain scoped to schema/status vocabulary; this crosswalk and all acceptance criteria remain unapproved.

## 2. Batch summary

| Metric | Result |
|---|---:|
| Audit 01 §6 rows | 29 |
| Draft rows | 29 |
| Literal-source traceability rows | 26 |
| Derived-control rows | 3 |
| MAPPED | 0 |
| NOT_REVIEWED | 29 |
| NO_DIRECT_COUNTERPART | 0 |
| CONFLICT (B1↔B2 semantic status) | 0 |
| Final child IDs minted | 0 |
| Runtime tests / qualification / deployment | Not run |

## 3. Atom-level records — 12 fields each

### B1-06-01 — SH4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-01/B1-06-01 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 122 — LITERAL B1 source / traceability atom. Literal: scalable Smart Home support.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 describes the authority and lifecycle but does not define a measurable scalability target.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: owner-approved capacity/scale rubric names supported device, entity, event and throughput ranges.
- **Required evidence:** Scale target, capability catalogue and relevant conformance evidence remain OPEN.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-06 runtime/resource governance.
- **Verification method:** Compare B1 and B2; independently review accepted scale criteria.
- **Change history:** Audit 01 atom B1-06-01, historical link SH4-01 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. The word “scale” has no quantitative threshold in B1.

### B1-06-02 — SH4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-01/B1-06-02 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 122 — LITERAL B1 source / traceability atom. Literal: extensible adapter/integration layer.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not supply an accepted adapter API/extension contract.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: a versioned adapter contract specifies identity, capabilities, errors, lifecycle and permission boundary.
- **Required evidence:** Accepted adapter contract, compatibility matrix and integration evidence remain OPEN.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-03 authority boundary.
- **Verification method:** Source comparison and independent adapter-contract review.
- **Change history:** Audit 01 atom B1-06-02, historical link SH4-01 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Historical parent SH4-01 retained; final child ID deferred.

### B1-06-03 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-03 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: lighting.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not fully classify lighting support or protocol/feature levels.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: catalogue marks required/optional/deferred capabilities and their qualified adapters.
- **Required evidence:** Lighting capability matrix, supported adapter/version entries and qualified-device evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17.
- **Verification method:** Source comparison; later review capability catalogue.
- **Change history:** Audit 01 atom B1-06-03, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list at line 124.

### B1-06-04 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-04 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: climate.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not fully classify climate capabilities, controls or device semantics.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: catalogue identifies supported climate primitives, safety boundaries and unsupported cases.
- **Required evidence:** Climate capability matrix and qualified adapter evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; safety/policy contracts.
- **Verification method:** Source comparison and later capability-catalogue review.
- **Change history:** Audit 01 atom B1-06-04, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list at line 124.

### B1-06-05 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-05 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: security systems.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not define security-system safety classes, fail-safe actions or feature support.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: safety class, permission set, fail-safe/degraded behavior and unsupported cases are defined per capability.
- **Required evidence:** Security capability matrix, safety/permission contracts, later negative/failure evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-04; MH-05; MH-12; MH-17.
- **Verification method:** Source comparison and later security/safety contract review.
- **Change history:** Audit 01 atom B1-06-05, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list; no device admission inferred.

### B1-06-06 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-06 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: cameras.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not classify camera streaming, recordings, metadata or privacy access.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: camera capabilities, retention/data class and access boundary are explicit for each admitted profile.
- **Required evidence:** Camera capability and data-class matrix; retention/access contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-13 privacy; media/surveillance domains.
- **Verification method:** Source comparison and later camera capability review.
- **Change history:** Audit 01 atom B1-06-06, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-07 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-07 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: intercoms.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not define intercom media/door-control capabilities or authorization semantics.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: supported intercom capabilities and consequential-action controls are explicit per adapter.
- **Required evidence:** Intercom feature/permission matrix and accepted adapter evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-04.
- **Verification method:** Source comparison and later capability/authorization review.
- **Change history:** Audit 01 atom B1-06-07, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-08 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-08 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: sensors.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not provide a sensor taxonomy, unit semantics, freshness or unknown-value policy.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: sensor identity, unit/type, update/freshness and unknown-value semantics are documented.
- **Required evidence:** Sensor schema and source/freshness rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-03 state semantics.
- **Verification method:** Source comparison and later schema review.
- **Change history:** Audit 01 atom B1-06-08, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-09 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-09 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: actuators.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not specify actuator safety/permission classes or uncertain command outcomes.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: actuator operations use defined authorization and fail-safe/unknown-outcome semantics.
- **Required evidence:** Actuator capability/permission matrix and command outcome contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-04; MH-05; MH-17; policy boundary.
- **Verification method:** Source comparison and later safety/command review.
- **Change history:** Audit 01 atom B1-06-09, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-10 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-10 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: electrical power systems.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not specify power telemetry/control semantics or safety boundaries.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: admitted power capabilities, safety classification and control restrictions are explicit.
- **Required evidence:** Power capability schema and safety/authorization contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-04; MH-05; MH-17.
- **Verification method:** Source comparison and later capability/safety review.
- **Change history:** Audit 01 atom B1-06-10, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-11 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-11 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: network equipment.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not define network-device credential, configuration or management boundaries.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: network equipment capability and credential boundaries are documented and authorized.
- **Required evidence:** Network-device access/credential and capability matrix.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-04; MH-05; MH-17; MH-21 network boundary.
- **Verification method:** Source comparison and later security-contract review.
- **Change history:** Audit 01 atom B1-06-11, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-12 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-12 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: controllers.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not define controller identity, ownership or takeover semantics.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: controller identities and ownership/takeover conditions are explicit per integration.
- **Required evidence:** Controller identity/ownership map and takeover rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-03 authority boundaries.
- **Verification method:** Source comparison and later ownership review.
- **Change history:** Audit 01 atom B1-06-12, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-13 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-13 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: hubs.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not define hub identity, protocol/capability ownership or bridging behavior.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: hub support and bridge/exposure semantics are listed in the capability catalogue.
- **Required evidence:** Hub capability/connection matrix.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17.
- **Verification method:** Source comparison and later capability-catalogue review.
- **Change history:** Audit 01 atom B1-06-13, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-14 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-14 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: wired systems.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not enumerate wired protocol support or installation profiles.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: supported wired protocol/device capabilities and constraints are listed per qualified adapter.
- **Required evidence:** Wired protocol/version/capability matrix and qualification evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17.
- **Verification method:** Source comparison and later protocol matrix review.
- **Change history:** Audit 01 atom B1-06-14, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-15 — SH4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-02/B1-06-15 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 124 — LITERAL B1 source / traceability atom. Literal category: wireless systems.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 does not enumerate wireless protocol support or lifecycle constraints.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: supported wireless protocol/device capabilities, security and constraints are listed per qualified adapter.
- **Required evidence:** Wireless protocol/version/capability matrix and qualification evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-04; MH-05; MH-17.
- **Verification method:** Source comparison and later protocol/security matrix review.
- **Change history:** Audit 01 atom B1-06-15, historical link SH4-02 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One item from the shared literal B1 category list.

### B1-06-16 — SH4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-03/B1-06-16 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 126 — LITERAL B1 source / traceability atom. Literal: automatic equipment discovery is envisaged.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §§8/14. B2 describes the Smart Home lifecycle and device admission but does not fully define automatic discovery triggers/scope.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: automatic discovery behavior, scopes, rate limits and failure outcomes are specified; discovery is not itself trust/enrollment.
- **Required evidence:** Discovery specification, identity/trust/admission sequence and bounded evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-04; MH-12.
- **Verification method:** Compare source and B2; review discovery/trust contract. D01 remains separately derived.
- **Change history:** Audit 01 atom B1-06-16, historical link SH4-03 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Source sentence says automatic discovery; trust/enrollment separation is derived as B1-06-D01.

### B1-06-17 — SH4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-04/B1-06-17 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 127 — LITERAL B1 source / traceability atom. Literal list item: identify the device.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 lifecycle includes Identify but the exact device-identity schema and unknown behavior are not specified in the reviewed clause.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: a versioned identity schema defines mandatory/optional fields and unknown/unrecognized outcomes.
- **Required evidence:** Device identity schema and sample provenance.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; identity/trust architecture.
- **Verification method:** Compare B1 and B2; review identity schema when accepted.
- **Change history:** Audit 01 atom B1-06-17, historical link SH4-04 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One literal item in the B1 discovery/onboarding list.

### B1-06-18 — SH4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-04/B1-06-18 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 128 — LITERAL B1 source / traceability atom. Literal list item: identify manufacturer.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 does not define manufacturer-field provenance, normalization or unknown cases.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: manufacturer values retain source/provenance and explicit unknown behavior.
- **Required evidence:** Identity schema, field provenance, unknown-field handling.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-10 trusted-source boundary.
- **Verification method:** Compare source and B2; review identity schema and provenance.
- **Change history:** Audit 01 atom B1-06-18, historical link SH4-04 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One literal item in the B1 discovery/onboarding list.

### B1-06-19 — SH4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-04/B1-06-19 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 129 — LITERAL B1 source / traceability atom. Literal list item: identify model.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 does not define model identifiers, model/firmware differentiation or unknown behavior.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: model identifiers/firmware are normalized without discarding source identity, and unknowns stay explicit.
- **Required evidence:** Device identity schema and manufacturer/model/version evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17.
- **Verification method:** Compare source and B2; review identity schema.
- **Change history:** Audit 01 atom B1-06-19, historical link SH4-04 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One literal item in the B1 discovery/onboarding list.

### B1-06-20 — SH4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-04/B1-06-20 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 130 — LITERAL B1 source / traceability atom. Literal list item: identify connection method.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 does not enumerate the connection-method taxonomy or unknown states.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: connection method is recorded against an accepted taxonomy and unknown methods remain unqualified.
- **Required evidence:** Connection-method taxonomy and per-device source evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-21 network boundary.
- **Verification method:** Compare source and B2; review taxonomy.
- **Change history:** Audit 01 atom B1-06-20, historical link SH4-04 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. One literal item in the B1 discovery/onboarding list.

### B1-06-21 — SH4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-05/B1-06-21 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 131 — LITERAL B1 source / traceability atom. Literal list item: check compatibility.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §§8/14. B2 includes capability/qualification concepts but does not define a complete compatibility matrix/version policy.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: compatibility has a versioned rule source and explicit unsupported/unknown outcomes.
- **Required evidence:** Compatibility/version matrix, rule provenance and unknown-case criteria.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17; MH-22 qualification.
- **Verification method:** Compare source and B2; independently review compatibility contract. D02 ordering remains derived, not literal.
- **Change history:** Audit 01 atom B1-06-21, historical link SH4-05 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Historical parent SH4-05 preserved; pre-offer temporal ordering is separately derived as B1-06-D02.

### B1-06-22 — SH4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-06/B1-06-22 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 132 — LITERAL B1 source / traceability atom. Literal list item: offer installation of the necessary integration.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B1 says offer installation; it does not authorize silent automatic installation. B2 lifecycle does not specify the exact consent/installation UX.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: onboarding presents an explicit offer with scope, effects and rejection path; install authorization follows accepted policy.
- **Required evidence:** Onboarding UX/state machine, permission decision, rollback plan and later test evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-04; MH-05; MH-16; MH-17.
- **Verification method:** Compare source and B2; review install/consent contract. No installation executed.
- **Change history:** Audit 01 atom B1-06-22, historical link SH4-06 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Historical parent SH4-06 retained; “offer” must not be normalized into unconditional automatic installation.

### B1-06-23 — SH4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-06/B1-06-23 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 133 — LITERAL B1 source / traceability atom. Literal list item: create the necessary configuration.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §§14/19. B2 does not specify the configuration schema, authorization, persistence or rollback details.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: configuration schema, authority path, failure/rollback and user-impact semantics are explicit.
- **Required evidence:** Configuration contract, authorization trace and rollback criteria.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-03; MH-04; MH-05; MH-14; MH-16; MH-17.
- **Verification method:** Compare source and B2; review configuration contract. No configuration created.
- **Change history:** Audit 01 atom B1-06-23, historical link SH4-06 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Historical parent SH4-06 retained; configuration creation does not imply authorization to mutate other authority domains.

### B1-06-24 — SH4-07 (Audit 01); SH4-06.c (Proposal 02 correction)

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/B1-06-24/SH4-07↔SH4-06.c — lineage discrepancy, not a final child ID
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 134 — LITERAL B1 source / traceability atom. Literal list item: expose the device through the unified MediaHub UI.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14; legacy parent-link mismatch OPEN. B2 §14 sets the Smart Home authority/lifecycle but lacks the accepted capability-to-read-model-to-UI contract. Audit 01 links line 134 to SH4-07, while Proposal 02 §6.1/§6.2 assigns line 134 to SH4-06.c and line 136 to shared vendor-neutral SH4-01.b/SH4-07.a.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: admitted device capabilities are exposed through an authorized MediaHub UI read model; resolve historical lineage without deleting legacy IDs.
- **Required evidence:** Exact B1 line 134; B2 §14; Audit 01; Proposal 02; accepted capability-to-UI contract and route trace.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-09; MH-17; UI/capability contracts.
- **Verification method:** Source-anchored comparison plus independent lineage review. Do not silently relabel the historical Audit 01 atom; no runtime/UI test performed.
- **Change history:** Audit 01 atom B1-06-24, historical link SH4-07 (Audit 01); SH4-06.c (Proposal 02 correction) preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. OPEN traceability finding: retain B1-06-24/SH4-07 as history; Proposal 02 anchor remains provisional pending independent owner/governance review.

### B1-06-25 — SH4-01 / SH4-07

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-01 / SH4-07/B1-06-25 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 136 — LITERAL B1 source / traceability atom. Literal clause component: maximize compatibility.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 §14 provides a general lifecycle but does not quantify compatibility breadth.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: owner defines a measurable compatibility target and supported/unsupported reporting model.
- **Required evidence:** Compatibility rubric and capability catalogue.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17.
- **Verification method:** Source comparison and owner-approved criteria review.
- **Change history:** Audit 01 atom B1-06-25, historical link SH4-01 / SH4-07 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Traceability subdivision of one source sentence at line 136, not an independent sentence.

### B1-06-26 — SH4-01 / SH4-07

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-01 / SH4-07/B1-06-26 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 136 — LITERAL B1 source / traceability atom. Literal clause component: do not restrict architecture to one manufacturer.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: PARTIAL, B2 §14. B2 does not specify measurable vendor-neutral conformance criteria in the reviewed clause.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: adapter contracts remain vendor-neutral and manufacturer-specific behavior is isolated behind adapter boundaries.
- **Required evidence:** Vendor-neutral adapter contract and conformance matrix.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17.
- **Verification method:** Source comparison and adapter-contract review.
- **Change history:** Audit 01 atom B1-06-26, historical link SH4-01 / SH4-07 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Traceability subdivision of one source sentence at line 136; Proposal 02 maps vendor-neutral objective to SH4-01.b / SH4-07.a.

### B1-06-D01 — SH4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-03/B1-06-D01 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 126 — DERIVED CONTROL — not verbatim B1 text. DERIVED CONTROL: discovery does not by itself imply trust/enrollment.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: DERIVED, B2 §§4/6/14 related. Audit 01 explicitly classifies this as derived security control, not literal B1 wording.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: trust/admission requires separate identity, capability and policy checks after discovery.
- **Required evidence:** Owner-approved discovery→identity→trust→capability→authorization lifecycle; future negative evidence only if authorized.
- **Lifecycle status:** DRAFT / DERIVED CONTROL / OWNER APPROVAL OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-04; MH-12; MH-17.
- **Verification method:** Review literal/derived classification and security contract; no runtime testing performed.
- **Change history:** Audit 01 atom B1-06-D01, historical link SH4-03 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Not a verbatim B1 requirement; preserve D-coded origin.

### B1-06-D02 — SH4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-05/B1-06-D02 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 131 — DERIVED CONTROL — not verbatim B1 text. DERIVED CONTROL: compatibility must be checked before offering integration.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: DERIVED, ordering interpretation. B1 mentions compatibility checking and offering integration but does not unambiguously state the exact temporal ordering as a separate source clause.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: owner/governance decision confirms or rejects this order; do not present it as literal B1 text until then.
- **Required evidence:** Explicit owner decision plus onboarding sequence contract.
- **Lifecycle status:** DRAFT / DERIVED CONTROL / OWNER APPROVAL OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-05; MH-17.
- **Verification method:** Review source language and confirm ordering with owner; no test performed.
- **Change history:** Audit 01 atom B1-06-D02, historical link SH4-05 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Derived ordering interpretation; preserve D-coded origin.

### B1-06-D03 — SH4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SH4-06/B1-06-D03 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in reviewed canonical sources.
- **Source atom / classification:** B1 §6 line 132 — DERIVED CONTROL — not verbatim B1 text. DERIVED CONTROL: explicit user confirmation for every consequential install/configuration change.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 relation: DERIVED, owner scope open. Audit 01 states B1 does not specify confirmation scope.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §14 (and §§8/14/19 where cited). No accepted MH-05/MH-17 domain contract ref is asserted.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: owner defines which install/configuration changes require confirmation and which policies permit automation.
- **Required evidence:** Explicit product decision, permission/confirmation UX and rollback contract.
- **Lifecycle status:** DRAFT / DERIVED CONTROL / OWNER APPROVAL OPEN
- **Reviewer / approval reference:** Product-owner decision record @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; schema/status vocabulary only. All atom mappings and derived controls remain unapproved; domain-owner confirmation is open.
- **Dependencies:** MH-04; MH-05; MH-16; MH-17.
- **Verification method:** Review decision scope and contract; no installation/configuration changed.
- **Change history:** Audit 01 atom B1-06-D03, historical link SH4-06 preserved. Proposal 02 §6.1/§6.2 consulted; no stable child ID minted. Derived security/product control, not a literal source atom.

## 4. Open traceability issue and review gates

1. Independently review the `B1-06-24 / SH4-07 / SH4-06.c` source-link discrepancy against B1 line 134 and Proposal 02 §6.1/§6.2. The draft follows Proposal 02 as the latest working anchor, but does not treat it as owner-approved correction.
2. Determine whether the line-136 vendor-neutral objective remains one normative obligation with legacy cross-links `SH4-01 / SH4-07`; do not duplicate it.
3. Approve required/optional/deferred device categories and per-domain safety/identity/compatibility acceptance separately.
4. Confirm the literal/derived boundary for D01–D03 with product/domain owners; do not promote them into B1 literal atoms.
5. Keep all mapping statuses `NOT_REVIEWED` until an individually accepted B2 mapping and required evidence are supplied.
6. Do not mint stable child IDs until a full repository/branch collision review is recorded.
7. Do not update canonical backlog, Baseline 1.0/2.0 or main traceability matrix from this draft.

## 5. Non-actions

B1, B2, main, the historical backlog, parent-level crosswalk and prior atom batches were not modified. No tests, qualification, installation, deployment, infrastructure/live-host operation, production change or merge was performed.
