# MediaHub OS — Wave 242: worker PR stale-base and security integration gate

- Date: 2026-10-20
- Status: **LIVE REF AUDIT COMPLETE; PR #405 INTEGRATION DEFERRED; CONTOUR A NOT_PROVEN / BLOCKED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- PR #405: https://github.com/VlDMlNSh/mediahub-os/pull/405
- Previous pass: [Wave 241 — large-document I/O and PAT_DISPATCH boundary](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-LARGE-DOCUMENT-IO-AND-PAT-DISPATCH-CAPABILITY-BOUNDARY-WAVE-241-2026-10-20.md)

## Live refs and source identities

- `main` HEAD: `8761f734031ef0b880b974cea24c2463e7a22046`; latest commit message: `test: remove temporary PAT dispatch smoke target`.
- Documentation branch HEAD: `00708bed4b8d1f0bc44774a6278bc9f9d5dab36b`.
- Bootstrap blob SHA: `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`.
- Canonical map Contents API blob SHA: `59973971096b716664e7c6cb6286af6fe84e4a1a`; returned content length was zero. Treat this as a connector/read limitation, not an empty or disposable map.
- Checkpoint blob SHA: `b9978ca997f966c1d3fc0c9baa2520a0c5366826` (858,660 characters).
- Master Roadmap blob SHA: `beef785c787702dc174cf9a5515bac8c9f4b292f` (317,131 characters).
- Baseline 2.0 on main blob SHA: `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.

## PR and CI revalidation

- PR #405 is OPEN, Draft, not merged; GitHub reports mergeable, which is not security approval.
- PR head remains `59951fb247a6251b1693d5f0bc807c96480f7424`; intended base is `main`.
- Live compare now reports DIVERGED: PR branch 2 commits ahead and 2 behind; merge base `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`; current main is `8761f734031ef0b880b974cea24c2463e7a22046`.
- Main advanced by two commits since the PR merge base. Therefore prior PR-head green runs are not current-base integration evidence.
- PR-head runs previously recorded: Astra Verify `39377730257` SUCCESS; Astra Cloud Runtime Validation `39377730292` SUCCESS. These were successful for the old exact PR head only.
- Current combined-status query for current main returned no status entries; the PR-run query is scoped to PR-triggered runs and returned no runs for current main. No new CI result is inferred.
- Issue #301 remains OPEN.

## Source-bound security findings

1. The PR branch workflow `.github/workflows/astra-distributed-local-worker.yml` uses `permissions: contents: read` and `persist-credentials: false` for checkouts (previously read-back verified workflow blob `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`).
2. The current main workflow still has `permissions: contents: write` and `persist-credentials: true`; the least-privilege mitigation is not yet present on main.
3. The worker source retains `git add -A`, commit, direct `git push origin HEAD:refs/heads/{branch}`, and `git ls-remote` publication logic. The PR does not remove this path.
4. Worker task loading validates JSON shape and required fields; target-SHA equality to checkout HEAD is not equivalent to verifying an issuer signature, capability scope, expiry, revocation, cancellation, or replay state.
5. The regression test in the PR locks down workflow settings, but does not prove an artifact-only handoff or that ambient self-hosted runner credentials cannot publish.
6. `PAT_DISPATCH` was not referenced by the PR workflow. Its existence, scope, expiry, and runtime injection remain unverified. No secret value was read or emitted.

## Decision

**Do not merge PR #405 in this pass.** The PR is stale relative to main and only reduces one source of token authority; it leaves a direct publisher path and has no accepted issuer/capability admission integration. A green check from the old head and GitHub's mergeable flag cannot close those blockers. Do not rebase/merge automatically until current-base CI and a security-reviewed publication boundary are evidenced.

No workflow was dispatched, no worker/agent was launched, no PAT or host credential was accessed, and no deployment or qualification was performed.

## Next bounded engineering step

1. Rebase/update the PR against current main in a controlled branch operation only after reviewing both main commits and branch protection; rerun all PR CI at the new exact head.
2. In the worker design, replace direct git mutation/push with an artifact-only result (patch/files + manifest + SHA-256). Put any publication credential only in a separate reviewed publisher, never in the worker/model subprocess.
3. Integrate a fail-closed signed-command/capability verifier bound to command ID, task digest, target SHA, node, executor and expiry; specify replay/revocation/cancellation/recovery and add negative fixtures.
4. Only after code and CI support these boundaries, use an explicitly available, authorized dispatch mechanism for a non-mutating canary. Capture run/job/artifact IDs and digests without exposing credentials.
5. Keep Contour A **NOT_PROVEN / BLOCKED** until issuer, runtime, provenance, recovery and qualification evidence is complete. Contour B remains gated on Contour A deployment and independent acceptance.

## Checksums and limitations

- Bootstrap SHA `4a101ab3d7ec766ccbd2d3541f84593e9a406a8b`; map SHA `59973971096b716664e7c6cb6286af6fe84e4a1a`; checkpoint SHA `b9978ca997f966c1d3fc0c9baa2520a0c5366826`; roadmap SHA `beef785c787702dc174cf9a5515bac8c9f4b292f`.
- Map content could not be read through the connected Contents endpoint; no map rewrite was attempted.
- The continuation checkpoint was read but not updated in this pass; its prior update path is documented as blocked and was not bypassed.
- This report records source inspection and current GitHub metadata only. No code change, workflow dispatch, runtime test, secret test, merge, deployment or acceptance occurred.
