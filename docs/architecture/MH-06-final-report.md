# MH-06 — Final Architecture Pass Report

Status: HEALTH / READINESS SEMANTIC CONTRACT ACCEPTED; MH-06 OVERALL NOT FROZEN
Date: 2026-09-04

## A. Governance decision

OPTION B — NEW SEMANTIC CONTRACT is GOVERNANCE ACCEPTED for Health/Readiness by `MH-06-ADR-001-health-readiness-semantic-contract.md`, commit `1d6e9cd6ad320fff752c6ec6e1aa8a94525ef5be`.

## B. Canonical state and frozen baselines

P0-04 remains the sole canonical mutation authority. P0-05 remains the mandatory integration/authorization boundary. P0-06 lifecycle/service contracts remain accepted/frozen and unchanged.

## C. Semantic contract

Health is observation-only with results UNKNOWN, HEALTHY, DEGRADED, FAILED, QUARANTINED. Readiness is an operation-scoped derived verdict with results UNKNOWN, NOT_READY, READY, DEGRADED, QUARANTINED. `P0-06 READY != Readiness READY`.

Readiness is evaluated as `Readiness(operation, observations) -> verdict` using bounded lifecycle, service/dependency health and classification, authority availability, generation/integrity, operation requirements, resource and supervisory observations.

## D. Dependency and precedence

CRITICAL failure/UNKNOWN => NOT_READY. OPTIONAL failure => DEGRADED only where the operation permits it; otherwise NOT_READY. FORBIDDEN/INCOMPATIBLE => NOT_READY or QUARANTINED; never READY. UNKNOWN classification => fail-closed NOT_READY.

Precedence: QUARANTINED → generation/integrity incompatibility → authority unavailable → lifecycle incompatible → critical dependency failure/unknown → operation resource constraint → optional degradation → all required observations healthy.

## E. Lifecycle

P0-06 remains exactly PROVISIONING, INITIALIZING, SELF_TEST, READY, DEGRADED, SAFE_MODE, RECOVERY. STOPPING, STOPPED, FAILED and QUARANTINED are not added by this decision.

## F. Quarantine

Quarantine is supervisory/health state, not P0-06 lifecycle. It blocks normal readiness and has no authority, capability or authorization semantics. Detailed runtime thresholds and recovery transitions remain unresolved evidence questions.

## G. Cross-MH reconciliation

MH-03 health semantics are reconciled: health remains observational/control metadata; readiness is separated as operation-specific usability; neither mutates canonical state nor issues capability. No semantic contradiction remains between MH-03 and accepted MH-06 Health/Readiness semantics.

## H. Security / authority

Health ≠ Trust. Readiness ≠ Trust. Readiness ≠ Authorization. Readiness ≠ Capability. Liveness ≠ Trust. The normal control path remains Readiness → Authorization → P0-05 → P0-04.

## I. Evidence

Historical P0-06 acceptance at `d9b5c9db128d8ec75dae6fbd03b5d54950bdddf5` remains historical. No reproducible current workflow run for that exact frozen implementation has been established; current execution remains NOT VERIFIED. This acceptance does not close that evidence gap.

## J. Open contradictions / unknowns

C-01 lifecycle terminology: RESOLVED.
C-02 evidence continuity: OPEN.
C-03 Health/Readiness semantic mapping: RESOLVED by accepted ADR.
C-04 P0-07 governance/API gap: OPEN.
C-05 concrete dependency/runtime policy: OPEN / UNKNOWN.

Remaining UNKNOWNs include exact dependency graph, complete operation classes, operation-specific dependencies, resource policy, quarantine thresholds, recovery transitions, publication mechanism, runtime topology, IPC, implementation location, future reproducible CI and host/iOS integration.

## K. Acceptance meaning

The Health/Readiness semantic architecture is GOVERNANCE ACCEPTED. MH-6 overall is not FROZEN and is not PRODUCTION READY. Architecture acceptance does not imply implementation complete, tests passed, CI verified, deployment authorized or production qualified.

## L. Implementation boundary

IMPLEMENTATION AUTHORIZATION: NO.

Development Chat must remain STOPPED for Health/Readiness implementation until a separate, explicit scoped implementation authorization is issued. No code change is authorized by this report or ADR.
