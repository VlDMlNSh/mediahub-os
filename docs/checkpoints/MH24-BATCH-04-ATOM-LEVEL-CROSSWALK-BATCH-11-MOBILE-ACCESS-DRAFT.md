# MH-24 — Supplemental Atom-Level Crosswalk: Baseline 1.0 §20 (Mobile Access Layer) — Draft 01

- **Status:** DOCUMENTARY DRAFT / SEMANTIC OWNER ACCEPTANCE OPEN / NOT A CANONICAL BACKLOG.
- **Working ref:** `docs/mediahub-chat-tree-map-20261012`.
- **Scope:** B1 §20, literal source lines 332–359, pinned B1 SHA `9df4892ed0734050ac79732603d15bb414717310`.
- **Purpose:** make the two user-facing mobile roles, Core-vs-Remote distinction and their source-backed gaps traceable without pretending that this is a complete implementation/qualification contract.
- **B2:** `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; relevant clauses §§2.3 (lines 63–72), 3–4 (authority, including §4 line 108), 5–7 (privacy/identity/data), 9 (platform profiles), 14–18 (domain capabilities), 22–23 (API/event/provenance) and §25 (mobile capability/packaging implementation work).
- **Working matrix:** `docs/checkpoints/mediahub-mh24-traceability-matrix.md@docs/mediahub-chat-tree-map-20261012`, SHA `73377891072bac3c739c44055ceeb0874154f64c`, row 20 Mobile Access and row 21 Mobile invariants. These are section-level summaries and are not replaced by this supplemental draft.
- **Schema authority:** Product Owner Decision Record 01 SHA `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd`; D-05 approves the 12-field schema and mapping-status vocabulary only, not individual mappings, mobile feature scope or pricing.
- **Identifier rule:** `PROVISIONAL/MA-20-xx` are newly created working traceability labels because this bounded search did not find an existing Batch 11/mobile-specific draft path and the prior structural audit did not include B1 §20. They are not final child IDs; preserve old rows/matrix and complete project-wide lineage/collision review before final IDs.
- **Mobile authority boundary:** neither the local Core app nor Remote Access becomes canonical MediaHub or Smart Home authority. B2 retains MediaHub State Authority and HA Core authority within their respective domains. Developer Mobile is explicitly a separate developer-only application surface in B2 §2.3; whether it is outside B1's literal "exactly two applications" count remains an explicit scope question rather than an inferred conflict.

## Mapping rules used in this draft

- `MAPPED` is bounded text correspondence only, not implementation, runtime, tests, qualification or production acceptance.
- `NOT_REVIEWED` remains for compound/list requirements whose full semantics are not established by a corresponding accepted B2 contract.
- `NO_DIRECT_COUNTERPART` is not used for generic app roles already named in B2. The exact "exactly two applications" scope is not forced into `MAPPED` because B2 separately mentions Developer Mobile.
- `CONFLICT` is not assigned without explicit contradictory normative text; the "two applications" vs separate developer-only surface is recorded as an unresolved scope interpretation, not an established contradiction.
- B2 §25 explicitly keeps mobile capability matrix/packaging and entitlement/subscription enforcement as downstream implementation/qualification work. Therefore B1's one-time payment statement is not considered mapped to that generic work item.

## Provisional atom / traceability records

### MA-20-01 — Two application roles; exact app-count scope

- **Requirement ID:** `PROVISIONAL/MA-20-01` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Layer domain owner is established in the inspected sources.
- **Source atom / classification:** B1 §20 line 334 — LITERAL: Mobile Access Layer is divided into exactly two applications. B2 §2.3 lines 65–70 states exactly two functional application roles (Core and Remote Access), but separately describes Developer Mobile as a developer-only app surface. Do not resolve whether B1's count includes or excludes that separate developer surface by assumption.
- **B2 mapping status:** NOT_REVIEWED
- **Canonical contract path/ref:** B1 `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main` SHA `9df4892ed0734050ac79732603d15bb414717310`, §20 line 334; B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §2.3 lines 63–72 and §§5,9.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: explicitly define whether 'exactly two applications' scopes the user-facing Mobile Access Layer only, with Developer Mobile outside that layer, or another approved interpretation. Preserve the two user-facing role distinction.
- **Required evidence:** Owner/governance scope disposition; updated mobile role/app inventory; explicit relationship between user Core, Remote Access and Developer Mobile.
- **Lifecycle status:** DRAFT / NOT APPROVED; app-count semantics and cross-domain scope OPEN.
- **Reviewer / approval reference:** No specific owner decision on whether B1's literal two-app count includes/excludes Developer Mobile was found in the inspected sources.
- **Dependencies:** MH-09; MH-13; MH-15; MH-21; MH-24.
- **Verification method:** Compare literal B1 §20 line 334 with B2 §2.3 lines 65–72 and platform list §9 lines 214–229; record scope rather than asserting contradiction or equivalence.
- **Change history:** New provisional traceability label only; no historical Audit 01 child ID or final stable ID minted.

### MA-20-02 — MediaHub Core is local full-minimal edition

- **Requirement ID:** `PROVISIONAL/MA-20-02` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Layer domain owner is established in the inspected sources.
- **Source atom / classification:** B1 §20.1 lines 336–338 — LITERAL: MediaHub Core for iPad/iOS/iPadOS is a full-minimal local MediaHub Core edition installed on the iPad, not a remote client.
- **B2 mapping status:** MAPPED — bounded documentary correspondence: B2 §2.3 line 67 explicitly defines MediaHub Core for iOS/iPadOS as a local full-minimal Core edition, not a remote client.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §2.3 line 67; no platform-specific implementation/qualification implied.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: preserve Core as a local role with platform-specific implementation, not as a renamed remote client; define its supported capability profile for each admitted iOS/iPadOS target.
- **Required evidence:** Accepted platform profile, feature/capability matrix, implementation evidence and platform qualification record when separately authorized.
- **Lifecycle status:** DRAFT / NOT APPROVED; documentary mapping present, platform implementation and qualification OPEN.
- **Reviewer / approval reference:** D-05 schema/vocabulary approval only; no specific product decision establishing an implementation or qualification result.
- **Dependencies:** MH-09; MH-13; MH-15; MH-24.
- **Verification method:** Read exact B1 §20.1 and B2 §2.3 line 67; do not infer supported hardware/runtime capability from the role definition alone.
- **Change history:** MAPPED denotes text correspondence only; no runtime evidence asserted.

### MA-20-03 — Local Core capability bundle

- **Requirement ID:** `PROVISIONAL/MA-20-03` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Layer domain owner is established in the inspected sources.
- **Source atom / classification:** B1 §20.1 lines 340–347 — LITERAL grouped capability list: basic Core; local UI; local Smart Home; local Media; local AI within available resources; local state and necessary local functions; minimal subset of the full MediaHub system.
- **B2 mapping status:** NOT_REVIEWED
- **Canonical contract path/ref:** B2 §§1–4, 8–10, 14–18 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; those sections define domains/platform/capabilities generally but do not prove each listed capability is implemented and qualified on each iOS/iPadOS profile.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define the local-Core feature/capability set, resource limits and domain-specific degraded/offline behavior for each supported mobile platform profile.
- **Required evidence:** Per-platform capability matrix; resource/runtime constraints; local-offline profile; privacy/authority boundaries; evidence and acceptance criteria for each capability.
- **Lifecycle status:** DRAFT / NOT APPROVED; exact capability matrix, implementation and qualification OPEN.
- **Reviewer / approval reference:** No specific complete local iPad Core capability/qualification acceptance package was verified.
- **Dependencies:** MH-03; MH-05; MH-09; MH-10; MH-13; MH-15; MH-17; MH-18; MH-24.
- **Verification method:** Compare each list item against the relevant B2 domain clause and platform/capability model; do not promote a section-level relationship into blanket feature coverage.
- **Change history:** Grouped literal-source taxonomy; not seven independent approved requirements; no final child IDs.

### MA-20-04 — One-time paid installation

- **Requirement ID:** `PROVISIONAL/MA-20-04` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Layer domain owner is established in the inspected sources.
- **Source atom / classification:** B1 §20.1 line 349 — LITERAL commercial statement: Core is paid with a one-time payment when installed on a device.
- **B2 mapping status:** NOT_REVIEWED
- **Canonical contract path/ref:** B2 §§2–3 and §25 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; B2 §25 line 509 carries entitlement/subscription enforcement as downstream work, but does not specify this exact price model.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: explicitly decide whether one-time per-device purchase remains product policy and define entitlement, re-install/restore, family/device transfer and refund behavior only through the approved product process.
- **Required evidence:** Owner product decision; versioned commerce/entitlement policy; positive/negative entitlement cases and lifecycle rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; pricing/entitlement semantics OPEN; no implementation claimed.
- **Reviewer / approval reference:** No explicit owner decision for the current one-time price model was included in the inspected source set.
- **Dependencies:** MH-07; MH-09; MH-13; MH-24.
- **Verification method:** Compare B1 line 349 with B2 product scope and §25 line 509; do not infer that a generic entitlement item confirms one-time payment policy.
- **Change history:** Preserve as historical literal source; no commercial policy was created or accepted by this crosswalk.

### MA-20-05 — Shared contract model and no authority bypass

- **Requirement ID:** `PROVISIONAL/MA-20-05` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Layer domain owner is established in the inspected sources.
- **Source atom / classification:** B1 §20.1 line 351 — LITERAL: architecture must retain the shared MediaHub contract model and must not create authority bypasses.
- **B2 mapping status:** `MAPPED` — bounded documentary correspondence only. B2 §22 explicitly states that domains communicate through versioned contracts, and B2 §2.3 line 72 states that no mobile application is an authority. Together these clauses support the abstract B1 constraint to preserve the shared MediaHub contract model and avoid authority bypasses.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §2.3 lines 65–72 and §22 lines 438–455. No concrete Core-to-domain command/API path is accepted by this mapping.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: all state-changing requests from Core re-enter the accepted domain/State Authority command path; local state and Smart Home state remain within their approved authorities.
- **Required evidence:** State/command path map for each local domain; authority-boundary negative-path acceptance criteria; privacy/security evidence at authorized implementation stage.
- **Lifecycle status:** DRAFT / NOT APPROVED; documentary architecture constraint mapped; concrete command-path implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Batch 11 Review 02 SHA `c143d1b349bcf2ba3a76ffdad03b1d4258a1ebe9` (bounded status review); D-04 approves mapping vocabulary only; no mobile-specific command-path acceptance artifact verified.
- **Dependencies:** MH-03; MH-04; MH-05; MH-09; MH-12; MH-13; MH-15.
- **Verification method:** Compare B1 line 351 with B2 §2.3 line 72 and §22 lines 438–455; keep abstract documentary constraint separate from proof of a concrete implementation path.
- **Change history:** 2026-10-12 — after bounded semantic Review 02, reclassified only the abstract shared-contract/no-mobile-authority constraint as `MAPPED`. This does not assert runtime bypass prevention or a concrete accepted command path.

### MA-20-06 — Separate Remote Access application role

- **Requirement ID:** `PROVISIONAL/MA-20-06` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Layer domain owner is established in the inspected sources.
- **Source atom / classification:** B1 §20.2 lines 353–355 — LITERAL: a separate application provides remote access to MediaHub.
- **B2 mapping status:** MAPPED — bounded documentary correspondence: B2 §2.3 line 68 describes a separate MediaHub Remote Access application family for remote access/management.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §2.3 line 68; no client implementation or production access security implied.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: retain Remote Access as a distinct role from local Core and Developer Mobile; define allowed services and authorization boundaries in its own contract.
- **Required evidence:** Remote Access interface/role contract; identity/authz scope; approved remote services and security acceptance criteria.
- **Lifecycle status:** DRAFT / NOT APPROVED; role mapping is documentary only, implementation/qualification OPEN.
- **Reviewer / approval reference:** D-05 approves mapping vocabulary, not the remote application implementation contract.
- **Dependencies:** MH-04; MH-09; MH-12; MH-13; MH-15; MH-21.
- **Verification method:** Compare B1 §20.2 and B2 §2.3 line 68; retain the distinct role without inferring runtime availability.
- **Change history:** MAPPED denotes the role definition correspondence only.

### MA-20-07 — Remote access feature set

- **Requirement ID:** `PROVISIONAL/MA-20-07` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Layer domain owner is established in the inspected sources.
- **Source atom / classification:** B1 §20.2 line 355 — LITERAL grouped capabilities: remote access, management, monitoring, notifications, remote interaction and access to permitted MediaHub services.
- **B2 mapping status:** NOT_REVIEWED
- **Canonical contract path/ref:** B2 §2.3 line 68 names remote access/management; the reviewed B2 clause does not fully specify monitoring, notification, interaction or service-by-service authorization behavior.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define each remote capability, event visibility, permissible commands, notification policy, service scope and behavior when local services/offline authorization are unavailable.
- **Required evidence:** Capability matrix; remote API/notification contract; identity and policy decisions; denied/expired-session and unavailable-service cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; detailed capability and failure semantics OPEN.
- **Reviewer / approval reference:** No complete Remote Access feature acceptance matrix was verified in the cited scope.
- **Dependencies:** MH-04; MH-09; MH-11; MH-12; MH-13; MH-15; MH-21.
- **Verification method:** Compare each capability named in B1 line 355 with B2 §2.3 and applicable domain clauses; a generic 'remote access/management' phrase is not full coverage.
- **Change history:** Grouped literal-source list; no runtime feature claims.

### MA-20-08 — Remote Access is not local Core

- **Requirement ID:** `PROVISIONAL/MA-20-08` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Layer domain owner is established in the inspected sources.
- **Source atom / classification:** B1 §20.2 line 357 — LITERAL invariant: Remote Access is not Local Core.
- **B2 mapping status:** MAPPED — bounded documentary correspondence: B2 §2.3 distinguishes the Core for iOS/iPadOS role from the separate Remote Access family; B2 §4 invariant 6 says Remote Mobile is not Local Core.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main` SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §2.3 lines 65–70 and §4 line 108.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: preserve a strict role boundary in UI, APIs, capabilities, identity and data paths; remote clients must not imply local Core presence or authority.
- **Required evidence:** Role/API boundary contract; integration/degraded-mode cases and authority/access negative checks, when separately authorized.
- **Lifecycle status:** DRAFT / NOT APPROVED; documentary mapping present; runtime conformance OPEN.
- **Reviewer / approval reference:** No implementation evidence inferred from B2 role language.
- **Dependencies:** MH-03; MH-04; MH-09; MH-12; MH-13; MH-15.
- **Verification method:** Re-read B2 §2.3 and §4 line 108; keep the role distinction through implementation and acceptance.
- **Change history:** MAPPED only for the explicit distinction, not proof of implementation.

