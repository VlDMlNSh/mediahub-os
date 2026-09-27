# P3.2 Ingestion / Metadata / Index Gap Reconciliation

Status: DISCOVERY_RECONCILIATION / P3.2 NOT CLOSED

## Queue requirement

`P3.2 Implement/qualify ingestion and metadata/index contracts.`

## Exact repository surfaces inspected

- `ops/mediahub_lifecycle_contract.py` — generic lifecycle, persistence/version and migration contract; no media ingestion/index API.
- `tests/test_mediahub_lifecycle_contract.py` — tests for the generic lifecycle contract.
- `ops/mediahub_streaming_boundary.py` — provider-neutral streaming transport boundary.
- `tests/test_mediahub_streaming_boundary.py` — deterministic streaming-boundary tests.

## Classification

- Ingestion contract: ABSENT in the inspected media-specific repository surface.
- Metadata contract: ABSENT as a media-specific ingestion/index acceptance surface.
- Index contract: ABSENT as a media-specific ingestion/index acceptance surface.
- Existing lifecycle contract: PRESENT, but insufficient to satisfy P3.2.
- Existing streaming transport boundary: PRESENT, but it does not establish ingestion, metadata/index, or playback semantics.

## Gate

This artifact only encodes the factual acceptance-surface gap. It does not add media semantics, implementation, qualification, or production authority. A future P3.2 implementation task requires an explicit media-specific contract, deterministic tests, and provenance-bound acceptance evidence.
