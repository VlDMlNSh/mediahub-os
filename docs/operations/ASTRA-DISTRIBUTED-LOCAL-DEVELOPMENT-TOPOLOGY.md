# Astra Distributed Local Development Topology

## 1. Authority and executor matrix

The required authority designation is **mh-dev-01 as controller/authority**. `mh-dev-01` owns command admission, queue coordination, qualification gates, and authoritative result publication. The required permanent lane designations are **mh-dev-02 as primary local pool** and **Voktors-Mac-mini.local as fast pool**.

The permanent production executor matrix contains exactly three Claude executor lanes:

1. `mh-dev-01` — controller-host Claude executor lane.
2. `mh-dev-02` — primary local Claude executor lane.
3. `Voktors-Mac-mini.local` — fast-pool Claude executor lane.

The stable identity `Voktors-Mac-mini.local` is canonical for queue admission and qualification. Historical host aliases and candidate execution surfaces are not additional permanent executors. Backend/model details are runtime configuration and must not be inferred from the executor label.

## 2. Concurrency and claims

**G-5 = 3 (G5 = 3):** G5 allows three simultaneous disjoint claims, one per permanent executor lane. The queue may admit at most three such claims at once. A claim is scoped by task identity and declared resource/file boundary. Overlapping claims must not execute concurrently. Claim acquisition, heartbeat, expiry, and recovery are enforced by the queue's claim contract; operators must not remove claim records manually to force progress.

## 3. Exact target-SHA binding

The **target-SHA binding** is mandatory. Every dispatch names one full 40-character target Git commit SHA. Before executing, the worker verifies that its checkout matches that exact SHA and that the workspace satisfies the worker's clean-workspace policy. The target SHA is carried through builder evidence, verifier input, scoped test results, branch-head evidence, and the final qualification aggregate. Evidence from another SHA, a stale run, or a different task/command identity is invalid.

Target-SHA metadata for the audited dispatch: `3e3c4daa62095d3049c8dcf121a614250ec5ebfc`. This records which commit was attempted; it does not mean the worker passed or that Astra Gold is qualified. Every future dispatch must record its own target SHA in run-scoped evidence.

## 4. Builder/verifier separation

Each task uses an A2 Builder to implement only the declared deliverable and an independent A3 Verifier to evaluate the actual diff and scoped test evidence against every acceptance criterion. The verifier must run independently and emit the exact machine-readable verdict required by the worker contract. Missing, malformed, contradictory, or negative verdicts fail closed; successful process exit alone is not a PASS.

A no-change result is acceptable only when the task explicitly permits it and the independent verifier proves that the existing repository state satisfies the acceptance criteria.

## 5. Isolated branches and GitHub evidence transport

Workers operate in **isolated branches** derived from the exact target SHA. The policy is explicit: **no worker writes directly to main**; workers never write directly to `main`. Any source change must remain within the task's declared boundary, pass security and scope checks, pass the required regression tests, and pass independent verification before it can be considered for promotion.

GitHub Actions is the transport for run-scoped worker evidence, including task/command identity, target SHA, test output, verifier verdict, and branch-head verification. The controller must validate provenance and SHA consistency before accepting evidence. A successful job or uploaded artifact by itself does not establish Astra Gold qualification.

## 6. Fail-closed promotion

Promotion is blocked if any required evidence is missing or stale, the checkout or branch SHA mismatches, a worker identity is not admitted, the task boundary is exceeded, a security check fails, a required test fails, the independent verifier does not emit the exact PASS verdict, or the aggregate cannot establish a consistent target SHA. Historical evidence must not substitute for a fresh qualification run.

No worker may merge to `main`, bypass branch protection, or publish directly to production. Promotion requires the repository's normal review and policy gates.

## 7. Secrets and security boundary

The **no credentials or secrets** rule is absolute. Credentials, tokens, private keys, personal data, and secret-bearing environment values must never be placed in task documents, source diffs, logs, or uploaded evidence. Workers receive only the credentials and capabilities required by their authorized execution path. Secret values must be redacted from diagnostics; a suspected secret in a diff blocks promotion.

Workers must not alter production infrastructure, credentials, or queue authority outside the explicitly authorized task boundary.

## 8. Operational interpretation

A runner admission probe proves only that the runner can accept a job. Node attestations prove only the checks represented by those attestations. A worker-level PASS proves only the task and target SHA named by that worker. Astra Gold is PASS only when the canonical supervisor completes successfully and its fresh aggregate binds all mandatory qualification evidence to the same intended commit.

### Observed runner-capacity blocker — 2026-10-10

The registered repository runner inventory showed exactly one online runner named `mh-dev-01` with the `mediahub-control` label. Both the supervisor's `supervise` job and the `mh-dev-01` distributed-worker job require that label. In supervisor run `38034436196`, `supervise` occupied the runner from `07:28:17Z` to `08:09:21Z`; worker run `38034576170` was created at `07:29:06Z` but its job did not start until `08:09:24Z`, immediately after the supervisor released the runner. This is direct evidence of runner-slot contention, not evidence of a 40-minute model execution.

Consequently, **G-5 = 3 describes the queue's claim limit, not three currently available concurrent runner slots**. Increasing remote wait time alone cannot resolve this self-dispatch dependency. Before asserting effective three-lane concurrency or attempting a fresh Astra Gold qualification, either register a second self-hosted runner service on `mh-dev-01` with compatible worker labels (a separate runner instance, not another label on the same instance), or refactor the orchestration so the controller does not wait on a worker job queued behind itself. A fresh run must demonstrate actual overlap; do not infer it from runner labels or attestations alone.

### Quarantined worker recovery

A claim in `QUARANTINED` state must not be released based on lease expiry or a successful cancellation request. Recovery requires a persisted worker run ID and persisted dispatch identity (`command_id`, node, and executor). From the controller checkout, an operator can run:

```sh
ASTRA_RECOVER_QUARANTINED_TASK_ID=MH25-QUEUE-002 PYTHONPATH=runtime python3 -m mediahub_runtime.autonomous_queue
```

Replace the example task ID with the exact quarantined task. The recovery command queries that run using `gh run view`, validates its exact workflow display title against the stored dispatch identity, and releases the claim only when GitHub reports `status=completed`. A missing run ID/identity, title mismatch, API/CLI failure, or nonterminal status returns `BLOCKED` and leaves the claim quarantined. A completed run is released as `REJECTED`; the task must be requalified through the normal queue rather than treating recovery as a PASS.

If a controller crash occurred after dispatch but before the run ID was persisted, this command intentionally refuses automatic recovery. Reconcile the run history manually against the exact command ID, task ID, node, executor and dispatch time; do not release the claim until the matching run is unambiguously identified and confirmed terminal.
