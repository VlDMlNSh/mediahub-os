# ASTRA GOLD — TEST LAUNCH QUALIFICATION RUNBOOK

Status: OPERATIONAL CHECKLIST / NOT A PROMOTION RECORD
Baseline: 2.0
Date: 2026-10-02

## 1. Repository and reconciliation

- [ ] Confirm exact engineering HEAD and clean worktree on every execution node.
- [ ] Run architecture drift gate.
- [ ] Confirm canonical reference architecture, qualification contract and unified system model agree.
- [ ] Reject any architecture drift or ambiguity.

Evidence required:
- source SHA;
- drift-gate PASS;
- clean-worktree evidence.

## 2. Runtime identity / G0

For every admitted executor/transport/node:
- [ ] node identity;
- [ ] executor identity and exact version;
- [ ] provider/model identity;
- [ ] repository identity;
- [ ] exact source SHA;
- [ ] workspace identity;
- [ ] clean worktree.

No historical evidence substitutes for fresh identity evidence.

## 3. Boundary / G1

Verify explicitly:
- [ ] Human final authority;
- [ ] A0 sole MediaHub State Authority;
- [ ] A1 architecture boundary;
- [ ] A2 bounded implementation;
- [ ] A3 independent verification;
- [ ] executor-only semantics;
- [ ] GitHub/FCC/OmniRoute transport-only semantics;
- [ ] no provider becomes MediaHub state authority;
- [ ] no credential creation by executor/tooling;
- [ ] no authority escalation.

## 4. Control plane / G2

Fresh runtime proof for:
- [ ] command creation;
- [ ] unique command_id;
- [ ] claim;
- [ ] lease;
- [ ] queue;
- [ ] duplicate suppression;
- [ ] result publication;
- [ ] heartbeat;
- [ ] stale-claim handling;
- [ ] duplicate-controller rejection.

## 5. Execution path / G3

For every mandatory path:
- [ ] runtime identity;
- [ ] bounded timeout;
- [ ] non-zero exit handling;
- [ ] malformed-result rejection;
- [ ] success marker;
- [ ] output/schema validation;
- [ ] workspace isolation;
- [ ] evidence digest.

## 6. Mandatory 115-round qualification / G4

Exactly five paths:

1. CODEX_FCC — 23 fresh PASS rounds.
2. CLAUDE_FCC — 23 fresh PASS rounds.
3. CODEX_OMNIROUTE — 23 fresh PASS rounds.
4. CLAUDE_OMNIROUTE — 23 fresh PASS rounds.
5. CLAUDE_CODE_DIRECT — 23 fresh PASS rounds.

Required total: 115 fresh successful rounds.

Evidence record must contain:
`command_id, node_id, component_id, executor_id, provider_or_model_id, transport_id, source_sha, round, timestamp, exit_status, timeout, workspace, verification_status, evidence_digest`.

Any missing, duplicate, stale or contradictory record blocks promotion.

## 7. Concurrency / G5

Fresh proof:
- [ ] maximum two autonomous claims;
- [ ] disjoint claims execute concurrently;
- [ ] shared surfaces serialize;
- [ ] duplicate controller is rejected;
- [ ] no duplicate result corruption;
- [ ] leases/fencing are enforced.

## 8. Recovery / G6

Fresh proof for each:
- [ ] executor timeout;
- [ ] executor failure;
- [ ] transport interruption;
- [ ] stale claim;
- [ ] worker restart;
- [ ] duplicate controller;
- [ ] replay;
- [ ] idempotent replay;
- [ ] result publication recovery.

Every failure must return to a deterministic safe state.

## 9. Integrated A3 / G7

Independent verifier must inspect:
- [ ] targeted runtime tests;
- [ ] regression suite;
- [ ] contract tests;
- [ ] architecture drift;
- [ ] security boundary;
- [ ] concurrency/fencing;
- [ ] failure/recovery;
- [ ] exact-SHA evidence;
- [ ] clean worktree.

A3 evidence must be independent from the execution claim.

## 10. PRE-SOAK / G8

Before any soak:
- [ ] G0-G7 PASS;
- [ ] every mandatory executor path PASS;
- [ ] recovery matrix PASS;
- [ ] A3 PASS;
- [ ] no unresolved contradiction;
- [ ] clean worktree;
- [ ] fresh evidence bundle;
- [ ] development queue can execute bounded real work;
- [ ] rollback/recovery path verified.

This gate is the final stop before 24h SOAK.

## 11. 24h SOAK / G9 — HUMAN DECISION REQUIRED

Do not start autonomously.

Required during soak:
- [ ] continuous heartbeat;
- [ ] no unexplained restart;
- [ ] no duplicate-claim corruption;
- [ ] no unresolved execution failure;
- [ ] evidence integrity;
- [ ] no authority-boundary violation.

Historical 17h08m run does not satisfy G9.

## 12. LAUNCH_READY / G10 — HUMAN DECISION REQUIRED

Requires:
- [ ] G0-G9 PASS;
- [ ] no unresolved blocker;
- [ ] fresh final evidence;
- [ ] exact launch candidate SHA;
- [ ] launch package reconciled.

## 13. HUMAN LAUNCH / G11 — HUMAN DECISION REQUIRED

ASTRA GOLD may not self-promote.

Required human action:
- explicit launch authorization;
- explicit acceptance of final evidence;
- explicit release/launch decision.

## 14. Current execution status — 2026-10-02

IMPLEMENTED:
- reference architecture;
- qualification contract;
- reconciliation v2;
- executable architecture drift gate;
- qualification blueprint;
- mandatory five-path/115-round workflow definition;
- MH-25 evidence identity hardening.

NOT PROVEN:
- fresh G0-G3 runtime evidence;
- 115 PASS rounds;
- G5 concurrency;
- G6 recovery;
- full A3;
- PRE-SOAK;
- real development queue execution;
- G9 soak.

BLOCKED:
- self-hosted GitHub runner service is currently failed after OOM;
- SentinelX service policy does not permit managing that runner service;
- current connector does not expose a dispatch operation for starting the push-triggered MH-25 workflow.

STOP:
- no 24h soak;
- no GOLD promotion;
- no SentinelX policy expansion;
- no credential/scope expansion;
- no force-push/reset/delete/policy changes.

## 15. Execution order

`RECONCILE → RUNNER RECOVERY → PREFLIGHT → G0/G1 → G2/G3 → 115 ROUNDS → G5 → G6 → A3 → PRE-SOAK → [HUMAN STOP] → SOAK_24H → LAUNCH_READY → [HUMAN LAUNCH]`


## 16. Runner recovery evidence — 2026-10-02

- Runner unit is owned by `mediahub-runner`.
- `ExecStart=/home/mediahub-runner/actions-runner/runsvc.sh`.
- `Restart=no`; therefore an OOM/failure does not automatically restart the runner.
- Current operator identity observed through Desktop Commander: `mediahub`, UID 1000, member of sudo group.
- Non-interactive privileged start is not available through the current Desktop Commander command policy; `systemctl start` returns `Interactive authentication required`.
- SentinelX separately rejects the runner service with `service_not_allowed`.
- Do not modify sudoers, polkit, SentinelX policy, systemd unit ownership, or runner registration as part of autonomous qualification.
- Required recovery action is a normal administrator-authorized start of the existing service, followed by runner/GitHub handshake verification.
- Re-registration is not indicated by current evidence.