### MA-20-09 — Remote Access operates over MediaHub API

- **Requirement ID:** `PROVISIONAL/MA-20-09` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted Mobile Access Layer domain owner is established in the inspected sources.
- **Source atom / classification:** B1 §20.2 line 357 — LITERAL transport/interface statement: Remote Access operates as a remote access layer over MediaHub API.
- **B2 mapping status:** NOT_REVIEWED
- **Canonical contract path/ref:** B2 §§22–23 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` define general versioned APIs/contracts and event model but do not supply a specific complete Remote Access API contract in the reviewed clause set.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define the versioned Remote Access API/interface, authentication/authorization, data exposure, command path, errors, compatibility and offline/reconnect behavior without granting the remote app authority.
- **Required evidence:** Accepted API schema/contract and version policy; identity/policy integration; contract/negative-path evidence when authorized.
- **Lifecycle status:** DRAFT / NOT APPROVED; API contract and implementation/qualification OPEN.
- **Reviewer / approval reference:** No accepted Remote Access API schema was verified in this bounded review.
- **Dependencies:** MH-03; MH-04; MH-09; MH-12; MH-13; MH-15; MH-21.
- **Verification method:** Compare B1 line 357 with B2 §§22–23; do not infer the specific mobile API from the general event/API model.
- **Change history:** No final IDs minted; no implementation inferred.


## Batch summary

- **Provisional records:** 9 (`PROVISIONAL/MA-20-01`…`PROVISIONAL/MA-20-09`).
- **Mapping distribution:** 4 MAPPED / 5 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT.
- Bounded `MAPPED` coverage: local Core role/full-minimal-not-remote distinction; abstract shared versioned-contract/non-authority constraint; separate Remote Access role; explicit Remote-vs-Local-Core distinction.
- Open: the literal scope of "exactly two applications" versus separate Developer Mobile; local capability-by-platform matrix; one-time payment/entitlement semantics; shared command/authority contracts; complete remote feature set; specific Remote Access API contract.
- B1 §20 is supplemental to matrix rows 20–21; this draft does not replace either row or close all Mobile Access invariants in B1 §21.
- No B1, B2, working matrix, canonical backlog, `main`, runtime, infrastructure or host was modified or operated. No tests, qualification, installation, deployment or merge occurred.

- 2026-10-12 — after Batch 11 Review 02 (pre-correction draft SHA `4e4293f8b9a6b7b449514678596ec9765187aa46`), changed only MA-20-05 from `NOT_REVIEWED` to bounded documentary `MAPPED` using B2 §2.3 line 72 and §22 lines 438–455. Distribution is now 4 MAPPED / 5 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT across nine provisional rows. Full Mobile Access owner/contract/implementation/qualification acceptance remains OPEN; Review01 is preserved. No B1/B2, matrix, canonical backlog or main change.
