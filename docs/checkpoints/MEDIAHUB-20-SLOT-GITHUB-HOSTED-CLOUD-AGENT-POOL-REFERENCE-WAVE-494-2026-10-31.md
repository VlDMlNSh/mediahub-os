# Wave 494 — Twenty-slot GitHub-hosted Cloud Agent Pool reference architecture (2026-10-31)

## Status

**REFERENCE DESIGN PREPARED / NOT ACCEPTED / NOT QUALIFIED / NOT DEPLOYED.** This pass changes documentation only. No workflow, secret, provider, billing, runner, account setting, or runtime was changed. No agent was dispatched.

## Immutable design baseline

- Canonical documentation parent: `docs/mediahub-chat-tree-map-20261012` at `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4`.
- Runtime source snapshot used by adjacent Waves 488–493: main `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Wave 488 runner matrix candidate: PR #601, head `02f0988cdeac2c6b360946c9a62b7a56f21c142d`.
- Wave 489 hosted runner manifest candidate: PR #603, latest inspected head `cb9f3a1f60ad3ceafb2f5b15b8ae4771c487cc5f`.
- Wave 493 Gemini orchestration report: PR #607, head `d9f61f127fcd8cf25fb49b95028c0e590efcbdd9`.
- Governing queue: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md).

The PRs above are independent, unmerged documentation candidates. Their exact-head status APIs returned no contexts/runs in this pass; that is **NOT VERIFIED**, not PASS. No claim is made that the proposed runner manifest or pool is accepted.

## 1. Objective and terminology

Design a high-utilization, 20-slot logical execution pool on GitHub-hosted ephemeral runners. A slot means one concurrently executing GitHub Actions job backed by one hosted runner allocation; it is not a permanently named VM, a persistent agent, or a guaranteed reservation.

The owner has clarified that the referenced 20 machines are GitHub-hosted cloud VMs, not physical owner-managed computers and not the existing SentinelX/self-hosted nodes. GitHub-hosted jobs request a runner label/profile; the workflow does not select one of 20 individually addressable VMs.

Wave 488 records the published Free-plan public-repository concurrency reference of 20 standard jobs and the 5-job macOS ceiling. This is a platform reference, not proof of this repository/account's effective plan, concurrency, free minutes, available slots, or a reservation. The effective account entitlement and current usage remain **NOT VERIFIED**. A scheduler must discover/verify effective capacity and enforce the lower of policy limit and observed GitHub capacity.

## 2. Reference 20-slot allocation

Use dynamic logical reservations, not permanent machine ownership:

| Lane | Nominal slots | Purpose | Reallocation |
|---|---:|---|---|
| Agent execution | 8 | Gemini and other admitted model agents: bounded implementation, research, documentation | May borrow test/research capacity when queues are empty |
| Build and test | 4 | Unit/integration tests, schema/contract validation, lint, deterministic builds | Priority rises for an active candidate PR |
| Independent review | 3 | Contract/architecture review, security/provenance review, regression review | Reserved for completed immutable candidate outputs |
| Research and discovery | 2 | OSS/source/license research, dependency and platform investigation | Borrowable by execution or test queues |
| Integration and evidence | 2 | Artifact verification, digest/provenance checks, PR evidence reconciliation | Used only after source artifacts exist |
| Control/recovery reserve | 1 | Queue reconciliation, controller recovery, retry/cleanup and operational probes | Not used for ordinary long-running model work |
| **Total** | **20** |  |  |

These are scheduler budgets, not fixed GitHub machine types. When a lane has no eligible work, its slots are borrowable under weighted-fair scheduling. The control reserve is a logical priority budget, not a permanently running VM. The scheduler must not keep jobs alive just to make utilization appear high.

## 3. Runner profile policy

- Default general-purpose profile: `ubuntu-24.04` x64.
- Secondary on-demand profiles: `ubuntu-24.04-arm`, `windows-2025`, `windows-11-arm`, `macos-26`, `macos-26-intel`.
- Use specialist profiles only when the task has an explicit OS/architecture requirement and the profile has passed its own qualification.
- Do not use `ubuntu-slim` for model workers.
- Larger runners are excluded from the free-only baseline; no paid/larger-runner fallback.
- Standard hosted runner profiles in the Wave 488 matrix do not provide a documented Linux/Windows GPU entitlement. macOS integrated GPU/Metal/MLX performance is not guaranteed by the runner catalogue and requires measurement.
- Standard jobs are ephemeral. Workspace is job-local; cross-job handoff uses bounded artifacts or immutable source-control commits. No shared filesystem, stable peer IP, direct runner-to-runner network, fixed egress IP, persistent GUI, or runner bandwidth SLA is assumed.

## 4. Workload DAG and parallelism

Parallelize independent tasks, not dependent phases of the same task.

1. A0 admission creates a signed, bounded task envelope with issuer, capability, task ID, immutable target SHA, allowed paths/tools, data classification, provider/model policy, quota, expiry, cancellation and evidence requirements.
2. Scheduler validates admission, provider quota, global concurrency, per-provider concurrency, per-repository limits and lane fairness before dispatch.
3. Independent task envelopes may execute concurrently across the 20-slot budget.
4. For one implementation task, Agent 1 creates a candidate PR/result first. Agent 2 and Agent 3 are then dispatched against the same immutable PR number, base SHA and head SHA. They must not review a moving branch or race a not-yet-created PR.
5. Deterministic build/test jobs can run in parallel with independent read-only reviews after the candidate head exists.
6. Integration/evidence jobs verify artifact digests, source provenance, exact-head CI and review conclusions. Missing or ambiguous evidence fails closed.
7. Merge, publication, deployment and product-state mutation remain separate authorities and gates.

The three Gemini roles remain distinct. Sequential A1 → A2 → A3 within one dependent review chain reduces peak concurrency and prevents review races. Pool-wide throughput is retained by running other independent tasks in parallel. Sequential orchestration does not necessarily reduce total Actions billed minutes.

## 5. Scheduler policy

Required scheduling properties:

- Weighted fair queue across task classes; prevent starvation with aging.
- Priority order: safety/security remediation; blocked critical-path dependencies; candidate-PR verification; deterministic CI; research; low-priority experiments.
- Per-provider concurrency and quota token buckets independent of runner-slot capacity. A free model quota is not multiplied by adding API keys or VM slots.
- Reserve quota before provider execution; reconcile actual usage after completion; release reservations on preflight rejection/cancel; honor provider reset/retry-after; exponential backoff with jitter for transient failures.
- No paid fallback. Unknown provider/model, unexpected actual model ID, quota ambiguity, or disallowed data classification => reject/hold, not fallback.
- Idempotent task IDs and durable dispatch receipts; duplicate delivery must not duplicate model execution or publication.
- Leases with expiry/heartbeat; cancellation propagation; timeout; retry classification; orphan-run reconciliation; bounded retry count.
- Stop dependent stages after failed/missing predecessor. Preserve partial evidence and mark incomplete results NOT VERIFIED.
- Global concurrency ceiling is `min(20, verified GitHub effective concurrency, repository policy ceiling)`; additionally apply platform-specific ceilings (including macOS).
- Backpressure when queue depth, provider quota, artifact retention, or review capacity exceeds safe limits.

## 6. Isolation, credentials and authority

- One fresh hosted VM per standard job; immutable target checkout; `persist-credentials: false`; read-only `contents` by default.
- No `secrets: inherit`. Provider credentials are injected only into the exact authorized runtime step and never into task envelopes, prompts, artifacts, caches or logs.
- `MEDIAHUB_GITHUB_TOKEN` remains controller-only; never expose it to agent processes. HMAC signing material remains controller-only.
- Agent workers produce bounded artifacts/patch proposals; they do not merge, publish releases, deploy, or mutate canonical product state.
- A0 owns task lifecycle/admission and capability enforcement; Jarvis and ASTRA A0 do not gain Product State Authority. Product State Authority remains separate.
- OPA may be evaluated as a policy decision engine only; it does not become the issuer, trust root, or MediaHub authority.
- Egress must be destination- and data-classification-aware. Standard runner dynamic egress and the absence of an enforced destination allowlist remain blockers for provider-connected execution until explicitly resolved.
- Keep audit, artifact retention/deletion, privacy/R-06, provenance, cancellation and replay receipts durable and correlated by task/run/job IDs.

## 7. Utilization and efficiency metrics

Measure actual useful work rather than raw runner occupancy:

- Slot utilization = busy eligible runner-job seconds / available eligible slot seconds, reported per lane and in aggregate.
- Useful-work ratio = completed, accepted task work / total runner time; report retries, failed jobs and idle waiting separately.
- Queue wait: p50/p95 by priority and lane.
- Stage duration: admission, queue, startup, execution, verification, artifact transfer, teardown.
- Provider efficiency: successful tasks per provider quota unit, throttling, quota wait and actual returned model IDs.
- Quality: first-pass test rate, review defect detection, rework rate, provenance completeness, false-success rate (target zero).
- Cost: Actions minutes by runner class and repository visibility; provider usage by project/key and model; no hidden paid fallback.
- Reliability: cancellation latency, orphan-run rate, replay rejection, recovery success, artifact digest verification and missing-evidence rate.

Do not maximize utilization at the expense of verification, fairness, quota controls or security. A lower utilization with complete evidence is preferable to busy but untrusted agents.

## 8. Capacity and deployment phases

**Phase 0 — verify entitlement:** obtain authoritative repository/account plan and effective concurrency, usage, runner classes, macOS cap, billing/usage and other-workflow contention. Do not infer capacity from the owner's VM count alone.

**Phase 1 — qualify one slot:** one non-secret, read-only `ubuntu-24.04` job, exact SHA, job-local workspace, no provider key, bounded artifact and teardown evidence.

**Phase 2 — scale by controlled steps:** 1 → 2 → 4 → 8 → 12 → 16 → 20 concurrent jobs, only after each level meets queue, failure, cancellation, artifact, provenance, egress and budget criteria. Stop/roll back on unexpected billing, concurrency throttling, missing evidence, data-egress violation or orphaned jobs.

**Phase 3 — multi-lane qualification:** exercise mixed independent workloads and provider quota arbitration; then qualify ARM/Windows/macOS specialist lanes only when demanded.

**Phase 4 — operational acceptance:** independent review of exact target manifest, scheduler behavior, issuer/capability, R-06, egress, secrets, provenance, replay, cancellation/recovery, cost and operational runbooks. Deployment and production acceptance remain distinct.

No phase is authorized by this design document alone.

## 9. Current blockers and evidence

- Issue #301 remains OPEN and controls A0 issuer/ingress/lease/cancel/recovery, R-06, target manifest, schema validation and independent review.
- PR #595 (cloud-first priority), #601 (runner target matrix), #603 (manifest reconciliation), #606 (mature OSS shortlist), and #607 (Gemini efficiency) are OPEN/DRAFT/UNMERGED at this pass.
- PR #601/#603/#606/#607 and #595 exact-head status/run APIs returned empty results in this pass; CI is **NOT VERIFIED**, not PASS. Formal review evidence was not established here.
- Wave 489 manifest v0.2 remains a candidate; its own record marks account plan, effective concurrency, artifact retention, destination-level egress, schema validation and independent review unresolved.
- Current Gemini controller uses fixed task profiles and does not accept this exact arbitrary 20-slot design packet. No dispatch was attempted.
- Secret/variable presence and scope remain NOT VERIFIED. No secret values were read.
- No agent dispatch, provider call, benchmark, workflow modification, merge, deployment, qualification or acceptance occurred.

## 10. Next bounded work

1. Reconcile this logical scheduler policy with the Wave 489 JSON manifest and define a versioned queue/scheduler contract (no runtime authority changes).
2. Define Draft 2020-12 schema plus behavioral tests for fair scheduling, per-provider quotas, idempotency, leases, cancellation, retry, backpressure and immutable A1→A2→A3 handoff.
3. Obtain independent A3 review and R-06/issuer/egress decisions before runtime changes.
4. Verify effective GitHub plan/concurrency and artifact retention from authoritative account settings.
5. Only then implement and qualify the smallest read-only pilot.

## References

- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #595 — Cloud Pool First priority](https://github.com/VlDMlNSh/mediahub-os/pull/595)
- [PR #601 — GitHub-hosted runner target matrix](https://github.com/VlDMlNSh/mediahub-os/pull/601)
- [PR #603 — hosted runner manifest reconciliation](https://github.com/VlDMlNSh/mediahub-os/pull/603)
- [PR #606 — mature OSS shortlist](https://github.com/VlDMlNSh/mediahub-os/pull/606)
- [PR #607 — Gemini runner efficiency](https://github.com/VlDMlNSh/mediahub-os/pull/607)
- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## Post-write evidence

This section is completed after the branch write and read-back.