# ASTRA GOLD — Geometric Critical-Path Blueprint

Status: EXECUTION BLUEPRINT / NO ARCHITECTURE AUTHORIZATION
Date: 2026-10-04
Canonical main at reconciliation: `f0c8fde6b9279cd286efdcc76184899ab07c3972`

## Objective

Minimize elapsed time to the first **permitted distributed test start** without weakening any qualification, security, evidence, or human-authorization gate.

The optimization target is the earliest real three-node Mesh admission and the bounded test immediately preceding full D4–D11 qualification. Optional component installation must not delay this path.

## Truth boundary

Current repository facts:

- current canonical `main` is `f0c8fde6b9279cd286efdcc76184899ab07c3972`;
- Mesh registry, node-profile and capability-inventory contracts are present on current main;
- registry/admission contract tests were consolidated by PR #185;
- safe Astra node-result publication was merged by PR #186;
- auxiliary FreeLLMAPI/OpenFlux/ECC inventory contracts were merged by PR #188;
- stale duplicate PR paths #176 and #177 were closed as superseded by #185;
- #178 is closed, but its historical discussion does not constitute a new production admission rule;
- the Mesh daemon remains intentionally disabled;
- heartbeat authentication is not implemented as a production runtime contract;
- current command consumer requires HMAC authentication, while the current supervisor does not act as an authoritative command signer;
- the current command issuer decision gate #187 is OPEN;
- the Mesh heartbeat architecture decision #175 is OPEN;
- distributed three-node admission is not proven;
- G4/G5/G6/G7/G8/G9/G10 remain fresh-evidence gates.

Historical evidence is not promoted to fresh qualification evidence.

## Geometric reduction rule

Each cycle MUST attack the earliest unresolved critical-path gate and, where safe, prepare downstream gates in parallel.

A cycle is successful only when it produces at least one of:

1. a verified repository state transition;
2. a verified CI result;
3. a verified node-side fact;
4. a closed dependency between already-proven facts;
5. a ready-to-run bounded task requiring no new architecture interpretation.

No cycle may manufacture PASS from absence of evidence.

## Critical path

```
ARCHITECTURE AUTHORITY
  #187 command issuer decision
  #175 authenticated heartbeat contract
          |
          v
MESH AUTHENTICATED CONTROL TRANSPORT
          |
          v
3-NODE REGISTRATION + HEALTH
          |
          v
3-NODE ADMISSION
          |
          v
BOUNDED DISTRIBUTED TEST
          |
          v
D4 -> D5 -> D6 -> D7 -> D8
          |
          v
G4 / G5 / G6
          |
          v
G7 A3 -> G8 PRE-SOAK -> G9 24H -> G10
          |
          v
G11 HUMAN-ONLY
```

## Current blockers

### B1 — #187: authoritative command issuer

Status: **OPEN / BLOCKED**

The existing consumer-side HMAC primitive is usable as the implementation basis, but an explicit architecture acceptance is required before production issuer implementation.

Required decision:

- reuse existing Astra GitHub Transport HMAC-SHA256;
- one authoritative control-plane publisher;
- signing secret only in secure runtime;
- canonical signed envelope;
- node binding;
- timestamp validation;
- replay/idempotency semantics;
- no new authority database;
- no force-push.

### B2 — #175: authenticated Mesh heartbeat

Status: **OPEN / BLOCKED**

Required before Mesh runtime activation:

- authenticated envelope;
- exact canonical serialization;
- node binding;
- timestamp/freshness semantics;
- replay and persisted monotonic sequence handling;
- publication classification;
- registry transition rules;
- negative security tests.

Authentication, freshness and non-replay are separate predicates.

### B3 — distributed runtime admission

Status: **NOT PROVEN**

Contracts and local tests exist, but current evidence does not prove authenticated three-node runtime admission.

### B4 — distributed qualification evidence

Status: **NOT STARTED**

No G4/G5/G6/G7 launch is authorized merely by repository readiness.

## Parallel preparation lanes

