# Astra Gold Autonomous Distributed Verification Design

Date: 2026-10-05
Status: Approved conversational design; implementation plan pending review

## Objective

Restore a provable, fail-closed transition from canonical qualification through distributed verification and autonomous queue execution, while preserving authority boundaries and preventing stale/replayed evidence from being accepted.

## Constraints

- Canonical execution node for Astra autonomous qualification: `mh-dev-01`.
- Runner identity must be `mediahub-runner` on `mh-dev-01`.
- No manual queue execution.
- No evidence may be synthesized or accepted from an older command.
- Every accepted result must bind `command_id`, `target_sha`, `node_id`, phase, status, and return code.
- GitHub Actions success is not itself qualification evidence.
- Existing authority/HMAC boundary remains mandatory.
- No duplicate Astra worker launch is permitted by GOLD soak admission.

## Observed failure boundary

The autonomous supervisor already materializes a fresh command, signs it, fetches the canonical node result branch, invokes `astra_github_agent.py`, and checks for `phase=autonomous_queue`, `status=PASS`, `returncode=0`, queue PASS, and VERIFIED queue results. The remaining failure boundary identified by the preceding audit was the distributed-verification transition: the controller could complete earlier qualification but could not prove the dedicated distributed-verification producer path.

The current supervisor also explicitly pins runtime identity to `mh-dev-01` / `mediahub-runner` and uses a fresh run-derived command ID. This behavior is retained.

## Design

### 1. Canonical admission

The supervisor resolves the canonical node from runtime identity and fails closed on hostname/user mismatch. It materializes a fresh command ID derived from node, run ID, and attempt, sets `target_sha=GITHUB_SHA`, signs the command, and only then invokes the controller.

### 2. Distributed verification producer

Introduce/repair a dedicated producer path for the distributed-verification phase. The producer must emit independently attributable evidence containing at minimum:

- `command_id`
- `node_id`
- `target_sha`
- producer identity
- phase
- status
- return code
- execution timestamp
- evidence/source SHA where applicable

The producer must reject missing or mismatched authority context and must not convert a BLOCKED state into success.

### 3. Freshness gate

The canonical result reader must reject:

- old `command_id`
- mismatched `target_sha`
- mismatched `node_id`
- missing phase
- non-zero return code
- queue status other than PASS
- any queue item not VERIFIED
- evidence whose producer identity does not match the current command

The result branch is therefore an evidence transport, not an authority source.

### 4. Autonomous queue gate

Only after distributed verification passes may the controller enter `autonomous_queue`. For each selected task, the controller must preserve the complete lifecycle:

`READY -> CLAIMED -> builder execution -> tests -> A2 -> A3 -> commit -> push -> VERIFIED`.

The controller must record the worktree and resulting commit SHA. A GitHub job's successful exit is insufficient without this evidence.

### 5. MH25-QUEUE-002

The verification path must explicitly expose whether MH25-QUEUE-002 was READY, CLAIMED, actually executed by the intended builder, tested, independently A3-verified, committed, pushed, and marked VERIFIED. If any link is absent, the overall result is BLOCKED rather than PASS.

### 6. GOLD boundary

The 24-hour GOLD soak remains an explicit admission action. Its existing preflight must continue to bind to the canonical worker and must not launch a duplicate worker. The soak starts only after the autonomous queue proof exists. The current GOLD workflow performs repeated runtime/test checks for 86,400 seconds and uploads sanitized evidence.

## Invariants

1. One mission = one fresh `command_id`.
2. One mission = one immutable `target_sha`.
3. Result freshness requires exact command/node/SHA agreement.
4. Authority is established by the signed command, not by result files.
5. Queue PASS requires real queue evidence and VERIFIED task state.
6. A2 and A3 must be independently evidenced.
7. Commit/push evidence must identify the actual resulting commit.
8. Any missing evidence fails closed.
9. No manual queue invocation is part of the autonomous path.
10. GOLD 24h soak is not shortened or inferred from a GitHub workflow success.

## Verification sequence

1. Run static/unit/regression checks for changed components.
2. Verify canonical runner admission.
3. Issue one fresh signed autonomous command through the normal GitHub supervisor.
4. Verify the distributed-verification producer evidence.
5. Verify fresh canonical result binding.
6. Verify autonomous queue lifecycle for MH25-QUEUE-002.
7. Verify A2, A3, commit and push evidence.
8. Verify final `phase=autonomous_queue`, `status=PASS`, `returncode=0`, and `queue.status=PASS`.
9. Only then admit GOLD 24h soak.

## Time model

The first proven autonomous queue PASS should be treated as a bounded qualification run, not as the GOLD product-completion time. After the queue PASS, the explicit GOLD runtime qualification adds a mandatory 24-hour soak. Therefore the critical-path lower bound from a clean queue PASS to GOLD-qualified state is approximately 24 hours, plus preflight, evidence finalization, and any remediation/verification time.

## Out of scope

- Replacing the existing authority model.
- Manual execution of queue tasks.
- Declaring PASS from GitHub job success alone.
- Removing the 24-hour GOLD soak requirement.
- Unrelated refactoring or optimization that does not affect the failing qualification path.
