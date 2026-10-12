# MH-24 — Supplemental Atom-Level Crosswalk: Baseline 1.0 §19 (AI Human Clone) — Draft 01

- **Date:** 2026-10-12
- **Working ref:** `docs/mediahub-chat-tree-map-20261012`
- **Status:** DOCUMENTARY DRAFT / SEMANTIC OWNER ACCEPTANCE OPEN / NOT A CANONICAL BACKLOG
- **Scope:** B1 §19, lines 313–330 at pinned B1 SHA `9df4892ed0734050ac79732603d15bb414717310`.
- **Purpose:** create source-anchored traceability for the dedicated AI Human Clone section without treating the section's requirement fragments as independently approved product requirements.
- **ID rule:** all `PROVISIONAL/AHC-xx` labels are temporary traceability labels only. No final `MH24-B04-...` child IDs are minted. Preserve the existing high-level `AI-HUMAN-CLONE-01` from Semantic Audit Batch 03 and the Batch 08 cross-link `CDAI4-02 / B1-17-05`; do not overwrite either history.
- **B1:** `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, SHA `9df4892ed0734050ac79732603d15bb414717310`, §19 lines 313–330.
- **B2:** `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, especially §§3, 5–7, 15–18.
- **Historical semantic finding:** `docs/checkpoints/MH24-SEMANTIC-AUDIT-BATCH-03.md` @ this branch, SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`, §2 entry `AI-HUMAN-CLONE-01`. It identifies the safeguards as a high-risk candidate semantic gap, not an accepted clone contract.
- **Related cloud cross-link:** Batch 08 draft `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-08-DRAFT.md`, SHA `a978d6846b747f397b266dc0befa05fc22cdd7ab`; Review 01 SHA `2c088f1837b8e5c6d257bc1b33ae3be0dedd938b`. B1-17-05 treats AI Human Clone as one named Cloud Development AI subsystem entry; it is retained as a cross-link, not merged with all §19 safeguards.
- **Domain sources:** MH-10 master `docs/architecture/MH-10-CHAT-MASTER-PROMPT.md@main`, SHA `6ea847ddbf1604878303572b21b506102b23c930`; MH-12 acceptance `docs/architecture/MH-12-acceptance-criteria.md@main`, SHA `40f37f1600c4730e622480d57bd492fa67f9ca4b`; MH-21 master `docs/architecture/MH-21-CHAT-MASTER-PROMPT.md@main`, SHA `61d552db4d1a1abefa2cef9f44eebcf634d11111`; MH-21 acceptance `docs/architecture/MH-21-acceptance-criteria.md@main`, SHA `582f898fe4be332b6a7fef3e8cca2e27c7328ac2`; MH-21 evidence register SHA `6bc646902395f690554604b39b16464de796c724`; MH-18 acceptance `docs/architecture/MH-18-acceptance-criteria.md@mh-18-media-content-architecture-handoff-v2`, SHA `1ce114d92ce401609d536138982a4c89408064dc`.
- **Owner schema:** Product Owner Decision Record 01, SHA `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd`. The 12-field schema/status vocabulary is approved; these individual mappings, acceptance criteria and backlog promotion are not approved.
- **Current matrix:** `docs/checkpoints/mediahub-mh24-traceability-matrix.md` @ working ref, SHA `73377891072bac3c739c44055ceeb0874154f64c`. Row 19 is a section-level summary, not a complete AI Human Clone contract.

## Mapping rules used in this draft

- `MAPPED` means a pinned B2 clause explicitly documents the same bounded capability or constraint; it is never implementation or qualification evidence.
- `NO_DIRECT_COUNTERPART` is scoped only to the named first-class subsystem requirement in the B2 clauses reviewed here. It is not a global repository-absence claim.
- `NOT_REVIEWED` is retained where B2 has related/general concepts but does not establish clone-specific semantics, acceptance criteria or lifecycle.
- `CONFLICT` is not assigned without explicit contradictory normative text.
- B2 §6's generic authorization/revocation vocabulary, §15 media rights and §17 artifact provenance/licensing are related controls but do not establish a complete human-likeness consent and rights contract.
- B2 §18 explicitly states that AI cannot directly obtain physical authority, canonical state authority or security bypass. That bounded non-authority constraint is recorded as documentary correspondence; it does not accept the entire AI Human Clone section.
- The 15 labels below are provisional traceability subdivisions, not 15 distinct independently approved product requirements. The owner-level requirement `AI-HUMAN-CLONE-01` remains the historical umbrella.

## Provisional atom records

### AHC-01 — Named first-class subsystem

- **Requirement ID:** `PROVISIONAL/AHC-01` (temporary traceability label; not a final child ID).
- **Owner:** TBD; no accepted AI Human Clone subsystem owner was established in the checked sources.
- **Source atom / classification:** B1 §19 line 315 — LITERAL: AI Human Clone is a separate Cloud Development AI subsystem and is described as an authorized digital clone participating in media creation.
- **B2 mapping status:** `NO_DIRECT_COUNTERPART` for the exact named first-class subsystem in B2 §§3, 5–7, 15–18. Those clauses contain related AI/media/privacy/identity controls but do not establish the named subsystem and its complete bounded contract.
- **Canonical contract path/ref:** No accepted AI Human Clone contract verified. Relevant sources: B2 §§3, 5–7, 15–18 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; MH-10/12/21 sources listed above.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: owner explicitly preserves, revises or defers the named subsystem; if preserved, define its owner, intended use, interfaces, allowed inputs/outputs and boundaries against ordinary media/AI features.
- **Required evidence:** Explicit owner/governance disposition; versioned subsystem contract; dependency and threat-boundary review; acceptance/evidence register.
- **Lifecycle status:** DRAFT / NOT APPROVED; design, implementation, verification, qualification and release remain OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`; D-05 schema approval only. No per-atom acceptance recorded.
- **Dependencies:** MH-10; MH-12; MH-13 privacy path unresolved in the referenced audit; MH-18; MH-21; MH-20/22 for provenance and qualification gates.
- **Verification method:** Compare the exact B1 §19 line 315 with pinned B2 sections and inspect an accepted first-class subsystem contract before changing the status.
- **Change history:** Supplemental row linked to historical `AI-HUMAN-CLONE-01` and `CDAI4-02 / B1-17-05`; neither prior artifact is overwritten. No final ID minted.