### Lane A — transport

Blocked on #175/#187. Prepare only testable, architecture-neutral pieces until acceptance exists.

### Lane B — node contracts

Keep current node-profile, capability inventory, registry and admission contracts synchronized with main. Do not equate installation with admission.

### Lane C — executor fabric

Maintain the five mandatory paths:

- CODEX_FCC
- CLAUDE_FCC
- CODEX_OMNIROUTE
- CLAUDE_OMNIROUTE
- CLAUDE_CODE_DIRECT

Each requires fresh exact-SHA evidence. Gateway execution does not become native-provider qualification by implication.

### Lane D — evidence/recovery

Prepare exact evidence schemas and recovery mapping for:

- timeout;
- executor failure;
- transport interruption;
- stale claim;
- worker restart;
- duplicate controller;
- replay/idempotency;
- result-publication recovery.

Do not launch qualification while control-plane authentication remains unresolved.

### Lane E — auxiliary inventory

FreeLLMAPI/OpenFlux/ECC remain inventory-visible with authority `NONE`. They do not receive provider, execution or qualification authority from discovery.

## Non-critical work

Do not spend critical-path time on optional model downloads, additional gateways, optional P2P adapters or unrelated component installation unless a later gate explicitly requires them.

## Safety invariants

- no credentials in Git or evidence;
- no force-push;
- no reset/rebase/history rewrite;
- no Mesh daemon activation while the runtime remains placeholder;
- no admission by installation;
- no qualification by registration;
- no self-qualification;
- no A2 self-verification;
- no historical evidence counted as fresh evidence;
- no G4/G5/G6 launch before their prerequisites;
- no 24h soak before pre-soak;
- G11 remains human-only.

## Per-request execution algorithm

For every subsequent development request:

1. Read current `main`, open issues and open PRs.
2. Reconcile against this critical path.
3. Identify the earliest unresolved independent blocker.
4. Execute all safe read-only verification around that blocker.
5. Execute safe repository-only work that does not require an architectural decision.
6. One production fix = one production commit.
7. Test-only changes may be consolidated when they remain independently reviewable.
8. Verify with available CI/evidence.
9. Recalculate blockers and downstream preparation.
10. Never report an unverified state as PASS.

## Geometric time-to-test metric

Do not invent wall-clock estimates.

Measure progress as:

- independent critical-path blockers remaining;
- architecture decisions remaining;
- downstream gates prepared;
- fresh evidence prerequisites satisfied;
- bounded test boundary remaining.

The highest-leverage cycle is one that removes one independent blocker while making multiple downstream gates immediately executable.

## First permitted test boundary

The first permitted test is **not Astra GOLD launch**.

It is a bounded distributed Mesh test after all of the following are proven with fresh evidence:

- #175 heartbeat contract accepted and implemented;
- #187 command issuer contract accepted and implemented;
- authenticated control transport works end-to-end;
- all three nodes have valid profiles;
- all three nodes have authenticated fresh heartbeat;
- registry/admission transitions are verified;
- executor identities are inventory-backed;
- evidence collection is operational;
- fail-closed negative paths are verified.

Only then may the qualification chain proceed toward D4–D11 and eventually G10. G11 remains human-only.

## Fresh runtime reconciliation (2026-10-04)

Fresh three-node resource/runtime attestations have been recorded in the Mesh decision trail. They establish current resource facts only; they do not establish authenticated heartbeat, ACTIVE admission, executor authority, or Astra Gold qualification. Two node roles remain intentionally unassigned rather than inferred.

This creates a useful downstream-ready state: node inventory/resource preparation can proceed independently, while authenticated control-plane admission remains blocked on #175/#187 and explicit admission semantics.

## Current session target

The current highest-leverage target is **not another installation wave**.

It is to reduce the two architecture blockers (#175 and #187) to explicit, reviewable decision packets while simultaneously keeping the current mainline contracts and test evidence ready for immediate implementation after acceptance.

No production authentication or Mesh runtime change is authorized before those decisions.
