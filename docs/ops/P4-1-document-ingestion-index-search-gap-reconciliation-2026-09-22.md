# P4.1 Document Ingestion / Index / Search Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P4.1 NOT CLOSED

## Queue requirement

`P4.1 Complete document ingestion/index/search contracts.`

## Exact architecture/contract surfaces inspected

- `specification/contract-registry.yaml` — CTR-034 defines unified indexing/search/knowledge-graph access and requires indexing provenance, consistency, authorization filtering, freshness, offline operation and rebuild.
- `specification/MEDIAHUB-FUNCTIONAL-BASELINE-1.0.md` — defines Document System and document search capabilities.
- `docs/architecture/MH-21-rag-boundary.md` — declares a RAG flow from ingestion through index and retrieval, with retrieved context treated as untrusted data.
- `docs/architecture/MH-21-rag-security.md` — declares hostile-document handling, provenance, classification, privacy and authorization boundaries.
- `docs/architecture/MH-21-resource-governance.md` — declares bounded resources for RAG retrieval/vector search and related AI workloads.

## Classification

- Document ingestion implementation contract: ABSENT as an executable document-specific acceptance surface.
- Document indexing implementation contract: ABSENT as an executable document-specific acceptance surface.
- Document search implementation contract: ABSENT as an executable document-specific acceptance surface.
- Architecture/requirements: PRESENT, including explicit indexing/search/RAG semantics, but declarations are not implementation evidence.

## Gate

This artifact records only the factual acceptance-surface gap. It does not invent document schemas, OCR behavior, chunking, embedding models, vector stores, ranking, synchronization or production behavior. A future P4.1 implementation task requires explicit document contracts, deterministic tests, provenance-bound acceptance evidence and reproducible rebuild/search behavior.