### AHC-02 — Intended media-generation scope

- **Requirement ID:** `PROVISIONAL/AHC-02`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §19 lines 317–325 — LITERAL purpose list: visual/audio-visual representation, video, presentation, educational, marketing and commercial media use.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §15 lists general local-first audio/video and media capabilities subject to capability and rights. It does not specify AI-generated human-likeness outputs or the permitted clone use cases.
- **Canonical contract path/ref:** No accepted clone-specific use-scope contract verified; B2 §15 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; MH-18 acceptance SHA `1ce114d92ce401609d536138982a4c89408064dc`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define allowed media modalities and use cases, prohibited uses, audience/distribution restrictions and review requirements per use.
- **Required evidence:** Approved use-case matrix, prohibited-use policy and per-modality acceptance criteria.
- **Lifecycle status:** DRAFT / NOT APPROVED; semantic coverage and media qualification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03 `AI-HUMAN-CLONE-01`; MH-18 remains NOT ACCEPTED / NOT FROZEN.
- **Dependencies:** MH-10; MH-12; MH-13; MH-18; MH-21.
- **Verification method:** Compare the literal B1 use list with B2 §15 and an accepted clone-specific contract; do not treat generic video support as cloned-likeness approval.
- **Change history:** Source list retained as one grouped purpose atom to avoid asserting every example as a separate normative requirement.

### AHC-03 — Subject consent

- **Requirement ID:** `PROVISIONAL/AHC-03`.
- **Owner:** TBD; human-subject/rights-holder accountability is not assigned in the checked documents.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: consent is mandatory.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §§5–7 contain general privacy, authorization and trust controls but do not explicitly define informed, recorded, scoped consent for AI-generated human likeness.
- **Canonical contract path/ref:** No accepted clone-consent contract verified; B2 §§5–7 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; MH-12 acceptance SHA `40f37f1600c4730e622480d57bd492fa67f9ca4b`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define valid consent, identity of consenting party, authorized uses, recording/versioning, expiry and denial behavior before content generation.
- **Required evidence:** Consent model/schema, authorization flow, negative tests for absent/expired/withdrawn consent, and independent privacy/security approval. Tests are required evidence later, not executed by this draft.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and verification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03 §2, `AI-HUMAN-CLONE-01`; MH-12 acceptance remains unsatisfied.
- **Dependencies:** MH-12; MH-13; MH-10; MH-21.
- **Verification method:** Confirm the exact B1 consent clause against B2 text; require an accepted subject-consent contract and negative-path evidence before mapping promotion.
- **Change history:** High-risk control; no inferred acceptance from generic authorization language.

