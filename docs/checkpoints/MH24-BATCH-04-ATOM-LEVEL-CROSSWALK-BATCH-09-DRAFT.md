# MH-24 — Supplemental Atom-Level Crosswalk: Baseline 1.0 §18 (Trusted Sources Intelligence Engine) — Draft 01

- **Status:** DOCUMENTARY DRAFT / SEMANTIC OWNER ACCEPTANCE OPEN / NOT A CANONICAL BACKLOG.
- **Working ref:** `docs/mediahub-chat-tree-map-20261012`
- **Scope:** Baseline 1.0 §18, exact source lines 297–309 at pinned B1 blob SHA `9df4892ed0734050ac79732603d15bb414717310`.
- **Purpose:** Expand the high-level `TRUSTED-SOURCES-01` semantic-audit item into source-anchored traceability fragments without pretending that list subdivisions are independently approved requirements.
- **ID rule:** `PROVISIONAL/TSI-xx` values are temporary traceability labels only. No final `MH24-B04-...` child IDs are minted by this draft. Preserve the existing high-level label `TRUSTED-SOURCES-01` and the related Batch 08 parent cross-link `CDAI4-02 / B1-17-04`; do not overwrite either historical record.
- **Pinned references:**
  - B1: `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md@main`, SHA `9df4892ed0734050ac79732603d15bb414717310`.
  - B2: `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
  - Current working MH-24 matrix: `docs/checkpoints/mediahub-mh24-traceability-matrix.md@docs/mediahub-chat-tree-map-20261012`, SHA `73377891072bac3c739c44055ceeb0874154f64c`. The matrix's row 18 is a section-level summary, not a complete accepted subsystem contract.
  - Semantic audit Batch 03: `docs/checkpoints/MH24-SEMANTIC-AUDIT-BATCH-03.md@docs/mediahub-chat-tree-map-20261012`, SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
  - Batch 08 crosswalk: `docs/checkpoints/MH24-BATCH-04-ATOM-LEVEL-CROSSWALK-BATCH-08-DRAFT.md@docs/mediahub-chat-tree-map-20261012`, SHA `a978d6846b747f397b266dc0befa05fc22cdd7ab`; Batch 08 Review 01 SHA `2c088f1837b8e5c6d257bc1b33ae3be0dedd938b`.
  - MH-10 master prompt: `docs/architecture/MH-10-CHAT-MASTER-PROMPT.md@main`, SHA `6ea847ddbf1604878303572b21b506102b23c930`.
  - MH-19 Acceptance Criteria: `docs/architecture/mh-19/MH-19-acceptance-criteria.md@architecture/mh-19-knowledge-graph-digital-twin`, SHA `9bc038123f01beb9c66e71d5f27cbc82ad3e4501`, status NOT ACCEPTED / NOT FROZEN.
  - MH-19 Evidence Register: `docs/architecture/mh-19/MH-19-evidence-register.md@architecture/mh-19-knowledge-graph-digital-twin`, SHA `854fe2c0fc604d80b4e1af7d384ec1fb943fe6df`, status OBSERVED / PROPOSED REGISTER; production graph, vector/RAG runtime and graph persistence are recorded UNKNOWN.
  - Product Owner Decision Record 01: `docs/checkpoints/MH24-BATCH-04-PRODUCT-OWNER-DECISION-RECORD-01.md@docs/mediahub-chat-tree-map-20261012`, SHA `9117098e22c26708d48ca8ba5954669faa209d68`. It approves the 12-field schema and mapping vocabulary, but not these individual mappings or a canonical backlog promotion.

## Mapping rules used in this draft

- `MAPPED` means a cited B2 clause explicitly documents the same bounded capability or constraint. It is not implementation or qualification evidence.
- `NO_DIRECT_COUNTERPART` is limited to the exact named first-class subsystem requirement in the pinned B2 text reviewed here. It does not assert global repository absence.
- `NOT_REVIEWED` is retained for partial, broader, overlapping or not-yet-contractual matches. A general “knowledge/search” label is not taken as full coverage of each specific source lifecycle operation.
- `CONFLICT` is not assigned absent explicit contradictory normative text.
- B2 §16 explicitly names source verification, provenance, evidence and the rule that AI-generated knowledge is not automatically verified. B2 §18 preserves AI's non-authority boundary and policy-subordinate routing. These are relevant documentary correspondences, not proof of the complete Trusted Sources engine.
- B2 matrix row 18 (“Trusted Sources | Verified evidence/provenance subsystem”) is noted as a section-level cross-reference, but it does not by itself specify the complete source lifecycle, trusted-source classification policy, interfaces, ownership or runtime contract.
- The 17 rows below are traceability subdivisions of B1 §18 lines 299–309. They are not asserted to be 17 distinct, independently approved product requirements.

## Provisional atom records

### TSI-01 — First-class subsystem identity

- **Requirement ID:** `PROVISIONAL/TSI-01` (temporary traceability label only; not a final child ID).
- **Owner:** TBD; no single accepted owner for the Trusted Sources subsystem was established by the inspected documents.
- **Source atom / classification:** B1 §18 line 299 — LITERAL: Trusted Sources Intelligence Engine is a separate first-class subsystem of Cloud Development AI.
- **B2 mapping status:** `NO_DIRECT_COUNTERPART`; B2 §18 names the three AI tiers but does not define Trusted Sources Intelligence Engine as a distinct first-class subsystem with a bounded contract. Matrix row 18 is an index-level summary, not a substitute for that contract.
- **Canonical contract path/ref:** No accepted subsystem contract verified. Related sources: B2 §16 and §18 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; matrix row 18 @ working ref SHA `73377891072bac3c739c44055ceeb0874154f64c`; MH-19 branch acceptance SHA `9bc038123f01beb9c66e71d5f27cbc82ad3e4501`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: owner explicitly preserves, revises or defers the named subsystem; if preserved, approve its purpose, interfaces, ownership and boundaries from ordinary knowledge/search and Cloud Development AI.
- **Required evidence:** Owner decision; versioned subsystem contract; source-policy/interface definitions; dependency and trust-boundary map; acceptance criteria and evidence register.
- **Lifecycle status:** DRAFT / NOT APPROVED; design, implementation, verification, qualification and release remain OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 approves vocabulary/schema only; semantic audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`; no per-atom owner approval recorded.
- **Dependencies:** MH-10; MH-19; MH-21; MH-12; MH-13; MH-20; MH-22.
- **Verification method:** Compare the exact B1 §18 line 299 requirement with pinned B2 §§16/18 and inspect an accepted subsystem contract before changing status.
- **Change history:** New supplemental traceability label; preserve `TRUSTED-SOURCES-01` and `CDAI4-02 / B1-17-04` as historical/high-level cross-links. No final child ID minted.

