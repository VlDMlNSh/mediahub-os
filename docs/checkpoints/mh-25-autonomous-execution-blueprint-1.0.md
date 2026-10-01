# MH-25 — Autonomous Agent Development Execution Blueprint 1.0

Status: CANONICAL EXECUTION PLAN — IMPLEMENTATION/QUALIFICATION GATED
Date: 2026-10-01
Scope: MediaHub OS / MediaHub iOS MH-25 Agent Fabric

## Objective
Bring the agent architecture to an executable reference state and run the first real 24-hour autonomous development queue test without transferring MediaHub domain authority to agents.

## Canonical topology
A0 Astra — coordination authority.
A1 Architect — architecture/contracts/reconciliation.
A2 Builder — bounded implementation.
A3 Verifier — independent verification.
Dynamic workers are task-scoped instances of A1/A2/A3. Persistent profile does not mean persistent daemon.

## Mandatory execution chain
TASK → CLAIM → WORKER → VERIFY → COMMIT → EVIDENCE → MANIFEST

## Gate order
G0 worker identity
G1 task/claim state contract
G2 worker execution E2E
G3 scheduler E2E
G4 multi-node fencing
G5 recovery/backup/restore
G6 fresh dependency/provider qualification where applicable
G7 3-node qualification
G8 one canonical 24h GOLD soak
G9 independent final verification

No autonomous development promotion before G0-G9 PASS.

## First-day autonomous queue
1. Reconcile main HEAD, working tree and immutable anchors.
2. Verify A0 identity and task-state persistence.
3. Execute ClaimStore collision, parent/child overlap, heartbeat and lease-expiry simulations.
4. Execute Astra task→claim→worker→verification→commit→evidence E2E.
5. Execute scheduler retry/idempotency/duplicate-prevention E2E.
6. Execute fencing on two or more nodes; prove only one writer per exclusive claim.
7. Execute recovery: interrupted task, claim expiry, worker restart, state restore and replay.
8. Execute 3-node qualification when three independently usable execution nodes are available.
9. Start one canonical 24h GOLD run on the exact qualified HEAD.
10. Run independent read-only verification against the final GOLD SHA and evidence bundle.
11. Only after G0-G9 PASS, enable autonomous queue execution in bounded waves of 2–3 builders plus one verifier, adapting downward under contention.

## Concurrency
Default: 2–3 substantive workers + 1 verifier. One writer per shared surface. Shared contracts, generated files, release metadata, State Authority and production controls are serialized.

## Hard stops
Authority ambiguity; missing lease/claim evidence; incompatible overlap; unqualified dependency; security/privacy failure; recovery failure; nondeterministic verification; missing exact SHA; production/user-data boundary violation.

## GOLD validity
A GOLD result is valid only when:
- preflight uses the exact qualified agent source anchor;
- canonical worker identity is verified;
- repository state is clean;
- regression and Agent Fabric tests pass;
- the same qualified HEAD is soaked for 24h;
- final evidence is retained;
- independent verification passes.

Historical or older-SHA GOLD runs do not qualify newer Agent Fabric changes.

## Current execution anchor
Current main HEAD at queue activation: 02b4c64464be588d6a98eb729182379dfbca31f2
Agent source blob SHA: 769306d93be818161af7ce49ba9b202eed6c5b24

## First real queue test activation
The first 24h queue test is implemented by `.github/workflows/mh25-first-24h-autonomous-queue.yml` and is intentionally separate from GOLD promotion. It runs only on the workflow-file activation push or explicit workflow dispatch, uses the canonical `mh-dev-01` runner, and executes bounded queue waves. Queue workers create task branches and evidence; they do not merge to `main`.
