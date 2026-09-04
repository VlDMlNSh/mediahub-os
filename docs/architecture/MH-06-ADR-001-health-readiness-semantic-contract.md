# MH-06 ADR-001 — Health / Readiness Semantic Contract

Status: ACCEPTED / GOVERNANCE ACCEPTED
Decision: OPTION B — NEW SEMANTIC CONTRACT
Scope: MH-06 Core Runtime Services
Implementation authorization: NO

## 1. Problem

P0-06 provides canonical lifecycle and bounded runtime primitives, but forensic reconciliation did not establish an accepted deterministic mapping from lifecycle, dependency, generation, integrity, resource and supervisory observations to an operation-specific readiness verdict. Reusing P0-06 `READY` would collapse lifecycle and readiness semantics.

## 2. Context

P0-04 remains the sole canonical mutation authority. P0-05 remains the mandatory controlled consumer/integration boundary. P0-06 lifecycle and service contracts are accepted/frozen and are not changed by this ADR. MH-03 treats health as observational/control metadata and does not grant mutation authority.

The governing chain remains:

Input → Boundary → Authorization → State Authority → Canonical State → Observation → Evidence

Health and Readiness remain non-authoritative derived/observational semantics.

## 3. Decision

Adopt OPTION B: a dedicated MH-06 Health/Readiness semantic contract. The contract is authoritative for MH-06 architecture semantics only. It does not authorize implementation, deployment, production qualification, or changes to P0-03 through P0-06.

## 4. Health semantics

Health is observation-only. Canonical health results are:

- UNKNOWN
- HEALTHY
- DEGRADED
- FAILED
- QUARANTINED

Health cannot mutate canonical state, grant capability, grant authorization, establish trust, initiate canonical mutation, create persistence authority, or bypass supervisor/security boundaries.

## 5. Readiness semantics

Readiness is an operation-scoped derived verdict:

`Readiness(operation, observations) -> verdict`

Canonical verdicts:

- UNKNOWN
- NOT_READY
- READY
- DEGRADED
- QUARANTINED

`UNKNOWN` never becomes `READY` by default. `READY` requires every mandatory prerequisite for the specified operation. `DEGRADED` is valid only where that operation explicitly permits degraded execution. `QUARANTINED` blocks normal readiness. Readiness never grants authorization or capability and never mutates canonical state.

## 6. Bounded inputs

The evaluator may consume only bounded, defined observations relevant to the operation:

1. P0-06 lifecycle state;
2. lifecycle transition validity;
3. runtime/service health;
4. dependency health;
5. dependency classification;
6. State Authority availability;
7. generation tuple;
8. generation compatibility;
9. integrity validation/reference;
10. operation-relevant resource constraints;
11. explicit operation requirements;
12. supervision/quarantine state;
13. bounded diagnostic observations.

Unbounded external input is not readiness evidence merely by being observable.

## 7. Dependency semantics

Dependencies must have explicit classification:

### CRITICAL
Failure or UNKNOWN means the operation is NOT_READY.

### OPTIONAL
Failure may yield DEGRADED only when the operation contract explicitly permits degraded execution; otherwise NOT_READY.

### FORBIDDEN / INCOMPATIBLE
An incompatible condition yields NOT_READY or QUARANTINED according to the established supervisory condition. It never yields READY.

### UNKNOWN CLASSIFICATION
Unknown classification is fail-closed: UNKNOWN observation resolves to NOT_READY for readiness purposes unless and until classification is explicitly established. No optimistic assumption is permitted.

Critical dependency cycles require explicit ADR/evidence; no new dependency graph is implied by this ADR.

## 8. Deterministic precedence

When multiple conditions are present, the strongest applicable condition wins in this order:

1. QUARANTINED
2. invalid/incompatible generation or integrity
3. unavailable State Authority
4. lifecycle incompatible with operation
5. failed or unknown critical dependency
6. operation-specific resource constraint
7. optional dependency degradation
8. all required observations healthy

A weaker positive signal, including process liveness or P0-06 lifecycle `READY`, cannot override a stronger negative condition.

## 9. Lifecycle relation

P0-06 lifecycle is unchanged:

- PROVISIONING → NOT_READY
- INITIALIZING → NOT_READY
- SELF_TEST → NOT_READY
- READY → candidate only; remaining readiness conditions still apply
- DEGRADED → READY or DEGRADED only when operation-specific requirements permit it
- SAFE_MODE → NOT_READY for normal operations
- RECOVERY → NOT_READY for normal operations

`P0-06 LifecycleState.READY != MH-06 Readiness.READY`.

This ADR does not add STOPPING, STOPPED, FAILED, or QUARANTINED to the P0-06 lifecycle.

## 10. Operation model

Readiness is evaluated against a concrete operation contract, not a global `systemReady` flag. Initial conceptual classes are:

- normal media operation;
- diagnostic operation;
- recovery operation;
- maintenance operation.

The list is architecture-controlled and remains extensible only through governance. Operation readiness answers whether prerequisites are satisfied. Authorization answers whether the subject is permitted to perform the operation.

## 11. Failure semantics

