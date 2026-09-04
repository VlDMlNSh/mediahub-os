# MH-06 — Contradiction Register

Status: OPEN / TRACKED

## C-01 — Lifecycle terminology
SEMANTICALLY RESOLVED. Generic service/health/supervision states remain separate from the accepted P0-06 canonical lifecycle. No P0-06 lifecycle expansion is authorized by MH-06.

## C-02 — Evidence continuity
OPEN. Historical P0-06 acceptance exists at `d9b5c9db128d8ec75dae6fbd03b5d54950bdddf5`, but no reproducible current workflow run for that exact frozen implementation has been established. Therefore current execution remains NOT VERIFIED.

## C-03 — Health/Readiness semantic mapping
RESOLVED by accepted `MH-06-ADR-001-health-readiness-semantic-contract.md`. Health is observational; Readiness is operation-scoped and derived; neither is authoritative; P0-06 lifecycle READY is not readiness READY.

## C-04 — P0-07 governance/API gap
OPEN. MH-6 must consume governed configuration/policy and must not invent a mutation publication path or bypass the unresolved P0-07 governance/API gap.

## C-05 — Concrete dependency/runtime policy
OPEN / UNKNOWN. Exact dependency graph, operation mapping, resource limits, quarantine thresholds, recovery transitions, IPC and topology are not yet evidenced. These are not semantic permission to weaken the accepted contract.

## Disposition rule

No contradiction in this register authorizes semantic change to P0-03…P0-06. Resolution requires evidence, explicit decision/ADR where appropriate, and governance acceptance.