### AHC-04 — Authorization

- **Requirement ID:** `PROVISIONAL/AHC-04`.
- **Owner:** TBD; authorization decision owner and enforcement boundary remain unspecified for this subsystem.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: authorization is mandatory in addition to consent.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §6 lists general authorization, but does not define clone-specific permission checks or bind them to the requested subject, assets, use and destination.
- **Canonical contract path/ref:** No accepted AI Human Clone authorization contract verified; B2 §6 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; MH-10 master SHA `6ea847ddbf1604878303572b21b506102b23c930`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define the policy authority, decision inputs, grant scope, evaluation point and fail-closed behavior.
- **Required evidence:** Authorization matrix and interface, denial/expiry/replay cases, and audit linkage to the exact media request.
- **Lifecycle status:** DRAFT / NOT APPROVED; policy, implementation and verification OPEN.
- **Reviewer / approval reference:** D-05 approves schema/vocabulary only; MH-12 remains governance review required.
- **Dependencies:** MH-10; MH-12; MH-13; MH-18; MH-21.
- **Verification method:** Demonstrate that general B2 authorization has an accepted clone-specific decision contract before changing status.
- **Change history:** Kept distinct from consent; one does not substitute for the other.

### AHC-05 — Identity provenance

- **Requirement ID:** `PROVISIONAL/AHC-05`.
- **Owner:** TBD; identity/provenance contract owner for the subject and likeness is not confirmed.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: identity provenance is mandatory.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §6 includes device/node identity and trust, but the reviewed text does not define human-subject identity provenance for generated likeness.
- **Canonical contract path/ref:** No accepted human-identity provenance contract verified; B2 §6 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define subject identity assertion, verification method, provenance records, uncertainty and correction/revocation linkage without exposing unnecessary identity data.
- **Required evidence:** Identity provenance schema, access/privacy rules and reviewable lineage from verified subject identity to authorized generation request.
- **Lifecycle status:** DRAFT / NOT APPROVED; verification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; MH-12 security/trust acceptance remains open.
- **Dependencies:** MH-12; MH-13; MH-10; MH-21.
- **Verification method:** Distinguish human identity provenance from infrastructure/device identity in B2 §6; require a scoped accepted contract.
- **Change history:** No inference from device/node identity rows to human identity coverage.

### AHC-06 — Rights-holder authorization

- **Requirement ID:** `PROVISIONAL/AHC-06`.
- **Owner:** TBD; rights-holder role, delegation and authority proof are unspecified.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: rights-holder authorization is mandatory.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §15 references DRM, rights and vendor restrictions; §17 requires authorization/licensing review for Engineering and Digital Twin artifacts. Neither clause defines rights-holder authorization for synthetic human likeness.
- **Canonical contract path/ref:** No accepted rights-holder contract verified; B2 §§15/17 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; MH-18 acceptance SHA `1ce114d92ce401609d536138982a4c89408064dc`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: identify rights holder(s), permitted rights and territories/duration/use, delegated authority and conflict resolution before generation or publication.
- **Required evidence:** Rights/authorization model, license/rights record, scope validation and invalid/contradictory-grant cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; policy and legal/rights acceptance OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; MH-18 remains NOT ACCEPTED / NOT FROZEN.
- **Dependencies:** MH-12; MH-13; MH-18; MH-21.
- **Verification method:** Compare the B1 rights-holder requirement with general B2 rights/licensing text; do not infer equivalent semantics from topic overlap.
- **Change history:** Specific rights-holder control remains separate from general request authorization.

### AHC-07 — Scope limitation

