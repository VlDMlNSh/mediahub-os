# MH-24 Batch 04 — Batch 16 Digital Twin Crosswalk Draft

**Date:** 2026-10-13  
**Status:** DOCUMENTARY DRAFT — SEMANTIC / OWNER ACCEPTANCE OPEN; NOT A CANONICAL BACKLOG UPDATE.  
**Scope:** Bounded source-anchored mapping of Functional Baseline 1.0 §25 to Functional Baseline 2.0 §17. This draft does not choose a commercial policy, authorize implementation, mint final child IDs, or claim qualification.

## 1. Pinned sources

| Source | Ref | Blob SHA | Role |
|---|---|---|---|
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Historical literal source, §25 lines 401–407 |
| `docs/checkpoints/mediahub-functional-baseline-2.0.md` | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Canonical current functional reference, §17 lines 368–378 |
| `docs/checkpoints/MH24-ATOMIC-TRACEABILITY-BACKLOG-01.md` | `docs/mediahub-chat-tree-map-20261012` | `ec2580f714e8f620bcf85ff7de2ae9242439e5e8` | Preserved parent item AT-18 |
| `docs/checkpoints/MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md` | `docs/mediahub-chat-tree-map-20261012` | `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd` | Owner-approved 12-field schema and mapping vocabulary; not approval of this crosswalk |

Baseline 1.0 remains historical source material; Baseline 2.0 remains the canonical current functional reference. No text is copied into or used to modify either baseline.

## 2. Provisional atom-level crosswalk

All labels below are **provisional traceability labels**, not stable child IDs. The approved 12-field schema is preserved exactly.

### PROVISIONAL/DT25-01 — Twin belongs to Full editions; not a separate OS

- **Requirement ID:** PROVISIONAL/DT25-01 (traceability label only; not a final child ID).
- **Owner:** TBD; domain-owner confirmation not evidenced in this pass.
- **Source atom / classification:** B1 §25 line 403 — LITERAL: Digital Twin is a physically present component of MediaHub OS Full and is not a separate operating system.
- **B2 mapping status:** MAPPED — B2 §17 line 370 states Digital Twin is part of Full editions, not a separate OS. Bounded textual correspondence only.
- **Canonical contract path/ref:** Functional Baseline 2.0 @ main, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §17.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: canonical product-edition contract consistently represents Digital Twin as part of Full editions rather than a separate OS.
- **Required evidence:** Accepted edition/capability contract and owner/domain review; runtime evidence remains a separate implementation/qualification gate.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN.
- **Reviewer / approval reference:** This draft only; no row-level approval recorded.
- **Dependencies:** AT-18; MH-09; MH-15; MH-19; MH-23; entitlement and product-edition governance.
- **Verification method:** Compare literal B1 §25 line 403 with B2 §17 line 370.
- **Change history:** New provisional row; no historical ID changed, no final child ID minted, no canonical backlog promotion.

### PROVISIONAL/DT25-02 — Exact Full SKU/runtime presence for Mac mini and Mini PC

- **Requirement ID:** PROVISIONAL/DT25-02 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable edition/hardware owner not confirmed by this crosswalk.
- **Source atom / classification:** B1 §25 line 405 — LITERAL: names MediaHub OS Full for Mac mini and MediaHub OS Full for Mini PC and says the Digital Twin runtime is present in those editions.
- **B2 mapping status:** NOT_REVIEWED — B2 §17 establishes Twin in Full editions generally but does not name these exact hardware-specific Full profiles in the reviewed clause. This is a bounded scope statement, not a global repository-absence claim.
- **Canonical contract path/ref:** Functional Baseline 2.0 @ main, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §17; hardware/profile acceptance references require separate map-directed review.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: exact Full edition/profile-to-runtime availability is explicitly defined without inferring hardware support from a generic Full-edition statement.
- **Required evidence:** Approved product-edition/profile matrix; target-specific component manifest; exact hardware/OS profile qualification evidence when separately authorized.
- **Lifecycle status:** NOT_REVIEWED / OWNER AND TARGET-PROFILE EVIDENCE OPEN.
- **Reviewer / approval reference:** This bounded source comparison only; no hardware or runtime qualification performed.
- **Dependencies:** AT-18; MH-15; MH-19; MH-22; product-edition and target-profile contracts.
- **Verification method:** Compare B1 §25 line 405 to B2 §17 and the accepted product-edition/target-profile contract; do not infer a hardware guarantee from the general clause.
- **Change history:** New provisional row; no hardware target chosen and no implementation authorized.

