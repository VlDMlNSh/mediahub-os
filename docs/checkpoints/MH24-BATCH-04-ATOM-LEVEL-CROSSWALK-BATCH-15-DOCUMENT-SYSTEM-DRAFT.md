# MH-24 — Supplemental Atom-Level Crosswalk: Baseline 1.0 §24 (Document System) — Draft 01

- **Date:** 2026-10-12
- **Working ref:** docs/mediahub-chat-tree-map-20261012
- **Status:** DOCUMENTARY DRAFT / AT-17 OPEN—OWNER DECISION / NOT A CANONICAL BACKLOG.
- **Scope:** B1 §24, source lines 391–397 at pinned B1 blob SHA 9df4892ed0734050ac79732603d15bb414717310.
- **Purpose:** transcribe the literal Document System functions and qualification condition into separately dispositionable provisional traceability labels, without inferring paid-tier policy, runtime selection or qualification from broad baseline wording.
- **ID rule:** DOC-24-01…DOC-24-12 are provisional traceability subdivisions only. Do not mint final MH24-B04 child IDs or treat the subdivisions as twelve independently approved product requirements.
- **B1:** specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md @ main, SHA 9df4892ed0734050ac79732603d15bb414717310, §24 lines 391–397.
- **B2:** docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16 Documents and Knowledge (lines 358–366), §21 OSS/supply-chain adoption sequence (line 430), §25 open implementation/qualification work (including product-edition qualification).
- **Historical semantic source:** docs/checkpoints/MH24-SEMANTIC-AUDIT-BATCH-04.md @ working ref, SHA e7f35460e3bf32cc3fce8b4584848907d07a7943, §24 / DOCUMENT-SYSTEM-01.
- **Atomic backlog:** docs/checkpoints/MH24-ATOMIC-TRACEABILITY-BACKLOG-01.md @ working ref, SHA ec2580f714e8f620bcf85ff7de2ae9242439e5e8; AT-17 remains OPEN—OWNER DECISION: identify Document System functions by edition and define lock/unlock/entitlement enforcement.
- **Traceability matrix:** docs/checkpoints/mediahub-mh24-traceability-matrix.md @ working ref, SHA 73377891072bac3c739c44055ceeb0874154f64c, row 24 “Documents”.
- **Owner schema:** Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd, D-05; schema/status vocabulary only.
- **Domain dependencies:** MH-19 Acceptance Criteria @ architecture/mh-19-knowledge-graph-digital-twin, SHA 9bc038123f01beb9c66e71d5f27cbc82ad3e4501, NOT ACCEPTED / NOT FROZEN; MH-19 Evidence Register SHA 854fe2c0fc604d80b4e1af7d384ec1fb943fe6df marks production KG/vector/RAG/Digital Twin runtime and persistence UNKNOWN. This is not runtime evidence.
- **Candidate path inventory:** six likely Batch 15 draft/review paths checked at this working ref and returned 404 before creation; this is bounded path evidence, not global absence across every branch/name.
- **Boundary:** this is documentary mapping only. It does not decide pricing, paid-tier scope, app/store entitlements, PaddleOCR selection, implementation, privacy/legal acceptance or qualification.

## Mapping rules

- MAPPED means the pinned B2 text explicitly documents the same bounded function/constraint. It does not prove runtime implementation, feature entitlement, adoption of an OSS component or qualification.
- B2 §16 explicitly names OCR, classification, metadata, search, provenance, extraction and workflows. Map only these bounded category matches.
- The exact “professional/paid Document System tier” is not defined in the reviewed B2 clauses; keep it scoped as NO_DIRECT_COUNTERPART and link AT-17.
- “Structured information” remains NOT_REVIEWED until its accepted schema/format/semantics are defined.
- The general OSS qualification/adoption sequence in B2 §21 is a bounded correspondence to B1's security/license/provenance gate. It does not select PaddleOCR.
- PaddleOCR appears in B1 only as an example conditional on qualification. Do not infer selection, installation, benchmark pass or approval.
- CONFLICT is not assigned absent explicit contradictory normative text.

## Provisional atom records

### DOC-24-01 — Named professional / paid Document System tier