- **Requirement ID:** `PROVISIONAL/AHC-07`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: an explicit scope is mandatory.
- **B2 mapping status:** `NOT_REVIEWED`; general workload/policy scoping does not specify which subjects, media, purposes, channels, audiences, duration or reuse are allowed for the clone.
- **Canonical contract path/ref:** No accepted clone scope contract verified; B2 §§5–7/18 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: bind every operation to explicit purpose, input assets, output types, audience, distribution, expiration and downstream reuse limits.
- **Required evidence:** Machine-readable scope schema, policy evaluation, negative cases for out-of-scope requests and change/renewal records.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and verification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; no specific owner acceptance recorded.
- **Dependencies:** MH-10; MH-12; MH-13; MH-18; MH-21.
- **Verification method:** Inspect the accepted authorization contract and prove that effective scope is evaluated at generation and publication boundaries.
- **Change history:** Separate scope from the existence of a general authorization grant.

### AHC-08 — Voice and appearance authorization

- **Requirement ID:** `PROVISIONAL/AHC-08`.
- **Owner:** TBD; the authorized subject and relevant rights holders must be identified by an accepted contract.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: voice/appearance authorization is mandatory.
- **B2 mapping status:** `NOT_REVIEWED`; B2 media and identity sections do not explicitly define separate permissions for voice and visual likeness generation.
- **Canonical contract path/ref:** No accepted voice/appearance authorization contract verified; B2 §§6, 15, 18 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: separately represent authorized voice and appearance modalities and permitted uses; fail closed where either required grant is missing, expired or revoked.
- **Required evidence:** Modality-specific permission model and negative-path evidence for cross-modal or out-of-scope use.
- **Lifecycle status:** DRAFT / NOT APPROVED; acceptance and enforcement OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03 identifies this as an unclosed safeguard; MH-12 acceptance remains unsatisfied.
- **Dependencies:** MH-12; MH-13; MH-18; MH-21.
- **Verification method:** Verify modality-specific grants against the exact B1 clause; general media capability is not authorization.
- **Change history:** Voice and appearance remain explicitly traceable; no modality equivalence inferred.

### AHC-09 — Model provenance

- **Requirement ID:** `PROVISIONAL/AHC-09`.
- **Owner:** TBD; model-registry and generation-service ownership are not accepted for this subsystem.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: model provenance is mandatory.
- **B2 mapping status:** `NOT_REVIEWED`; B2 identifies qualified model registries and supply-chain review, but the checked clauses do not specify provenance for the model/version used in a human-likeness generation.
- **Canonical contract path/ref:** No accepted clone model-provenance contract verified; B2 §§7, 18, 21 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: bind each generation result to model identity/version, source lineage, provider/runtime, policy/configuration and relevant model approval.
- **Required evidence:** Model provenance record, version pinning, supply-chain review and replay/audit link to generation output.
- **Lifecycle status:** DRAFT / NOT APPROVED; evidence and qualification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; B2 supply-chain gates do not accept this subsystem.
- **Dependencies:** MH-10; MH-12; MH-20; MH-21; MH-22.
- **Verification method:** Confirm a generation record links exact model/version and policy to each output; don't treat model-registry presence as clone acceptance.
- **Change history:** Model provenance remains distinct from asset provenance.

### AHC-10 — Asset provenance

- **Requirement ID:** `PROVISIONAL/AHC-10`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: asset provenance is mandatory.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §17 requires provenance for Engineering/Digital Twin artifacts, but the inspected clauses do not define lineage for a person's source media, derivative assets and generated outputs.
- **Canonical contract path/ref:** No accepted human-likeness asset provenance contract verified; B2 §§7, 15, 17, 23 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: preserve source asset identity, rights/consent linkage, transformations, generated derivatives and deletion/revocation dependencies.
- **Required evidence:** Asset lineage model, immutable source references, allowed retention/access policy and derivative/revocation propagation rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; design, implementation and verification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; no clone-specific artifact-provenance acceptance found.
- **Dependencies:** MH-12; MH-13; MH-18; MH-20; MH-21.
- **Verification method:** Compare the asset lineage chain against the B1 requirement and accepted media/provenance contract.
- **Change history:** No assumption that general Engineering/Digital Twin provenance covers synthetic human likeness.

### AHC-11 — Auditability

