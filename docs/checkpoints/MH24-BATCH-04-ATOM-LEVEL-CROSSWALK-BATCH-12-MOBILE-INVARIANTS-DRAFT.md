# MH-24 — Supplemental Atom-Level Crosswalk: Baseline 1.0 §21 (Mobile Access Invariants) — Draft 01

- **Status:** DOCUMENTARY DRAFT / SEMANTIC OWNER ACCEPTANCE OPEN / NOT A CANONICAL BACKLOG.
- **Working ref:** `docs/mediahub-chat-tree-map-20261012`.
- **Scope:** B1 §21, literal source lines 361–374, pinned B1 SHA `9df4892ed0734050ac79732603d15bb414717310`.
- **Purpose:** crosswalk the mobile authority, bypass, contract/security and remote-command-path invariants separately from the B1 §20 application-role definitions.
- **B2:** `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; relevant §§2.3 (lines 63–72), 3–4 (authority), 5–7 (privacy/identity/security/data), 14 (Smart Home), 18 (AI authority boundary) and 22–23 (API/events/provenance).
- **Working matrix:** `docs/checkpoints/mediahub-mh24-traceability-matrix.md@docs/mediahub-chat-tree-map-20261012`, SHA `73377891072bac3c739c44055ceeb0874154f64c`, row 21 (Mobile invariants). Matrix status remains unchanged.
- **Schema authority:** Product Owner Decision Record 01 SHA `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd`; D-05 approves the 12-field schema/status vocabulary only.
- **Relationship to Batch 11:** Batch 11 crosswalks B1 §20 application roles and product-facing mobile functions; this Batch 12 draft covers B1 §21 invariants. Keep them separately traceable without treating either as implementation proof.
- **ID rule:** `PROVISIONAL/MAI-21-xx` labels are temporary traceability labels; no final child IDs are minted.

## Mapping rules used in this draft

- `MAPPED` records bounded textual correspondence only. It does not prove mobile-specific integration or enforcement.
- `NOT_REVIEWED` is retained where the general authority/API model does not define the concrete mobile command route or the precise enforcement behavior.
- `NO_DIRECT_COUNTERPART` is not used: B2 contains generic authority, contract and security rules relevant to these invariants.
- `CONFLICT` is not assigned without explicit contradictory normative text.
- All listed mobile controls remain subordinate to the single canonical MediaHub State Authority and the scoped Home Assistant Core authority for Smart Home.

## Provisional atom / traceability records

### MAI-21-01 — Mobile is not a separate authority

- **Requirement ID:** `PROVISIONAL/MAI-21-01` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Invariants owner is established in the inspected sources.
- **Source atom / classification:** B1 §21 lines 363–364 — LITERAL invariant: the Mobile Access Layer does not become a separate authority.
- **B2 mapping status:** MAPPED — bounded documentary correspondence: B2 §2.3 line 72 states no mobile application is an authority; B2 §3 identifies the canonical MediaHub State Authority and other domain authorities.
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`, §21 lines 361–374; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §§2.3 and 3.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: keep each mobile app a consumer/client surface; all canonical state mutation must pass through the relevant accepted authority/contract path.
- **Required evidence:** Authority and command-path contract; negative mobile mutation/bypass cases when implementation verification is separately authorized.
- **Lifecycle status:** DRAFT / NOT APPROVED; documentary rule mapped, implementation conformance OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 / B2 authority model; no mobile-specific runtime evidence provided.
- **Dependencies:** MH-03; MH-04; MH-09; MH-12; MH-13; MH-15.
- **Verification method:** Compare exact B1 line 364 with B2 §2.3 line 72 and §3; distinguish explicit architecture text from runtime enforcement.
- **Change history:** MAPPED is documentary only; no runtime test or qualification claimed.

### MAI-21-02 — No direct physical-device access bypassing MediaHub

