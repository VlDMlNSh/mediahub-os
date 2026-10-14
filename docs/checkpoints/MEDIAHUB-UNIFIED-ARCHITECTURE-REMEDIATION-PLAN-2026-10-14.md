# MediaHub OS — Unified Architecture Remediation Plan

- **Date:** 2026-10-14
- **Repository:** `VlDMlNSh/mediahub-os`
- **Status:** `WORKING REMEDIATION REGISTER / NOT ACCEPTED / NOT FROZEN`
- **Purpose:** consolidate currently evidenced duplicates, source conflicts, navigation defects, governance gaps and verification blockers into one prioritized continuation plan.
- **Authority boundary:** this plan is a tracking artifact, not a normative contract, owner decision, implementation authorization, test/qualification result, release, deployment or acceptance.
- **Canonical functional baseline:** [Functional Baseline 2.0](mediahub-functional-baseline-2.0.md) on `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. Baseline 1.0 remains historical provenance; neither baseline is rewritten by this plan.

## 1. Audit boundary and live source identity

### 1.1 Refs observed

- `main` HEAD: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`.
- `docs/mediahub-chat-tree-map-20261012` HEAD at audit start: `0f4be9c11c9f09e1283bd03fd997ad7c0110e706`.
- Comparison: **DIVERGED**, docs branch ahead by 808 commits and behind by 2; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Complete recursive `main` tree at the inspected HEAD: tree SHA `cbb1862fcb4aa22ba24fea4ff12b580ffb305593`, 798 entries, `truncated=false`.
- The scan is a complete path inventory plus targeted source reading and consistency checks. It is **not** a semantic line-by-line audit of all 798 files; runtime behavior, CI outcome and actual service health remain unverified.

### 1.2 Evidence classes

- **CONFIRMED STATIC CONFLICT/DEFECT:** incompatible source text or IDs were directly observed.
- **CONFIRMED DUPLICATE FAMILY / SEMANTIC DIVERGENCE:** multiple paths with the same case-insensitive basename exist and sampled counterparts differ.
- **OPEN GOVERNANCE DECISION:** sources leave authority or acceptance to the owner; no technical guess may close it.
- **UNVERIFIED RISK:** needs a separately authorized test, runtime inspection, qualified review or broader source pass.
- **REPAIRED IN DOCS BRANCH ONLY:** a documentation correction exists on the docs branch but has not been integrated into `main`.

## 2. Consolidated finding register

