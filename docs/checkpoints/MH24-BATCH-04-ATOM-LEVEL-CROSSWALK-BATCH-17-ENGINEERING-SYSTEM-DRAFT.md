# MH-24 Batch 04 — Batch 17 Engineering System Crosswalk Draft

**Date:** 2026-10-13  
**Status:** DOCUMENTARY DRAFT — SEMANTIC / OWNER ACCEPTANCE OPEN; NOT A CANONICAL BACKLOG UPDATE.  
**Scope:** Bounded source-anchored mapping of historical Functional Baseline 1.0 §26 to canonical Functional Baseline 2.0 §17 and preserved parent AT-19. This pass inventories the named Engineering System scope and OSS-component gate only. It does not select engineering product scope, define artifact schemas, authorize implementation, mint final child IDs, or claim qualification.

## 1. Pinned sources

| Source | Ref | Blob SHA | Role |
|---|---|---|---|
| `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` | `main` | `9df4892ed0734050ac79732603d15bb414717310` | Historical literal source, §26 lines 411–416 |
| `docs/checkpoints/mediahub-functional-baseline-2.0.md` | `main` | `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` | Canonical current functional reference, §17 lines 368–378 |
| `docs/checkpoints/MH24-ATOMIC-TRACEABILITY-BACKLOG-01.md` | `docs/mediahub-chat-tree-map-20261012` | `ec2580f714e8f620bcf85ff7de2ae9242439e5e8` | Preserved parent AT-19 |
| `docs/checkpoints/MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md` | `docs/mediahub-chat-tree-map-20261012` | `eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd` | Owner-approved 12-field schema and mapping vocabulary; not approval of this crosswalk |

Baseline 1.0 remains historical provenance; Baseline 2.0 remains the canonical current functional reference. Neither baseline nor the canonical backlog is modified by this draft.

## 2. Provisional atom-level crosswalk

The labels below are provisional traceability labels only, not final child IDs. Every row preserves the owner-approved 12-field schema: Requirement ID; Owner; Source atom / classification; B2 mapping status; Canonical contract path/ref; Acceptance criteria; Required evidence; Lifecycle status; Reviewer / approval reference; Dependencies; Verification method; Change history.

### PROVISIONAL/ENG26-01 — Engineering calculations

- **Requirement ID:** PROVISIONAL/ENG26-01 (traceability label only; not a final child ID).
- **Owner:** TBD; Engineering domain owner not confirmed in this pass.
- **Source atom / classification:** B1 §26 line 413 — LITERAL: Engineering System supports engineering calculations.
- **B2 mapping status:** MAPPED — B2 §17 lines 372–378 explicitly includes calculations. This is bounded textual correspondence, not evidence of accepted calculation methods, domain-specific validation, or production suitability.
- **Canonical contract path/ref:** `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §17.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: the Engineering owner defines required calculation classes, input/output schemas, units/precision, provenance, validation and failure semantics before any implementation claim.
- **Required evidence:** Accepted engineering artifact/schema inventory; calculation-specific acceptance criteria; independent domain validation and qualification evidence where authorized.
- **Lifecycle status:** BOUNDED TEXTUAL CORRESPONDENCE / DOMAIN CONTRACT OPEN.
- **Reviewer / approval reference:** This documentary draft only; no row-level approval recorded.
- **Dependencies:** AT-19; MH-12; MH-13; MH-15; MH-19; MH-22.
- **Verification method:** Compare B1 §26 line 413 with B2 §17 lines 372–378, then trace required calculation classes into an accepted domain contract.
- **Change history:** New provisional row; no calculation schema, numerical guarantee or implementation inferred.

### PROVISIONAL/ENG26-02 — Buildings, engineering networks and spatial data

- **Requirement ID:** PROVISIONAL/ENG26-02 (traceability label only; not a final child ID).
- **Owner:** TBD; Engineering / spatial-domain owner not confirmed.
- **Source atom / classification:** B1 §26 line 413 — LITERAL: buildings, engineering networks and spatial data are in the Engineering System scope.
- **B2 mapping status:** NOT_REVIEWED — B2 §17 contains equipment, engineering systems and spatial model, but the reviewed clause does not explicitly define building/network models or their exact scope. This is not a claim that no counterpart exists elsewhere in the repository.
- **Canonical contract path/ref:** B2 `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §17; related MH domain contracts require map-directed review.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: the owner resolves required building/network/spatial entities, topology, references, supported formats, lifecycle and authoritative ownership without inferring these from the generic phrase “engineering systems.”
- **Required evidence:** Approved domain/model inventory; spatial/network schema and versioning contract; source/provenance and authorization rules; acceptance matrix for supported workflows.
- **Lifecycle status:** NOT_REVIEWED / OWNER AND DOMAIN SCOPE OPEN.
- **Reviewer / approval reference:** Bounded B1 §26 ↔ B2 §17 comparison only.
- **Dependencies:** AT-19; MH-05; MH-12; MH-13; MH-15; MH-17; MH-19; MH-22.
- **Verification method:** Inspect map-directed engineering, spatial and network primary contracts; compare exact named concepts and versioned schemas to B1 §26.
- **Change history:** New provisional row; no topology, format or engineering-model decision inferred.

### PROVISIONAL/ENG26-03 — BIM workflows, Digital Twin and simulation

