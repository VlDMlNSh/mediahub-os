# MH-2 — Boundary Implementation / Qualification Blueprint

Date: 2026-09-30
Status: qualification-input
Scope: convert MH-2 boundary invariants into an executable qualification plan. This is not permission for production deployment.

## Objective
Demonstrate that the implemented MediaHub system preserves the MH-2 boundary model under normal, degraded and failure conditions.

## Wave 0 — provenance and contract freeze
1. Read the canonical MH-2 boundary architecture.
2. Read the boundary interface contract.
3. Verify R4 ancestry/provenance.
4. Register Q-MH2-01 as the only unresolved product decision.
5. Mark historical compute-contribution statements as superseded for current architecture.

Acceptance:
- one canonical State Authority model;
- HA Core scoped only to Smart Home operations;
- no hidden authority;
- User/Developer boundary explicit.

## Wave 1 — positive boundary tests
Verify:
- UI -> Public API -> contract -> policy -> authority;
- AI -> policy -> authority;
- Smart Home -> HA Core;
- External -> adapter -> validation -> qualification -> admission;
- Remote Mobile -> Public API only;
- approved telemetry -> Observability.

Acceptance: every authorized path reaches the intended authority without bypass.

## Wave 2 — negative boundary tests
Must prove:
- AI cannot directly mutate canonical state;
- AI cannot bypass HA Core;
- UI cannot call internal domain services;
- Remote Mobile cannot call internal services;
- Developer cannot access User Data;
- Cloud Development cannot access User Data;
- unknown devices cannot enter production;
- telemetry/cache cannot mutate canonical state;
- CPRG cannot provide general data-plane access;
- external adapters cannot obtain unrestricted internal access.

Acceptance: all forbidden paths fail closed.

## Wave 3 — data-boundary tests
Test every class:
- User Data;
- System State;
- Domain Data;
- Security Data;
- Developer Data;
- Cloud Development Data;
- Telemetry.

Verify classification, authorization, residency, egress policy and audit evidence.

Acceptance: no unclassified or unauthorized cross-boundary transfer.

## Wave 4 — deployment-boundary tests
For each qualified hardware profile:
- map logical domains to processes/services/nodes;
- verify no accidental authority duplication;
- verify shared-node isolation;
- verify distributed-domain consistency;
- verify capability limitations remain qualification data rather than architecture forks.

Acceptance: Domain != Deployment Unit remains true.

## Wave 5 — failure-boundary tests
Inject:
- Internet loss;
- Cloud loss;
- one MediaHub node loss;
- partial LAN failure;
- primary AI failure;
- one storage failure;
- stale authority;
- external integration failure.

Verify:
containment -> degraded mode -> recovery -> reconciliation -> audit.

Acceptance: optional domain failure does not collapse the qualified local core.

## Wave 6 — developer/cloud isolation
Prove:
- no User Data reaches Developer Fabric;
- no Developer Fabric path reaches State Authority;
- no cloud development path reaches user storage;
- user network is not routed over Developer Fabric;
- high-speed fabric is not implicitly trusted.

Acceptance: zero successful unauthorized probes.

## Wave 7 — mobile boundary
Prove:
- iPad Core can operate as qualified local node;
- iPhone/Android are Remote Access only;
- remote clients cannot discover or call internal services;
- all remote mutation is contract/policy controlled.

## Wave 8 — observability and evidence
Prove:
- telemetry is non-authoritative;
- high-cardinality/user payload data is not emitted;
- evidence records boundary decisions;
- audit records survive restart/recovery as required by downstream persistence design.

## Wave 9 — independent qualification
MH-20/MH-22 execute the full matrix independently.
No textual claim of PASS is accepted without fresh evidence.

## Required evidence
For every boundary:
- source contract/version;
- positive test;
- negative test;
- failure test where applicable;
- observed authority;
- data classification;
- audit/evidence reference;
- environment and hardware profile;
- result.

## Final gate
MH-2 qualification may be marked CLOSED only when:
1. all P0 boundary tests pass;
2. all P1 boundary tests pass or have explicit accepted exceptions;
3. Q-MH2-01 is resolved;
4. no hidden authority path is found;
5. User/Developer data isolation is demonstrated;
6. Local First failure tests pass;
7. MH-20/MH-22 independently record the evidence.

Until then the correct state is:
**QUALIFIED ARCHITECTURE / QUALIFICATION PENDING**.
