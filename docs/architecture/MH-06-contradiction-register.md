# MH-06 — Contradiction Register

Status: OPEN / TRACKED

## C-01 — Lifecycle terminology
MH-6 generic lifecycle vocabulary includes stop/fail/quarantine concepts, while accepted P0-06 canonical lifecycle has a closed seven-value relation. Resolution: keep generic service/health/supervision states separate; do not alter P0-06 lifecycle without governance.

## C-02 — Evidence continuity
The repository contains MH-06 architectural records, but this pass did not independently close the complete P0-06 implementation verification chain or all P0-03/P0-04/P0-05/P0-07 source-path reconciliation. Therefore implementation claims remain evidence-dependent.

## C-03 — Architecture vs implementation qualification
MH-06 can be architecturally coherent while implementation topology, host integration, IPC, scheduler, resource limits, isolation and recovery parameters remain unknown. No implementation or production qualification follows from the architecture records alone.

## C-04 — P0-07 governance/API gap
MH-6 must consume configuration/policy through the governed interface; it must not invent a mutation publication path or bypass the unresolved P0-07 governance/API gap.

## Disposition rule
No contradiction in this register authorizes semantic change to P0-03…P0-06. Resolution requires evidence, an explicit decision/ADR where appropriate, and governance acceptance.