| ID | Priority | Finding | Evidence / affected sources | Required disposition | State |
|---|---|---|---|---|---|
| MH-ARCH-001 | P0 | **Jarvis/ASTRA lifecycle authority conflict.** ASTRA component scheme on `main` says A0-ASTRA is “single coordination and MediaHub State Authority”; Jarvis ARC-003/018 limits ASTRA to its engineering lifecycle and requires one cross-system lifecycle owner. This wording can be read as granting product-state authority that conflicts with the P0-04 sole canonical mutation boundary. | `main` component scheme SHA `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1`; docs component scheme SHA `d321565a6e0fac1eef329adec67a35ba795b63aa`; [DEC-DEV crosswalk](MEDIAHUB-DEC-DEV-01-08-CROSSWALK-VALIDATION-WAVE-01-2026-10-14.md); owner packet §6.5. | Owner/governance must choose the existing DEC-DEV-02 model A/B/C and approve a typed lifecycle/delegation contract. Do not grant product-state authority to A0. | OPEN_CONFLICT |
| MH-ARCH-002 | P0 | **Concurrency limit 2 vs 3 on `main`.** Component scheme §14 says maximum 2 autonomous claims; launch schema and governance registry say 3, as do prose sources. Existing topology test asserts 3 in selected prose files but does not assert the component-scheme value, so it would not detect this specific conflict. | `main` component scheme SHA `54ba34ce53d1d7ecd97eef459be7d055b4fd19b1`; launch schema `aef6229477ed8ec45e45170f98ea87f7ba75ca29`; governance `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`; topology test `cc5410f631a161b3e3bfb4bae198340f905da6e4`. | Canonical schema is currently named as numeric authority; align `main` through a separately authorized, narrowly scoped change and strengthen drift assertions. The docs branch already removes the duplicated numeric value from the component scheme; do not infer that this resolves `main`. | OPEN / MAIN DRIFT |
| MH-ARCH-003 | P1 | **Authority wording inside governance contract is broader than its field-level authority map.** The purpose says one machine-readable source for gate identity and thresholds, while `authority_source` and `gate_registry.source_of_truth` designate the launch schema and governance holds mirrored threshold values. | Governance SHA `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`; launch schema SHA `aef6229477ed8ec45e45170f98ea87f7ba75ca29`; owner packet §7.1. | Owner/governance selects and documents field-level ownership. Current recommendation recorded in the owner packet is schema-authoritative numeric values with governance registry/mirror and fail-closed drift checks; it is not an accepted decision yet. | OWNER/GOVERNANCE |
| MH-ARCH-004 | P1 | **Design readiness can be mistaken for live qualification.** Unified YAML says `status: QUALIFICATION_READY_HYBRID_FABRIC` while generated Current Truth says all G0–G11 BLOCKED and overall `NOT_PROVEN / BLOCKED`. Model version 1.1 and paired Markdown version 1.0 also need explicit lineage semantics. | Unified YAML `adc852009c3a79d0e64265a3af8a4910a1388057`; Current Truth `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`; [wave 06 audit](MEDIAHUB-PROJECT-WIDE-ARCHITECTURE-INTEGRITY-WAVE-06-2026-10-14.md). | Approve a governed interpretation or versioned status-schema change that separates design maturity from runtime qualification. Until then, Current Truth is the live gate source; no design label promotes a gate. | OPEN |
| MH-ARCH-005 | P1 | **MH-03 document-family duplication with divergent contents.** Eighteen same-basename pairs exist between `architecture/MH-03-*.md` and `docs/architecture/mh-03/MH-03-*.md`; all 18 root/nested blob-SHA pairs differ. Four pairs have already been compared as text, and the contradiction-register pair has a direct status conflict: root `C03-08` requires governance review for the proposed HA path, while the nested copy says no current explicit contradictions are identified. `architecture/MH-03-index.md` (blob `b2d2eeb1b89117d10605c231e79378eebc437c5f`) lists the root-level artifacts as required, but remains PROPOSED; the nested directory has no `MH-03-index.md`. | Full 18-pair source/SHA table in Wave 09 below; examples: root contradiction register `5879ad2ab19110ae7418f881cbd7603a10ff996e` vs nested `7986b072983f1d6f828b7214f4896b91c91392f2`; root runtime foundation `325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2` vs nested `2457451017daa0f91e9e978e44c91e1e49d0d7a3`; lifecycle `300363a06fe678d3511c2a4b843678bf200df5f0` vs `41baa81406dcd25b8b1537adf9c8b1289c38edcd`; acceptance `e96adaac2eb52e2f8058cc889485ec982bf606e5` vs `eefb645d89c7c3046636d8344515aa02b7ccebe3`. | Preserve both trees and provenance. Confirm the active MH-03 source location and intended role of nested files; then reconcile each of the 18 pairs through a narrow reviewed change or explicitly label the copies as historical/derived. Root index is evidence of intended layout, not an accepted/frozen decision. Do not delete files before checking inbound references and ID lineage. | CONFIRMED DIVERGENT FAMILY; OWNER/GOVERNANCE ROUTE OPEN |
| MH-ARCH-006 | P0 | **P0-07 trusted-context and mutation/publication path remains unproven.** Existing evidence does not demonstrate an accepted trusted issuer/provisioner lifecycle or end-to-end P0-07 → P0-05 → P0-04 request/context/resource/revision binding. D1 is NOT DEMONSTRATED; D2 NOT EVIDENCED; D3/D4/D5 remain evidence-gated; D6 is open; D7 change-control ownership remains open. | [D2 proposal](P0-07-D2-TRUSTED-CONTEXT-AUTHORITY-LIFECYCLE-PROPOSAL-2026-10-13.md), SHA `39400abce88da7ea54be7d9d7505f215eba43408`; [traceability matrix](mediahub-unified-system-traceability-matrix-v0.1.md), SHA `43e495aae6b4dc55a0d2e07fa4723d364898a5c1`; owner register. | Continue source tracing only where it can prove an existing path. Otherwise route the proposal to governance. Keep P0-07 mutation/publication blocked and P0-05 v1.1 NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN. | BLOCKED |
| MH-ARCH-007 | P0 | **Qualified independent P0-07 D2 review is absent.** R-01…R-06 worksheet in the D2 proposal is blank; an internal desk review and source routing are not an independent review. | D2 proposal §13, SHA `39400abce88da7ea54be7d9d7505f215eba43408`; [crosswalk wave 01](MEDIAHUB-DEC-DEV-01-08-CROSSWALK-VALIDATION-WAVE-01-2026-10-14.md). | Owner/governance appoints a qualified independent reviewer or defers. Record competence, independence/conflicts, exact proposal/source SHAs, itemized R-01…R-06 dispositions and attributable sign-off. | WAITING OWNER / REVIEWER |
| MH-ARCH-008 | P0 | **Contour A → Contour B acceptance gate is not closed.** Contour B product work remains prohibited until Contour A is deployed, independently qualified and explicitly accepted with traceable evidence. | Master roadmap §5 and DEC-DEV-08; owner packet; current qualification truth. | Preserve the hard gate. No product implementation in Contour B until required Contour A deployment and independent acceptance evidence exist. | BLOCKING |
| MH-ARCH-009 | P1 | **Traceability and placement artifacts remain proposals.** Unified traceability matrix and node/service placement register are marked PROPOSED / NOT ACCEPTED / NOT FROZEN; they cannot be used as accepted implementation contracts. | Traceability matrix SHA `43e495aae6b4dc55a0d2e07fa4723d364898a5c1`; placement register SHA `59107fd6d7b8a73d671098adcf2824c310642907`. | Resolve prerequisite owner decisions and primary-source conflicts; submit bounded documents for domain-owner/governance acceptance and freeze before using them as implementation authority. | OPEN |
| MH-ARCH-010 | P1 | **Cross-branch drift is material.** Docs branch is 808 commits ahead and 2 behind `main`; there are source wording differences and branch-only corrections. A broad merge/rebase/cherry-pick would combine a large, diverged history and is not justified by this audit. | Live compare: `main` `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; docs branch `0f4be9c11c9f09e1283bd03fd997ad7c0110e706`; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. | Do not integrate branches as a shortcut. Use a file-level change-control queue with exact base SHA, owner/source approval, narrow diff, review and post-write readback for each authorized main change. | DIVERGED / NO INTEGRATION |
| MH-ARCH-011 | P1 | **Project map and continuation artifacts are large and append-heavy.** Map ≈686 KB, checkpoint ≈274 KB and traceability matrix ≈303 KB. They provide extensive provenance but increase retrieval cost and make duplicated/obsolete conclusions harder to notice. | Live docs-branch files; map SHA `128747b623e9ca34f36796b1aa2923ab0a533895`; checkpoint SHA `b41c1019df4c106c1000865f6d0c00eec559a0d7`; traceability SHA `43e495aae6b4dc55a0d2e07fa4723d364898a5c1`. | Preserve historical entries; do not truncate history. Add a short current-state index and a single prioritized remediation register (this document), then link old wave reports rather than repeating full conclusions. Consider archival/indexing only under approved documentation policy. | MAINTAINABILITY RISK |
| MH-ARCH-012 | P2 | **Repeated basenames require classification, not blanket deletion.** The refreshed docs-branch inventory contains 24 distinct case-insensitive basename-collision groups, representing 44 path occurrences beyond the first path for each basename. These groups include 18 MH-03 pairs; expected conventions (`README.md`, `SKILL.md`, `__init__.py`); and three non-MH-03 pairs requiring classification. The exact count supersedes the earlier estimate of 37; this count does not mean 24 semantic defects. No case-only collision of complete repository paths was found. | Current tree: docs ref `6326b659d62177585e8a58f49e52f8546fdd242e`, 904 entries / 827 blobs, `truncated=false`; main tree `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`, 798 entries / 721 blobs. Same-basename examples: mesh capability schema `d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c` vs domain capability schema `fe80659b570ac58829f10410feb5c700388f87c0`; launch-agent plist `2cca029b502fd911ec38272871c823a8717ed8fd` vs `d1d8aea99c2303c26e542a3d1c5e54b4596521d0`; mesh state model `d02780894cfb5d3c0fc7878d57a08fac2e428efc` vs runtime StateAuthority interface `a2115b81f52a63feb357e484bd982a6a32641d81`. | Maintain a per-group classification: expected package/document convention, intentionally distinct schema, distinct Python responsibility, potentially co-installable deployment manifests, or divergent copy. Do not rename/delete by basename alone. The `capability.schema.json` pair has distinct `$id` and object semantics; the `state.py` pair serves different purposes. | INVENTORY CONFIRMED; CLASSIFICATION PARTIAL |
| MH-ARCH-013 | P1 | **Qualification status remains blocked; required rounds are criteria, not evidence.** Current Truth has G0–G11 BLOCKED and overall NOT_PROVEN / BLOCKED. The 23-round-per-path, 115-round aggregate and 24-hour soak requirements do not prove those activities occurred or passed. | [Current Truth](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/qualification/CURRENT-TRUTH.generated.md), SHA `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`; launch schema; qualification blueprint. | Preserve fail-closed status. Only authorized, fresh, immutable evidence and the required independent A3/human gates can change qualification status. | NOT_PROVEN / BLOCKED |
| MH-ARCH-014 | P2 | **Broad static integrity does not prove CI/test health or runtime behavior.** Existing governance invariant enforcement references were path-checked; tests, workflows, credentials, services and host state were not exercised in this pass. | Wave 06 audit and live repository tree. | After explicit authorization, plan a separate read-only/test qualification wave with scope, commands, target SHA, expected outputs, evidence storage and rollback boundaries. Until then, do not claim tests pass or the runtime is healthy. | UNVERIFIED |
| MH-ARCH-024 | P1 | **MH-03 lifecycle/acceptance mirror coverage diverges.** Root and nested lifecycle documents have different transition/failure detail; root acceptance criteria list explicit acceptance conditions, while nested criteria add a fuller gate set and evidence/decision-register review. Both copies remain PROPOSED/NOT ACCEPTED. This confirms coverage asymmetry, not by itself an incompatible invariant. | Root lifecycle `architecture/MH-03-lifecycle.md` SHA `300363a06fe678d3511c2a4b843678bf200df5f0`; nested lifecycle `docs/architecture/mh-03/MH-03-lifecycle.md` SHA `41baa81406dcd25b8b1537adf9c8b1289c38edcd`; root acceptance `architecture/MH-03-acceptance-criteria.md` SHA `e96adaac2eb52e2f8058cc889485ec982bf606e5`; nested acceptance `docs/architecture/mh-03/MH-03-acceptance-criteria.md` SHA `eefb645d89c7c3046636d8344515aa02b7ccebe3`; root index `architecture/MH-03-index.md` SHA `b2d2eeb1b89117d10605c231e79378eebc437c5f` is PROPOSED and no nested index exists. | Preserve both trees. Compare remaining clause-level behavior and dependencies; after owner/governance selects root, nested, or governed synchronized views, reconcile with source anchors and inbound-reference/ID checks. Do not promote acceptance status from either copy. | CONFIRMED ASYMMETRIC COVERAGE; AUTHORITY OPEN |
| MH-ARCH-016 | P1 | **Functional Baseline 1.0 authority/version conflict across branches.** The same path has materially different documents: `main` blob `9df4892ed0734050ac79732603d15bb414717310` is a 68-section historical edition 1.0 passport; the docs branch blob `1a2f06f50dd69990be58b12a98376b92f12fd14f` is a much shorter document declaring itself `NORMATIVE / SINGLE SOURCE OF TRUTH`. Accepted Functional Baseline 2.0 explicitly supersedes Baseline 1.0 as current functional reference. | `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` on both refs; `docs/checkpoints/mediahub-functional-baseline-2.0.md` on `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`. | Do not rewrite or delete either branch's baseline in this pass. Preserve Baseline 2.0 as canonical; obtain provenance/owner disposition for the docs-branch rewrite, then label the branch copy as historical/superseded or restore a traceable historical artifact through a separately authorized narrow change. Check inbound links and historical IDs before any consolidation. | CONFIRMED CROSS-BRANCH AUTHORITY CONFLICT |

## 3. Previously repaired documentation defects

These are recorded as repaired only on the documentation branch; they are not global closure:

1. **Map navigation collisions:** seven duplicate numbered section IDs were repaired by preserving first occurrences, assigning unique IDs to later headings and fixing a self-reference. Verified map SHA: `128747b623e9ca34f36796b1aa2923ab0a533895`; the wave-06 report records the collision table and post-write checks.
2. **ASTRA component-scheme duplicated numeric threshold:** docs branch now refers to `runtime_thresholds.max_parallel_autonomous_claims` and its schema authority instead of duplicating the numeric value. Current docs component scheme SHA: `d321565a6e0fac1eef329adec67a35ba795b63aa`. `main` still contains the old value 2.
3. **Administrative questions:** the existing owner decision packet contains ADMIN-01…ADMIN-04 with options and recommendations. They are proposals, not owner decisions.

## 4. Prioritized development sequence

### Wave 0 — Establish the controlled decision queue (P0, documentary)

- Use this plan as the single prioritized cross-cutting register; retain prior reports as evidence sources, not competing master plans.
- Refresh source refs/SHA immediately before every subsequent change.
- Preserve the canonical Baseline 2.0, the Contour A/B boundary, historical IDs and fail-closed status.
- Do not integrate branches; no merge/rebase/cherry-pick is part of this wave.

**Exit:** every P0/P1 issue has one owner/authority, exact source anchors, an explicit state and a next evidence/decision action.

### Wave 1 — Owner/governance decisions (P0)

1. **ADMIN-01 / MH-ARCH-001:** select DEC-DEV-02 A/B/C lifecycle ownership model. Recommendation in existing owner packet: C as safe interim boundary unless a single delegated lifecycle can be proven and accepted.
2. **ADMIN-02 / MH-ARCH-007:** appoint a qualified independent P0-07 D2 reviewer or explicitly defer; no review is fabricated.
3. **ADMIN-03 / MH-ARCH-004:** choose a governed meaning/versioning model for design readiness vs runtime truth.
4. **ADMIN-04 / MH-ARCH-010:** choose a controlled source-change route for main/docs wording, without authorizing broad branch integration.
5. **ADMIN-05 / MH-ARCH-003:** confirm field-level source-of-truth ownership for numeric thresholds; current recommendation is launch schema as numeric authority, governance as registry/mirror with fail-closed drift checking.

**Exit:** attributable owner/governance decisions exist for the questions that are actually ripe; no recommendation is silently promoted.

### Wave 2 — P0-07 / P0-05 / P0-04 trust and change-control chain (P0)

- Trace existing caller → authenticated principal → trusted context issuer/lifecycle → operation/scope → P0-04 canonical mutation → revision/evidence path.
- Separate D1, D2, D3, D4, D5, D6 and D7 closure criteria; do not collapse them into one generic “security passed”.
- Obtain the independent D2 R-01…R-06 review and separate owner/governance disposition.
- Resolve the D6 normative-text status only with exact acceptance evidence; do not edit a DRAFT header by inference.
- Preserve P0-07 mutation/publication BLOCKED until accepted contract/API and evidence close the gap.

**Exit:** exact end-to-end source/evidence binding and governed contracts; otherwise explicit BLOCKED with remaining unknowns.

### Wave 3 — Canonical ASTRA contract and cross-branch repair (P1)

- Reconcile concurrency wording in `main` against the current launch-schema authority and add assertions that include the component scheme.
- Resolve the governance contract purpose/authority-source wording and equality checks.
- Separate design maturity and live qualification status; document model version lineage.
- Reconcile A0 scope only after DEC-DEV-02 governance disposition.
- Submit narrow, source-reviewed changes through the authorized route; reread all changed files and record resulting blob/commit SHAs.

**Exit:** one machine-readable authority per field, no contradictory normative prose, and no false runtime-ready label.

### Wave 4 — Duplicate document families and link/ID integrity (P1/P2)

- Compare all 18 MH-03 basename pairs; document per-file authority, provenance, status, consumers and required synchronization.
- Classify the 24 basename-collision groups / 44 extra path occurrences recorded in Wave 09 as expected package layout, separate artifacts, historical copies or defects; do not equate same basename with duplicate content.
- Continue Markdown relative-link/path and section-ID scans across the map-selected architecture/checkpoint sources.
- Preserve old IDs and use redirects/provenance notes where consolidation is approved.

**Exit:** duplicate-family inventory with an explicit disposition for every pair and no unresolved ambiguous canonical references in the scoped set.

### Wave 5 — Evidence-backed qualification and acceptance (P0; authorization required)

- Only after explicit permission, define a bounded test/qualification plan; do not run it merely because this plan lists it.
- Verify governance invariant tests, schema/drift checks, relevant workflow contracts and evidence freshness on an exact target SHA.
- Preserve separate statuses for design, implementation, tests, verification, qualification, release, deployment and acceptance.
- Contour B remains blocked until Contour A deployment, independent qualification and explicit acceptance are evidenced.

**Exit:** all required gates have fresh, attributable PASS evidence and human authorization; otherwise remain NOT_PROVEN / BLOCKED.

## 5. Administrative decision block

Reply with the existing ID and option letter. The recommendation is not adopted unless the owner explicitly selects it. These questions consolidate the existing owner packet; they do not create new normative decision IDs.

### ADMIN-01 — DEC-DEV-02 lifecycle authority
- **A:** Jarvis owns the cross-system engineering task lifecycle; ASTRA is a bounded execution/qualification adapter.
- **B:** ASTRA owns a bounded lifecycle explicitly delegated by Jarvis through an accepted typed contract, scope, revocation and fencing semantics.
- **C (safe interim recommendation):** strictly disjoint Jarvis/ASTRA lifecycle domains until a reviewed delegation contract exists.
- **No response:** keep OPEN_CONFLICT; no authority expansion or implementation.

### ADMIN-02 — P0-07 D2 independent review
- **A (recommended):** appoint a qualified independent reviewer and record competence, independence/conflicts, exact proposal/source SHAs, R-01…R-06 dispositions and attributable sign-off.
- **B:** defer; D2 stays NOT EVIDENCED and mutation/publication stays BLOCKED.
- **No response:** same fail-closed state.

### ADMIN-03 — ASTRA design-status semantics
- **A (recommended):** retain the current enum only as design/model readiness; Current Truth alone reports live runtime gate state.
- **B:** approve a versioned schema/model change to explicitly separate design maturity and runtime qualification, including consumer updates.
- **C:** defer changes; treat runtime qualification as NOT_PROVEN / BLOCKED.
- **No response:** no status promotion.

### ADMIN-04 — main/docs source correction route
- **A (recommended):** authorize a minimal file-level change request for specifically approved wording only, with before/after SHA and review; no broad branch integration.
- **B:** require architecture review/rewording before proposing a source change.
- **C:** defer and preserve the drift as open.
- **No response:** no main changes, merge, rebase or cherry-pick.

### ADMIN-05 — numeric threshold authority
- **A (recommended):** launch schema is the numeric authority; governance contract is the registry/mirror, with equality checks and fail-closed drift handling.
- **B:** governance contract becomes the sole numeric authority; revise schema authority fields and consumers under controlled governance.
- **C:** keep both files but define field-level ownership and require mismatch to block qualification.
- **No response:** current explicit schema authority remains the working interpretation, but no disputed value is silently changed.

### Decisions deliberately not re-asked
- P0-05 D6 remains defer/request evidence; do not infer normative acceptance from implementation-tree acceptance.
- Existing P0-05 D1–D7 owner directions remain in force.
- DEC-DEV-01 and DEC-DEV-03/04/05/06/07 retain their recorded evidence prerequisites.
- DEC-DEV-08 is a binding Contour A → Contour B gate, not a discretionary bypass.
- Baseline 2.0 remains accepted/canonical/immutable; Baseline 1.0 remains historical.

## 6. Linked evidence register

- [Project-wide architecture integrity sweep wave 06](MEDIAHUB-PROJECT-WIDE-ARCHITECTURE-INTEGRITY-WAVE-06-2026-10-14.md) — map IDs, tree coverage, ASTRA contracts, admin questions.
- [ASTRA source-of-truth reconciliation wave 05](MEDIAHUB-ASTRA-SOURCE-OF-TRUTH-RECONCILIATION-WAVE-05-2026-10-14.md) — threshold authority wording and prior correction.
- [ASTRA cross-branch source-drift wave 04](MEDIAHUB-ASTRA-CROSS-BRANCH-SOURCE-DRIFT-WAVE-04-2026-10-14.md) — main/docs A0 and concurrency drift.
- [DEC-DEV-01…08 crosswalk validation wave 01](MEDIAHUB-DEC-DEV-01-08-CROSSWALK-VALIDATION-WAVE-01-2026-10-14.md) — placement/lifecycle authority findings.
- [P0-07 D2 trusted-context authority/lifecycle proposal](P0-07-D2-TRUSTED-CONTEXT-AUTHORITY-LIFECYCLE-PROPOSAL-2026-10-13.md) — review proposal and blank independent-review worksheet.
- [Owner decision packet 01](MEDIAHUB-OWNER-DECISION-PACKET-01.md) — existing decision options and recommendations.
- [Unified system traceability matrix](mediahub-unified-system-traceability-matrix-v0.1.md) — cross-contract evidence links; proposed/not accepted/not frozen.
- [Node/service placement and decision register](MEDIAHUB-NODE-SERVICE-PLACEMENT-AND-DECISION-REGISTER-01.md) — placement and DEC-DEV prerequisites.

## 7. Guardrails and closure semantics

- A finding is closed only by exact source evidence, authorized change or attributable owner/governance decision appropriate to that finding, followed by readback verification.
- Documentation cleanup is not implementation. Static source inspection is not a test. A blank worksheet is not an independent review. A workflow definition is not a successful workflow run.
- No tests, qualification, host/runtime inspection, credentials, model/provider calls, installation, infrastructure change, deployment, migration, merge, rebase or cherry-pick were performed as part of this plan.
- No main-branch normative file was changed.
- **Current overall status remains: architecture globally NOT ACCEPTED / qualification NOT_PROVEN / BLOCKED.**

## 8. Wave 07 addendum — test-contract alignment (2026-10-14)

This pass read back the current docs-branch topology/drift tests and paired ASTRA model. It was static inspection only; no test runner was invoked.

### Additional confirmed finding

| ID | Priority | Finding | Evidence | Required disposition | State |
|---|---|---|---|---|---|
| MH-ARCH-015 | P0 | **A drift test hard-codes the disputed A0 state-authority claim.** `tests/test_astra_gold_architecture_drift.py` asserts `qualification.authority.state_authority == "A0-ASTRA"` and `unified.authority.astra.role == "single_coordination_authority"` (test blob `d6a0e6a6d81dc6e15e343cd80ee950431b1e3b14`). Those assertions encode the same disputed interpretation identified in MH-ARCH-001 rather than checking a settled, owner-approved boundary. A green result from this test could not establish that the lifecycle/product-state authority conflict is resolved. | Paired model YAML blob `193f81eb3cf463ebc38c6b2c3fca8c19e502f176`; component-scheme conflict and owner packet refs listed in MH-ARCH-001. | After owner disposition of DEC-DEV-02, update the contract and test assertions together. Before that decision, do not change the normative value by inference; make the unresolved authority boundary explicit and keep the associated acceptance gate blocked. | CONFIRMED TEST-CONTRACT RISK / OWNER-BLOCKED |

### Additional consistency observations

- The topology test on the docs branch now checks the schema/governance/model numeric mirror for concurrency and asserts that selected prose no longer repeats the number (test blob `1362ff8723a63e3594a3559c97dc9e3091d0c674`). This is source-code inspection only; the test was not run, so no pass claim is made.
- The paired Markdown architecture remains version 1.0 (`architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.md`, blob `610a611f42d19a55ab7a172e00068c40c5ce5da5`) while its paired YAML model is version 1.1 (blob `193f81eb3cf463ebc38c6b2c3fca8c19e502f176`). This may be intentional semantic-versioning/format lineage, but the source set does not establish that relationship clearly enough; it remains within MH-ARCH-004 and requires explicit lineage metadata or a documented compatibility rule.
- The YAML top-level status `QUALIFICATION_READY_HYBRID_FABRIC` is now accompanied by a comment distinguishing design/model readiness from live qualification. This improves wording but does not reconcile status enums or change `CURRENT-TRUTH.generated.md`, which remains `NOT_PROVEN / BLOCKED`.
- The source test explicitly asserts version 1.1 for YAML and the source links for reference/schema. That validates the YAML model's own expected version, not the relationship between the paired Markdown and YAML documents.
- No normative contract was changed in this addendum. The remediation plan remains `WORKING / NOT ACCEPTED / NOT FROZEN`; no test, qualification, runtime inspection or branch integration was performed.


### Wave 08 addendum — Baseline 1.0 cross-branch authority drift (2026-10-14)

- Compared the exact same path on both live refs. `main` blob `9df4892ed0734050ac79732603d15bb414717310` is 33,711 characters and identifies itself as the historical 68-section Functional Baseline 1.0 passport. The docs-branch blob `1a2f06f50dd69990be58b12a98376b92f12fd14f` is 14,527 characters and calls itself `NORMATIVE / SINGLE SOURCE OF TRUTH`.
- The accepted Functional Baseline 2.0 on `main` explicitly supersedes Baseline 1.0 as the current functional reference while retaining Baseline 1.0 as historical provenance. This makes the docs-branch Baseline 1.0 authority label materially misleading and a cross-branch source/provenance conflict.
- Added MH-ARCH-016 (P1). No baseline file was modified: provenance and owner disposition are required before any relabeling, restoration or consolidation. Baseline 2.0 remains canonical.
- Static/documentary finding only; no tests, qualification, runtime inspection or branch integration. Main and docs refs remain diverged.

## 9. Wave 09 — full repository path/duplicate and qualification-contract consistency sweep (2026-10-14)

### 9.1 Live repository inventory and branch coverage

- `main` HEAD: `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`.
- `docs/mediahub-chat-tree-map-20261012` HEAD at this pass: `6326b659d62177585e8a58f49e52f8546fdd242e`.
- Compare: DIVERGED; docs branch ahead 820 / behind 2; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- Main tree: 798 entries / 721 blob files, tree SHA `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`, not truncated.
- Documentation tree: 904 entries / 827 blob files, tree SHA `6326b659d62177585e8a58f49e52f8546fdd242e`, not truncated.
- Every path in the main tree also exists in the documentation tree; 106 blob paths exist only on the documentation branch. This is path coverage only: it does **not** mean same-path contents are equal. The two commits unique to `main` modify `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md`, whose main/docs blobs differ materially (see MH-ARCH-016).
- This was a full recursive path inventory with targeted content reads, not semantic line-by-line review of every file. No tests, CI workflows, runtime or host state were executed/inspected.

### 9.2 Complete basename-collision inventory and classification

- The tree scan found **24 distinct basename-collision groups** and **44 path occurrences beyond the first entry** for those repeated basenames. A prior working estimate of 37 is superseded. There are zero full-path case-insensitive/case-only collisions.
- Exact duplicate blob scan found one repeated-content group: ten zero-byte `__init__.py` package markers sharing blob `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391`. No other repeated blob-SHA groups were found. Same basename therefore must not be equated with duplicate content or a defect.
- The 24 groups are: 18 mirrored MH-03 pairs; 8 `README.md` files; 16 `__init__.py` package markers; 2 `SKILL.md` files; 2 `capability.schema.json` files; 2 `com.mediahub.astra.github-agent.plist` deployment manifests; and 2 `state.py` files. The group totals count unique basenames, while the repeated path counts above are the excess entries beyond one representative per group.
- `architecture/mesh/capability.schema.json` (`d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c`) and `schemas/domain/capability.schema.json` (`fe80659b570ac58829f10410feb5c700388f87c0`) are different contracts with different `$id`, required fields and semantics; do not merge them solely because the basename matches.
- `ops/mesh/state.py` (`d02780894cfb5d3c0fc7878d57a08fac2e428efc`) implements mesh node/replica lifecycle transitions; `runtime/mediahub_runtime/state.py` (`a2115b81f52a63feb357e484bd982a6a32641d81`) defines the canonical StateAuthority interface. These are distinct responsibilities, not duplicate implementations.

### 9.3 MH-03 divergent mirror pairs — all paths and blob SHAs

Each left path is under `architecture/`; its same-basename right path is under `docs/architecture/mh-03/`. All 18 blob-SHA pairs differ. This establishes divergent content bytes; it does not assert that every pair has been semantically reviewed.

| Basename | `architecture/` blob SHA | `docs/architecture/mh-03/` blob SHA |
|---|---|---|
| `MH-03-acceptance-criteria.md` | `e96adaac2eb52e2f8058cc889485ec982bf606e5` | `eefb645d89c7c3046636d8344515aa02b7ccebe3` |
| `MH-03-command-execution.md` | `b9197759e70107f1be5968e8669288d991360003` | `8a9e1066f00cf9a7a3128c00eada857b18cef32f` |
| `MH-03-contradiction-register.md` | `5879ad2ab19110ae7418f881cbd7603a10ff996e` | `7986b072983f1d6f828b7214f4896b91c91392f2` |
| `MH-03-decision-log.md` | `e202a60c48726a78b0e5b7d1c191f62cfd2caaa1` | `4089e4573a083adcde921acd8ac0bd09c98d6a2f` |
| `MH-03-degraded-mode.md` | `f724cedc52f7421c520c1183fa8e8e078fe93082` | `7b70229049b80a230b201806aab59f394e0d33bd` |
| `MH-03-error-handling.md` | `bd2157deb94c2823c6b6fac2988945b7bc412ef3` | `a33051aabb24447cf993755e84569917fe37f037` |
| `MH-03-event-model.md` | `bd7c50063c518f428217ca2e906c615017f02ae6` | `330b98cba91125ac6e57e662d4eebeb37b6df00a` |
| `MH-03-evidence-register.md` | `07dd464fe23ba91943053f658c8d804ec67b5fb6` | `865a1bda46984cd8b3384aaea99ec9f9c86746d4` |
| `MH-03-health-model.md` | `a4b9e8838d6b88ea629b9ee3642b6bcc791cba47` | `2f5840218dfdc0103e16721ebf467150d19cb216` |
| `MH-03-lifecycle.md` | `300363a06fe678d3511c2a4b843678bf200df5f0` | `41baa81406dcd25b8b1537adf9c8b1289c38edcd` |
| `MH-03-recovery-boundary.md` | `dd3746ab986a736af559d400f66f578d91aa4188` | `24f957fdc7070cd39ed4a116c5e1e0c40e912253` |
| `MH-03-runtime-dependencies.md` | `7bf2c9db634cfe149f8f6199d2eeae1813499be5` | `115dfbbf8d00b01865c4db4590f44a7f7a5eced7` |
| `MH-03-runtime-foundation.md` | `325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2` | `2457451017daa0f91e9e978e44c91e1e49d0d7a3` |
| `MH-03-runtime-model.md` | `03a3ce4837591827e5eb3e20e36214e394ffca82` | `d43d456f745f4503c6dc0ad3f76dbaf051940747` |
| `MH-03-runtime-observability.md` | `aa33cd18290bf486b19fad08f3a377aa5ed7a298` | `f7fba8708bc57eb8baa2d8ecc866fb58d18c9d6b` |
| `MH-03-service-boundaries.md` | `02672aa1c377d04a3a7e0a7cff5b767a89ee0fcb` | `cb9e5800d20ab3ee463bc30446419c95d556a87c` |
| `MH-03-shutdown-sequence.md` | `37d2dad130cb611799191bdbde5b4803adea37bb` | `cef347ea1e6ce02a38283aba4a47ae4353082f30` |
| `MH-03-startup-sequence.md` | `87ecefe90cb0f8c306682d31a8c6f613a2fcfcf9` | `a2fa93260f13f909c345319252a5b63440265ecc` |

The root index identifies the root-level filenames as its required artifacts, but its own status is PROPOSED. The nested directory has no `MH-03-index.md`. One direct semantic conflict is already confirmed: the root contradiction register records C03-08 as governance review required for a proposed PostgreSQL/etcd/NATS HA path conflicting with the frozen single-node/in-memory foundation; the nested copy states that no current explicit contradictions were identified. Keep this family P1 and ask for controlled source disposition rather than silently choosing one version.

### 9.4 Additional confirmed findings

| ID | Priority | Finding | Evidence | Required action | State |
|---|---|---|---|---|---|
| MH-ARCH-017 | P1 | **ASTRA G4 mandatory-path matrix differs between machine schema and prose.** The canonical launch schema defines five mandatory paths: `CODEX_FCC`, `CLAUDE_FCC`, `CODEX_OMNIROUTE`, `CLAUDE_OMNIROUTE`, `CLAUDE_CODE_DIRECT`. The unified Markdown G4 section says “every mandatory execution path” but enumerates only the three Claude paths. This is distinct from the three permanent Claude production lanes: qualification path inventory and permanent runtime pool are different concepts. | Main schema blob `aef6229477ed8ec45e45170f98ea87f7ba75ca29`; docs schema `0b86b07dfa916d4485ce1f8f54d19de136d98491`; main unified Markdown `e2067dc41b52983fc4e0b2549fb6af3c099cbc60`; docs Markdown `610a611f42d19a55ab7a172e00068c40c5ce5da5`; schema test `090ce2ecb02e58a3c48a7a729279dea9a387f339`. | Make prose reference the canonical mandatory-path list (or enumerate the full five-path contract), and add an exact test assertion that prevents the prose/schema sets from drifting. Preserve the separate three-lane production topology. | CONFIRMED CONTRACT/PROSE MISMATCH |
| MH-ARCH-018 | P1 | **Two launch-agent manifests share one LaunchAgent label but invoke different programs and environments.** If both are installed in the same macOS launchd domain, label collision/overwrite or ambiguous service ownership is possible. Installation state was not inspected, so co-installation is not asserted. | `deploy/com.mediahub.astra.github-agent.plist` blob `2cca029b502fd911ec38272871c823a8717ed8fd` launches `/usr/bin/python3 /opt/mediahub/astra/astra_github_agent.py`; `ops/launchd/com.mediahub.astra.github-agent.plist` blob `d1d8aea99c2303c26e542a3d1c5e54b4596521d0` launches `/bin/bash /Users/voktor/astra-work/ops/astra-github-bootstrap.sh`; both use `com.mediahub.astra.github-agent`. | Classify manifests as mutually exclusive deployment profiles or assign distinct labels if they represent separate services; document canonical owner and prevent accidental co-installation. Requires target/operations owner confirmation; no host was inspected. | CONFIRMED MANIFEST COLLISION / DEPLOYMENT UNKNOWN |
| MH-ARCH-019 | P1 — repaired in docs branch | **Project-map navigation IDs had collisions at both the original three nested headings and a later appended MH-03 wave.** Wave 06's first broad check missed mixed heading levels; a later appended section reused `20.185`, creating a new duplicate after the earlier fix. | Original pre-fix map `19e775bc581229dad48e7d603a74202eb9f12fab`; second pre-fix map `e3eadac3f1f36cae870d694bb25ae2150775a726`. Original IDs: `20.97`, `20.98`, `20.183`; reintroduced ID: `20.185`. | Original headings rekeyed to `20.98.1`, `20.98.2`, `20.184.1`; later MH-03 drift heading rekeyed `20.185` → `20.204`; complete wave 09 entry is `20.205`. All heading levels were rescanned after the final write. Navigation-only; no source-contract meaning changed. | PATCH APPLIED; FINAL READ-BACK VERIFIED (2026-10-14) |
| MH-ARCH-020 | P2 | **File-basename collisions that are not duplicate contracts need explicit classification.** The two capability schemas have distinct IDs/semantics; the two `state.py` files serve mesh lifecycle versus product StateAuthority interface. | Schema SHAs and state module SHAs listed in §9.2. | Keep them separate; where discoverability is ambiguous, clarify path/namespace in the index and verify consumer references before any rename. | DISTINCT RESPONSIBILITIES / NAMING RISK |
| MH-ARCH-021 | P1 | **MH-03 mirror-family governance/status drift exceeds the known contradiction-register conflict.** The proposed root index lists root-level artifacts as required, but is itself PROPOSED; root/nested decision logs differ (root adds MH3-D10/D11 on future-governed persistence/HA), evidence registers differ in acceptance/implementation-authorization wording and E03-06 provenance, and the contradiction registers disagree on whether C03-08 is an active governance review. These are material status/lineage differences, not mere duplicate files. | Root index blob `b2d2eeb1b89117d10605c231e79378eebc437c5f`; root decision log `e202a60c48726a78b0e5b7d1c191f62cfd2caaa1`; nested decision log `4089e4573a083adcde921acd8ac0bd09c98d6a2f`; root evidence register `07dd464fe23ba91943053f658c8d804ec67b5fb6`; nested evidence register `865a1bda46984cd8b3384aaea99ec9f9c86746d4`; root contradiction register `5879ad2ab19110ae7418f881cbd7603a10ff996e`; nested contradiction register `7986b072983f1d6f828b7214f4896b91c91392f2`. | Keep both trees unchanged. Governance owner must explicitly designate canonical source or synchronized-view model, resolve status/decision/evidence deltas, and then reconcile all 18 pairs with provenance and reference checks. Root index supports root as intended location but is PROPOSED, so this is not sufficient authority to promote it. | CONFIRMED SOURCE/STATUS DRIFT; OWNER DISPOSITION REQUIRED |
| MH-ARCH-022 | P1 | **MH-03 runtime-foundation mirror pair has asymmetric contract coverage, but no direct semantic contradiction established in this pass.** Both files remain PROPOSED and agree on sole State Authority, in-memory state, mandatory P0-05 boundary, single-node/no-HA and no unauthorized physical persistence. The root copy adds an explicit offline-first chain, full command/event mutation path and enumerated acceptance gates; the nested copy adds shutdown ordering and technology-choice candidate wording. Root index lists root artifacts as required but is itself PROPOSED; it does not resolve canonical authority. | `architecture/MH-03-runtime-foundation.md` blob `325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2`; `docs/architecture/mh-03/MH-03-runtime-foundation.md` blob `2457451017daa0f91e9e978e44c91e1e49d0d7a3`; root index `architecture/MH-03-index.md` blob `b2d2eeb1b89117d10605c231e79378eebc437c5f`. | Preserve both files. Record this as scope/coverage drift, not a proven contradiction. Add a bidirectional clause crosswalk only after owner selects root canonical, nested canonical, or governed synchronized views. Check inbound references and acceptance-criteria paths before any sync/delete. | CONFIRMED ASYMMETRIC COVERAGE; CANONICAL AUTHORITY OPEN |
| MH-ARCH-023 | P2 — repaired in docs branch | **Project map contained a legacy duplicate top-level numeric heading ID `16`.** The earlier Baseline 1.0 passport heading and its subsections use ID 16; a later `## 16. Owner decision register` reused that ID. | Pre-repair map blob `430a32472afa5df6511c6458be09b931d7b8bbba`, duplicate heading at line 3821; earlier heading at line 498. Current map blob in verification `7dea16102dbc1908906d89b4637f90f196a15f4d`. | Preserved historical `16`; rekeyed the later heading to `20.208`; map repair record is `20.209`. Map-local scan found no inbound fragment reference to `#16-owner-decision-register`; repository-wide fragment audit remains open. Anchored scan across Markdown headings 1–6 counted 263 numeric section headings, all 263 IDs unique, zero duplicates (191 level-2 and 72 level-3 headings). Earlier broader count of 282/281 is not comparable until its matching rule is reproduced. | PATCH APPLIED; READ-BACK VERIFIED / REPOSITORY-WIDE FRAGMENT AUDIT OPEN |

