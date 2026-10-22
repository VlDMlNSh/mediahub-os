# Wave 363 — four-executor orchestration readiness and SentinelX route audit

Date: 2026-10-22
Status: ENGINEERING AUDIT COMPLETE / EXECUTOR QUALIFICATION BLOCKED / PROPOSED DOCS
Repository: https://github.com/VlDMlNSh/mediahub-os
Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Executive result

The target state is a repeatable `/next` orchestration cycle with three independent Gemini child workflows plus one separately routed local Claude executor. A chat turn should prepare the immutable task package, dispatch only through approved routes, collect four result envelopes, verify evidence/tests, reconcile failures/timeouts, and leave changes as PRs until separate review/merge authority gates pass.

Current controller code already contains a signed GitHub API dispatch path for three child workflows. This is not yet proof of a current successful controller-owned batch. The reported `MEDIAHUB_GEMINI_BATCH_ENABLED=false` gate remains closed. This session did not dispatch a controller probe or agent batch.

The local executor path is blocked by repeated SentinelX session churn and unresolved host authorization identity. Do not remote-execute or launch agent-browser until the exact approved Alamo identity and its capabilities/allowlist are positively verified. The currently online host is `Voktors-Mini.Dlink`; the project contract says not to infer that it is the approved Alamo host.

## Live GitHub recheck

- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open: “Contour A: qualify and operationalize the cloud-agent development fabric”.
- Controller source: [gemini-batch-dispatch-controller.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml), blob SHA `3becd61702b3cad5a40f7d2a4de0b7fd6aee4b4f`.
- Controller inputs: `mode=probe|agents`, `confirm=no|yes`, optional immutable `target_sha`. Probe is the default and uses a no-secret caller-context probe.
- Agent admission requires `vars.MEDIAHUB_GEMINI_BATCH_ENABLED == true`; agent mode requires `confirm=yes`. The issue-comment path requires exact `/next` on Issue #301 by an OWNER, and the workflow injects `secrets.MEDIAHUB_GITHUB_TOKEN` and `secrets.MEDIAHUB_DISPATCH_HMAC_KEY` only in the dispatch job.
- The dispatch script prepares three tasks, each with a unique dispatch ID and HMAC signature, uses a shared target SHA, dispatches child workflows through GitHub API, correlates child run IDs and fails the batch if any child is missing or unsuccessful. This is useful implementation evidence, but its current execution is not qualified.
- PR [#444](https://github.com/VlDMlNSh/mediahub-os/pull/444) is OPEN, unmerged, and now reports mergeable=true. Head SHA `ce165cef71775ab2d34cf7001702d98ab8e1fcfd`. Exact-head combined-status returned an empty list; PR workflow-run query returned zero runs; formal reviews returned zero. These are NOT VERIFIED, not PASS.
- PR [#441](https://github.com/VlDMlNSh/mediahub-os/pull/441) remains OPEN/unmerged and reports mergeable=false at head `9f40b90c3106662cfcc337c48f29e4794fa713dc`. Formal review API returned zero entries in this pass; exact-head CI remains NOT VERIFIED.
- The current linked GitHub tool surface exposes no workflow-dispatch action. No dispatch was simulated and no run ID was invented. A manual trusted-main probe remains available in GitHub Actions UI; it must not be replaced by a physical-server route.
- Canonical Bootstrap was re-read; the large canonical map and checkpoint/roadmap remain the source of truth. No canonical files were overwritten in this wave.

## SentinelX live diagnosis

Host inventory at `2026-10-22T11:09:51Z`:
- Online/operational host: `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`, agent `0.22.0`.
- RDM device ID historically recorded: `e264f341-2e21-4dfc-9f97-9b95cd08bcd3`.
- Free plan capacity: 1 active slot / 1 used / 0 available.
- `mh-dev-01` (`host_58114817a6ab4dd0`) and `mh-dev-02` (`host_5bda3b5006655e9e`) are disabled in SentinelX.
- A `sentinel_ping` eventually returned `pong=true`; however capabilities and state calls failed with `agent_disconnected`, reason `duplicate_session` or `read_loop_ended`. A separate capabilities request in the same diagnostic window also failed with `duplicate_session`.
- `sentinel_diagnose` returned inconclusive cause, confidence none. Its 24-hour counters reported 869 calls, 585 successes, 210 reconnects, reconnect-interval CV 16.7%, 83 `duplicate_session`, 76 `read_loop_ended`, and 33 capability timeouts. These counts indicate a material reliability problem, but do not identify a proven root cause.
- The SentinelX help index is reachable and describes the allowlist-gated, outbound-WebSocket architecture. No command was executed on the host in this pass.
- Because the exact approved Alamo identity and allowlist could not be verified, `agent-browser skills get core` was not run on any host and no browser session was launched.

## Required orchestration architecture

### One immutable task package per /next

The integrator prepares a task envelope containing:
- task ID, parent `/next` correlation ID, target full SHA, base ref and expiry;
- objective, bounded scope, inputs and exact repository paths;
- role and permitted capabilities for each executor;
- explicit prohibitions (no secrets in output, no merge/deploy, no nested dispatch, no cross-contour authority);
- required tests, evidence schema, output location and terminal-state rules;
- budget/provider/model route, quota/fallback constraints and cancellation policy.

All four tasks should share the same immutable target SHA. Different roles are intentional:
1. Gemini Agent 1 — scoped implementation/research.
2. Gemini Agent 2 — independent contract/test review; do not simply duplicate Agent 1.
3. Gemini Agent 3 — security, authority, provenance and negative-test audit.
4. Local Claude — separately approved bounded repository task, using only the approved host and qualified free-only local route.

### Dispatch and result reconciliation

- Gemini 1–3: GitHub Actions controller only. Record controller run ID, child workflow/run/job IDs, dispatch IDs, terminal status, report and artifact digest. Keep a batch closed unless admission and all gates pass.
- Local Claude: SentinelX only after exact host identity, capability/allowlist, repository path, runtime, model/provider, budget and no-paid-fallback are verified. The local task is a separate lane; it must not become a Gemini transport.
- Normalize every result into a signed or integrity-protected evidence envelope containing task ID, target SHA, executor identity/route, timestamps, terminal status, changed paths, test commands/results, artifact hashes, and known limitations.
- Integrator verifies target SHA, scope, artifact digest, tests and security claims. A successful executor exit is not equivalent to VERIFIED or ACCEPTED.
- Reconcile ambiguous dispatch outcomes by correlation ID before retrying. Do not create duplicate work when the prior outcome is unknown.
- Timeout, disconnected host, absent report, empty CI response or missing artifact must become NOT VERIFIED / BLOCKED, never PASS.
- PR creation, review, merge, deployment, qualification and acceptance remain distinct gates.

### Persistent /next lifecycle

1. Read saved continuation context, then revalidate current GitHub refs, source blobs, Issue #301, PRs, exact-head CI, controller gate and executor inventory.
2. Pick one bounded task package and freeze the target SHA.
3. Prepare the three Gemini tasks and local Claude task in the shared manifest. Do not claim dispatch until the transport reports it.
4. Dispatch the Gemini batch only through the trusted controller after gates pass. Dispatch local Claude only through the qualified approved SentinelX host.
5. Collect four outputs, reconcile each to the same task/target IDs, and independently validate reports, tests, paths and digests.
6. Integrate only verified results into a dedicated branch. Run exact-head checks, reread changed files and blob SHAs.
7. Publish dated report, map addendum and checkpoint overlay; open PR(s), not direct merge.
8. At the next `/next`, poll outstanding jobs/notifications and resume only unresolved work; avoid asking the owner to repeat known configuration.

## Estimate to the next level

Planning estimate for engineering effort, not a guaranteed elapsed-time SLA:
- controller, source refs and governance audit: 2–4 h;
- close/verify Gemini dispatch gates and qualify a real three-child run: 3–6 h;
- stabilize SentinelX session and qualify the approved Claude route: 3–6 h;
- common task envelope, result reconciliation, retry/cancel and evidence integration: 3–5 h;
- end-to-end run plus independent review: 1–3 h.

Indicative total: 12–24 engineering hours, assuming existing controller and credentials can be qualified without architectural redesign. Additional work may be required if the approved Alamo host is unavailable or governance/credential scopes are incomplete. A first dispatch milestone can be reached earlier than full qualification; they must not be conflated.

## Status ledger

| Item | Status | Evidence |
|---|---|---|
| Controller source review | VERIFIED AS SOURCE READ | blob `3becd61702b3cad5a40f7d2a4de0b7fd6aee4b4f` |
| Gemini controller probe in this pass | NOT RUN | no workflow-dispatch action in linked tool surface |
| Gemini three-agent batch in this pass | NOT RUN / BLOCKED | owner-reported batch flag false |
| SentinelX host ping | SUCCEEDED ONCE | `pong=true` |
| SentinelX capabilities/state stability | NOT VERIFIED | repeated `duplicate_session` / `read_loop_ended` |
| Approved Alamo identity/allowlist | NOT VERIFIED | current host identity does not establish approval |
| Claude Code task in this pass | NOT RUN | executor gate not qualified |
| agent-browser on approved host | NOT RUN | approved host and CLI not qualified |
| PR #444 exact-head CI/review | NOT VERIFIED | empty status/run/review results |
| Contour A | BLOCKED / NOT QUALIFIED / NOT ACCEPTED | issue acceptance gates remain open |

## Next bounded actions

1. Stabilize SentinelX transport and inspect its session/allowlist through the supported capabilities endpoint once a stable connection is available; do not run commands while duplicate-session churn persists.
2. Resolve exact approved Alamo identity from project authority records, not by guessing from hostname.
3. Have owner perform the non-launching trusted-main controller probe via Actions UI if no approved dispatch API becomes available; keep batch flag false until the probe and remaining gates pass.
4. Verify PR #444 exact-head CI and review state; PR #441 remains mergeability-blocked and should not be represented as ready.
5. Use existing task envelope/schema candidates in Issue #301 rather than creating a competing schema. Add a dedicated four-executor orchestration implementation only after A0 issuer/ingress/lease/cancel/recovery and R-06 audit/privacy gates are closed.

## Source links

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #444](https://github.com/VlDMlNSh/mediahub-os/pull/444)
- [PR #441](https://github.com/VlDMlNSh/mediahub-os/pull/441)
- [SentinelX context Wave 362](https://github.com/VlDMlNSh/mediahub-os/pull/444)
