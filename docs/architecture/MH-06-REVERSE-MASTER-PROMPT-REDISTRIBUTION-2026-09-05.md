# MH-06 — Reverse Master Prompt
## Redistribution / Reconciliation Control Point — 2026-09-05

Status: RECONCILED / SEMANTIC CONTRACT GOVERNANCE ACCEPTED / IMPLEMENTATION BLOCKED

## 1. MH identifier
MH-06 — Core Runtime Services / Health / Readiness / Scheduling / Resource Governance / Recovery / IPC / Observability.

## 2. Historical scope
The current MH-06 historical contour is represented by the recovered MH-06 architecture corpus and the previously reconciled Core Runtime Services scope. The redistribution scope is: runtime orchestration, lifecycle relation, startup/shutdown, health/readiness, supervision, scheduling, resource governance, execution context, dependency coordination, recovery, failure domains, IPC, observability, configuration/policy interaction, AI interaction, persistence boundary and update/recovery boundary.

This is projection/reconciliation, not a restart of forensic recovery.

## 3. Source evidence
Authoritative control sources on `recovery/full-functional-spec`:
- `recovery/forensic-control-point-2026-09-05.md` — SHA `203e38cfeb0282991307a32a6566c4f7f4e0e506`
- `recovery/mh01-23-redistribution-projection-matrix-2026-09-05.yaml` — SHA `d4c65f38899006b258c0a8f013d7398203e951ee`
- `specification/capability-registry.yaml` — SHA `1f3a061ac75cedc4374f852f13fdce6ea9c7ecbb`
- `specification/contract-registry.yaml` — SHA `84b4ecbf3150e50dd5d4fe3101b5087a272beefe`
- `specification/invariant-registry.yaml` — SHA `b4a254eec855f3fede893f2de1fa123ad051268a`
- `specification/decision-registry.yaml` — SHA `b66ac89287ec1b74b71b7be1465d1c3e3fab13a4`
- `development/implementation-map.yaml` — SHA `42f5ffb2d2835d7981cb275eeda4f1b7e8cbb7f6`
- `docs/architecture/MH-06-ADR-001-health-readiness-semantic-contract.md` — governance accepted; SHA `7dda05379bd70007dc18acd62ed14fc83f0c9226`

## 4. Provenance
Historical MH-06 material is preserved as evidence. Canonical registries are authoritative for current capability/contract/invariant/decision projection. Missing historical material is not treated as loss.

## 5. Capability mapping
Primary MH-06 capability:
- CAP-032 `health_observation_and_operation_scoped_readiness` → owner `observability`.

Cross-cutting/supporting capabilities materially exercised by MH-06:
- CAP-031 unified telemetry → `observability`;
- CAP-033 diagnostics → `diagnostics`;
- CAP-034 self-recovery → `recovery_core`;
- CAP-035 offline-first → `runtime_core`;
- CAP-042 backup/restore → `recovery_core`;
- CAP-044 update/firmware lifecycle → `lifecycle_core`;
- CAP-048 resource quotas/priority/workload governance → `resource_governance`;
- CAP-050 simulation/verification/acceptance → `verification`;
- CAP-047 contextual notifications/event history → `event_core` where runtime observation/event integration is required.

These cross-domain references do not create duplicate ownership.

## 6. Requirement mapping
Canonical requirements for MH-06 are expressed through the accepted capability baseline, contract families, invariants and accepted decisions. The primary semantic requirement is CAP-032 plus CTR-020 Health and CTR-021 Readiness. Runtime orchestration requirements remain bounded by P0-03/P0-04/P0-05/P0-06 and by MH-06 security invariants.

## 7. Contract mapping
Primary:
- CTR-020 health — observation-only health semantics.
- CTR-021 readiness — operation-scoped readiness semantics.
Supporting:
- CTR-001 state-authority.
- CTR-002 consumer-boundary.
- CTR-003 identity/authentication/authorization.
- CTR-004 trust.
- CTR-006 device-command where runtime admits commands.
- CTR-007 event.
- CTR-010 scheduling.
- CTR-023 recovery.
- CTR-024 update-lifecycle.
- CTR-033 telemetry.
- CTR-035 resource-governance.
- CTR-036 verification-acceptance.

## 8. Invariant mapping
Directly applicable:
- INV-001 Function preservation.
- INV-002 Security by design.
- INV-005 Authentication does not equal Authorization.
- INV-006 Remote access does not increase authorization.
- INV-008 Local-first operation.
- INV-009 Offline-first where technically possible.
- INV-019 Deferred does not mean rejected.
- INV-020 Physical connection does not grant authorization.
- INV-021 Security is system-level and cross-cutting.
- INV-022 Health is observation-only.
- INV-023 Readiness is operation-scoped.
- INV-024 Health, Readiness, Liveness, Trust and Authorization remain distinct.
- INV-026 Historical evidence is preserved.
- INV-027 Canonical function is unique.
- INV-029 Cloud Development Cluster is distinct from Local MediaHub Cluster.

Additionally, frozen P0-04/P0-05/P0-06 controls remain mandatory even where they are not duplicated as registry invariants.

## 9. Decision mapping
- DEC-001 functional baseline is primary truth.
- DEC-005 local/offline-first direction.
- DEC-008 health observation-only; readiness operation-scoped.
- DEC-009 security system-level.
- DEC-012 deferred technical detail is not rejection.