### 9.5 Updated prioritized sequence

1. **P0 security/authority:** ADMIN-01 lifecycle authority and P0-07 D1/D2/D3/D5/D6/D7 gaps; commission qualified independent D2 R-01…R-06 review; keep mutation/publication blocked until contract and evidence close the chain.
2. **P1 source-control/ASTRA:** ADMIN-03/04/05; reconcile the main-only concurrency text 2 vs canonical schema 3; resolve A0 scope only after DEC-DEV-02; fix the G4 five-vs-three mandatory-path prose discrepancy under controlled source review; clarify paired YAML/Markdown model version/status lineage.
3. **P1 MH-03 source family:** resolve the intended root vs nested documentation location; inspect references/IDs; then issue an explicit source-of-truth/redirect or controlled content reconciliation for all 18 pairs. Do not delete historical content.
4. **P1 deployment manifest:** ask the target/operations owner to classify whether the two same-label LaunchAgent files are alternative profiles or distinct services. No runtime/host inspection or installation was performed.
5. **P1/P2 documentation integrity:** retain the map's hierarchical heading-ID repair and perform a fresh full-level scan; classify all 24 repeated-basename groups without treating conventional README/skill/package markers as defects.
6. **P0 qualification/acceptance:** after explicit authorization, define a separate test/qualification wave against exact SHA. Current Truth stays G0–G11 BLOCKED / NOT_PROVEN; Contour B remains gated.

