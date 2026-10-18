# Contour A roadmap addendum — cloud-agent enablement and manual queue fallback
Date: 2026-10-18
Status: OWNER-DIRECTED EXECUTION PLAN / PROPOSED OPERATIONAL PROCEDURE / NOT RUNTIME-QUALIFIED
Canonical roadmap: [MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
Control issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
Related source hardening: [PR #358](https://github.com/VlDMlNSh/mediahub-os/pull/358)
Prior operating model: [Wave 145](MEDIAHUB-MANUAL-CLOUD-AGENT-PARALLEL-DEVELOPMENT-OPERATING-MODEL-WAVE-145-2026-10-18.md)
Prior worker correlation fix: [Wave 146](MEDIAHUB-CONTOUR-A-FAIL-CLOSED-WORKER-RUN-CORRELATION-WAVE-146-2026-10-18.md)

## 1. Decision recorded

Do not block Contour A engineering on the completion of Gemini automation or on the autonomous queue. Until the queue is independently demonstrated to move tasks end-to-end, operate a controlled **manual cloud-agent lane** in parallel with queue hardening. Gemini is one contributor class, not a required single-provider dependency. Other authorized cloud coding/review agents may be used through their available authenticated interfaces, with GitHub branches and PRs as the common review/evidence boundary.

This is a work-sequencing decision, not evidence that any provider is connected, dispatched, qualified, or authorized for every data class. A provider is considered active for a task only when there is observable task-specific output (for example, a PR/commit or an auditable invocation result). Never report an agent as connected/working based only on account availability or a historical successful workflow.

## 2. Operating lanes

### Lane A — autonomous queue, hardening in progress
Continue implementing the queue and worker path as the long-term target. Current PR #358 improves exact/fresh workflow-run correlation, but does not establish A0 signed-envelope enforcement or full GitHub-derived provenance. It remains draft/open/unmerged; Contour A is not qualified. The next engineering gates are:
1. validate the canonical signed A0 command envelope at the actual worker ingress (issuer, capability, signature/HMAC, expiry/freshness, target/ref/source SHA, audience/node, task digest, replay/idempotency and revocation according to accepted contracts);
2. correlate dispatch with immutable GitHub run ID and validate workflow identity, event, ref, source SHA, job ID, attempt, conclusion, artifact ID/digest, and task-envelope digest using GitHub-derived metadata;
3. add negative fixtures for missing, stale, mismatched, replayed, revoked, duplicate and forged metadata; never use live dispatch merely to test parsers;
4. ensure CI explicitly runs and reports the focused tests as well as the full suite;
5. keep queue claim/lease/cancel/retry/recovery, quarantine and evidence promotion fail-closed;
6. demonstrate a controlled end-to-end read-only worker only after the relevant ingress, credential, policy and repository gates pass;
7. qualify the required executor paths, recovery, independent A3 review and soak before any launch-ready claim.

### Lane B — manual provider-assisted implementation (effective immediately as an operating model)
Use task-scoped provider sessions until Lane A demonstrably accepts and advances tasks without human handoff. For each task:
- create a task packet with objective, exact base SHA, permitted paths, explicit out-of-scope paths, expected tests/evidence, time/budget limit if defined, and prohibited actions;
- assign one provider to one bounded work item; parallelize only non-overlapping files/contracts;
- use a dedicated branch and PR per contributor; no direct writes to main, no self-merge, no secret inclusion in prompts, patches, logs, artifacts or fixtures;
- require source links, commit SHA, changed-file list, tests actually run with exact command/results, and known limitations;
- treat provider output as untrusted proposed code; primary thread performs independent diff review, runs or verifies tests, checks authority boundaries and decides integration under normal protections;
- if the provider cannot open a PR, accept a patch only with exact base SHA and a reproducible diff; do not claim delivery until the artifact is actually available and reviewed;
- stop a provider route if policy, data classification, credentials, budget, or egress eligibility is unclear. Do not route around restrictions with VPN/proxy/region spoofing.

## 3. Gemini and other cloud-agent admission sequence

Admission is per provider, model, route and task—not a blanket trust grant.

1. **Discover access:** confirm the provider can be invoked from an authenticated, supported interface. Record the exact observable evidence and date. Do not infer callable Gemini dispatch from the existence of Gemini in another UI.
2. **Read-only task:** start with contract review, test design, workflow review or source-bound audit using non-secret data.
3. **Patch contribution:** allow a dedicated branch/PR for bounded changes, only after data policy and task scope permit it.
4. **Validation:** run project CI; inspect provenance, dependency/license/security effects, test discovery and negative cases. Provider-authored tests are not independent verification.
5. **Scoped execution:** only when the worker route and signed A0 envelope are qualified for that task class; least privilege, immutable source SHA, isolated workspace, runtime-only secrets, egress policy, quotas and cancellation apply.
6. **Queue admission:** register a provider in the operational registry only when identity, model/provider route, capabilities, allowed data classes, expiry/revocation, quotas, execution isolation and evidence contract are implemented and tested.
7. **Independent qualification:** no provider may qualify its own work or promote itself, a run, or a queue state. A3/independent review and human launch authority remain separate.

Apply the same sequence to Gemini, Claude-based coding agents, OpenHands-based executors, Codex and any later provider; availability differs and must be evidenced per route. Existing evidence indicates only one historical successful Gemini read-only workflow and does not prove current end-to-end dispatch. A prior tool inventory found no registered Codex remote task environment and no callable Gemini dispatch API from that session; refresh before making current claims. SentinelX is an auxiliary host bridge, not the queue, issuer or qualification authority.

## 4. Initial parallel work packets

Keep work non-overlapping and require a PR or reviewable artifact for each:
- **Packet A0-INGRESS:** negative tests and contract review for signed command envelope, issuer/capability, freshness, target binding, replay and revocation. No live dispatch.
- **Packet RUN-PROVENANCE:** workflow/run/job/attempt/ref/event/source SHA/artifact digest binding and tests for missing, duplicate, stale and mismatched records.
- **Packet SCHEMA-QUALIFICATION:** standards-compliant JSON Schema Draft 2020-12 validation, format assertions, positive/negative fixtures and reproducible tool/version/digest record for task envelope, registry and evidence manifest v0.2.
- **Packet CI-OBSERVABILITY:** verify the exact PR head runs focused tests and publishes useful failure evidence; never equate green unrelated checks with test execution.
- **Primary integrator:** reconcile contracts, inspect all diffs, rerun tests, maintain the roadmap/map/checkpoint, and block merges where authority/provenance gates remain open.

If only one provider is usable, run these sequentially rather than waiting for additional providers. The project should progress on independently actionable work even if Gemini access or a provider quota is blocked.

## 5. Manual fallback lifecycle and stop/go rules

Manual mode remains active until all of these are demonstrated:
- queue discovers an eligible task from the canonical queue state and records an auditable claim/lease;
- issuer/capability checks and signed A0 envelope are enforced at ingress, not merely in a controller;
- worker starts from an immutable allowed source SHA in an isolated, bounded workspace;
- secrets are runtime-only and unavailable to untrusted task content and artifacts;
- run/job/attempt/source/ref/artifact provenance is fetched from authoritative GitHub metadata and cryptographically/digest-bound to the task evidence;
- retries, cancellation, replay prevention, duplicate dispatch, quarantine and recovery have passing negative/chaos fixtures;
- a task can be dispatched, executed, independently verified and reconciled to terminal state without manual selection of the run or hand-carried evidence;
- required executor-path rounds, recovery, independent A3 review and current soak meet the accepted qualification contract.

Until then, every manually assisted task must remain explicitly marked MANUAL / PROVIDER-ASSISTED and must not be counted as proof of autonomous queue operation. Green CI, a provider response, a merged PR, or a single successful run alone is not Contour A qualification. No Contour B work starts before Contour A deployment and independent acceptance.

## 6. Security and authority invariants

- Human retains final launch authority; A0 controls only ASTRA internal engineering queue state under its accepted contract.
- Jarvis corporation-level mission coordination and MediaHub Product State Authority's canonical product-state mutation remain separate.
- GitHub dispatch permission is not issuer authorization; workflow titles are correlation metadata, not authorization.
- No secrets in repository content, prompts, source patches, artifacts or reports.
- No paid fallback without task-specific budget authorization; no hidden provider/egress substitution.
- Provider output is untrusted input; the provider cannot self-review, self-qualify or self-promote.
- No merge/deploy/launch while required CI, branch protection, provenance, architecture or acceptance gates are unresolved.

## 7. Current evidence and next action

- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains the governing Contour A tracker; it explicitly says CAF-Q-001…CAF-Q-015 is documentary, not a live scheduler.
- [PR #358](https://github.com/VlDMlNSh/mediahub-os/pull/358) is open, draft and unmerged. Latest live PR snapshot during this pass reports head `a36fa0ec8b23d522d3953b4b8f93ee486bad7df5`; do not use earlier head SHAs as current.
- The PR snapshot exposes a dedicated workflow step for `test_worker_run_correlation.py`; workflow runs associated with the latest observed head are green (Astra Cloud Runtime Validation run 39117895925; Astra Verify run 39117896120). This does not independently prove the focused test step executed successfully; inspect job logs/step results before accepting that test claim.
- No live worker dispatch, provider task dispatch, deployment or Contour A qualification was performed by this document update.

**Next:** inspect run/job logs for the exact PR head; close test-execution evidence; implement ingress envelope/provenance validation on a dedicated branch; simultaneously issue the bounded manual packets through whichever authenticated provider sessions are actually available and record each resulting PR/artifact. Keep manual fallback until the lifecycle criteria above pass.
