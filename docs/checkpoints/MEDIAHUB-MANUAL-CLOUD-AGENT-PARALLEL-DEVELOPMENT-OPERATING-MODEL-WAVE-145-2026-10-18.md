# MediaHub OS — Manual Cloud-Agent Parallel Development Operating Model — Wave 145

Date: 2026-10-18
Repository: VlDMlNSh/mediahub-os
Status: OPERATIONAL PROPOSAL RECORDED; provider enrollment and autonomous admission NOT CLAIMED.
Scope: Establish a safe manual parallel-development path while Gemini integration remains unreliable.

## Executive decision

Do not block Contour A engineering on Gemini automation. Use cloud agents as task-scoped contributors through isolated branches/PRs, with a human/A0-controlled intake and independent acceptance. Manual task assignment can start immediately where the user has a working provider session; this repository session cannot directly open a Gemini UI or prove that a task was accepted by a provider.

## Current evidence snapshot

- `main` HEAD: `c06015e0b1526e0aaa6a522306052b077455aba5` (queried live through GitHub API on 2026-10-18).
- Canonical documentation branch HEAD observed: `56782952ea8ee0df90334508d96073a7eb5145b1`.
- `main...docs/mediahub-chat-tree-map-20261012`: diverged; docs branch 2,262 commits ahead and 27 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`. Do not merge the broad docs branch into main as a side effect of agent enablement.
- Issue #301 remains open: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #333 remains open/unmerged; observed base SHA `a0c432273914fa5c4bd9e756736f9c9b72b41a77`, head SHA `a83030bc6449109626b072dc0a090a59709b4a5b`: https://github.com/VlDMlNSh/mediahub-os/pull/333
- Gemini evidence PRs #355/#356/#357 are open/unmerged. Latest observed heads: #355 `9862df3ade9d7888e9e134fe3f25b08d981e7d3f`, #356 `4fe3b41c763b0e8c929f5ef4a8233939b72fe06e`, #357 `6acbc14a8dcce7e2f822861e86dbc7e8fbf0ec1f`. Their recent Actions runs reported `action_required`, not passing CI.
- SentinelX: one operational host (`Voktors-Mac-mini.local`), Free plan limit 1/1 active slots; two enrolled hosts are disabled by user. This is a local bridge, not a pool of cloud model agents.
- Codex remote task environment listing returned no registered environments.
- Canonical ASTRA scheme assigns final authority to the human, coordination/state authority to A0-ASTRA, architecture to A1, implementation to A2, independent verification to A3, and executor-only authority to providers. Qualification schema requires fresh evidence, fail-closed, no self-qualification/self-promotion, independent A3, recovery and soak gates.

## Why all proposed agents are not simply “deployed” today

“Agent” is not a single installable component. Each provider requires an account/session or API entitlement, supported integration path, explicit task invocation, repository access, budget/usage policy, and a result channel. This session has GitHub and one SentinelX host, but no registered Codex remote environment and no callable Gemini task-dispatch API. Thus provider work can be assigned manually in the provider's own UI, but this session cannot truthfully report provider acceptance or completion until a PR/result is observed.

The architecture also intentionally prevents a model/provider from becoming A0 issuer, qualification authority, or Product State Authority merely because it was connected. That is a security control, not a reason to pause ordinary PR-based engineering.

## Manual parallel work protocol

1. Keep the authoritative task ledger in Issue #301 or a dedicated issue. Give each agent one non-overlapping task, one exact base SHA, allowed paths, forbidden paths, acceptance tests, and a required evidence format.
2. Each agent works in its own branch and opens a PR; no direct writes to `main`, no secrets in prompts or artifacts, no agent merges its own PR, no agent modifies issuer/capability or Product State Authority contracts unless that exact task is explicitly authorized.
3. Require every agent to return: provider/model identity as claimed (not trusted by itself), task ID, base/head SHA, changed paths, tests actually executed with command/exit status, CI run/job URLs, artifact digests, limitations, and known risks. Static analysis must be labelled static-only.
4. A0/maintainer triages provenance and scope. An independent reviewer checks behavior and negative cases. CI must run on the exact PR head; stale or `action_required` runs do not qualify.
5. Merge only after branch protection, required checks, authority review, no data loss, and acceptance criteria pass. Agent success reports never self-promote qualification or deployment status.

## Suggested parallel work packets (manual dispatch)

- **Gemini agent 1 — A0 ingress negative tests:** inspect the canonical issuer/capability contract and add isolated unit tests for missing/empty command IDs, bad HMAC, stale command, wrong node, wrong target SHA, replay, and task digest mismatch. Do not change production authorization code in the same PR. Report exact test command and output.
- **Gemini agent 2 — workflow-run correlation tests:** add pure tests for empty command ID, duplicate dispatches, wrong workflow/event/source ref, stale run, mismatched inputs and target SHA. Propose a fail-closed helper; do not dispatch a real worker.
- **Gemini agent 3 — evidence provenance contract:** define the smallest schema binding evidence to GitHub run ID, job ID, attempt, workflow path/ref, source SHA and artifact digest; add negative fixtures and document what GitHub API data is authoritative. Do not claim cryptographic attestation unless implemented and verified.
- **Primary engineering thread — independent implementation/review:** inspect all three PRs and exact main sources; avoid duplicate edits. Once test-only PRs exist, implement the smallest fail-closed fix on a dedicated branch and run tests without dispatching workers.

These are task packets ready for manual submission, not evidence that any agent has been launched or accepted the work.

## Wave 144 dependency

The Wave 144 report remains the current source-level blocker record:
https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-WORKER-DISPATCH-AUTHORITY-AND-EVIDENCE-BINDING-REVIEW-WAVE-144-2026-10-18.md

## Verification status

- Live GitHub refs, Issue #301, PR #333 and recent workflow run statuses were queried.
- Canonical scheme and qualification schema were read from `main`.
- No agent was remotely dispatched by this session; no new code was implemented; no tests were executed; no workflow was dispatched; no provider credentials were created; no PR was merged; no deployment/qualification status was changed.
- The canonical map is over 1 MB and its Contents API response was empty, although the API exposed its blob SHA and raw URL. A map addendum is therefore used rather than rewriting the large canonical map without a verified full-content round trip.

## Next step

Manually submit the three packets above through the already authenticated Gemini sessions, if available, while this primary thread independently develops and tests the run-correlation/authentication fix. Treat a task as started only after a branch/PR or other provider result is visible in GitHub.