### 9.6 Additional administrative questions for owner/governance

These questions do not create new normative DEC IDs. Existing ADMIN-01…ADMIN-05 remain in §5.

**MH-03 source family — what is the authoritative disposition?**
- **A (recommended):** Treat root `architecture/MH-03-*.md` as the intended canonical location because `architecture/MH-03-index.md` lists those filenames; after provenance/link review, label nested counterparts as historical/derived redirects and reconcile material deltas.
- **B:** Declare `docs/architecture/mh-03/` canonical and update the root index/pointers only through a governed change.
- **C:** Keep both as explicit separate views with a named owning source and required synchronization/evidence; no path may be cited as accepted until that rule is recorded.
- **Recommendation:** A is the strongest existing-source interpretation but remains a proposal because the root index itself is PROPOSED and content conflict exists.

**LaunchAgent manifests — how should the same-label profiles be governed?**
- **A:** Declare one manifest canonical and mark the other obsolete/non-coinstallable, preserving history.
- **B:** They represent distinct deployment profiles/services; give each its own label and explicit target/owner in a separately authorized change.
- **C (safe interim):** Treat them as mutually exclusive examples until the operations owner confirms intended target; do not install both or infer active service state.
- **Recommendation:** C until the target/operations owner resolves intended use; then A or B based on evidence.