- **Requirement ID:** PROVISIONAL/DOC-24-01 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 393 — LITERAL: Document System is a professional/paid functional tier.
- **B2 mapping status:** NO_DIRECT_COUNTERPART; Reviewed B2 §§5, 16 and 25 describe data/privacy boundaries, generic Documents/Knowledge capabilities and carried-forward product-edition qualification work, but do not define this exact paid Document System tier/entitlement. This status is limited to the paid/pro tier and its entitlement semantics; generic document functions are covered by separate rows. It is not a whole-repository absence claim.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Obtain owner decision that defines which editions have which document functions and how professional features are entitled, locked/unlocked, revoked and handled offline.
- **Required evidence:** Approved edition-feature matrix, commercial/entitlement decision, enforcement contract and negative-path evidence for unauthorized access, expiry, revocation, offline mode, restore/reinstall and device transfer.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** AT-17; MH-09/MH-15/MH-19; identity, entitlement, storage and privacy controls; B2 §§5, 7, 16, 25.
- **Verification method:** Compare B1 §24 line 393 to B2 §§5/16/25; do not infer paid scope or enforcement from generic document functionality.
- **Change history:** Preserves DOCUMENT-SYSTEM-01; AT-17 remains OPEN—OWNER DECISION. No paid feature decision inferred. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-02 — Document capability domain

- **Requirement ID:** PROVISIONAL/DOC-24-02 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 395 — LITERAL list atom: documents.
- **B2 mapping status:** MAPPED; B2 §16 line 360 explicitly states that Documents include OCR, classification, metadata, search, provenance, extraction and workflows. Maps the general document-capability category only; it does not establish the paid-tier scope or runtime.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define supported document classes and platform/edition boundaries in the owning Document System contract.
- **Required evidence:** Accepted document-scope contract, per-edition feature list and implementation evidence when separately authorized.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-19/MH-21; AT-17; B2 §16 and privacy/data-class rules.
- **Verification method:** Compare B1 §24 line 395 with B2 §16 line 360; retain paid entitlement separately.
- **Change history:** Bounded text-level mapping, not implementation acceptance. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-03 — OCR

- **Requirement ID:** PROVISIONAL/DOC-24-03 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 395 — LITERAL list atom: OCR.
- **B2 mapping status:** MAPPED; B2 §16 line 360 explicitly lists OCR as a Documents capability. General OCR capability only; language/model accuracy, file coverage, throughput, runtime dependency and product-edition gate are not specified by this mapping.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define supported input formats/languages, quality and resource criteria, privacy and failure behavior per qualified profile.
- **Required evidence:** Versioned OCR capability matrix, privacy/security review, model/component provenance and profile-bound accuracy/performance/negative-path evidence.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-19; MH-12/MH-13; B2 §§5, 7, 8, 16, 20; AT-17 for entitlement.
- **Verification method:** Compare the exact B1 OCR item to B2 §16; do not infer a selected OCR engine.
- **Change history:** PaddleOCR remains only a B1 example candidate, separately tracked below. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-04 — Classification

- **Requirement ID:** PROVISIONAL/DOC-24-04 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 395 — LITERAL list atom: classification.
- **B2 mapping status:** MAPPED; B2 §16 line 360 explicitly lists classification. Category-level mapping only; taxonomy, confidence/uncertainty, manual correction and sensitive-data rules are not established by the generic word.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define classification labels, versioning, confidence/unknown handling, manual correction, sensitive-data policy and failure behavior.
- **Required evidence:** Approved taxonomy/schema, versioned classification contract, privacy review and negative-path verification.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-19; MH-12/MH-13; B2 §§5–7, 16; AT-17 for edition gates.
- **Verification method:** Compare B1 and B2 category text; require a separate accepted taxonomy before claiming semantic completeness.
- **Change history:** No classification schema or runtime accepted by this row. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-05 — Search

- **Requirement ID:** PROVISIONAL/DOC-24-05 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 395 — LITERAL list atom: search.
- **B2 mapping status:** MAPPED; B2 §16 line 360 explicitly lists search; line 362 further describes semantic/full-text search in Knowledge. General search capability only; indexing backend, permissions, ranking, freshness, deletion and offline behavior are not established.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define query/index scope, access-control filtering, freshness/deletion semantics, supported formats and degraded/offline behavior.
- **Required evidence:** Search contract, data-flow/privacy boundaries, permission/tenant tests and per-profile capability/qualification evidence.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-19; MH-12/MH-13; B2 §§5, 7, 13, 16, 20.
- **Verification method:** Compare B1 §24 with B2 §16 and separate broad search capability from any specific backend/runtime choice.
- **Change history:** Does not adopt or qualify a search engine. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-06 — Metadata

