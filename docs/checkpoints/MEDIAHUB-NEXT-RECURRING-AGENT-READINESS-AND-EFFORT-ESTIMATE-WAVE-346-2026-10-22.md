# Wave 346 — recurring /next agent readiness and engineering effort estimate

- Date: 2026-10-22
- Status: **BLOCKED / NOT QUALIFIED / NOT ACCEPTED**
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Controller: [gemini-batch-dispatch-controller.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml)
- Related PRs: [#437](https://github.com/VlDMlNSh/mediahub-os/pull/437), [#441](https://github.com/VlDMlNSh/mediahub-os/pull/441)

## Current source-backed state

- Controller blob SHA on main: `9453403bba899a2400ee3fb874d32badd034c704`.
- Latest observed repository-scoped commit result: `f4ad65acdb82d25b93845279361502b6737e1d21`; not treated as an independently fetched main ref.
- PR #437 head `e7e99c2fe5f090df3a731b0b1a7f3fcb5335bd14`; PR #441 head `9f40b90c3106662cfcc337c48f29e4794fa713dc`. Connected exact-head status/run/review results remain empty; CI and independent review are NOT VERIFIED.
- The controller already defines a no-secret `probe` mode and an explicit `agents` mode requiring confirmation, plus an owner-only exact `/next` comment trigger on Issue #301. The trigger can dispatch all three child workflows; it is not safe to post while gates are unresolved.
- Readiness consumes `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY`, and `MEDIAHUB_GEMINI_BATCH_ENABLED`. Owner has already reported these settings present in Issue #301. Do not ask owner to repeat this; effective token scope, runtime injection and governance enforcement are still NOT VERIFIED.
- Three role-specific child tasks are encoded in the controller; all use a common immutable target SHA and signed authorization envelope. Current proof does not establish successful execution.
- SentinelX host `host_5f7264034bdf0b51` (`Voktors-Mini.Dlink`) has recently returned `agent_disconnected/read_loop_ended`; local Ollama/Claude/browser execution is not qualified.
- The available connected GitHub actions in this session do not expose a workflow-dispatch write operation. No controller, probe, child workflow or local job was started in this pass.

## Effort estimate

These are engineering estimates, not measured durations or commitments. They assume one engineer/operator with repository access and existing owner-reported settings, and exclude provider quota waits or prolonged external review queues.

| Work package | Estimate | Basis |
|---|---:|---|
| Resolve PR #437 contract changes; obtain exact-head CI and independent security review; fix any discovered defects | 3–6 h | Tests exist in draft diff, but current exact-head results/review are unverified |
| Verify trusted-main no-secret probe, token scope/injection, branch/ruleset governance and fail-closed gates | 2–4 h | Required runtime/governance evidence is still missing |
| Execute first approved three-agent batch; capture controller + child IDs, terminal states, outputs/digests; independently validate useful results | 2–4 h | Controller defines roles, but successful dispatch/output is not evidenced |
| Restore SentinelX session and qualify Ollama/Claude/browser route without paid fallback; prove a bounded task reaches terminal state | 3–6 h | Recent host command channel disconnected; route/browser remain unqualified |
| Wire/verify repeatable per-`/next` orchestration, result aggregation, failure recovery, audit trail and regression checks | 2–5 h | Existing owner-only comment trigger exists; operational reliability and recovery are not yet proven |
| **Total for a first repeatable qualified cycle** | **12–25 h** | Includes one remediation/retest allowance, not arbitrary external waiting |

A narrower case of **4–8 engineering hours** is plausible only if the PR gates are already passing, trusted-main probe and effective permissions verify cleanly, and SentinelX execution recovers without implementation changes. The evidence currently available does not justify using that optimistic case as the plan.

A realistic calendar elapsed time is approximately **1–3 working days** if CI, reviewer response and host access are promptly available; external review or infrastructure outages can extend it. After qualification, each ordinary `/next` should need roughly **5–15 minutes of orchestration/triage**, while agent execution time runs asynchronously. That estimate is contingent on stable automation and is not yet measured.

## Acceptance definition for “each /next”

A single `/next` must yield all of the following before it is called successful:
1. one immutable target SHA and a bounded task envelope;
2. one controller run ID and three child run/job IDs, or explicit failed/missing status;
3. three terminal statuses and durable reports/artifact digests;
4. evidence that each child did real bounded work, not merely started;
5. independent contract/security review and exact-head CI;
6. a separately recorded Ollama/Claude executor job/session with route identity and no paid fallback;
7. updated dated report/checkpoint/map with read-back SHA evidence;
8. fail-closed behavior: no dispatch when any required gate is unknown or failed.

## Next step

First close PR #437 and #441 exact-head evidence/review gaps, verify the no-secret trusted-main probe and governance/token permissions, and restore stable SentinelX read-only execution. Then run the first authorized end-to-end batch, record all IDs/results, and only after that qualify the recurring `/next` loop. Do not post the controller's exact `/next` trigger before gates pass.

No tests, dispatch, local executor job, merge, deployment, qualification or acceptance were performed in this pass.
