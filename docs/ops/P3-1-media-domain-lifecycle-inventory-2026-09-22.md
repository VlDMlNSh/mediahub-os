# P3.1 Media Domain Contract and Lifecycle Inventory

Status: VERIFIED_LOCAL_SUBSCOPE / P3.1 NOT CLOSED

## Repository-observed contract

Source: `ops/mediahub_lifecycle_contract.py`
Tests: `tests/test_mediahub_lifecycle_contract.py`

Observed lifecycle states: `ABSENT`, `CANDIDATE`, `VALIDATED`, `AUTHORIZED`, `PUBLISHED`, `APPLIED`, `SUPERSEDED`.

Observed transitions are explicit and monotonic through the `_ALLOWED` transition map. Invalid transitions are rejected.

Observed persistence contract requires `authority == state-authority`, a typed `VersionIdentity`, and an explicit boolean `durable` flag; physical durability is not implied by construction.

Observed migration contract requires non-empty migration identity, typed source/target versions, boolean rollback support, and a revision change.

## Verification

Command: `pytest -q tests/test_mediahub_lifecycle_contract.py`

Acceptance: the existing lifecycle/persistence/migration contract tests pass at the current repository state.

## Boundary

This evidence inventories only the repository-native lifecycle contract. It does not qualify media ingestion, metadata/indexing, playback/control, authorization, storage, retention, recovery, integration, performance, or production behavior.