- **Requirement ID:** `PROVISIONAL/MAI-21-02` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Invariants owner is established in the inspected sources.
- **Source atom / classification:** B1 §21 line 365 — LITERAL prohibition: Mobile Access must not directly access physical devices by bypassing MediaHub.
- **B2 mapping status:** NOT_REVIEWED
- **Canonical contract path/ref:** B2 §§3–4, 14, 18 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; B2 defines state/Smart Home authority and general anti-bypass boundaries but does not specify the concrete mobile-to-device command route or its enforcement.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define the only permitted device-command path from mobile through MediaHub's accepted API/policy and the domain's authority (including HA Core for Smart Home). Deny unsupported direct vendor/device routes.
- **Required evidence:** Versioned command/API contracts; mobile-to-device topology; authorization and policy boundaries; denied-path cases and integration evidence when authorized.
- **Lifecycle status:** DRAFT / NOT APPROVED; concrete route and enforcement OPEN.
- **Reviewer / approval reference:** No mobile-specific device-command integration contract verified in the bounded source set.
- **Dependencies:** MH-03; MH-04; MH-05; MH-09; MH-12; MH-15; MH-17.
- **Verification method:** Compare B1 line 365 with B2 §§3–4/14/18; generic non-authority language alone is not evidence of a particular command path.
- **Change history:** Keep NOT_REVIEWED until the mobile command route is explicit.

### MAI-21-03 — No alternative State Authority

- **Requirement ID:** `PROVISIONAL/MAI-21-03` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Invariants owner is established in the inspected sources.
- **Source atom / classification:** B1 §21 line 366 — LITERAL prohibition: Mobile Access must not create an alternative State Authority.
- **B2 mapping status:** MAPPED — bounded documentary correspondence: B2 §3 establishes a single logical MediaHub State Authority; B2 §4 line 103 confirms it as the sole canonical platform-state authority, and §2.3 says mobile apps are not authorities.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §§2.3, 3–4.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: prohibit shadow canonical state stores or independent mobile mutation authority; retain the one-authority model even when mobile operates offline or reconnects.
- **Required evidence:** State/data ownership map, API/command path, rejected-shadow-state cases and consistency contract.
- **Lifecycle status:** DRAFT / NOT APPROVED; documentary rule mapped; implementation conformance OPEN.
- **Reviewer / approval reference:** B2 authority model; no specific mobile runtime evidence provided.
- **Dependencies:** MH-03; MH-09; MH-14; MH-15.
- **Verification method:** Compare B1 line 366 with B2 §§3–4; do not infer code-level enforcement from the normative baseline.
- **Change history:** MAPPED records architecture correspondence only.

### MAI-21-04 — Use defined MediaHub contracts

- **Requirement ID:** `PROVISIONAL/MAI-21-04` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Invariants owner is established in the inspected sources.
- **Source atom / classification:** B1 §21 line 367 — LITERAL requirement: Mobile Access uses defined MediaHub contracts.
- **B2 mapping status:** MAPPED — bounded documentary correspondence: B2 §22 lines 438–446 states that domains communicate through versioned contracts and transport is subordinate to protocol semantics.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §22 lines 438–446; no complete Mobile Access API contract verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: identify the actual contracts applicable to local Core and Remote Access, including versioning, compatibility, authority, authorization, errors and lifecycle.
- **Required evidence:** Versioned mobile API contract inventory; schema/compatibility rules; contract evidence and approval record.
- **Lifecycle status:** DRAFT / NOT APPROVED; generic architecture rule mapped; mobile-specific contracts OPEN.
- **Reviewer / approval reference:** B2 §22; no explicit mobile contract catalogue verified.
- **Dependencies:** Compare B1 line 367 with B2 §22 and inspect any specific mobile-facing contract before claiming coverage.
- **Verification method:** MAPPED only for the general versioned-contract principle, not for a complete mobile API.
- **Change history:** 2026-10-12 — provisional atomization of B1 §21 line 367; B2 §22 supports only the generic versioned-contract principle; mobile-specific contracts remain OPEN; no final ID minted.

