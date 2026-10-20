# MediaHub OS — Wave 275: legacy workflow retirement drift audit

- Date: 2026-10-20
- Status: **SOURCE-LEVEL AUDIT / BRANCH DIVERGENCE CONFIRMED / NO RUNTIME ACTION**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Related controller proposal: https://github.com/VlDMlNSh/mediahub-os/pull/421

## Purpose

Determine why two old-server-only migration workflows that were deliberately retired for the clean-slate target remain present on `main`, and record their exact source-level risk before any branch integration or runtime action.

## Ref and branch evidence

At this audit:

- `main` HEAD: `80be45a70732b1d568164571d4273a6397792c3b`.
- Documentation branch HEAD before this report: `f8993cd0b18f8c81083e9b61ead126cc74087e42`.
- Compare `main...docs/mediahub-chat-tree-map-20261012`: `diverged`, documentation branch 2,824 commits ahead and 44 behind, merge base `f0f406feb9f9816b009f4e6e756813541e53b9bc`.
- GitHub compare returned 300 file records. This is a truncated/bounded view, not an exhaustive no-loss review.
- Workflow directory inventory: 36 files in `main`, 28 in the documentation branch. The 28 shared paths had identical blob SHAs at read time. Eight paths are on `main` only: six Gemini/controller workflow paths plus the two old-server migration workflows reviewed here.

The exact refs were read again in this pass. No branch ref was moved and no merge/rebase/cherry-pick was performed.

## Legacy workflow evidence

### 1. One-time storage migration

Current `main` path: [mediahub-one-time-storage-migration.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/mediahub-one-time-storage-migration.yml)

- Blob SHA: `b0f71f515419067c6b1508dc073b2dbce4f2ca7b`.
- Original addition: [commit 1299d31](https://github.com/VlDMlNSh/mediahub-os/commit/1299d31a6e5c93bd45f7fb5e9c46a17466b9bb13).
- The workflow listens to a push to `main` that changes this workflow file. Its job targets a self-hosted Linux runner labeled `mediahub-control` and grants `contents: write`.
- Source-level effects include `rsync -aHAX --numeric-ids --delete` from `/home/mediahub/local-ai/` to `/srv/mediahub/data/local-ai/`, replacing the original directory with a symlink, removing `/home/mediahub/local-ai.root-backup`, and pushing a commit to `main`.
- These effects are destructive to the source/backup lifecycle and tied to the old host layout. Source inspection is not evidence that the workflow ran or that a migration succeeded.

The documentation branch contains [retirement commit 8d9dc21](https://github.com/VlDMlNSh/mediahub-os/commit/8d9dc210b1347cc254dfa745221c1d7857ee1019), titled “retire old-server-only storage migration workflow from clean-slate target”; it removes the workflow. The file still exists on `main`, so that retirement has not been integrated into the default branch.

### 2. Old runner migration smoke

Current `main` path: [mediahub-runner-migration-smoke.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/mediahub-runner-migration-smoke.yml)

- Blob SHA: `1f6682584d51b8155e66959734d1f335802dde67`.
- Original addition: [commit 73295c2](https://github.com/VlDMlNSh/mediahub-os/commit/73295c2463cadfb8696febfbdbda7f76a9c15493).
- It is manually dispatchable and targets a self-hosted Linux runner labeled `mediahub-control`; its checks are hard-bound to hostname `mh-dev-01`, UID/GID 1001, branch `implementation/p0-06-core-runtime-services`, and commit `6191a6f56892d4aeb1444d04420a3665b989b896`.
- These are old-host-specific assumptions, not evidence for the clean-slate Contour A target.

The documentation branch contains [retirement commit 5babc50](https://github.com/VlDMlNSh/mediahub-os/commit/5babc50cbf230c72fec2adbdc52c8897cc8ec564), titled “retire old-server-specific runner migration smoke workflow”; it removes the workflow. The file remains on `main`.

## Findings and disposition

1. The removals are intentional, source-backed changes on the documentation branch, not unexplained missing files. They did not reach `main` because the refs are materially diverged.
2. Neither workflow should be invoked as part of the clean-slate target or used as proof of current runner identity/readiness.
3. The one-time storage workflow has materially destructive behavior and a self-hosted execution dependency. Its run history and the actual host/data state were not established by this source-only pass.
4. Do not merge the divergent documentation branch wholesale. A separate path-limited pull request is the safe mechanism to propose retirement on `main`, preserving independent review and CI.
5. Keep PR #421's controller gates separate; this audit does not authorize Gemini dispatch, merge, deployment or qualification.

## Verification boundaries

- Verified by source: current refs, compare status/counts, both file blobs/content, original-addition commits, and branch retirement commits.
- Not verified: whether either legacy workflow ever ran successfully, whether an old runner is currently registered, host/data status, runtime routing, or actual retirement on `main`.
- No workflow dispatch, provider/model call, secret access, host inspection, tests, runtime mutation, merge, deployment or qualification was performed.

## Next step

Open a dedicated, reviewable PR based on current `main` that removes only the two retired old-server workflow files. Do not merge until exact-head CI and independent review pass; do not change any runner or server state. Then resume tracing the authoritative A0 Task Contract/issuer lifecycle and static or mock-only negative tests.