### 9.7 Scope and non-claims

- The tree scan is complete and untruncated at the listed refs; semantic review remains risk-based and targeted.
- Selected navigation-critical files were link-checked and had no missing relative paths at the earlier checked revisions; the project-wide Markdown link graph has not been exhaustively validated.
- No tests, qualifications, CI runs, runtime/host inspection, credential/provider/model calls, installation, infrastructure change, deployment, migration, merge, rebase or cherry-pick were performed.
- Current main qualification truth remains G0–G11 BLOCKED / overall NOT_PROVEN. Baseline 2.0 remains canonical, Baseline 1.0 remains historical provenance, and Contour B remains blocked.



### 9.8 Map heading-ID repair — independent read-back (2026-10-14)

- Re-fetched the current documentation-branch map at blob `05980cf0dcd96dffcc59aa981cd1a8e2c311ea9c` and scanned all Markdown headings whose section number begins the heading title.
- Counted 257 numbered section headings; found **zero duplicate section IDs**. Confirmed the intended nested IDs `20.98.1`, `20.98.2`, and `20.184.1` are present.
- An exploratory broad regex initially flagged `20.68` twice because a later heading's prose title references “§20.68”; this is not a duplicate section ID. The anchored section-number scan removes that false positive.
- The first three nested-heading collisions were fixed and verified at map blob `05980cf0dcd96dffcc59aa981cd1a8e2c311ea9c`. Wave 09 later appended an MH-03 drift heading reusing existing ID `20.185`; this created a second collision, now fixed by rekeying that appended heading to `20.204` and adding project-wide wave 09 at `20.205`. Final map blob after recheck is `020969a87b3a1701e5d484fe76c93f2db9e240b9`. This read-back does not claim a full Markdown-link-graph audit or semantic review of every file.