### MAI-21-05 — Authentication, authorization, trust, privacy, audit and revocation

- **Requirement ID:** `PROVISIONAL/MAI-21-05` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Invariants owner is established in the inspected sources.
- **Source atom / classification:** B1 §21 line 368 — LITERAL grouped security/privacy control list: authentication, authorization, trust, privacy, audit and revocation.
- **B2 mapping status:** MAPPED — bounded documentary correspondence to generic controls: B2 §5 privacy boundary; §6 explicitly lists authentication, authorization, trust, audit and revocation; §7 provides data classification. This does not establish mobile-specific policy wiring or enforcement.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §§5–7.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define which identity, trust, privacy, audit and revocation rules apply to local Core vs Remote Access, including remote-session expiry, least privilege, data minimization and audit-data access.
- **Required evidence:** Mobile threat/data-flow model; identity/session/permission contract; privacy classification; audit/revocation transitions and negative cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; generic controls mapped; mobile integration and enforcement OPEN.
- **Reviewer / approval reference:** B2 generic identity/security/privacy model; no complete mobile-specific enforcement evidence supplied.
- **Dependencies:** MH-04; MH-09; MH-11; MH-12; MH-13; MH-15.
- **Verification method:** Verify each listed term against B2 §5–7 and separately require a mobile-facing contract/evidence before asserting integration.
- **Change history:** MAPPED is documentary correspondence, not proof of security control enforcement.

### MAI-21-06 — Remote access command chain

- **Requirement ID:** `PROVISIONAL/MAI-21-06` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Invariants owner is established in the inspected sources.
- **Source atom / classification:** B1 §21 lines 370–371 — LITERAL flow: Remote Mobile Application → MediaHub API → MediaHub Core / State Authority / relevant subsystem.
- **B2 mapping status:** NOT_REVIEWED
- **Canonical contract path/ref:** B2 §§3–4, 22–23 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; general authority/API/event principles are relevant, but the complete mobile-specific route, authorization hand-off and subsystem dispatch contract are not specified in the inspected clauses.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define the remote request chain with authenticated caller, policy decision, versioned API, domain routing, authority-owned mutation, result/evidence and fail-closed error behavior.
- **Required evidence:** Sequence/interface contract; actor/permission and domain-route matrix; rejected-path and unavailable-subsystem cases; security/privacy review evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; exact route semantics and integration acceptance OPEN.
- **Reviewer / approval reference:** No complete Remote Access chain contract verified in the bounded sources.
- **Dependencies:** MH-03; MH-04; MH-09; MH-12; MH-13; MH-15; MH-21.
- **Verification method:** Compare exact B1 lines 370–371 with B2 §§3–4/22–23; general API transport is not proof of the complete authority-preserving chain.
- **Change history:** Keep NOT_REVIEWED until the concrete mobile API sequence is accepted.
## Batch summary

- **Provisional records:** 6 (`PROVISIONAL/MAI-21-01`…`PROVISIONAL/MAI-21-06`).
- **Mapping distribution:** 4 MAPPED / 2 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT.
- The four MAPPED rows correspond to the generic non-authority rule, single State Authority rule, versioned-contract principle, and generic authentication/authorization/trust/privacy/audit/revocation controls. These are documentary correspondences only.
- The two NOT_REVIEWED rows retain the mobile-specific physical-device bypass route and exact Remote Mobile → MediaHub API → Core/State Authority/subsystem chain as open contract semantics.
- No B1, B2, matrix, canonical backlog, `main`, runtime, infrastructure or host was modified or operated. No tests, qualification, installation, deployment or merge occurred.

- 2026-10-12 — after Batch 12 Review 02 (`f8d50509014f8c72476ab845476dcc40569c3357`), replaced the uninformative MAI-21-04 `Change history: undefined` value with source-linked history. No mapping status or row count changed; distribution remains 4 MAPPED / 2 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT. Full Mobile Access invariant acceptance remains OPEN.