- **Requirement ID:** PROVISIONAL/DOC-24-06 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 395 — LITERAL list atom: metadata.
- **B2 mapping status:** MAPPED; B2 §16 line 360 explicitly lists metadata. General metadata capability only; schema, mandatory/optional fields, identity, data retention and migration semantics remain outside this row.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define document/asset metadata schema, versioning, validation, privacy/retention and migration compatibility.
- **Required evidence:** Accepted schema/version contract, provenance and migration evidence, and privacy/negative-path review.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-19; B2 §§5, 7, 13, 16, 19, 20.
- **Verification method:** Compare the exact list atom with B2 §16; require the schema contract separately.
- **Change history:** No field schema or persistence behavior inferred. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-07 — Provenance

- **Requirement ID:** PROVISIONAL/DOC-24-07 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 395 — LITERAL list atom: provenance.
- **B2 mapping status:** MAPPED; B2 §16 line 360 explicitly lists provenance for Documents, and B2 §17 separately requires provenance for engineering/Twin artifacts. Category-level provenance mapping only; this row does not define a complete lineage schema, evidence contract or audit-retention policy.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define source identity, transformations, extraction/model version where applicable, corrections, deletion and downstream-reference semantics.
- **Required evidence:** Accepted provenance/lineage contract and integrity/retention/reconstruction criteria.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-19; MH-12; B2 §§6–7, 16–17, 20; AT-17.
- **Verification method:** Compare B1's provenance item with B2 §16; do not infer schema completeness from term presence.
- **Change history:** Preserves provenance as a distinct traceability label. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-08 — Knowledge extraction

- **Requirement ID:** PROVISIONAL/DOC-24-08 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 395 — LITERAL list atom: knowledge extraction.
- **B2 mapping status:** MAPPED; B2 §16 line 360 explicitly lists extraction, and line 362 describes Knowledge concepts. General extraction capability correspondence only; ontology, evidence-admission rules, uncertainty and knowledge authority are not defined by this item.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define extraction targets, schema/ontology version, source lineage, uncertainty and admission rules; preserve that knowledge is not authority and AI-generated knowledge is not automatically verified.
- **Required evidence:** Extraction contract, ontology/schema versioning, provenance and evidence-status criteria, negative-path verification.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-19; MH-10; B2 §§3–4, 16, 18, 23.
- **Verification method:** Compare B1 knowledge-extraction text with B2 §16 and AI non-authority/unverified-generation rules; do not infer a complete knowledge graph/RAG runtime.
- **Change history:** No extraction model, graph/vector backend or runtime qualified by this mapping. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-09 — Document workflows

- **Requirement ID:** PROVISIONAL/DOC-24-09 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 395 — LITERAL list atom: document workflows.
- **B2 mapping status:** MAPPED; B2 §16 line 360 explicitly lists workflows. Workflow category only; no specific ingestion/approval/export lifecycle, task owner, retries, audit events or entitlement checks are specified.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Define each workflow, owning authority, stages/states, authorization/consent where relevant, error/retry and audit behavior.
- **Required evidence:** Versioned workflow contracts, state/command paths, permission tests and failure/recovery evidence.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-19; MH-21; B2 §§3–7, 16, 20, 22; AT-17.
- **Verification method:** Compare exact category wording, then require workflow-specific contracts for concrete behavior.
- **Change history:** No workflow implementation or accepted process inferred. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-10 — Structured information

- **Requirement ID:** PROVISIONAL/DOC-24-10 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 395 — LITERAL list atom: structured information.
- **B2 mapping status:** NOT_REVIEWED; B2 §16 describes metadata, graph relations, temporal relations, provenance and extraction, but the reviewed clause does not define the full Document System contract for structured information as a bounded output/data class. Topical overlap only; formats, schemas, validation, authority, export and round-trip requirements are unresolved.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Owner defines whether this means structured document records, extracted entities, normalized fields, tabular data, or all of these, then approves schemas and import/export semantics.
- **Required evidence:** Explicit scope decision, schema/version contract and parse/validate/round-trip acceptance criteria.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-19; B2 §§7, 13, 16, 23; AT-17.
- **Verification method:** Compare B1's exact ‘structured information’ phrase to B2 §16; retain NOT_REVIEWED absent a more precise accepted contract.
- **Change history:** Conservative status; no inferred semantic coverage. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-11 — OSS security/license/provenance qualification gate

