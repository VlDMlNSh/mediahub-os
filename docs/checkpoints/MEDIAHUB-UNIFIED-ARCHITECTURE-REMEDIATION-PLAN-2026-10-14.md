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
| MH-ARCH-005 | P1 | **MH-03 document-family duplication with divergent contents.** 18 case-insensitive basename collisions exist between `architecture/MH-03-*.md` and `docs/architecture/mh-03/MH-03-*.md`. Four sampled pairs (lifecycle, runtime model, acceptance criteria, decision log) have different blob SHAs and different text, so these are not byte-identical copies; authoritative location and synchronization rules are unclear from the sampled files. | Examples: lifecycle `300363a06fe678d3511c2a4b843678bf200df5f0` vs `41baa81406dcd25b8b1537adf9c8b1289c38edcd`; runtime model `03a3ce4837591827e5eb3e20e36214e394ffca82` vs `d43d456f745f4503c6dc0ad3f76dbaf051940747`; acceptance `e96adaac2eb52e2f8058cc889485ec982bf606e5` vs `eefb645d89c7c3046636d8344515aa02b7ccebe3`; decision log `e202a60c48726a78b0e5b7d1c191f62cfd2caaa1` vs `4089e4573a083adcde921acd8ac0bd09c98d6a2f`. | Compare all 18 pairs, identify the normative/current location for each artifact, classify historical snapshots versus active sources, then add an explicit redirect/provenance header or a governed consolidation proposal. Do not delete either family before provenance and inbound references are checked. | CONFIRMED DIVERGENT FAMILY; SCOPE OPEN |
| MH-ARCH-006 | P0 | **P0-07 trusted-context and mutation/publication path remains unproven.** Existing evidence does not demonstrate an accepted trusted issuer/provisioner lifecycle or end-to-end P0-07 → P0-05 → P0-04 request/context/resource/revision binding. D1 is NOT DEMONSTRATED; D2 NOT EVIDENCED; D3/D4/D5 remain evidence-gated; D6 is open; D7 change-control ownership remains open. | [D2 proposal](P0-07-D2-TRUSTED-CONTEXT-AUTHORITY-LIFECYCLE-PROPOSAL-2026-10-13.md), SHA `39400abce88da7ea54be7d9d7505f215eba43408`; [traceability matrix](mediahub-unified-system-traceability-matrix-v0.1.md), SHA `43e495aae6b4dc55a0d2e07fa4723d364898a5c1`; owner register. | Continue source tracing only where it can prove an existing path. Otherwise route the proposal to governance. Keep P0-07 mutation/publication blocked and P0-05 v1.1 NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN. | BLOCKED |
| MH-ARCH-007 | P0 | **Qualified independent P0-07 D2 review is absent.** R-01…R-06 worksheet in the D2 proposal is blank; an internal desk review and source routing are not an independent review. | D2 proposal §13, SHA `39400abce88da7ea54be7d9d7505f215eba43408`; [crosswalk wave 01](MEDIAHUB-DEC-DEV-01-08-CROSSWALK-VALIDATION-WAVE-01-2026-10-14.md). | Owner/governance appoints a qualified independent reviewer or defers. Record competence, independence/conflicts, exact proposal/source SHAs, itemized R-01…R-06 dispositions and attributable sign-off. | WAITING OWNER / REVIEWER |
| MH-ARCH-008 | P0 | **Contour A → Contour B acceptance gate is not closed.** Contour B product work remains prohibited until Contour A is deployed, independently qualified and explicitly accepted with traceable evidence. | Master roadmap §5 and DEC-DEV-08; owner packet; current qualification truth. | Preserve the hard gate. No product implementation in Contour B until required Contour A deployment and independent acceptance evidence exist. | BLOCKING |
| MH-ARCH-009 | P1 | **Traceability and placement artifacts remain proposals.** Unified traceability matrix and node/service placement register are marked PROPOSED / NOT ACCEPTED / NOT FROZEN; they cannot be used as accepted implementation contracts. | Traceability matrix SHA `43e495aae6b4dc55a0d2e07fa4723d364898a5c1`; placement register SHA `59107fd6d7b8a73d671098adcf2824c310642907`. | Resolve prerequisite owner decisions and primary-source conflicts; submit bounded documents for domain-owner/governance acceptance and freeze before using them as implementation authority. | OPEN |
| MH-ARCH-010 | P1 | **Cross-branch drift is material.** Docs branch is 808 commits ahead and 2 behind `main`; there are source wording differences and branch-only corrections. A broad merge/rebase/cherry-pick would combine a large, diverged history and is not justified by this audit. | Live compare: `main` `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; docs branch `0f4be9c11c9f09e1283bd03fd997ad7c0110e706`; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. | Do not integrate branches as a shortcut. Use a file-level change-control queue with exact base SHA, owner/source approval, narrow diff, review and post-write readback for each authorized main change. | DIVERGED / NO INTEGRATION |
| MH-ARCH-011 | P1 | **Project map and continuation artifacts are large and append-heavy.** Map ≈686 KB, checkpoint ≈274 KB and traceability matrix ≈303 KB. They provide extensive provenance but increase retrieval cost and make duplicated/obsolete conclusions harder to notice. | Live docs-branch files; map SHA `128747b623e9ca34f36796b1aa2923ab0a533895`; checkpoint SHA `b41c1019df4c106c1000865f6d0c00eec559a0d7`; traceability SHA `43e495aae6b4dc55a0d2e07fa4723d364898a5c1`. | Preserve historical entries; do not truncate history. Add a short current-state index and a single prioritized remediation register (this document), then link old wave reports rather than repeating full conclusions. Consider archival/indexing only under approved documentation policy. | MAINTAINABILITY RISK |
| MH-ARCH-012 | P2 | **Repeated basenames require classification, not blanket deletion.** The 798-path inventory has 37 case-insensitive basename collisions. Many are expected (README, `__init__.py`, package directories); some may be parallel representations (e.g. mesh capability schema, launch-agent plist) and must be judged by schema IDs, consumers and deployment role, not name alone. | Recursive main tree `cbb1862fcb4aa22ba24fea4ff12b580ffb305593`; examples `architecture/mesh/capability.schema.json` SHA `d9360b62520aabd2fa8d74a2b74bf3fc328c9c7c` vs `schemas/domain/capability.schema.json` SHA `fe80659b570ac58829f10410feb5c700388f87c0`; `deploy/com.mediahub.astra.github-agent.plist` SHA `2cca029b502fd911ec38272871c823a8717ed8fd` vs `ops/launchd/com.mediahub.astra.github-agent.plist` SHA `d1d8aea99c2303c26e542a3d1c5e54b4596521d0`. | Build a consumer/reference map and classify each pair as intentional parallel artifact, historical copy, generated output or defect. No automated deletion based on basename. | OPEN CLASSIFICATION |
| MH-ARCH-013 | P1 | **Qualification status remains blocked; required rounds are criteria, not evidence.** Current Truth has G0–G11 BLOCKED and overall NOT_PROVEN / BLOCKED. The 23-round-per-path, 115-round aggregate and 24-hour soak requirements do not prove those activities occurred or passed. | [Current Truth](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/qualification/CURRENT-TRUTH.generated.md), SHA `48d581a8f6a6a5fd380abbb7a7ce938b3b1e6731`; launch schema; qualification blueprint. | Preserve fail-closed status. Only authorized, fresh, immutable evidence and the required independent A3/human gates can change qualification status. | NOT_PROVEN / BLOCKED |
| MH-ARCH-014 | P2 | **Broad static integrity does not prove CI/test health or runtime behavior.** Existing governance invariant enforcement references were path-checked; tests, workflows, credentials, services and host state were not exercised in this pass. | Wave 06 audit and live repository tree. | After explicit authorization, plan a separate read-only/test qualification wave with scope, commands, target SHA, expected outputs, evidence storage and rollback boundaries. Until then, do not claim tests pass or the runtime is healthy. | UNVERIFIED |
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
- Classify all 37 basename collisions as expected package layout, separate artifacts, historical copies or defects; do not equate same basename with duplicate content.
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

