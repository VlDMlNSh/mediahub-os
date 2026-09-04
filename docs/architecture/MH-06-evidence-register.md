# MH-06 — Evidence Register

Status: RECONCILED / REQUIRES VERIFICATION

## Repository-resident evidence verified in this pass
- MH-06 index, core runtime model, lifecycle model, security invariants, dependency map, decision log, contradiction register, unknown register and acceptance criteria are present on the default branch.
- The lifecycle artifact explicitly preserves the accepted P0-06 seven-value canonical lifecycle relation and separates service/health states from canonical P0-06 lifecycle.
- The core runtime artifact preserves P0-04 as sole canonical mutation authority and P0-05 as the mandatory integration/authorization boundary.
- The security artifact contains the 20 MH-6 security invariants.
- The acceptance artifact explicitly separates architecture acceptance from implementation quality and production qualification.

## Evidence not independently closed by this pass
- frozen P0-06 implementation verification chain and exact implementation/test evidence;
- direct repository path reconciliation for P0-03/P0-04/P0-05/P0-07 source artifacts;
- full semantic reconciliation with MH-1…MH-5;
- runtime topology, host and hardware evidence;
- security negative tests for future conceptual services;
- implementation-specific startup/shutdown, scheduling, resource, IPC, isolation and recovery parameters.

## Evidence rule
Repository presence is evidence of artifact existence, not proof of runtime correctness. Absence of evidence means REQUIRES VERIFICATION, not VERIFIED. Architecture acceptance, implementation verification and production qualification remain separate gates.