### 9.9 MH-03 contradiction-register pair — source-anchored classification (2026-10-14)

- Read the root index, root and nested contradiction registers, decision logs, and evidence registers from the live documentation branch. No source files in either MH-03 tree were modified.
- The root index lists root-level filenames as required artifacts, but the index status is PROPOSED / NOT ACCEPTED. This is evidence of intended placement, not an accepted canonical-source decision.
- Root contradiction register records C03-08 as GOVERNANCE REVIEW REQUIRED for the proposed PostgreSQL/etcd/NATS HA path conflicting with the inherited single-node/in-memory foundation; the nested register says no current explicit contradictions were identified.
- Root decision log adds MH3-D10/D11 (future governance-gated persistence/HA and non-authoritative technology integration) absent from the nested decision log. Root/nested evidence registers also differ materially in status language, including “ACCEPTED / IMPLEMENTATION AUTHORIZED” in nested E03-01 versus PROPOSED in the root register.
- Added MH-ARCH-021. Classification: confirmed source/status drift; no conclusion that one copy is authoritative. Preserve both copies pending owner disposition. Next decision required: canonical root source, canonical nested source, or explicitly governed synchronized views.

### 9.10 Final map heading-ID verification after wave 09 (2026-10-14)

- Before-fix map blob: `e3eadac3f1f36cae870d694bb25ae2150775a726`. An anchored scan found a duplicate level-2 ID `20.185`: the original P0-07 canonical-read join trace and a newly appended MH-03 source/status drift entry. The appended section had reused a historical ID.
- Corrected only the project map: preserved the original `20.185` heading, changed the appended MH-03 drift entry to `20.204`, updated map incremental-update metadata to `§20.205`, and added a summary of the Wave 09 unified audit at `§20.205`.
- Read-back map blob: `020969a87b3a1701e5d484fe76c93f2db9e240b9`; update commit `1bbceb26656bb3da7fa23468ff8a2e32fd245174`.
- The initial post-wave-09 scan exposed a second appended heading reusing `20.204` (the separate unified-passport consolidation entry added after the scan input was read). This was corrected by rekeying the passport heading to `20.206`, preserving `20.204` for the MH-03 source/status finding and `20.205` for wave 09. The final anchored read-back on map blob `261910c6a2827036dc3ecd23ed4a8aa25216768b` counted 260 numeric headings, 260 unique IDs and zero duplicates. Any broader Markdown link-graph defect remains outside this check.
- The unified plan remains the single current remediation register. No normative MH-03 file, baseline, ASTRA gate source or `main` file was changed; this map repair does not decide which MH-03 tree is canonical.

