# Wave 497 — PR check-state correction for Alamo/FCC/Claude Ubuntu runner

- Date: 2026-10-31
- Status: **IMPLEMENTED ON WORKING BRANCH / EXACT-HEAD CI NOT VERIFIED / NOT ACCEPTED**
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/610
- Branch: `contour-a/alamo-fcc-claude-hosted-runner-20261031`
- Previous tested head: `60a8b0100582fd0709f39df6666ac433ccbbac85`
- Code-change commit: `4bd96e478c53bc7f1f0429c26ca84644e344f28d`
- Current workflow blob: `e8a7ba9d34bde5654a42ed3bc9f33a5d3cf9e58e`
- Current contract-test blob: `f62ac0184e5e251d1fdb2dcab2d6a4ff07afa01a`

## Problem observed

The previous PR-triggered workflow had a passing contract-test job, but the `dispatch-gate` and `alamo-local-fcc-claude` jobs were marked `skipped`. The three workflows associated with the previous head concluded success, but those skipped jobs did not prove the runtime path and made the check matrix non-green/ambiguous to the requested gate.

## Bounded correction

- `dispatch-gate` now runs for both PR and manual dispatch events. On PR it emits `admitted=false` and exits successfully without authorizing execution.
- `alamo-local-fcc-claude` now runs a harmless PR-only declaration step, so the job itself can conclude success on PR.
- Every installation, model-download, FCC startup and Claude Code smoke step is explicitly limited to `workflow_dispatch`.
- Evidence upload is limited to manual dispatch.
- Added a contract test asserting the PR-safe behavior and explicit live-execution boundary.

## Verification

- Read back workflow and test from the working branch; blob SHAs above match.
- Previous head `60a8b010...`: workflow run `41183890589` contract job `124486735745` SUCCESS; dispatch-gate job `124486736562` SKIPPED; runtime job `124486736741` SKIPPED. Astra Cloud Runtime run `41183890472` SUCCESS; Astra Verify run `41183890499` SUCCESS.
- New exact head `4bd96e478c53bc7f1f0429c26ca84644e344f28d`: no associated PR workflow runs returned at observation time; combined commit status returned an empty status list. **Exact-head CI = NOT VERIFIED**, not PASS.
- Independent PR reviews: none. Review threads: none.
- No workflow dispatch, runner install, model pull, FCC startup, Claude Code request, or artifact generation occurred.
- Alamo/Ollama equivalence remains `NOT_VERIFIED`; no qualification or acceptance.

## Next gate

Wait for exact-head PR checks on `4bd96e478c53bc7f1f0429c26ca84644e344f28d`. Inspect all job conclusions; require no failed, cancelled, skipped required jobs. Then obtain independent security/contract review. Do not merge or manually dispatch the live runtime before those gates pass.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
