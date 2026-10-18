# MediaHub OS — Contour A Exact-Head Evidence and Executor-Admission Review — Wave 143

Date: 2026-10-18
Repository: VlDMlNSh/mediahub-os
Scope: independently inspect Wave 142 follow-up PRs and current Contour A queue/worker contracts.
Status: SOURCE REVIEW COMPLETE; PR EVIDENCE INCOMPLETE; NO INTEGRATION OR RUNTIME QUALIFICATION.

## 1. Live refs

- `main` HEAD at review: `c06015e0b1526e0aaa6a522306052b077455aba5`.
- Documentation branch HEAD at review: `d2218e1be9c1aa36741f03c8d9b35275eb3550b6`.
- Compare: docs branch is DIVERGED from main, 2253 ahead / 27 behind; merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. No merge/rebase/cherry-pick performed.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap blob on docs branch: `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Canonical Component Manifest 2.0 blob on main: `45988bf9da202c9597d0ca2de50e92e5c2e6ed55`.
- Governance contract blob on main: `1d3ac25e7817f365807ad85d0d7c9007bd48bebf`.
- Qualification launch schema blob on main: `aef6229477ed8ec45e45170f98ea87f7ba75ca29`.
- Queue implementation blob on main: `72c4a5ccb367884fb02d247b1b8848ea62c3c6b1`.
- Queue contract test blob on main: `e3466fd5f8d6d47a846f8ec75b0ab3ca46ed0dc7`.
- Claim/lease implementation blob on main: `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd`.
- Worker workflow blob on main: `f650f2416c19dc75b4a0eeec037661c0c6169910`.
- Clean target reconciliation Wave 10 blob on docs branch: `1f748bf80e08067fd85a7e1b0821cc4d12bda676`.

## 2. Independent PR status and disposition

| PR | Exact head SHA | Current check-runs at inspection | Disposition |
|---|---|---|---|
| [#355](https://github.com/VlDMlNSh/mediahub-os/pull/355) | `9862df3ade9d7888e9e134fe3f25b08d981e7d3f` | 0 | Useful manifest-to-scheme crosswalk; no exact-head CI evidence; candidate only |
| [#356](https://github.com/VlDMlNSh/mediahub-os/pull/356) | `4fe3b41c763b0e8c929f5ef4a8233939b72fe06e` | 0 | Properly labels external JSON Schema engine as NOT_VERIFIED and negative fixtures as proposed; no exact-head test evidence |
| [#357](https://github.com/VlDMlNSh/mediahub-os/pull/357) | `6acbc14a8dcce7e2f822861e86dbc7e8fbf0ec1f` | 0 | Explicit static-only audit; no tests executed; no exact-head CI evidence |

All three remain OPEN and UNMERGED. The corresponding Gemini workflow runs establish that workflow jobs generated their review artifacts; they do not establish PR checks, independent acceptance, live execution, or qualification. Review comments were added:
- PR #355: https://github.com/VlDMlNSh/mediahub-os/pull/355#issuecomment-6248133657
- PR #356: https://github.com/VlDMlNSh/mediahub-os/pull/356#issuecomment-6248134091
- PR #357: https://github.com/VlDMlNSh/mediahub-os/pull/357#issuecomment-6248134602

## 3. Source review: queue and worker path

### Confirmed source facts
1. `runtime/mediahub_runtime/autonomous_queue.py` declares three permanent executor lanes (`mh-dev-01`, `mh-dev-02`, `Voktors-Mac-mini.local`) and caps claims to the pool size.
2. `process_task_remote` dispatches `.github/workflows/astra-distributed-local-worker.yml` with `--ref main`, then polls a workflow run, downloads an evidence artifact, checks schema/status/command/target/node/task/executor/verifier identities, checks worker and remote branch SHAs, and releases its claim in `finally`.
3. The workflow routes each node ID to a distinct `self-hosted` runner label set. It checks host/user/executor and required local CLI/model presence. Action references in the reviewed workflow are version tags (for example `actions/checkout@v4` and `actions/upload-artifact@v4`), not immutable full commit SHAs.
4. `tests/test_autonomous_queue_contract.py` is primarily source-string/order assertions. It does not itself exercise GitHub dispatch, runner availability, real cancellation, timeout recovery, artifact tampering or a full queue-to-worker lifecycle.
5. `architecture/ASTRA-GOLD-QUALIFICATION-LAUNCH-SCHEMA.yaml` requires fresh evidence, isolated workspace, all mandatory executor paths, at least 23 rounds per path, concurrency, recovery, independent A3, pre-soak and current 24-hour soak; launch G11 remains human-only.
6. Wave 10 target reconciliation states no owner-accepted exact clean target manifest exists and records target identity/profile UNKNOWN/BLOCKED. This remains a deployment admission blocker.

### Risks and unproven assumptions
- A pool entry in Python is not evidence that the corresponding GitHub self-hosted runner is currently online, isolated, correctly labeled, or qualified. SentinelX host state and GitHub runner registration/availability are separate evidence sources.
- Mutable action tags reduce supply-chain reproducibility; before production qualification, resolve and pin each action to a verified full commit SHA and record upstream source/version. This review did not change those references because no pinned update was implemented or tested here.
- The controller's SHA and artifact checks are useful guards but do not prove all runtime security/recovery properties. The worker path must be tested against malicious/malformed evidence and timeout/cancel/restart/replay cases at a fixed source SHA.
- The existing queue test's textual assertions are insufficient as the sole evidence for runtime invariants.

## 4. Parallel-agent operating decision

All three Gemini agents remain supplemental. The primary engineering thread continues independently while they run: reading canonical contracts, checking exact refs/SHA, selecting components against actual capability gaps, reviewing source, and recording verified results. No task is handed off exclusively to agents unless explicitly documented as a dependency. Agent statements remain untrusted candidate evidence until independently verified.

## 5. Next bounded engineering action

1. Keep PRs #355–#357 open and unmerged until exact-head checks and review requirements are available.
2. Add behavior-level tests for worker evidence rejection, dispatch/run identity matching, malformed artifact handling, stale/expired claims, timeout/cancel/recovery, and exact target SHA. Use fixtures/mocks; do not dispatch live workers merely to test parser logic.
3. Resolve/pin GitHub Actions by verified upstream commit SHAs and add a regression check that rejects tag-only `uses:` references in the protected Contour A workflow set.
4. Separately verify current GitHub self-hosted runner inventory/labels and accepted workspace/network/secret profile. Do not infer it from SentinelX connectivity.
5. Revisit the clean target manifest and A0/R-06 acceptance blockers before attempting full runtime qualification.

## 6. Disposition

Source review only. No tests were executed by this pass, no workflow was dispatched, no provider or credential was invoked, no runtime was installed, and no PR was merged. Contour A remains NOT READY FOR DEPLOYMENT / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED.

Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
