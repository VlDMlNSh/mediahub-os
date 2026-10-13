# P0-07 D7 — canonical state-version crosswalk

Date: 2026-10-13
Status: READ-ONLY SOURCE CROSSWALK / PARTIAL / NOT ACCEPTED / NOT FROZEN

## Evidence

Read from `main`:
- `runtime/mediahub_runtime/in_memory_state.py` — `0fbc71369d19e09944ba67a60ccb9df802f30a4b`
- `runtime/mediahub_runtime/generation.py` — `4e4fe0e40d67c18c918881d79dc2cc9933988b2c`
- `runtime/mediahub_runtime/authorization.py` — `4d8df5d3c1c26f7f133a8093cd270635b085f4d5`
- `runtime/mediahub_runtime/consumer_boundary.py` — `98bf2da9cea85da2c82145b4baef417c20b9ae73`
- `runtime/mediahub_runtime/state.py` — `a2115b81f52a63feb357e484bd982a6a32641d81`

## Findings

The inspected in-memory authority stores a canonical integer `state_version`. Transactions capture the current generation and version. Commit checks transaction status, authorization, generation ID, binary/schema compatibility, and exact current-version freshness; successful commit advances the current version. Generation compatibility requires matching generation ID, binary version, schema version and state version. Restore checks checkpoint ownership, integrity, generation compatibility and self-test, then advances the current version rather than resetting to the checkpoint's historical version.

P0-05 delegates through opaque consumer transaction handles. P0-04 authorization uses explicit principal/capability/operation grants and default-deny, but the inspected module does not identify the issuer or authentication lifecycle. These files do not demonstrate a complete trusted P0-07 → P0-05 → P0-04 caller path.

## Disposition

D7 is PARTIAL: in-memory version/generation mechanics are source-evidenced, but accepted ownership of generation/schema change control and end-to-end revision binding are NOT EVIDENCED in this source set. Persistence, crash recovery, migration and runtime qualification are not proven; the implementation explicitly states persistence is out of scope.

P0-07 mutation/publication remains BLOCKED — GOVERNANCE/API GAP. P0-05 v1.1 remains NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN. Qualification remains NO-GO / NOT PROVEN.

Next: re-read map-selected MH-14 persistence, MH-16 lifecycle/migration and MH-22 qualification primary artifacts; identify whether they specify an accepted change-control owner and evidence path. No tests, runtime actions, deployment or merge were performed.


## Follow-up — governance-question deduplication and metadata/change-control boundary (2026-10-13)

- Re-read the existing P0-05 v1.1 candidate (docs/checkpoints/p0-05-consumer-contract-v1.1-candidate-for-governance-review-2026-10-12.md, live docs-branch blob 79e2b4865c47b5394ade266cd3cd7cfbe3097717). Its D7 already asks whether the candidate becomes P0-05 v1.1 or a separately governed domain-operation contract. Do not create a duplicate owner question or a new decision ID.
- Existing owner directions in docs/checkpoints/mediahub-owner-decisions-2026-10-12.md retain D7 C → B: inspect versioning/change-control rules first; propose v1.1 only if in scope, otherwise route a separately governed contract. This direction is not adoption, acceptance, freeze or implementation authorization.
- Current main tree SHA 1d45bbccbbbd27309c39cb9e9351bb291cdb47a8 contains schemas/core/contract-metadata.schema.json blob 0e9e6b0233612c37f316fa83e7786325c992af13, which requires schema_id, semver-shaped schema_version, owner, required/optional fields and constraints. This is a metadata-shape contract only; it does not define who is authorized to change/freeze a schema, compatibility rules, migration approvals, immutable revision binding, or cross-component evidence ownership.
- P0-06 governance packet blob 95d5d7292e55e1bc438d0742137988888d651e7a says changes to P0-04/P0-05 semantics, authority invariants, persistence scope or P0-06 security boundary invalidate its implementation authorization and require a new governance decision. This is relevant change-control evidence, but it is scoped to P0-06 and does not establish the missing cross-domain owner for P0-07 D7.
- Therefore no additional owner question is needed at this stage: the candidate already contains the unresolved D7 choice. The next useful step is to prepare a source-anchored comparison of the existing candidate's D7 scope against the schema metadata and MH-14/MH-16/MH-22 gates, then route that same existing decision to its owner. Do not change its wording or mark it answered without owner disposition.
- D7 remains PARTIAL / NOT ACCEPTED / NOT FROZEN; P0-07 mutation/publication BLOCKED — GOVERNANCE/API GAP; P0-05 v1.1 NON-NORMATIVE / NOT ACCEPTED / NOT FROZEN; qualification NO-GO / NOT PROVEN.