- **Requirement ID:** PROVISIONAL/DOC-24-11 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 397 — LITERAL control: mature OSS components may be used, including examples, only after security/license/provenance qualification.
- **B2 mapping status:** MAPPED; B2 §21 line 430 expresses an OSS adoption sequence: capability gap, mature search, license, security, provenance, adapter, benchmark and adoption. B2 §17 also requires provenance, authorization, licensing review and qualification for engineering/Twin artifacts. Mapped only to the general component-admission gate; it is not approval of a particular library, version, license, security posture or integration.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: Before adopting any component, document exact identity/version/license, security/provenance review, adapter boundary, benchmark and explicit adoption/owner decision.
- **Required evidence:** Pinned component review, license/SBOM, security/provenance records, bounded adapter/benchmark evidence and separate approval.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-12; MH-20/MH-21/MH-22/MH-23; B2 §§17, 20–21.
- **Verification method:** Compare B1 §24's conditional OSS rule with B2 §21's adoption sequence; mark only the generic qualification gate MAPPED.
- **Change history:** No OSS component is selected, installed or qualified by this row. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.

### DOC-24-12 — PaddleOCR as an example candidate

- **Requirement ID:** PROVISIONAL/DOC-24-12 (traceability label only; not a final child ID).
- **Owner:** TBD; accountable Document System and entitlement decision owners are not confirmed by this crosswalk.
- **Source atom / classification:** B1 §24 line 397 — LITERAL example: PaddleOCR is named only as an example subject to qualification.
- **B2 mapping status:** NOT_REVIEWED; B2 §16 does not select PaddleOCR or another specific OCR implementation. B2 §21 defines a generic adoption process, not PaddleOCR acceptance. This is a candidate identity cross-reference, not a requirement to adopt it. No OCR implementation choice is made.
- **Canonical contract path/ref:** No accepted Document System implementation/entitlement contract verified. Relevant current reference: docs/checkpoints/mediahub-functional-baseline-2.0.md @ main, SHA 1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f, §16; AT-17 remains OPEN—OWNER DECISION.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: If PaddleOCR is proposed later, require a separate owner-governed comparison of license/security/provenance, language/format coverage, accuracy, performance, packaging and recovery; otherwise record a different selected candidate with justification.
- **Required evidence:** Candidate comparison/ADR, exact version and license/security checks, benchmark, adapter/integration review and authorized install/qualification evidence if separately approved.
- **Lifecycle status:** DOCUMENTARY DRAFT / SEMANTIC AND OWNER ACCEPTANCE OPEN; implementation, verification and qualification not established.
- **Reviewer / approval reference:** Semantic Audit Batch 04 SHA e7f35460e3bf32cc3fce8b4584848907d07a7943; Product Owner Decision Record 01 SHA eb6fcbad3c8324ebbdf01f71305cb3d7d4b4c0bd (D-05 approves schema/status vocabulary only). No individual row approval recorded.
- **Dependencies:** MH-12; MH-19; MH-21/MH-22/MH-23; B2 §§16, 20–21.
- **Verification method:** Verify the example against exact B1 line 397 and explicitly distinguish conditional example from selected component.
- **Change history:** PaddleOCR remains an unselected candidate. No installation or runtime evaluation performed. Existing DOCUMENT-SYSTEM-01 / AT-17 historical records preserved; no final child ID minted.


## Initial mapping disposition

- Provisional records: 12.
- Distribution: **9 MAPPED / 2 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT**.
- Status order: MAPPED / NOT_REVIEWED / NO_DIRECT_COUNTERPART / CONFLICT.
- AT-17 remains OPEN—OWNER DECISION. The edition-feature entitlement matrix and lock/unlock/expiry/revocation/offline/reinstall/device-transfer cases remain unaccepted.
- PaddleOCR remains a B1 example candidate only. No specific OCR engine is selected or qualified.
- Existing DOCUMENT-SYSTEM-01, matrix row 24, Semantic Audit Batch 04 and atomic backlog AT-17 remain unchanged. No final child IDs or collision-check inventory created.
- B1, B2, traceability matrix, atomic/canonical backlog and main remain unchanged. No tests, qualification, installation, deployment or infrastructure action performed.