### TSI-02 — Source discovery

- **Requirement ID:** `PROVISIONAL/TSI-02`.
- **Owner:** TBD; Trusted Sources domain owner is not accepted in the reviewed record.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: discovery of sources.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §16 describes document/knowledge search and source verification, but does not define external-source discovery scope, connectors or policy.
- **Canonical contract path/ref:** No accepted TSI contract verified; related B2 §16 and §18, B1 §18 line 301, MH-10 master prompt SHA `6ea847ddbf1604878303572b21b506102b23c930`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define source classes, discovery scope, trust boundaries, allowed networks/connectors and prohibited source classes.
- **Required evidence:** Approved source-catalogue contract, connector inventory, threat/data-source policy and source-discovery acceptance record.
- **Lifecycle status:** DRAFT / NOT APPROVED; functionality and verification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-19; MH-21; MH-12; MH-13.
- **Verification method:** Compare B1 §18 line 301 with B2 §16; review an accepted source-discovery contract and evidence before mapping further.
- **Change history:** Subdivision of existing high-level `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-03 — Search sources

- **Requirement ID:** `PROVISIONAL/TSI-03`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: source search.
- **B2 mapping status:** `NOT_REVIEWED`; semantic/full-text search is explicit in B2 §16, but exact source-search scope, filtering and result provenance are not fully specified by that clause.
- **Canonical contract path/ref:** No accepted TSI contract verified; B2 §16 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define query semantics, source selection, ranking/filtering, citation integrity and policy restrictions.
- **Required evidence:** Search API/interface contract, deterministic examples or fixtures, source attribution requirements and independent review record.
- **Lifecycle status:** DRAFT / NOT APPROVED; design and verification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-19; MH-21.
- **Verification method:** Compare source search with B2 §16's broader semantic/full-text search and check whether source-level semantics are normatively defined.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-04 — Trust classification

- **Requirement ID:** `PROVISIONAL/TSI-04`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: classification of source trustworthiness.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §6 addresses identity, trust and security generally, but the reviewed text does not specify trust classification for information sources.
- **Canonical contract path/ref:** No accepted TSI trust-classification contract verified; B2 §§6 and 16 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define trust dimensions, evidence requirements, decay/reassessment rules, uncertainty representation and separation from user authorization.
- **Required evidence:** Approved source-trust taxonomy/policy, representative edge cases and review/override rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; policy and implementation verification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-12; MH-13; MH-19; MH-21.
- **Verification method:** Compare B1 §18 line 301 with B2 §6/§16; do not equate network identity trust with source-content trust.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-05 — Retrieval

- **Requirement ID:** `PROVISIONAL/TSI-05`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: retrieval.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §16 mentions search and AI context, but the retrieval lifecycle, access policy, source snapshots and citation linkage are not fully specified.
- **Canonical contract path/ref:** No accepted retrieval contract verified; B2 §16 and §18 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define retrieval inputs/outputs, permissions, query provenance, source version pinning and behavior for inaccessible or changed sources.
- **Required evidence:** Retrieval interface contract, source/version trace, policy-denial cases and reproducible retrieval examples.
- **Lifecycle status:** DRAFT / NOT APPROVED; design, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-19; MH-21; MH-12; MH-13.
- **Verification method:** Compare B1 §18 line 301 with B2 §16 and confirm an accepted retrieval API/contract exists before upgrading status.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-06 — Source verification

- **Requirement ID:** `PROVISIONAL/TSI-06`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: verification of sources.
- **B2 mapping status:** `MAPPED`; B2 §16 explicitly lists source verification within Knowledge. This is documentary capability correspondence only.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, §16, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; no accepted verification-engine contract verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: specify verification methods, source authenticity/freshness criteria, conflict handling, limitations and how unsupported claims remain unresolved.
- **Required evidence:** Accepted verification-policy contract; positive/negative examples; source provenance records; implementation/qualification evidence when authorized.
- **Lifecycle status:** DRAFT / NOT APPROVED; documentary mapping present, implementation/verification/qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 approves vocabulary/schema only; Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-19; MH-12; MH-13; MH-21; MH-22.
- **Verification method:** Re-read B2 §16 at the pinned SHA; separately verify that an accepted implementation contract and current execution evidence exist before claiming runtime behavior.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; MAPPED is documentary only; no final child ID minted.

### TSI-07 — Provenance

- **Requirement ID:** `PROVISIONAL/TSI-07`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: provenance.
- **B2 mapping status:** `MAPPED`; B2 §16 explicitly lists provenance in Documents and Knowledge. No implementation status is inferred.
- **Canonical contract path/ref:** B2 §16 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; no accepted TSI-specific provenance contract verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define provenance schema, source identifiers, content/version fingerprints, timestamps, transformation lineage and integrity rules.
- **Required evidence:** Accepted provenance schema/contract, lineage examples and consistency/integrity verification evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; documentary mapping present, implementation/verification/qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 approves vocabulary/schema only; Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-19; MH-21; MH-12; MH-13; MH-22.
- **Verification method:** Compare exact B1 line 301 with B2 §16; verify required provenance fields in a separately accepted contract before further mapping.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; MAPPED is documentary only; no final child ID minted.

### TSI-08 — Source comparison

- **Requirement ID:** `PROVISIONAL/TSI-08`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: comparison of sources.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §16 documents source verification and provenance but does not specify source-to-source comparison or conflict adjudication.
- **Canonical contract path/ref:** No accepted source-comparison contract verified; B2 §16 and §23 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define comparison dimensions, source precedence constraints, contradiction representation and human/governance escalation.
- **Required evidence:** Source-comparison contract, conflict fixtures, provenance-linked results and explicit undecidable/unknown cases.
- **Lifecycle status:** DRAFT / NOT APPROVED; design and verification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-19; MH-20; MH-21.
- **Verification method:** Inspect B2 §16 and relevant accepted knowledge/provenance contracts; source comparison must not infer authority from confidence.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-09 — Change detection

- **Requirement ID:** `PROVISIONAL/TSI-09`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: source change detection.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §16 includes temporal relations, but does not define change detection, polling/subscription, version comparison or notification behavior.
- **Canonical contract path/ref:** No accepted change-detection contract verified; B2 §16 and §23 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define change identity, content/version comparison, scheduling, freshness, false-positive handling and retention.
- **Required evidence:** Change-detection contract, versioned source fixtures, freshness policy and event provenance.
- **Lifecycle status:** DRAFT / NOT APPROVED; design/verification/qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-11; MH-19; MH-21.
- **Verification method:** Compare B1 line 301 with B2 §16 temporal relations; do not infer change detection from temporal metadata alone.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-10 — Evidence formation

- **Requirement ID:** `PROVISIONAL/TSI-10`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: formation of evidence.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §16 names evidence but does not specify an evidence-formation workflow, admissibility or completeness rules.
- **Canonical contract path/ref:** B2 §16 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; no accepted evidence-formation contract verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define evidence atom schema, admissibility, source linkage, missing-field/uncertainty handling and review lineage.
- **Required evidence:** Accepted evidence schema, provenance-link checks, negative cases and reviewer decision record.
- **Lifecycle status:** DRAFT / NOT APPROVED; design/verification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-19; MH-20; MH-21; MH-22.
- **Verification method:** Separate the existence of an evidence concept in B2 §16 from approved evidence production/workflow semantics.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-11 — Accumulation of verified knowledge

- **Requirement ID:** `PROVISIONAL/TSI-11`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: accumulation of verified knowledge.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §16 describes Knowledge and source verification, but does not define verified-knowledge lifecycle, admission, update or correction semantics.
- **Canonical contract path/ref:** B2 §16 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; no accepted verified-knowledge lifecycle contract verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define admission criteria, versioning, correction/retraction, retention and distinction between verified evidence and derived knowledge.
- **Required evidence:** Accepted knowledge lifecycle contract, version/correction fixtures and linked source/evidence lineage.
- **Lifecycle status:** DRAFT / NOT APPROVED; design, implementation, verification and qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-19; MH-21; MH-12; MH-13; MH-22.
- **Verification method:** Compare B1 line 301 with B2 §16; verify an accepted admission/update/retraction contract before moving from NOT_REVIEWED.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-12 — Track information origin

- **Requirement ID:** `PROVISIONAL/TSI-12`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 301 — LITERAL capability fragment: tracking origin/provenance of information.
- **B2 mapping status:** `NOT_REVIEWED`; overlaps with TSI-07 provenance. The independent meaning (lineage across transformations, retrieval and generated summaries) must be clarified before duplicate obligations are created.
- **Canonical contract path/ref:** B2 §16 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; no accepted transformation-lineage contract verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: owner resolves whether this is a distinct transformation-lineage obligation or a refinement of TSI-07; define lineage boundaries if distinct.
- **Required evidence:** Owner disposition; lineage schema and examples spanning source → retrieved passage → synthesis/output.
- **Lifecycle status:** DRAFT / NOT APPROVED; duplicate/overlap disposition OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-19; MH-20; MH-21.
- **Verification method:** Review TSI-07/TSI-12 alongside B1 line 301 and B2 §16; do not mint a final child ID before overlap resolution.
- **Change history:** Explicitly records a potential overlap; no silent deduplication and no final child ID minted.

### TSI-13 — Distinguish verified evidence

- **Requirement ID:** `PROVISIONAL/TSI-13`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 lines 303–304 — LITERAL category fragment: verified evidence.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §16 names evidence, provenance and source verification but does not define the “verified evidence” category or threshold.
- **Canonical contract path/ref:** B2 §16 and §23 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; no accepted evidence-state taxonomy verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define when evidence may carry verified status, who/what can issue it and what invalidates/revokes that status.
- **Required evidence:** Evidence-state taxonomy, verification criteria, provenance link and invalidation/revocation rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; taxonomy and verification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-12; MH-13; MH-19; MH-20; MH-21.
- **Verification method:** Compare literal B1 category with B2 §16; confirm an accepted taxonomy and evidentiary threshold.
- **Change history:** Subdivision of category list in `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-14 — Distinguish external source

