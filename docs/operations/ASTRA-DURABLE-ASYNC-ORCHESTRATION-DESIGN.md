# Astra durable asynchronous orchestration design

## Decision

Use a durable asynchronous dispatcher/poller to remove the self-contention cycle between the supervisor and the `mh-dev-01` worker. Do not add another runner or change runner registration without explicit infrastructure approval. Do not treat a dispatched workflow, successful admission, uploaded artifact, or terminal worker success as qualification completion.

This design is a specification for a staged implementation; it is not evidence that the current synchronous queue has already been converted.

## Current implementation status (local prototype, not deployed)

The working tree now contains a staged supervisor workflow prototype that moves queue dispatch/polling into a GitHub-hosted runner job, then runs a fresh post-queue distributed attestation wave before the self-hosted controller finalizes the signed command. This separates the wait loop from the only `mediahub-control` runner and directly addresses the observed self-contention cycle. A dedicated `validate_autonomous_queue_summary.py` emits a sanitized summary artifact and fails closed on target/command mismatch, worker failure/cancellation, missing independent-verifier PASS, bad evidence digest shape, or branch/remote-head mismatch. The queue additionally recomputes the worker artifact digest and checks that the actual GitHub workflow conclusion is `success` before accepting evidence.

This is still a **local, uncommitted prototype**. It has not been pushed or exercised by a fresh GitHub run. The queue internals still use synchronous dispatch-and-poll within the separate queue job, and the claim ledger is in that job's workspace rather than an external durable store. Process interruption/restart replay and durable dispatch-intent recovery therefore remain incomplete. These changes alone do not qualify Astra Gold.

## Durable record

Each task attempt must persist one atomic record keyed by `(command_id, task_id, node_id, executor, target_sha)` with at least:

- schema/version and monotonically increasing attempt identifier;
- command/task/node/executor/verifier identity and immutable full `target_sha`;
- current state, state version, created/updated timestamps;
- dispatch-intent timestamp and idempotency key;
- worker workflow ID, run ID, attempt, exact display title, and last observed status/conclusion;
- lease/heartbeat timestamps and poll retry count;
- result artifact name/ID, digest, schema version, and provenance binding;
- independent verifier verdict and evidence digest;
- branch/head SHA and remote-head verification when the task changes source;
- sanitized error code and bounded diagnostic details.

Never persist credentials, tokens, secret-bearing environment values, or raw command output without sanitization. Use atomic replace plus file and parent-directory `fsync`; mutations must be serialized and use compare-and-swap against state version and identity.

## State transition table

| Current state | Event and required evidence | Next state | Recovery rule |
|---|---|---|---|
| READY | Immutable intent validated; current checkout equals target SHA; task dependencies and claim boundary pass | CLAIMED | If persistence fails, do not dispatch |
| CLAIMED | Durable dispatch intent written before external side effect | DISPATCHED | After crash, reconcile by idempotency key/exact title and creation-time fence; never blindly redispatch |
| DISPATCHED | Exactly one new run bound to command/task/node/executor/target SHA is identified and run ID is persisted by CAS | RUNNING | Zero matches -> remain unresolved/BLOCKED; multiple matches -> QUARANTINED |
| RUNNING | Poll observes same run ID and exact identity; lease heartbeat is durable | RUNNING | API uncertainty preserves claim and state; timeout is not proof of termination |
| RUNNING | GitHub reports terminal status and artifact is retrieved with exact run provenance | RESULT_RECEIVED | Missing/invalid artifact -> BLOCKED; retain evidence and claim until terminality is confirmed |
| RESULT_RECEIVED | Schema, task scope, command ID, node, executor, verifier binding, target SHA, and push/head checks pass | INDEPENDENTLY_VERIFIED only after verifier runs | Any mismatch or verifier failure -> REJECTED/BLOCKED, never PASS |
| INDEPENDENTLY_VERIFIED | Durable FINALIZING marker is written; claim release CAS succeeds; final VERIFIED marker is atomically promoted | COMPLETED | Promotion failure rewrites a non-authoritative failure marker; never infer completion from FINALIZING |
| Any nonterminal | Contradictory identity, ambiguous run discovery, uncertain remote state, persistence/CAS failure | QUARANTINED or BLOCKED | No lease-expiry release; exact remote terminality and claim identity must be re-established |
| Any state | Independent verifier rejects or worker concludes failure/cancelled | REJECTED | Preserve evidence; any retry gets a new attempt identity and must not reuse stale artifacts |

## Failure matrix

| Failure point | Required persisted state | Safe next action | Forbidden action |
|---|---|---|---|
| Crash before intent persisted | READY or no record | Retry validation | Dispatch without durable intent |
| Crash after intent, before dispatch | CLAIMED/DISPATCHED intent | Reconcile idempotency key and workflow history | Assume no dispatch happened |
| Dispatch accepted but CLI response lost | DISPATCHED | Exact-title plus time-fenced discovery, then CAS-persist run ID | Blind redispatch or choose newest run |
| Run ID discovered concurrently by two pollers | DISPATCHED/RUNNING | CAS permits the same ID only; conflicting IDs block | Last-writer-wins overwrite |
| GitHub API unavailable | DISPATCHED/RUNNING/BLOCKED | Backoff and retry within a durable lease; keep claim pinned | Release on timeout or network error |
| Worker still queued behind another job | DISPATCHED/RUNNING | Poll and yield the orchestration runner | Hold the sole worker runner while waiting for itself |
| Worker cancelled/fails | RESULT_RECEIVED then REJECTED, if evidence exists | Preserve sanitized terminal status and result | Treat `completed` as success without checking conclusion/artifact |
| Artifact missing, stale, malformed, or wrong SHA | BLOCKED | Request a new authorized attempt after diagnosis | Reuse older evidence or synthesize PASS |
| Independent verifier fails | REJECTED | Retain evidence and revise task/implementation | Weaken verifier or accept builder's claim |
| Crash during finalization | FINALIZING | Reconcile claim and durable marker under CAS | Treat FINALIZING as completed |
| Claim changed concurrently | BLOCKED/QUARANTINED | Stop and re-read under lock; require operator/recovery path | Overwrite the newer claim |
| Remote branch head differs from worker evidence | REJECTED | Investigate push/provenance and retry on a new attempt | Mark VERIFIED based only on artifact metadata |

## Runner scheduling contract

GitHub Actions selects an online idle runner satisfying every requested label. A workflow dispatched to a job requiring the same single runner currently occupied by its dispatcher can remain queued until that runner is released. G-5 claim capacity is therefore not equivalent to runner capacity. The controller's dispatch operation must be bounded and durable, then return; polling must be a separate short-lived invocation or a process that does not consume the worker's only eligible runner.

The worker workflow must continue to pin checkout to the immutable target SHA, retain independent verification, sanitize evidence, and avoid writes to `main`. No change to labels, timeouts, claim limits, verifier rules, or permissions alone fixes this scheduling cycle.

## Implementation gates

Before enabling async mode, tests must cover: 0/1/>1 run matches; old same-title run; malformed JSON; API unavailable; duplicate dispatch/recovery; conflicting run ID; claim identity mutation; terminal success/failure/cancelled; active worker; artifact provenance mismatch; crash after every state write/external side effect; lease/heartbeat expiry; finalization write failure; verifier failure; and remote-head mismatch. Tests must use deterministic clocks and fake transport; no test may launch GitHub Actions.

Enable the new mode only after migration compatibility, restart/replay tests, and a separately authorized real run prove that dispatch returns without waiting, the poller resumes persisted work, and no state can become COMPLETED without fresh independent evidence.
