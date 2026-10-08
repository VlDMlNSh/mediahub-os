# Astra executor capability matrix

Status: CANONICAL EXECUTOR-WORKFLOW POLICY
Date: 2026-10-08

## Purpose

The external ECC/Control Plane design reviewed on 2026-10-08 contains useful capability separation:
A0 coordination, A1 planning/architecture, A2 bounded implementation, A3 independent verification,
dependency-aware scheduling, leases/heartbeats/recovery, deterministic model selection, resource profiling,
stable/development separation, backups, and a larger library of specialist workflow roles.

Astra adopts the useful *capabilities*, not a second controller.

## Authority mapping

| Capability | Astra owner | Runtime form |
|---|---|---|
| Global coordination/state | A0 Astra | autonomous queue + claim/evidence state |
| Architecture/contracts | A1 | task-scoped architect profile |
| Implementation | A2 | permanent Claude lanes |
| Independent verification | A3 | separate verifier process |
| Dependency ordering | A0/A1 | task `dependencies` + readiness selection |
| Lease/heartbeat/recovery | A0 | claim TTL, heartbeat, expiry/recovery workflows |
| Model selection | A0 | bounded executor/model admission; no executor self-selection |
| Security review | A0/A3 | executable security gate + verifier |
| Resource qualification | A0/A3 | node/model evidence before promotion |
| Stable/development separation | A0 | target-SHA binding + branch isolation |
| Backup/recovery | A0 | evidence/claim persistence and recovery workflows |
| Specialist workflows | A1/A2/A3 | skills/agent profiles, never new authority |
| Evidence ledger | A0/A3 | immutable target-SHA-bound evidence |

## ECC specialist-role policy

ECC's larger role library is treated as a **capability library**, not 26 permanent
autonomous authorities.

Examples of specialist capabilities that can be invoked inside an A1/A2/A3 task:

- planning / architecture
- TDD / test guidance
- implementation
- code review
- security review
- build-error diagnosis
- end-to-end testing
- evaluation harnesses
- documentation
- delivery gating
- context/compaction discipline
- continuous learning as advisory workflow only

A specialist role never:
- creates Astra claims;
- changes G-5;
- promotes a scheme;
- changes target SHA;
- writes directly to canonical main;
- certifies its own work;
- becomes an alternative source of truth.

## Dependency-aware dispatch

A task is dispatchable only when:

1. its contract is valid;
2. its declared dependencies are complete for the same base SHA;
3. its permanent executor binding is valid;
4. no claim conflict exists;
5. G-5 capacity is available.

## Model/resource qualification

Model presence is not model qualification.

Before a model/executor scheme can become PASS, evidence should include:

- exact executor identity;
- exact model identifier/variant;
- runtime backend;
- target SHA;
- resource profile where relevant;
- timeout/result behavior;
- fresh execution;
- independent A3 verification.

A larger model installed on a node is not automatically selected.

## Stability boundary

Astra does not create a second Stable/Development control plane.
The canonical distinction is:

- repository main/target SHA = canonical source;
- task branch/worktree = isolated execution state;
- claim/evidence store = runtime state;
- qualification registry = promotion state.

Any attempt to infer PASS from historical state is BLOCKED.

## Reconciliation rule

If architecture documentation, task contracts, runtime claims, workflow configuration,
or evidence disagree about executor identity, G-5, target SHA, or verifier independence,
the result is **RECONCILIATION_REQUIRED**, not PASS.
