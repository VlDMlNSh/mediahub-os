# MHX v1.0 — Local Execution Loop

This pass turns the MHX skeleton into an operational local loop:

`manifest -> index -> chunk -> task -> cache -> result -> review -> revision -> integration`

## Safety boundary

MHX is development/execution infrastructure. Governance state remains external and frozen.

- no VAL identity creation
- no governance approval
- no baseline approval
- no historical equivalence
- worker output is untrusted until primary review
- master changes occur only through reviewed integration

## Task lifecycle

`PENDING -> RUNNING -> COMPLETED`

Governance-impacting tasks are rejected into `tasks/failed/` with `BLOCKED / GOVERNANCE_IMPACT`.

## Cache

Exact lookup uses the task fingerprint. Related results can be stored separately for explicit delta reuse.

`EXACT -> reuse`, `RELATED -> delta`, `NONE -> execute`.

## Integration

Only reviewed `ACCEPT` results can integrate. Integration writes changed artifacts through temporary files and records rollback material before updating the local revision state. Hash mismatches or write failures trigger rollback.

## CLI

```text
mhx init
mhx manifest .
mhx index
mhx chunk --lines 80

mhx task create TASK-001 "..."
mhx task claim TASK-001 W-LOCAL

mhx result normalize raw-result.json RESULT-001
mhx cache-store <task-hash> .mhx/results/normalized/RESULT-001.json
mhx cache <task-hash>

mhx review RESULT-001 ACCEPT
mhx revision
mhx integrate RESULT-001
mhx status
```

The CLI intentionally does not expose commands for creating VAL records or changing governance/baseline state.