- **Requirement ID:** `PROVISIONAL/AHC-11`.
- **Owner:** TBD; audit/evidence owner and retention authority remain unresolved for this subsystem.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: audit is mandatory.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §6 and §7 reference audit as a general security/data class, but clone-specific events, payload-minimization and evidence retention are not defined.
- **Canonical contract path/ref:** No accepted clone audit contract verified; B2 §§6–7 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define auditable request, consent/authorization result, policy decision, model/assets, output digest, publication/distribution action, revocation and deletion events without retaining unnecessary personal payloads.
- **Required evidence:** Audit event schema, integrity/access controls, retention/deletion policy and traceability from request to result.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation and evidence verification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; MH-12 acceptance requires audit coverage and remains governance-review required.
- **Dependencies:** MH-12; MH-13; MH-18; MH-20; MH-21.
- **Verification method:** Compare general audit controls with the required clone lifecycle; verify minimum necessary audit evidence and retention semantics.
- **Change history:** Audit necessity preserved as a separate control from provenance and revocation.

### AHC-12 — Revocation

- **Requirement ID:** `PROVISIONAL/AHC-12`.
- **Owner:** TBD; decision authority, propagation scope and revocation SLA are unspecified.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: revocation is mandatory.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §6 lists generic revocation, but does not specify revocation of clone consent, voice/appearance permissions, source-asset grants, existing derivatives or publication permissions.
- **Canonical contract path/ref:** No accepted AI Human Clone revocation contract verified; B2 §6 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define who may revoke, how it is authenticated, what becomes blocked immediately, how cached/generated/published derivatives are handled and how completion is confirmed.
- **Required evidence:** Revocation state machine, downstream dependency inventory, propagation/negative-path evidence and recovery rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; no clone-specific revocation acceptance found.
- **Dependencies:** MH-12; MH-13; MH-18; MH-20; MH-21.
- **Verification method:** Confirm revocation blocks future use and defines applicable handling for existing derivatives; generic identity revocation alone is not sufficient proof.
- **Change history:** Revocation remains separate from initial consent and authorization.

### AHC-13 — Real/synthetic separation

- **Requirement ID:** `PROVISIONAL/AHC-13`.
- **Owner:** TBD; disclosure/presentation policy owner is not accepted.
- **Source atom / classification:** B1 §19 line 326 — LITERAL control: real and synthetic representations must be separated.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §§15 and 18 cover media rights and AI non-authority, but the checked text does not explicitly prescribe synthetic-media disclosure, persistent labeling or separation from authentic media.
- **Canonical contract path/ref:** No accepted real/synthetic separation contract verified; B2 §§15, 18 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define disclosure/labeling in metadata, presentation and export, plus rules for transformations that remove or detach a label.
- **Required evidence:** Label/metadata schema, end-to-end export/display rules and negative cases for missing or invalid synthetic-status metadata.
- **Lifecycle status:** DRAFT / NOT APPROVED; acceptance and enforcement OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03; no accepted synthetic disclosure contract verified.
- **Dependencies:** MH-10; MH-12; MH-13; MH-18; MH-21.
- **Verification method:** Trace synthetic status from generation to stored asset, export and display; general AI non-authority is not equivalent to real/synthetic labeling.
- **Change history:** Specific synthetic-media disclosure is kept separate from general AI authority.

### AHC-14 — No authority elevation

- **Requirement ID:** `PROVISIONAL/AHC-14`.
- **Owner:** MediaHub State Authority / AI architecture owner for the authority-boundary portion; final named-subsystem owner remains TBD.
- **Source atom / classification:** B1 §19 line 328 — LITERAL control: AI Human Clone is not State Authority, system authority or Smart Home authority and cannot independently manage MediaHub.
- **B2 mapping status:** `MAPPED` for the bounded non-authority constraint only: B2 §3 defines canonical/Smart Home authority boundaries and §18 states AI cannot directly obtain physical authority, canonical state authority or security bypass. This is documentary correspondence, not implementation evidence or acceptance of the clone subsystem.
- **Canonical contract path/ref:** B2 §§3, 4, 18 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; MH-10 master SHA `6ea847ddbf1604878303572b21b506102b23c930`.
- **Acceptance criteria:** Existing architecture boundary remains authoritative: any requested product-state change must re-enter the MediaHub policy/authorization/command/consumer/State Authority path; clone outputs and agents cannot mutate canonical state or bypass HA/security policy.
- **Required evidence:** Source review is recorded here; implementation-stage evidence would require authority-boundary and negative-path verification at the exact implementation SHA, if separately authorized.
- **Lifecycle status:** ARCHITECTURAL RULE DOCUMENTED; implementation conformance and qualification OPEN.
- **Reviewer / approval reference:** B2 accepted baseline; MH-10 master prompt. No AI Human Clone-specific implementation approval inferred.
- **Dependencies:** MH-03 / State Authority; MH-05 Smart Home boundary; MH-10; MH-12.
- **Verification method:** Compare the exact B1 prohibition with B2 §§3/18 and the MH-10 mutation path; do not infer product-state authority from output generation, identity, or storage.
- **Change history:** First bounded documentary `MAPPED` row in this draft; does not change other AHC row statuses.