MH-06 semantic ADR-001 is now GOVERNANCE ACCEPTED as an MH-06 architecture decision, but is not a registry replacement for the existing accepted decision baseline unless central reconciliation later elects to add a canonical DEC entry.

## 10. Architecture / boundary mapping
MH-06 projects to:
- `runtime_core`
- `observability`
- `recovery_core`
- `resource_governance`
- `scheduling_core`

Supporting boundaries: security/authorization, data/persistence boundary, event/notification, verification and lifecycle. These are cross-domain relationships, not ownership duplication.

## 11. Classification
- RETAIN: existing MH-06 runtime/lifecycle/health/readiness/security/observability/recovery boundaries consistent with canonical baseline.
- REMAP: Health/Readiness is projected as a dedicated semantic layer under CAP-032 / CTR-020 / CTR-021 while preserving P0-06 lifecycle.
- RECONCILE: historical generic health/supervision terminology versus canonical P0-06 lifecycle vocabulary.
- REPLACE: reuse of P0-06 `READY` as a readiness verdict; global `systemReady`; optimistic UNKNOWN→READY; health-as-authorization; readiness-as-capability.
- RETIRE: none on absence evidence alone.
- UNKNOWN: exact dependency graph, complete operation classes, operation-specific dependencies, resource policy, quarantine thresholds, recovery transitions, publication mechanism, runtime topology, IPC implementation, implementation location, reproducible future CI, host/iOS integration.

## 12. Contradictions
- C-01 lifecycle terminology — SEMANTICALLY RESOLVED.
- C-02 evidence continuity — OPEN; historical P0-06 acceptance does not equal current reproducible verification.
- C-03 Health/Readiness mapping — RESOLVED by accepted MH-06 ADR-001.
- C-04 P0-07 governance/API gap — OPEN; MH-06 does not create a mutation publication bypass.

## 13. Missing evidence
Current reproducible CI for exact frozen P0-06 implementation SHA remains NOT VERIFIED. Concrete runtime implementation topology and dependency graph evidence remain open.

## 14. Dangling references
No new dangling reference was created by the accepted semantic contract. Any future implementation reference to operation classes, dependency IDs or quarantine policies must be backed by governed contracts before becoming canonical.

## 15. Stale references
Generic references that equate lifecycle `READY` with system/readiness readiness are stale and must not be carried into implementation. Generic STOPPING/STOPPED/FAILED/QUARANTINED labels must not be imported into P0-06 lifecycle.

## 16. Proposed technical decisions
No new technology lock-in is proposed. Future decisions requiring evidence include dependency graph, scheduler technology, IPC transport, runtime topology, resource limits, quarantine thresholds and implementation location.

## 17. Contract impacts
CTR-020 and CTR-021 are the canonical contract families for Health/Readiness. No mutation semantics are added. P0-03/P0-04/P0-05/P0-06 remain unchanged.

## 18. Invariant impacts
No invariant is weakened. The accepted semantic contract reinforces INV-022, INV-023 and INV-024 and preserves authority/security invariants.

## 19. Dependency impacts
Readiness consumes explicit dependency classification: CRITICAL, OPTIONAL, FORBIDDEN/INCOMPATIBLE, UNKNOWN. Unknown classification is fail-closed. The complete graph is not inferred by this projection.

## 20. Verification requirements
Future implementation evidence must cover readiness states, deterministic precedence, dependency aggregation, operation-scoped evaluation, UNKNOWN fail-closed behavior, quarantine containment/exit, authorization separation, P0-04/P0-05 boundaries, security bypass resistance and reproducible CI at exact implementation SHA.

## 21. Acceptance evidence
Architecture semantic acceptance is recorded by ADR-001. Implementation acceptance remains a separate future gate. Production qualification remains blocked.

## 22. Acceptance authority
MH-06 governance acceptance applies to the MH-06 semantic contract only. Central reconciliation and explicit human acceptance remain required for Master Architecture acceptance. No MH-06 local projection may rewrite canonical registries unilaterally.

## 23. Remaining OPEN items
All UNKNOWNs above remain open. C-02 and C-04 remain open. No implementation authorization exists.

## 24. Anti-loss confirmation
**PASS — ZERO FUNCTION LOSS ESTABLISHED FOR THIS PROJECTION.** No capability is retired or removed by this MH-06 reconciliation. CAP-001…CAP-058 remain canonical baseline. UNKNOWN/evidence gaps remain explicitly preserved.

## 25. Suggested canonical registry changes
1. Consider adding a dedicated canonical decision entry referencing MH-06 ADR-001 if central reconciliation requires every accepted architecture ADR to have a DEC identifier.
2. Consider linking CAP-032 explicitly to CTR-020 and CTR-021 in a future registry relation artifact.
3. Consider linking CAP-032 to the accepted MH-06 ADR-001 in the traceability registry if/when such a registry is introduced.

For each suggestion: reason = traceability normalization; evidence = accepted MH-06 ADR-001 and current registries; affected CAP = CAP-032; affected CTR = CTR-020/CTR-021; affected INV = INV-022/INV-023/INV-024; affected DEC = DEC-008 or future dedicated DEC; dependency impact = none until graph is governed; verification impact = traceability check; acceptance authority = central reconciliation / explicit human acceptance.

**These are proposals only. MH-06 has no unilateral authority to apply them.**

## 26. Explicit authority statement
MH-06 cannot change canonical capability ownership, retire capabilities, alter accepted decisions, weaken invariants, or rewrite canonical registries. This Reverse Master Prompt is a projection artifact for central reconciliation.