### 9.11 Final collision count after concurrent map addition (2026-10-14)

- A subsequent live read found the unified-passport consolidation heading had been appended with ID `20.204`, duplicating the MH-03 mirror-family heading. The map now has monotonic terminal IDs `20.203` (Baseline 1.0 drift), `20.204` (MH-03 source/status drift), `20.205` (Wave 09 project-wide audit), and `20.206` (unified passport consolidation).
- The duplicated passport heading was changed only to `20.206`; map metadata now identifies the latest verified incremental entry as §20.206.
- Final map read-back blob `261910c6a2827036dc3ecd23ed4a8aa25216768b`; 260 numbered section headings across levels 2–4, all 260 IDs unique, zero collisions.
- This resolves only the map heading-ID collision. It does not declare the complete Markdown link graph clean or any architecture accepted/frozen.



### 9.12 MH-03 runtime-foundation pair — bounded scope/provenance comparison (2026-10-14)

**Sources re-fetched from** `docs/mediahub-chat-tree-map-20261012`:
- Root index `architecture/MH-03-index.md`, blob `b2d2eeb1b89117d10605c231e79378eebc437c5f`, status PROPOSED; lists root-level artifacts as required.
- Root runtime foundation `architecture/MH-03-runtime-foundation.md`, blob `325cf6b47e7db926b8e45d9517e3a2f1d8e7ffa2`, status PROPOSED.
- Nested runtime foundation `docs/architecture/mh-03/MH-03-runtime-foundation.md`, blob `2457451017daa0f91e9e978e44c91e1e49d0d7a3`, status PROPOSED.