### AHC-15 — Not a replacement for the real person

- **Requirement ID:** `PROVISIONAL/AHC-15`.
- **Owner:** TBD; product/governance owner for representation and disclosure boundaries remains open.
- **Source atom / classification:** B1 §19 line 328 — LITERAL control: the AI Human Clone is not a replacement for a real person.
- **B2 mapping status:** `NOT_REVIEWED`; the B2 AI non-authority rule does not by itself define product/representation limits or prohibit presenting synthetic identity as the real person.
- **Canonical contract path/ref:** No accepted human-likeness representation/disclosure contract verified; B2 §§6, 15, 18 @ `main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define identity claims the system may make, prohibited impersonation/misrepresentation behaviors, user-facing disclosure and how these remain bound to authorization scope.
- **Required evidence:** Approved representation policy, display/export disclosure criteria, and reviewable negative cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; semantic acceptance, implementation and qualification OPEN.
- **Reviewer / approval reference:** Semantic Audit Batch 03 `AI-HUMAN-CLONE-01`; no clone-specific policy acceptance recorded.
- **Dependencies:** MH-10; MH-12; MH-13; MH-18; MH-21.
- **Verification method:** Compare the literal no-replacement rule with B2's general AI and media boundaries; require an accepted clone-specific policy before changing status.
- **Change history:** Kept separate from the non-authority constraint; no broader B2 equivalence inferred.

## Initial mapping disposition

- Rows: 15 provisional traceability labels.
- Distribution: **1 MAPPED / 13 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT**.
- No stable child IDs are minted; no collision inventory is claimed.
- `AI-HUMAN-CLONE-01` and Batch 08 `CDAI4-02 / B1-17-05` remain intact as historical/high-level cross-links.
- MH-12 acceptance remains governance-review required; MH-21 remains NOT ACCEPTED / NOT FROZEN / NOT PRODUCTION READY; MH-18 remains NOT ACCEPTED / NOT FROZEN. These gate states are not modified by this draft.
- This document has not been independently reviewed. All mapping/acceptance decisions remain provisional. B1, B2, the working traceability matrix, the canonical backlog and `main` are unchanged.

## 20.62a — Duplicate-path reconciliation notice (2026-10-12)

**Status:** NON-AUTHORITATIVE PARALLEL DRAFT — RETAINED FOR PROVENANCE; DO NOT USE AS THE ACTIVE BATCH 10 CROSSWALK.

A fresh read-back during project-map recovery discovered that the active working Batch 10 crosswalk already exists at `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-10-AI-HUMAN-CLONE-DRAFT.md`, blob SHA `44b9369fea0be06e4e64f2052fd49f6d493f6603`, with its own Review 01 (`36148379d7d1e39252bd918ad17772036cf0d972`) and semantic Review 02 (`612162b164b7d2585fa9646871839274cec5a343`). Those records contain 19 provisional labels, preserve the existing B1 §17 / Batch 08 identity lineage, and are the active crosswalk record set indexed by the current working Passport and Contract.

This differently named `BATCH-10-DRAFT.md` was created in the current continuation before that pre-existing artifact path was discovered. Its 15-row AHC-01…AHC-15 label set duplicates only part of the same §19 scope and uses a different temporary label scheme. It is preserved rather than deleted, but **must not** be counted, merged into, used to revise, or cited as the current Batch 10 mapping distribution. Do not mint child IDs from this file. Continue to use the established `BATCH-10-AI-HUMAN-CLONE-DRAFT.md` and its Reviews 01/02.

This correction is a provenance/disambiguation notice only; it does not alter the canonical working Batch 10 draft, any owner decision, Baseline 1.0/2.0, the matrix or the canonical backlog. The map is the navigation authority and must record this duplicate explicitly.

