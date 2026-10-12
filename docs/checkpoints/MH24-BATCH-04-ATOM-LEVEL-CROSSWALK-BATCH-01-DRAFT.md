# MH-24 Batch 04 — Atom-Level Crosswalk Batch 01 (B1 §3 State Authority)

- Date: 2026-10-12
- Branch: `docs/mediahub-chat-tree-map-20261012`
- Status: **DOCUMENTARY DRAFT / OPEN — NOT APPROVED; NOT A CANONICAL BACKLOG**
- Purpose: atom-level source-to-B2 mapping for B1 §3 only, using the owner-approved 12-field schema. This is a bounded next pass, not a claim that Batch 04 or all MH domains are complete.
- Source scope: B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` @ `main`, SHA `9df4892ed0734050ac79732603d15bb414717310`; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md` @ `main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Supporting audit/proposal: Audit 01 `docs/checkpoints/MH24-B1-SECTIONS-03-06-12-15-17-CLAUSE-COVERAGE-AUDIT-01.md`, SHA `d0938f14ed4110545118f075175dee3be412097b`; Proposal 02, SHA `7e737c8add9e3453062e9fc459790e7010e55689`; owner decision record, SHA `9117098e22c26708d48ca8ba5954669faa209d68`.

## 1. Interpretation and limits

- The `B1-03-xx` values below are existing Audit 01 source-atom labels, not final Requirement IDs. Parent IDs SA4-01…SA4-07 are preserved. No stable child IDs have been minted.
- Approved B2 mapping statuses are exactly `MAPPED`, `CONFLICT`, `NO_DIRECT_COUNTERPART`, `NOT_REVIEWED`. `PARTIAL-MAP` from Audit 01 is preserved in the explanatory field but represented as `NOT_REVIEWED` because the approved vocabulary has no PARTIAL value.
- `MAPPED` means documentary explicit coverage only. It does not establish implementation, test, qualification, or production readiness.
- B1 line 77 is one compound sentence. Its actor-specific traceability splits below do not inflate the number of literal sentences/requirements.
- This batch does not resolve all atoms within Batch 04, the remaining GOV-MH24 issues, or domain contracts. UI4-04 remains `HOLD / CROSS-LINK-ONLY` elsewhere.
- The Product Owner Decision Record approves the 12-field schema and mapping vocabulary, not this complete atom mapping. Independent semantic review remains open.

## 2. Batch-01 summary

| Metric | Result |
|---|---:|
| Source scope | B1 §3, lines 63–79 |
| Source-atom rows | 19 |
| Explicit B2 documentary mappings | 8 `MAPPED` |
| Related but partial/individual mapping not yet closed | 11 `NOT_REVIEWED` |
| `CONFLICT` | 0 (none evidenced in this batch) |
| `NO_DIRECT_COUNTERPART` | 0 (not assigned: each atom has a reviewed related B2 clause, though many are partial) |
| Stable child Requirement IDs minted | 0 |
| Runtime tests / qualification / deployment | Not run |

## 3. Atom-level records — 12 fields each

### B1-03-01 — SA4-01

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-01/B1-03-01 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 63 — LITERAL B1 SOURCE. MediaHub State Authority — единственный канонический источник истины платформенного состояния MediaHub.
- **B2 mapping status:** MAPPED. B2 §3 — Platform canonical state: MediaHub State Authority.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: One and only one logical MediaHub State Authority is named as canonical platform-state owner; no alternate platform-state authority is accepted.
- **Required evidence:** Exact B1 line 63; B2 §3; authority/path contract and later mutation-path evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** B2 §3–4; MH-03 State Authority foundation.
- **Verification method:** Compare the exact B1 line and B2 §3 at the pinned SHAs; independent reviewer confirms equivalent core invariant.
- **Change history:** Audit 01 atom B1-03-01; historical Batch 04 parent SA4-01 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-01 preserved; atom label from Audit 01; final child ID not minted.

### B1-03-02 — SA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-02/B1-03-02 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 66 — LITERAL B1 SOURCE. состояние системы;
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §§3–4/13; B2 does not yet supply the reviewed atom-level state/schema trace.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4/13; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: A reviewed schema inventory identifies system-state entities and routes canonical changes through the State Authority; criterion remains proposed.
- **Required evidence:** Exact B1 line 66; B2 §§3–4/13; accepted schema inventory and mutation-path trace still required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-14 persistence boundary, subject to its own governance gates.
- **Verification method:** Source-anchor check, exact-clause comparison, and later schema/authority-path review; no runtime test performed.
- **Change history:** Audit 01 atom B1-03-02; historical Batch 04 parent SA4-02 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-02 preserved; source atom B1-03-02; stable child ID deferred.

### B1-03-03 — SA4-02

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-02/B1-03-03 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 67 — LITERAL B1 SOURCE. состояние MediaHub-объектов;
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §§3–4/13.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4/13; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: A reviewed object/schema inventory identifies canonical ownership and mutation paths for MediaHub-object state; proposed acceptance criterion only.
- **Required evidence:** Exact B1 line 67; B2 §§3–4/13; object inventory and owner/path evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-14, with no implied physical-persistence authorization.
- **Verification method:** Compare source anchor with B2; independently review object types and owner/path table when supplied.
- **Change history:** Audit 01 atom B1-03-03; historical Batch 04 parent SA4-02 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-02 preserved; source atom B1-03-03; stable child ID deferred.

### B1-03-04 — SA4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-03/B1-03-04 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 68 — LITERAL B1 SOURCE. состояние пользовательских конфигураций;
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §§3/13/19.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4/13; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Configuration mutations are assigned to one canonical authority path and their state transitions are documented; proposed acceptance criterion only.
- **Required evidence:** Exact B1 line 68; B2 §§3/13/19; configuration state machine and mutation trace required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-14; MH-16 lifecycle/recovery.
- **Verification method:** Exact-source comparison and independent review of configuration lifecycle contract; no runtime verification authorized here.
- **Change history:** Audit 01 atom B1-03-04; historical Batch 04 parent SA4-03 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-03 preserved; source atom B1-03-04; stable child ID deferred.

### B1-03-05 — SA4-03

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-03/B1-03-05 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 69 — LITERAL B1 SOURCE. жизненный цикл ресурсов;
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §§3/13/19.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4/13; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Resource lifecycle transitions have one canonical owner and explicit transition/denial outcomes; proposed acceptance criterion only.
- **Required evidence:** Exact B1 line 69; B2 §§3/13/19; versioned lifecycle and ownership map required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-14; MH-16.
- **Verification method:** Compare B1/B2 clauses and review a resource lifecycle contract when accepted.
- **Change history:** Audit 01 atom B1-03-05; historical Batch 04 parent SA4-03 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-03 preserved; source atom B1-03-05; stable child ID deferred.

### B1-03-06 — SA4-04

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-04/B1-03-06 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 70 — LITERAL B1 SOURCE. авторизацию операций изменения состояния;
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §6.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§6; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Before a canonical mutation, identity/capability/policy authorization returns an explicit allow/deny outcome; this enforcement sequence is a derived acceptance control, not verbatim detail in B1 line 70.
- **Required evidence:** Exact B1 line 70; B2 §6; accepted authorization-to-mutation contract and negative-path evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03 State Authority; MH-04 Security; MH-07 Policy.
- **Verification method:** Compare the literal responsibility to B2 §6; later contract review plus deny-path/authority-bypass evidence under separate authorization.
- **Change history:** Audit 01 atom B1-03-06; historical Batch 04 parent SA4-04 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-04 preserved; source atom B1-03-06; stable child ID deferred.

### B1-03-07 — SA4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-05/B1-03-07 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 71 — LITERAL B1 SOURCE. консистентность;
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §§3/13/19/23.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3/13/19/23; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: The consistency contract states invariants and outcomes for competing/stale/unknown mutations; critical-state consistency semantics remain to be specified.
- **Required evidence:** Exact B1 line 71; B2 §§3/13/19/23; owner-reviewed consistency contract and conflict-path evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-14; MH-20; MH-23.
- **Verification method:** Source comparison; independent review of explicit consistency invariant and proposed test matrix.
- **Change history:** Audit 01 atom B1-03-07; historical Batch 04 parent SA4-05 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-05 preserved; source atom B1-03-07; stable child ID deferred.

### B1-03-08 — SA4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-05/B1-03-08 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 72 — LITERAL B1 SOURCE. provenance;
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §§3/13/19/23.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3/13/19/23; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Canonical changes can be traced to their source, version, actor and decision reference; the exact provenance schema is still open.
- **Required evidence:** Exact B1 line 72; B2 §§3/13/19/23; accepted provenance schema and sample evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-10 trusted-source/evidence boundary; MH-14.
- **Verification method:** Source comparison and schema/lineage review; no runtime evidence inferred.
- **Change history:** Audit 01 atom B1-03-08; historical Batch 04 parent SA4-05 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-05 preserved; source atom B1-03-08; stable child ID deferred.

### B1-03-09 — SA4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-05/B1-03-09 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 73 — LITERAL B1 SOURCE. audit;
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §§3/13/19/23.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3/13/19/23; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: A documented audit-event contract identifies recorded decisions/actions, access restrictions and retention; details remain open.
- **Required evidence:** Exact B1 line 73; B2 §§3/13/19/23; audit schema/retention decision and sanitized sample evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-11 Observability; MH-12 Security; MH-03; MH-14.
- **Verification method:** Source comparison and independent schema/retention review; no logs or runtime state accessed.
- **Change history:** Audit 01 atom B1-03-09; historical Batch 04 parent SA4-05 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-05 preserved; source atom B1-03-09; stable child ID deferred.

### B1-03-10 — SA4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-05/B1-03-10 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 74 — LITERAL B1 SOURCE. recovery;
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §§3/13/19/23.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3/13/19/23; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Recovery restores canonical state without creating competing authority and has explicit integrity/rollback outcomes; recovery model is still open.
- **Required evidence:** Exact B1 line 74; B2 §§3/13/19/23; recovery/restore/rollback contract and authorized drill evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-14; MH-16; MH-22 qualification gate.
- **Verification method:** Source comparison and contract review; any recovery drill requires separate explicit authorization.
- **Change history:** Audit 01 atom B1-03-10; historical Batch 04 parent SA4-05 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-05 preserved; source atom B1-03-10; stable child ID deferred.

### B1-03-11 — SA4-05

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-05/B1-03-11 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 75 — LITERAL B1 SOURCE. migration.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 classifies related coverage as PARTIAL in B2 §§3/13/19/23.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3/13/19/23; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Migration preserves canonical ownership and required provenance with explicit failure/rollback outcomes; proposed criterion, not approved.
- **Required evidence:** Exact B1 line 75; B2 §§3/13/19/23; migration contract and later migration evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-14; MH-16; MH-23.
- **Verification method:** Source comparison and independent migration-contract review; no migration executed.
- **Change history:** Audit 01 atom B1-03-11; historical Batch 04 parent SA4-05 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-05 preserved; source atom B1-03-11; stable child ID deferred.

### B1-03-12 — SA4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-06/B1-03-12 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 77 (shared compound sentence) — LITERAL B1 SOURCE. Actor-specific element: AI may not become an alternate canonical MediaHub state source. Traceability subdivision of one compound source sentence; not a separate literal sentence.
- **B2 mapping status:** MAPPED. Audit 01 classifies the AI exclusion as EXPLICIT in B2 §§3/18.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: AI outputs are advisory/proposals and cannot directly perform canonical mutation outside the State Authority path.
- **Required evidence:** Exact B1 line 77; B2 §§3/18; later API/tool bypass-negative evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-10; MH-12.
- **Verification method:** Source comparison; later direct-mutation/bypass negative tests under approved verification scope.
- **Change history:** Audit 01 atom B1-03-12; historical Batch 04 parent SA4-06 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-06 preserved. This is a traceability subdivision of one B1 sentence, not an additional sentence-level requirement; stable child ID deferred.

### B1-03-13 — SA4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-06/B1-03-13 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 77 (shared compound sentence) — LITERAL B1 SOURCE. Actor-specific element: a cloud component may not become an alternate canonical MediaHub state source. Traceability subdivision of one compound source sentence; not a separate literal sentence.
- **B2 mapping status:** MAPPED. Audit 01 classifies the cloud exclusion as EXPLICIT in B2 §§3/18.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Cloud services return supporting data only and cannot mutate canonical MediaHub state independently.
- **Required evidence:** Exact B1 line 77; B2 §§3/18; cloud mutation-path and egress-policy evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-21; MH-12.
- **Verification method:** Source comparison; later API/data-plane negative tests require separate authorization.
- **Change history:** Audit 01 atom B1-03-13; historical Batch 04 parent SA4-06 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-06 preserved. Traceability subdivision of B1 line 77; stable child ID deferred.

### B1-03-14 — SA4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-06/B1-03-14 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 77 (shared compound sentence) — LITERAL B1 SOURCE. Actor-specific element: a mobile application may not become an alternate canonical MediaHub state source. Traceability subdivision of one compound source sentence; not a separate literal sentence.
- **B2 mapping status:** MAPPED. Audit 01 classifies the mobile exclusion as EXPLICIT in B2 §§3/18.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Mobile-originated writes are validated and committed through the canonical authority path; no independent mobile authority exists.
- **Required evidence:** Exact B1 line 77; B2 §§3/18; mobile command-path contract and bypass-negative evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; mobile domain; MH-12.
- **Verification method:** Source comparison; future API/write-path review and negative-path evidence under approved scope.
- **Change history:** Audit 01 atom B1-03-14; historical Batch 04 parent SA4-06 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-06 preserved. Traceability subdivision of B1 line 77; stable child ID deferred.

### B1-03-15 — SA4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-06/B1-03-15 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 77 (shared compound sentence) — LITERAL B1 SOURCE. Actor-specific element: Home Assistant UI may not become an alternate canonical platform-state source. Traceability subdivision of one compound source sentence; not a separate literal sentence.
- **B2 mapping status:** MAPPED. Audit 01 classifies the Home Assistant UI exclusion as EXPLICIT in B2 §§3/18.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: HA UI remains a Smart Home interface; platform canonical mutations remain owned by MediaHub State Authority.
- **Required evidence:** Exact B1 line 77; B2 §§3/18; HA integration contract and route/write-path evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-05; MH-09; MH-17.
- **Verification method:** Source comparison; review accepted HA/State Authority interface and future bypass negatives.
- **Change history:** Audit 01 atom B1-03-15; historical Batch 04 parent SA4-06 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-06 preserved. Traceability subdivision of B1 line 77; stable child ID deferred.

### B1-03-16 — SA4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-06/B1-03-16 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 77 (shared compound sentence) — LITERAL B1 SOURCE. Actor-specific element: an external ecosystem may not become an alternate canonical platform-state source. Traceability subdivision of one compound source sentence; not a separate literal sentence.
- **B2 mapping status:** NOT_REVIEWED. Audit 01 marks the relation PARTIAL in B2 §§3/18; ingress paths are not exhaustively specified.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4/13; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: External-ecosystem ingress and mutation paths are inventoried and none becomes independent canonical authority; proposed criterion.
- **Required evidence:** Exact B1 line 77; B2 §§3/18; external integration inventory and negative-path evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-04; MH-05; MH-21.
- **Verification method:** Source comparison; independently review source/identity/path inventory before considering mapping closed.
- **Change history:** Audit 01 atom B1-03-16; historical Batch 04 parent SA4-06 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-06 preserved. Traceability subdivision of B1 line 77; stable child ID deferred.

### B1-03-17 — SA4-06

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-06/B1-03-17 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 77 (shared compound sentence) — LITERAL B1 SOURCE. Actor-specific element: a separate automation engine may not become an alternate canonical platform-state source. Traceability subdivision of one compound source sentence; not a separate literal sentence.
- **B2 mapping status:** MAPPED. Audit 01 classifies the automation-engine exclusion as EXPLICIT in B2 §§3/18.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Automation engines submit commands through controlled domain/API and State Authority paths; they do not own canonical platform state.
- **Required evidence:** Exact B1 line 77; B2 §§3/18; automation integration contract and bypass-negative evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-05; MH-06; MH-10; MH-17.
- **Verification method:** Source comparison; later direct-write/bypass negative checks under separate authorization.
- **Change history:** Audit 01 atom B1-03-17; historical Batch 04 parent SA4-06 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-06 preserved. Traceability subdivision of B1 line 77; stable child ID deferred.

### B1-03-18 — SA4-07

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-07/B1-03-18 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 79, first sentence — LITERAL B1 SOURCE. При неоднозначности система должна работать по принципу fail closed.
- **B2 mapping status:** MAPPED. Audit 01 classifies the fail-closed rule as EXPLICIT in B2 §§3–4.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: Unclear authority/policy outcomes deny the state-changing action and do not silently pick another writer.
- **Required evidence:** Exact B1 line 79 first sentence; B2 §§3–4; later negative-path/failure evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-04; MH-12.
- **Verification method:** Source comparison; review explicit deny semantics and future fault/negative tests when authorized.
- **Change history:** Audit 01 atom B1-03-18; historical Batch 04 parent SA4-07 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-07 preserved; source atom B1-03-18; stable child ID deferred.

### B1-03-19 — SA4-07

- **Requirement ID (provisional; stable child ID not minted):** PROVISIONAL/SA4-07/B1-03-19 (not a stable child Requirement ID)
- **Owner:** TBD — domain owner not independently confirmed in the reviewed canonical sources.
- **Source atom / classification:** B1 §3 line 79, second sentence — LITERAL B1 SOURCE. Отказ State Authority не должен создавать альтернативную authority.
- **B2 mapping status:** MAPPED. Audit 01 classifies the no-fallback-authority invariant as EXPLICIT in B2 §§3–4.
- **Canonical contract path/ref:** docs/checkpoints/mediahub-functional-baseline-2.0.md@main#§3–4; B2 SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f. No accepted domain-level contract ref is asserted by this row.
- **Acceptance criteria:** PROPOSED — NOT APPROVED: State Authority failure leaves no alternate canonical writer; degraded/failure path is explicit and cannot accept unqualified authority takeover.
- **Required evidence:** Exact B1 line 79 second sentence; B2 §§3–4; future recovery/fencing evidence required.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and qualification OPEN.
- **Reviewer / approval reference:** MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md @ docs/mediahub-chat-tree-map-20261012, SHA 9117098e22c26708d48ca8ba5954669faa209d68; applies to schema/status vocabulary only. Atom-level acceptance still requires independent review and explicit owner/governance disposition.
- **Dependencies:** MH-03; MH-04; MH-12; MH-14/16 recovery boundary.
- **Verification method:** Source comparison and explicit failure-state review; no runtime/chaos test performed.
- **Change history:** Audit 01 atom B1-03-19; historical Batch 04 parent SA4-07 preserved; Proposal 02 §6.1 supplies the provisional source anchor. This batch adds a source-anchored mapping draft only; no source baseline, canonical backlog, matrix on main, or runtime was changed. Historical parent SA4-07 preserved; source atom B1-03-19; stable child ID deferred.

## 4. Independent review checklist and next batch

- [ ] Independently verify all 19 B1 source atoms against the exact B1 SHA and line anchors.
- [ ] Independently confirm the Audit 01 classification and exact B2 clause for all 19 rows.
- [ ] Review whether each proposed acceptance criterion over-specifies the literal source; keep derived controls separately labelled.
- [ ] Keep every `NOT_REVIEWED` status until an individually supported mapping is evidenced; do not promote a parent status to children.
- [ ] Continue with B1 §4 Home Assistant Core as a distinct batch; then §§5–6, 12, 15–17, ensuring the 153 Audit 01 IDs are not treated as 153 independent literal requirements.
- [ ] Perform full current-branch/repository collision review before minting final child IDs.
- [ ] Only after all applicable atoms receive independent review and owner/governance resolution may any canonical backlog promotion be considered.

## 5. Non-actions

B1, B2 and main were not modified. The historical Batch 04 backlog, current parent-level crosswalk and traceability matrix were not modified by this draft. No test, qualification, installation, deployment, infrastructure/production action, live-host operation or merge was performed.
