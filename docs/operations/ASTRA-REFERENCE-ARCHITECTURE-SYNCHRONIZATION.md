# Astra reference-architecture synchronization

Status: **engineering guidance only — not an Astra qualification result**.
Reviewed: 2026-10-09.
Scope: adopt proven control patterns from mature agent-runtime/orchestration projects without importing frameworks that duplicate Astra's queue, authority, or evidence systems.

## Sources reviewed

| Upstream project | Verified architectural idea | Astra adoption decision |
|---|---|---|
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) — [Docker runtime architecture](https://github.com/OpenHands/docs/blob/main/openhands/usage/architecture/runtime.mdx) | Execute agent actions in an isolated runtime; separate the agent from the environment in which its code runs. | **Adopt the boundary, not the whole runtime.** Keep production services, host credentials, and controller authority outside worker workspaces. A disposable worktree is useful for version control, but is not a security sandbox by itself. Production qualification must prove the runner's actual filesystem/process/network boundary. |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) — [ACI](https://github.com/SWE-agent/SWE-agent/blob/main/docs/background/aci.md) and [configuration](https://github.com/SWE-agent/SWE-agent/blob/main/docs/config/config.md) | A purpose-built agent-computer interface, concise file/search results, edit-time feedback, and explicit tool configuration. | **Adopt.** Keep worker tools least-privilege and task-scoped; validate syntax/diff at the boundary; return explicit outcomes for empty command output; reject out-of-scope tracked and untracked files before publishing. Prompt text is not an enforcement boundary. |
| [LangGraph](https://github.com/langchain-ai/langgraph) — [persistence](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/persistence.mdx) and [checkpointers](https://github.com/langchain-ai/docs/blob/main/src/oss/langgraph/checkpointers.mdx) | Persist state at stage boundaries and preserve completed-node writes so a failed run can resume without repeating successful work. | **Adopt.** A queue checkpoint must bind `command_id`, `task_id`, `node_id`, `target_sha`, attempt, lifecycle stage, worker run ID, and evidence digest. Reconcile the checkpoint with live GitHub run state before relaunching. Do not accept stale/mismatched evidence. |
| [Temporal Python SDK](https://github.com/temporalio/sdk-python) — [workflow docs](https://docs.temporal.io/develop/python/workflows) and [error-handling practices](https://github.com/temporalio/documentation/blob/main/docs/develop/python/best-practices/error-handling.mdx) | Durable workflow execution, bounded retry policies, idempotent activities, separate transient from permanent failures. | **Adopt the semantics.** Retry transport timeouts/rate limits with bounded exponential backoff and jitter; do not retry authorization, target-SHA, executor-binding, secret-gate, or verifier failures unchanged. Persist attempt IDs and use lease fencing/idempotency before any redispatch. Do not add a Temporal service until Astra demonstrates a need that its current persistent store cannot meet. |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) — [workflow model](https://github.com/microsoft/agent-framework) and [observability](https://learn.microsoft.com/en-us/agent-framework/workflows/observability) | Typed sequential/concurrent stages, explicit routing, workflow checkpoints, and telemetry for executor/edge outcomes. | **Adopt.** Keep stages separate: admission → claim → dispatch → execute → independent verify → evidence validate → finalize. Emit structured, redacted lifecycle events with trace/command/task/node/SHA and outcome. Never put prompts, tokens, credentials, or raw sensitive outputs into telemetry. |

The upstream repositories and documents provide design evidence; their existence does **not** prove that a repository was itself developed autonomously. Astra does not record such provenance unless the project has a verifiable maintainer statement or reproducible evidence.

## Astra invariants

1. **One canonical controller.** Only the authorized controller node schedules queue work. A resident health service must not be described as a queue controller unless its process actually runs the queue.
2. **One lane claim per physical executor.** A task claim includes both its repository write boundary and a stable sentinel path for its permanent executor lane. The persistent claim store must be shared by all controller invocations on the canonical node.
3. **Fenced lease.** Every acquired lease has a fresh generation/lease ID. Heartbeat and release must match that generation; stale owners cannot renew or finalize another owner's claim.
4. **Recover before retry.** When a controller resumes after a timeout/crash, search for the unique worker run identified by command ID + task ID + node + executor. Attach to and verify that run before considering a redispatch. Never assume that a timed-out client means the remote job stopped.
5. **Durable progression.** Record lifecycle events atomically and append an fsynced, secret-free journal entry for claim, dispatch/adoption, terminal worker result, evidence acceptance, and final rejection. Persist completed status only after evidence validation and successful fenced claim release. Recovery must be fail-closed for truncated/corrupt records.
6. **Independent verifier.** Builder and verifier are separate process invocations. Accept only a single exact `ASTRA_VERDICT: PASS` machine verdict; a substring, duplicate verdict, or mixed output is not PASS.
7. **Restricted execution.** Work in a disposable task workspace bound to the exact target SHA; inspect committed, uncommitted, and untracked changes against the task boundary. Do not expose production credentials, host service sockets, or unrestricted host filesystem access to the worker. A task prompt or post-hoc diff scan alone is insufficient isolation.
8. **Bounded retry policy.** Retry only classified transient errors. Preserve immutable attempt identity and collect the final outcome. A timeout remains UNKNOWN/BLOCKED until the existing run is reconciled.
9. **One promotion gate.** GitHub job success alone is not queue PASS. Require target-SHA binding, node identity, real executor/verifier evidence, verified artifact digest, clean security gate, and verified task state.
10. **24-hour GOLD soak remains separate.** No shorter test, pre-soak check, documentation update, or successful single task can substitute for a fresh 86,400-second soak on the exact admitted SHA.

## Current implementation status

| Control | Status at review | Required proof |
|---|---|---|
| Claude-only permanent executor mapping and max-three bound | Implemented in queue contract | Fresh real evidence from all three nodes |
| Atomic claim store with lease generation/fencing | Existing implementation | Concurrency test + live recovery/fencing test |
| Same-node duplicate task prevention | Lane-sentinel claim and regression tests added on PR branch | Passing CI and two concurrently invoked controller attempts |
| Exact verifier verdict | Exact-output helper and regression test added on PR branch | Passing CI and fresh independent verifier artifacts |
| Recovering an existing GitHub worker run before redispatch | Implemented on PR branch; **not CI/runtime qualified** | Crash/restart integration test with the same command/task key |
| Durable redacted transition journal | Append-only fsynced journal implemented on PR branch; **journal replay is not implemented or qualified** | Corrupt/truncated journal, crash recovery and replay tests |
| Enforced host sandbox | **Not proven** | Host-level filesystem/process/network test for all three runner identities |
| Stable always-on controller lifecycle | **NOT PASS** | The installed `mediahub-astra.service` has previously been inspected as a minimal resident health loop, not the queue controller |
| Three-node execution + GOLD soak | **NOT PASS** | All three nodes produce current evidence, aggregate gate PASS, then a real 24-hour soak |

This table is intentionally conservative. No reference project changes Astra's authority model, and no proposed control is marked PASS merely because code or tests exist.

## Implementation order

1. Finish and test lease/lane serialization and exact verifier handling.
2. Add crash-safe run reconciliation and append-only lifecycle evidence.
3. Enforce a non-production execution sandbox on each physical worker, then test its real boundaries.
4. Repair controller deployment and runner identity through authorized host operations.
5. Re-run the full suite and an immutable-target three-node queue wave.
6. Admit the separate 24-hour soak only after the exact-SHA queue gate passes.