- **Requirement ID:** `PROVISIONAL/TSI-14`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 lines 303–305 — LITERAL category fragment: external source.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §16 includes source verification but does not define external-source identity, trust boundary or provenance requirements by category.
- **Canonical contract path/ref:** B2 §16 and §23 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; no accepted external-source classification contract verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define source identity, fetch time, publisher/authority, external trust boundary and immutable origin references.
- **Required evidence:** External-source schema/policy, source-identity fixtures and provenance verification records.
- **Lifecycle status:** DRAFT / NOT APPROVED; schema/policy/verification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-12; MH-13; MH-19; MH-21.
- **Verification method:** Compare the category list in B1 §18 with B2 §16; do not infer category semantics from general provenance alone.
- **Change history:** Subdivision of category list in `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-15 — Distinguish inferred information

- **Requirement ID:** `PROVISIONAL/TSI-15`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 lines 303–306 — LITERAL category fragment: inferred information.
- **B2 mapping status:** `NOT_REVIEWED`; B2 distinguishes knowledge and evidence but does not establish a named inferred-information state or its rules.
- **Canonical contract path/ref:** B2 §16 and §18 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; no accepted inference-state contract verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define inference label, supporting evidence links, uncertainty/confidence representation and prohibition against silently promoting inference to verified evidence.
- **Required evidence:** Inference-state schema, provenance-linked example and negative tests/acceptance checks proving that inference is not relabelled as verified source evidence.
- **Lifecycle status:** DRAFT / NOT APPROVED; contract and verification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-12; MH-13; MH-19; MH-20; MH-21.
- **Verification method:** Compare B1 §18's explicit category with B2 §§16/18; inspect state-transition rules if supplied.
- **Change history:** Subdivision of category list in `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-16 — Distinguish AI-generated information