**Observed alignment:** both files state that State Authority is the sole canonical mutation authority, current state is in-memory, P0-05 is the mandatory boundary, the foundation is single-node/no-HA, physical persistence is not authorized, commands are requests and events are facts, and State Authority failure does not create fallback authority.

**Observed scope asymmetry:** the root file explicitly enumerates the offline-first deterministic chain, a full command → validation → authorization/policy → consumer contract → State Authority → event → observers path, and several acceptance prerequisites. The nested file adds a shutdown ordering and an explicit statement that technology choices remain CANDIDATE until evidence/compatibility/security/architecture decision. These differences are not by themselves proof of contradiction, but they mean neither file is a byte-identical mirror or complete substitute for the other.

**Disposition:** MH-ARCH-022 records confirmed asymmetric coverage, not a semantic conflict. The root index's required-artifact list is evidence of intended placement only; its PROPOSED status does not confer canonical authority. Both files remain unchanged. This was not an exhaustive inbound-reference search and does not decide the canonical tree. Next: extend the provenance/reference inventory to one additional pair, while owner/governance disposition remains required before reconciliation.

### 9.13 Core-document relative-link path check (2026-10-14)

- Refreshed the complete, non-truncated documentation-branch tree at `010546262e58c5a1b5b0fe2569b443ef6b7559a9` (904 tree entries / 827 blobs).
- Re-fetched the current exact blobs for the single remediation plan (`e2419c2d0dd7be7df09dcebe6e95bf1c7eb7d1b9`), map (`261910c6a2827036dc3ecd23ed4a8aa25216768b`), roadmap (`bed279bb26f6cea99a9217198ac18f0731998dba`) and checkpoint (`ac63eec13e8ce034d8e77750438159f7503d51c0`).
- Parsed Markdown inline link targets and resolved repository-relative paths against the correct documentation-branch tree. Counts: plan 14 relative links, map 98, roadmap 10, checkpoint 29. All **151 inspected relative links resolve to existing repository paths**; no missing-path target was found in these four core documents.
- Scope limitation: this verifies resolved path existence, not fragment/heading anchors, generated links, raw HTML links, or the complete link graph across all repository files. It is not a semantic or runtime check.
- The single remediation plan remains the current issue register. This check created no new defect ID and does not change any acceptance/qualification status.



### 9.14 Project-map duplicate numeric heading ID — follow-up repair (2026-10-14)

- The map scan on pre-repair blob `430a32472afa5df6511c6458be09b931d7b8bbba` confirmed that `## 16. Owner decision register — 2026-10-12` reused the earlier Baseline 1.0 passport section ID `16`. The later heading has now been rekeyed to `20.208`.
- MH-ARCH-023 is a documentation/navigation defect, not an architecture-contract conflict. The map-only scan found no explicit inbound fragment reference, but other repository documents were not exhaustively searched.
- Read-back verification on map blob `7dea16102dbc1908906d89b4637f90f196a15f4d`: metadata points to §20.209; heading `20.208` is unique; the anchored heading-number scan found 263 headings / 263 unique IDs / zero collisions. The previous 282/281 scan has a different or undocumented matching scope and is not reused as a current verified count. No normative contract or `main` source is in scope.


### 9.15 MH-03 lifecycle and acceptance-criteria mirror review (2026-10-14)

- Refreshed the exact root/nested lifecycle and acceptance-criteria blobs on `docs/mediahub-chat-tree-map-20261012`; compared headings, status labels, lifecycle/failure semantics, acceptance prerequisites and the root index. This is a bounded source comparison, not a complete audit of every clause in all 18 pairs.
- Root lifecycle (`architecture/MH-03-lifecycle.md`, `300363a06fe678d3511c2a4b843678bf200df5f0`) explicitly lists READY dependency readiness, optional-dependency DEGRADED behavior, recovery inside existing authority boundaries, and no shadow state/fallback mutation on State Authority failure. Nested lifecycle (`docs/architecture/mh-03/MH-03-lifecycle.md`, `41baa81406dcd25b8b1537adf9c8b1289c38edcd`) summarizes READY/DEGRADED/recovery and adds a repeated-failure no-authority-escalation constraint, but omits some explicit root statements.
- Root acceptance criteria (`architecture/MH-03-acceptance-criteria.md`, `e96adaac2eb52e2f8058cc889485ec982bf606e5`) enumerate acceptance conditions and contradiction review. Nested criteria (`docs/architecture/mh-03/MH-03-acceptance-criteria.md`, `eefb645d89c7c3046636d8344515aa02b7ccebe3`) explicitly enumerate gates and evidence/decision-register review and articulate the required runtime/State Authority outcome.
- Both sets remain PROPOSED / NOT ACCEPTED; root `architecture/MH-03-index.md` (`b2d2eeb1b89117d10605c231e79378eebc437c5f`) is also PROPOSED and lists root artifacts, while no nested index exists. This does not establish accepted canonical authority.
- Added MH-ARCH-024 as **asymmetric coverage confirmed; direct contradiction not established by this pass**. No MH-03 source was modified, deleted or promoted. Remaining 18-pair reconciliation requires owner/governance choice and reviewed inbound-reference/ID checks.
- Live refs at start of this pass: `main` HEAD `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; docs branch HEAD `547f8558f5f56d7eab15433974d9cc28909eef37`; branch comparison remains DIVERGED, ahead 854 / behind 2, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. These counts are snapshot-specific and must be refreshed before future writes.
- No tests, CI, qualification, runtime/host inspection, credentials/provider/model calls, installations, infrastructure changes, deployment, migration, merge, rebase or cherry-pick were performed.