- **Requirement ID:** PROVISIONAL/ENG26-03 (traceability label only; not a final child ID).
- **Owner:** TBD; BIM / Digital Twin / Engineering domain owners not confirmed in this pass.
- **Source atom / classification:** B1 §26 line 413 — LITERAL: BIM workflows, Digital Twin and simulation are in scope.
- **B2 mapping status:** MAPPED — B2 §17 includes BIM, 2D/3D, simulation and Digital Twin-related engineering capabilities in the Full edition. The correspondence is bounded to capability families; workflow completeness, model exchange and simulation fidelity are not established.
- **Canonical contract path/ref:** B2 `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §17; preserved AT-18 remains `OPEN—CONTRACT`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: owners define supported BIM/Twin/simulation workflows, input/output artifacts, model lineage, interoperability, validation boundaries and lifecycle transitions.
- **Required evidence:** Accepted workflow/artifact matrix; schema and lineage contracts; interoperability/licensing/security review where applicable; separately authorized implementation and qualification evidence.
- **Lifecycle status:** BOUNDED TEXTUAL CORRESPONDENCE / WORKFLOW ACCEPTANCE OPEN.
- **Reviewer / approval reference:** This documentary draft; Batch 16 AT-18 crosswalk is related evidence, not approval of AT-19.
- **Dependencies:** AT-18; AT-19; MH-12; MH-13; MH-14; MH-15; MH-19; MH-22.
- **Verification method:** Compare B1 §26 line 413 with B2 §17 lines 370–378 and the existing Batch 16 crosswalk; avoid treating shared nouns as proof of end-to-end workflows.
- **Change history:** New provisional row; no Twin, BIM or simulation workflow is accepted by this row.

### PROVISIONAL/ENG26-04 — Technical documentation, inspection and analysis

- **Requirement ID:** PROVISIONAL/ENG26-04 (traceability label only; not a final child ID).
- **Owner:** TBD; Engineering documentation / inspection domain owner not confirmed.
- **Source atom / classification:** B1 §26 line 413 — LITERAL: technical documentation, inspection and analysis are in scope.
- **B2 mapping status:** NOT_REVIEWED — B2 §17 mentions as-built data, diagrams and engineering project packages, but the reviewed clause does not explicitly define inspection lifecycle or analysis workflows. Broader repository counterparts have not been established in this pass.
- **Canonical contract path/ref:** B2 `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §17; relevant document/inspection/analysis contracts require map-directed review.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define artifact classes, review/sign-off, inspection evidence, analysis result provenance, revision history and the boundary between generated documentation and authoritative engineering records.
- **Required evidence:** Approved artifact inventory; document/inspection/analysis lifecycle contracts; provenance and access-control rules; workflow-level acceptance matrix.
- **Lifecycle status:** NOT_REVIEWED / ARTIFACT AND WORKFLOW CONTRACT OPEN.
- **Reviewer / approval reference:** Bounded source comparison only; no workflow acceptance recorded.
- **Dependencies:** AT-19; AT-17; MH-09; MH-12; MH-13; MH-19; MH-22.
- **Verification method:** Compare B1 §26 line 413 with B2 §17 and then inspect map-directed document and engineering workflow sources; do not infer inspection semantics from “project packages.”
- **Change history:** New provisional row; no mandatory inspection process, schema or analysis method invented.

### PROVISIONAL/ENG26-05 — OSS component admission and qualification gate

- **Requirement ID:** PROVISIONAL/ENG26-05 (traceability label only; not a final child ID).
- **Owner:** TBD; Engineering platform, security and licensing decision owners not confirmed.
- **Source atom / classification:** B1 §26 line 415 — LITERAL: OSS components are used only after license review, security review, provenance, benchmark, adapter integration and qualification.
- **B2 mapping status:** NOT_REVIEWED — B2 §17 requires provenance, authorization, licensing review and qualification for engineering artifacts before production use, but that artifact-level statement does not fully specify the B1 OSS-component admission sequence, security review, benchmark or adapter integration. No contradiction is inferred.
- **Canonical contract path/ref:** B2 `main`, blob `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`, §17; OSS/component supply-chain and adapter qualification contracts require map-directed review.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: the responsible owners establish a versioned component admission gate covering license/security review, provenance, benchmark, adapter integration, qualification, evidence retention and rejection handling.
- **Required evidence:** Approved OSS intake/checklist; license and security review records; source/provenance inventory; benchmark and adapter evidence; explicit qualification decision for each candidate component.
- **Lifecycle status:** NOT_REVIEWED / COMPONENT-ADMISSION CONTRACT OPEN.
- **Reviewer / approval reference:** This bounded comparison only; no OSS component was evaluated or approved.
- **Dependencies:** AT-19; MH-12; MH-13; MH-15; MH-19; MH-20; MH-22; software supply-chain and adapter governance.
- **Verification method:** Compare B1 §26 line 415 with B2 §17 lines 376–378, then inspect map-directed OSS, security, adapter and qualification sources before assigning a stronger mapping status.
- **Change history:** New provisional row; no package, license, adapter or benchmark was selected, executed or qualified.

## 3. Current disposition

- Five provisional traceability rows; no final child IDs minted.
- Mapping distribution: **2 MAPPED / 3 NOT_REVIEWED / 0 NO_DIRECT_COUNTERPART / 0 CONFLICT**. MAPPED means bounded textual correspondence only, not semantic or owner acceptance.
- AT-19 remains **OPEN—CONTRACT**. Exact engineering workflow scope, model/artifact schemas, inspection/analysis lifecycle and the complete OSS admission sequence remain unverified.
- AT-18 remains **OPEN—CONTRACT** and is not closed by this adjacent-domain pass.
- No change to B1, B2, the canonical backlog or `main` is made or implied.
- Documentary work only: no tests, qualification, installation, runtime/host inspection, infrastructure changes, deployment, migration, merge or rebase.
