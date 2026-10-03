# ASTRA GOLD — Geometric Critical-Path Blueprint

Status: EXECUTION BLUEPRINT / NO ARCHITECTURE AUTHORIZATION
Date: 2026-10-03

## Objective

Minimize elapsed time to the first **permitted test start** without weakening any qualification, security, evidence, or human-authorization gate.

The optimization target is the critical path to a real three-node Mesh admission and subsequent D4–D11 qualification. Optional candidate installation must not delay this path.

## Truth boundary

Current canonical main: `288713b9749727e7323166d9b822b1d42a885fb1`.

Fresh node attestations exist for:
- `mh-dev-01`
- `mh-dev-02`
- `Voktor-Mini-Astra`

Current facts:
- all three nodes are reachable at the level of fresh user-supplied runtime attestation;
- Mesh daemon is intentionally not enabled;
- `mh-dev-01` and `Voktor-Mini-Astra` do not yet have canonical node roles proven;
- authenticated heartbeat is not implemented;
- node-profile and inventory adapter work exists in open PRs #181 and #183, not on main;
- D4 local regression coverage exists, but distributed D4 admission is not proven;
- G4/G5/G6/G7/G8/G9/G10 remain fresh-evidence gates.

## Geometric reduction rule

Each cycle MUST attack the earliest unresolved critical-path gate and, where safe, prepare the next gate in parallel.

A cycle is considered successful only when it produces at least one of:
1. a verified repository state transition;
2. a verified CI result;
3. a verified node-side fact;
4. a closed dependency between two already-proven facts;
5. a ready-to-run bounded task that no longer requires architectural interpretation.

No cycle may manufacture PASS from absence of evidence.

## Critical path

```
ARCHITECTURE DECISIONS
  #178 authority semantics
  #175 authenticated heartbeat
          |
          v
NODE PROFILE + INVENTORY
  PR #181 + PR #183
          |
          v
MESH TRANSPORT / REGISTRY
          |
          v
3-NODE ADMISSION
          |
          v
D4 DISTRIBUTED
          |
          v
D5 -> D6 -> D7
          |
          v
G4 / G5 / G6
          |
          v
G7 A3 -> G8 PRE-SOAK -> G9 24H -> G10
          |
          v
G11 HUMAN-ONLY LAUNCH
```

## Parallel preparation lanes

### Lane A — Mesh contract

Blocked on architecture decisions #175/#178. Do not guess.

### Lane B — node identity/profile

Prepare node-local profile inputs from fresh attestations. Installation is not admission.

### Lane C — executor fabric

Do not reinstall already-present Codex/Claude/FCC/OmniRoute. Prepare deterministic qualification matrix for the five mandatory paths.

### Lane D — evidence/recovery

Prepare manifests, recovery scenario mapping and exact-SHA evidence requirements without starting GOLD/24h soak.

### Lane E — candidate inventory

Keep OpenFlux/ECC/FreeLLMAPI and other candidates inventory-visible, but do not allow them to delay the mandatory execution path.

## Hard blockers

1. #178 — architecture decision: whether qualified `authority=NONE` may enter executor admission.
2. #175 — architecture decision: authenticated heartbeat envelope, replay semantics and persistence boundary.
3. PR #181 — inventory-to-capability adapter is not on main.
4. PR #183 — canonical node profile contract is not on main.
5. Canonical runtime producer from node inventory to signed Mesh heartbeat is absent.
6. Three-node runtime admission is not proven.
7. Distributed D4–D8 evidence is absent.
8. G9 24h soak has not started and must not start before pre-soak gates.

## Non-critical candidates

These are NOT prerequisites for the first permitted distributed test unless a later gate explicitly selects them:

OpenOPC, OpenFlux, SoL-Pi, Colibri, WebTool-DeepSeek, DeepSeek Harness, Stagewise, Delx Memory Bun, Cursor, unlazy, naabu, IPFS, additional cloud gateways, additional local model checkpoints.

## Safety invariants

- no credentials in Git or evidence;
- no force-push;
- no reset/rebase/history rewrite;
- no daemon activation while runtime is placeholder;
- no implicit admission from installation;
- no implicit qualification from registration;
- no self-qualification;
- no A2 self-verification;
- no GOLD/24h soak before pre-soak;
- G11 remains human-only.

## Next-cycle algorithm

For every subsequent cycle:

1. Read current main and open PR/issue state.
2. Reconcile against the critical path.
3. Select the earliest unblocked bounded task.
4. Execute all safe independent read-only checks around that task.
5. If a repository-only change is safe and unambiguous, make exactly one commit.
6. Verify the commit with available CI/evidence.
7. Recalculate critical path.
8. Emit only facts, blockers and the next bounded task.

## Time-to-test metric

Do not estimate wall-clock completion from model intuition.

Report instead:

- **critical-path gates remaining**;
- **independent blockers remaining**;
- **gates that can be prepared in parallel**;
- **gates requiring human architecture decisions**;
- **first permitted test boundary**.

A cycle that removes one independent blocker while preparing two downstream gates is considered a higher-leverage cycle than one that merely installs another optional component.

## Current first permitted test boundary

The first permitted test is NOT Astra GOLD launch.

It is a bounded distributed Mesh test after:
- authenticated heartbeat contract exists;
- node profiles are valid;
- three nodes are registered;
- admission rules are explicit;
- executor identities are inventory-backed;
- evidence collection is enabled;
- fail-closed behavior is verified.

D4–D11 qualification follows only from fresh evidence.
