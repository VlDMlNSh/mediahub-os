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
