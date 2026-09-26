# MediaHub Forensic Semantic Status Normalization — 2026-09-05

STATUS: PROPOSED / RECOVERY GOVERNANCE ONLY
BRANCH: recovery/full-functional-spec

## Purpose

This artifact closes the terminology defect identified during the consolidated forensic pass. It does not change the functional baseline and does not accept the Master Architecture.

## Required semantic distinction

The recovery corpus must distinguish these states:

- `CONFIRMED_ACCEPTED` — explicitly accepted baseline requirement/capability/evidence at the relevant authority level.
- `RECOVERY_FINDING` — historically observed material requiring reconciliation; not evidence of loss.
- `UNKNOWN_EVIDENCE` — the relevant source/evidence is unavailable or not recoverable from the currently accessible corpus.
- `DEFERRED` — the capability/requirement remains valid, but an implementation or technical detail is intentionally unresolved.
- `OPEN_BOUNDARY_QUESTION` — canonical ownership exists, but an exact cross-component or technical boundary is not yet specified.
- `PARTIAL` — evidence/verification/acceptance coverage exists but is not complete.
- `RECONCILED` — competing historical/semantic representations have been reconciled at the stated level.
- `REJECTED` — explicitly rejected by an authoritative decision. This state must never be inferred from absence, deferral, or architecture limitations.
- `LOST` — permitted only when authoritative evidence establishes that a previously accepted capability was intentionally removed/retired. Current recovery evidence establishes no such product capability loss.

## Current corrections

1. `LOST-001` in `recovery/lost-capabilities.yaml` describes a historical MH-18 media architecture surface with disposition `RECOVER_AND_RECONCILE`. Its semantic status is therefore a `RECOVERY_FINDING`, not proven `LOST` functionality. The legacy identifier is preserved for historical compatibility.
2. `LOST-002` is explicitly `UNKNOWN_NOT_LOSS`; it must be interpreted as `UNKNOWN_EVIDENCE` despite its legacy identifier.
3. `LOST-003` is `DEFERRED`; it is not loss.
4. `known_unowned_gaps` in `recovery/unowned-capabilities.yaml` are not proof of absent canonical owners. They are `OPEN_BOUNDARY_QUESTION` records because canonical component ownership is already declared.
5. No historical artifact is renamed, deleted, or rewritten solely to normalize terminology.

## Governance rule

Legacy identifiers are evidence labels. Semantic state is determined by the disposition/status fields and authoritative evidence, not by the identifier prefix.

## Functional impact

NONE. CAP-001…CAP-058 remain preserved. No capability is removed, downgraded, or reinterpreted as rejected.

## Gate impact

- Functional baseline: unchanged, `CONFIRMED_ACCEPTED`.
- Historical reconciliation: still `IN PROGRESS`.
- Verification/acceptance: still `PARTIAL / OPEN`.
- Technical contracts: still `OPEN / DEFERRED`.
- Master Architecture: still `DRAFT — NOT ACCEPTED`.
- MH-01…MH-23 redistribution: still `BLOCKED`.
- Production implementation: still `BLOCKED`.

## Next required closure artifact

A complete CAP-001…CAP-058 verification/acceptance matrix remains required. Each row must identify requirement linkage, contract linkage, invariant linkage, owner, architecture boundary, dependency evidence, verification identity, acceptance evidence, authority, provenance, and terminal state without inventing missing evidence.