### PROVISIONAL/DT25-03 — Professional capability lock/unlock by paid entitlement

- **Requirement ID:** PROVISIONAL/DT25-03 (traceability label only; not a final child ID).
- **Owner:** TBD; product entitlement owner and domain owner must be confirmed.
- **Source atom / classification:** B1 §25 line 405 — LITERAL: professional features may be LOCKED / UNLICENSED until the corresponding paid entitlement is obtained; the source describes activation after payment.
- **B2 mapping status:** MAPPED — B2 §17 line 376 states professional capabilities are entitlement-controlled. This maps the abstract control principle only; exact entitlement lifecycle and commercial behavior are not thereby specified.
- **Canonical contract path/ref:** Functional Baseline 2.0 @ main, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §17; AT-18 and AT-24 remain open.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define authoritative entitlement state, grant/deny behavior and protected operations; explicitly resolve expiry, revocation, offline operation, restore/reinstall and device-transfer behavior before implementation acceptance.
- **Required evidence:** Owner-approved edition-feature/entitlement matrix; versioned entitlement contract; negative-path evidence for absent, invalid, expired and revoked entitlements; separate implementation and qualification records.
- **Lifecycle status:** ABSTRACT MAPPING ONLY / ENTITLEMENT SEMANTICS AND OWNER ACCEPTANCE OPEN.
- **Reviewer / approval reference:** This documentary draft; no commercial policy decision inferred.
- **Dependencies:** AT-17; AT-18; AT-23; AT-24; MH-09; MH-12; MH-13; MH-15; MH-19; MH-21; MH-22.
- **Verification method:** Compare B1 §25 line 405 with B2 §17 line 376, then validate the exact entitlement lifecycle against an approved contract and evidence.
- **Change history:** New provisional row; no price, licensing terms, lifecycle semantics or enforcement implementation selected.

### PROVISIONAL/DT25-04 — Digital Twin domain and capability scope

- **Requirement ID:** PROVISIONAL/DT25-04 (traceability label only; not a final child ID).
- **Owner:** TBD; Digital Twin / Engineering domain owner confirmation not evidenced.
- **Source atom / classification:** B1 §25 line 407 — LITERAL capability scope: buildings, rooms, equipment, engineering systems, spatial data, 3D, BIM, simulation, monitoring and engineering workflows.
- **B2 mapping status:** MAPPED — B2 §17 lines 372–378 includes 2D/3D, BIM, CAD, equipment, engineering systems, spatial model, simulation, project state, as-built data, calculations, diagrams, cable journals and engineering project packages. This is bounded capability correspondence, not proof that every B1 noun has a defined schema or accepted workflow.
- **Canonical contract path/ref:** Functional Baseline 2.0 @ main, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §17.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: domain owner identifies required data models, artifact types, monitoring inputs/outputs, workflow lifecycle, provenance, authorization and qualification conditions; unrepresented granularity remains open.
- **Required evidence:** Accepted domain contract and artifact/schema inventory; provenance and authorization controls; workflow-level acceptance criteria; separate implementation/qualification evidence.
- **Lifecycle status:** BOUNDED TEXTUAL CORRESPONDENCE / FULL SEMANTIC AND DOMAIN ACCEPTANCE OPEN.
- **Reviewer / approval reference:** This documentary draft; no schema or workflow acceptance recorded.
- **Dependencies:** AT-18; AT-19; MH-12; MH-13; MH-14; MH-15; MH-19; MH-22.
- **Verification method:** Compare B1 §25 line 407 with B2 §17 lines 372–378 and trace each required artifact/workflow into the accepted domain contract.
- **Change history:** New provisional row; no artifact schema, simulation guarantee, monitoring contract or workflow implementation inferred.

## 3. Current disposition

- Four provisional traceability rows; no stable child IDs minted.
- Mapping distribution: **3 MAPPED / 1 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT**. MAPPED means bounded textual correspondence only, not semantic/owner acceptance.
- AT-18 remains **OPEN—CONTRACT**. Runtime presence on named hardware profiles, entitlement state/lifecycle/enforcement, full artifact/workflow semantics, implementation and qualification remain unproven.
- No change to B1, B2, the canonical backlog, the canonical traceability matrix or `main` is authorized by this draft.
- Documentary work only: no tests, qualification, installation, provider/model calls, runtime/host inspection, infrastructure changes, deployment, migration, merge or rebase.