- unavailable observation → UNKNOWN;
- critical dependency failure → NOT_READY;
- critical dependency UNKNOWN → NOT_READY;
- optional dependency failure → DEGRADED only when operation permits degradation;
- forbidden/incompatible condition → NOT_READY or QUARANTINED according to supervisory semantics;
- generation/integrity incompatibility → NOT_READY or QUARANTINED according to supervisory semantics;
- unsafe lifecycle → NOT_READY;
- process liveness alone → insufficient for READY.

## 12. Quarantine semantics

Quarantine is a supervisory/health condition, not a P0-06 lifecycle state. It does not acquire State Authority, issue capability, grant authorization, mutate canonical state, or automatically change P0-06 lifecycle.

Entry conditions are limited to explicit supervisory evidence such as a defined integrity/security incompatibility, repeated bounded failure policy, or an explicitly governed containment condition. Exit requires explicit recovery evidence sufficient to clear the triggering condition; absence of a current observation is not sufficient proof of recovery. Recovery must remain bounded and governed. While quarantined, normal-operation readiness is blocked. Any recovery operation must have its own operation contract and authorization path.

The exact runtime-specific entry thresholds, attempt counts, resource limits and recovery transitions remain UNKNOWN until separately evidenced; this does not weaken the semantic rule that quarantine blocks normal readiness.

## 13. Authority boundary

No authority changes. P0-04 remains the sole canonical mutation authority. Health, Readiness, Supervisor, Scheduler, Diagnostics, AI and plugin runtime receive no mutation exception.

## 14. P0-05 relation

No boundary changes. The normal path remains:

Readiness → Authorization → P0-05 Consumer Boundary → P0-04 State Authority

Readiness does not replace authorization and does not replace P0-05.

## 15. Security / trust relation

Health ≠ Trust.
Readiness ≠ Trust.
Readiness ≠ Authorization.
Readiness ≠ Capability.
Liveness ≠ Trust.

A live process may be unhealthy, unready, untrusted, unauthorized, or quarantined.

## 16. MH-03 reconciliation

MH-03 health semantics are reconciled by preserving health as observational/control metadata, separating readiness as operation-specific usability, and preserving the prohibition on canonical mutation and capability issuance. MH-03 generic health/supervision vocabulary is not imported into the P0-06 lifecycle. No contradiction remains at the semantic boundary.

## 17. Evidence requirements

Acceptance of this ADR does not convert implementation evidence into verification. Required future evidence includes:

- contract-level tests for every readiness state and precedence rule;
- negative tests for UNKNOWN, forged/invalid observations and unauthorized paths;
- dependency aggregation tests for critical/optional/forbidden/unknown classification;
- operation-scoped readiness tests;
- quarantine entry/exit and containment tests;
- P0-03/P0-04/P0-05/P0-06 boundary tests;
- security/bypass scans;
- reproducible CI evidence at the exact implementation SHA;
- governance acceptance of implementation separately from architecture acceptance.

Historical P0-06 acceptance at `d9b5c9db128d8ec75dae6fbd03b5d54950bdddf5` remains historical evidence. Absence of a reproducible current workflow run for that exact frozen implementation remains NOT VERIFIED.

## 18. Rejected alternatives

A. Reuse P0-06 `READY` as readiness verdict — rejected because lifecycle readiness are distinct semantics.

B. Global `systemReady` — rejected because readiness is operation-scoped.

C. Optimistic UNKNOWN → READY — rejected; fail-closed semantics required.

D. Health as authorization — rejected.

E. Readiness as capability — rejected.

F. Add FAILED/STOPPED/QUARANTINED to P0-06 lifecycle — rejected without a separate governance decision.

G. Health/Readiness as a second canonical state — rejected.

H. Implementation-first resolution — rejected.

## 19. Remaining UNKNOWNs

1. exact dependency graph;
2. complete operation classes;
3. operation-specific required dependencies;
4. exact resource policy;
5. exact runtime quarantine thresholds;
6. detailed recovery transitions;
7. publication mechanism;
8. runtime topology;
9. IPC contract;
10. implementation location;
11. reproducible CI execution for future implementation;
12. host/iOS integration.

These are implementation/topology evidence questions, not reasons to weaken the semantic contract. Each must receive owner, required evidence and decision gate before being treated as resolved.

## 20. Contradictions

- C-01 lifecycle terminology: SEMANTICALLY RESOLVED.
- C-02 evidence continuity: OPEN; historical P0-06 acceptance is not current reproducible verification.
- C-03 Health/Readiness semantic mapping: RESOLVED by this accepted ADR.
- C-04 P0-07 governance/API gap: OPEN; MH-06 must not invent a mutation publication path.

## 21. Implementation impact

This ADR creates an architecture contract only. It does not authorize code changes. A future implementation authorization, if granted, must be separately scoped to a bounded Health/Readiness evaluator and must preserve P0-03/P0-04/P0-05/P0-06 unchanged.

## 22. Governance status

GOVERNANCE ACCEPTED for the MH-06 semantic contract.

Architecture acceptance means:

ARCHITECTURE ACCEPTED
↓
IMPLEMENTATION AUTHORIZED (separate gate)
↓
IMPLEMENTED
↓
TESTED
↓
VERIFIED
↓
GOVERNANCE ACCEPTED
↓
PRODUCTION QUALIFIED

This ADR grants none of the later gates.