- **Requirement ID:** `PROVISIONAL/TSI-16`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 lines 303–307 — LITERAL category fragment: AI-generated information.
- **B2 mapping status:** `NOT_REVIEWED`; B2 §16 explicitly addresses AI-generated knowledge and verification, but not the complete four-category taxonomy or all generated-information types.
- **Canonical contract path/ref:** B2 §16 and §18 @ main SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; no accepted AI-output labeling/schema contract verified.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: define how generated content is identified, carries lineage and remains distinguished from external-source material and inference.
- **Required evidence:** Output-provenance schema, generated-content fixtures and downstream consumer rules.
- **Lifecycle status:** DRAFT / NOT APPROVED; contract, implementation and verification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 (schema/vocabulary only); Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-12; MH-13; MH-19; MH-21.
- **Verification method:** Compare B1 category list with B2 §16 and §18; verify explicit identification and propagation of generated-origin metadata.
- **Change history:** Subdivision of category list in `TRUSTED-SOURCES-01`; no final child ID minted.

### TSI-17 — No automatic verification of generated information

- **Requirement ID:** `PROVISIONAL/TSI-17`.
- **Owner:** TBD.
- **Source atom / classification:** B1 §18 line 309 — LITERAL invariant: AI-generated information must not automatically be considered verified evidence.
- **B2 mapping status:** `MAPPED`; B2 §16 explicitly states that AI-generated knowledge is not automatically verified. This records text correspondence only; enforcement remains unverified.
- **Canonical contract path/ref:** B2 `docs/checkpoints/mediahub-functional-baseline-2.0.md@main`, §16, SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`; related MH-10 master prompt SHA `6ea847ddbf1604878303572b21b506102b23c930`.
- **Acceptance criteria:** PROPOSED / NOT APPROVED: generated information carries explicit origin state; verification status cannot be granted by generation alone; any verification transition has a recorded, reviewable basis.
- **Required evidence:** Accepted provenance/verification contract; positive and negative cases for generated output; enforcement evidence when tests are separately authorized.
- **Lifecycle status:** DRAFT / NOT APPROVED; documentary mapping present, implementation/verification/qualification OPEN.
- **Reviewer / approval reference:** Product Owner Decision Record 01 approves schema/vocabulary only; Semantic Audit Batch 03 SHA `fcd006e99d812dac5071b34c531f2783f4f54e88`.
- **Dependencies:** MH-10; MH-12; MH-13; MH-19; MH-20; MH-21; MH-22.
- **Verification method:** Re-read B1 line 309 and B2 §16 at pinned SHAs; separately verify an accepted state/provenance contract and implementation evidence before claiming enforcement.
- **Change history:** Subdivision of `TRUSTED-SOURCES-01`; `MAPPED` is documentary only; no final child ID minted.

## Batch summary

- 17 provisional traceability rows.
- Status distribution: **3 MAPPED / 13 NOT_REVIEWED / 1 NO_DIRECT_COUNTERPART / 0 CONFLICT**.
- This status distribution is scoped to B1 §18, not to all of B1 or the parent-level Batch 04 backlog.
- No final child IDs, no canonical backlog promotion, no Baseline/matrix changes, and no implementation/test/qualification claims are made.
- B1 §18's `TRUSTED-SOURCES-01` high-level item remains open; the named subsystem, its source lifecycle, ownership and acceptance criteria require explicit semantic/governance disposition.
