# MediaHub Contour A — Wave 244: temporary PAT dispatch probe containment audit

- Date: 2026-10-20
- Status: **CURRENT MAIN NO LONGER CONTAINS THE TWO TEMPORARY SMOKE WORKFLOWS; SECRET HISTORY/EXPOSURE UNKNOWN; CONTOUR A BLOCKED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Worker-token PR #405: https://github.com/VlDMlNSh/mediahub-os/pull/405
- Signed-command verifier PR #400: https://github.com/VlDMlNSh/mediahub-os/pull/400
- Temporary cleanup PR #406: https://github.com/VlDMlNSh/mediahub-os/pull/406

## Finding

At observed `main` HEAD `48cd45187a3a7c52368204577ab7857e85b44606`, the temporary caller workflow `.github/workflows/mediahub-token-dispatch-smoke-caller.yml` was configured to run on pushes that modify its own path. It exposed `${{ secrets.MEDIAHUB_GITHUB_TOKEN }}` to a shell environment variable and used it in an authenticated API call to dispatch a second temporary workflow. The script did not intentionally print the token, but making credential-bearing workflow execution depend on changes to the workflow itself is an avoidable secret-exposure boundary.

The paired target workflow was a simple dispatch smoke test with read-only repository permissions. Neither workflow was needed for production routing.

## Actions and evidence

1. Read both files from `main` before changing anything:
   - caller blob SHA: `03c5e08b316295703684f5b178edc3ede299037b`
   - target blob SHA: `b4b372d4cca101e16177cd94a70a43bd9c290929`
2. Created branch `security/remove-temporary-pat-dispatch-probe-wave244` from the observed `main` commit `48cd45187a3a7c52368204577ab7857e85b44606`.
3. Committed deletion of the caller workflow in commit `705df041c661006970e70869339c7c852babc31c`; then deletion of the target in commit `8002a3e67bf9634819394e612db91c790723fc4c`.
4. Opened Draft PR #406 for review. Exact-head Actions runs for commit `8002a3e67bf9634819394e612db91c790723fc4c`:
   - Astra Cloud Runtime Validation run `39383253077`: **SUCCESS**
   - Astra Verify run `39383253079`: **SUCCESS**
   - Combined status endpoint returned no legacy status entries; workflow-run results are the CI evidence.
5. During this pass, `main` advanced to `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`, commit message `test: remove temporary token dispatch smoke target`. Read-back from current `main` returned 404 for both temporary workflow paths, confirming both files are absent from the current branch. The target deletion is explicitly visible in that commit's diff. Therefore PR #406 became redundant and was not merged. The attempted PR closure was blocked by the tool safety layer; its current closure state is not claimed here.
6. No secret values were read, printed, or passed to an agent. No workflow dispatch was performed by this pass. The existence, scope, prior use, and possible historical exposure of `MEDIAHUB_GITHUB_TOKEN` were not independently verified.

## Current refs and blockers

- `main`: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`
- Canonical documentation branch observed after concurrent updates: `c89e84db19c6c052c83e6b525cbadd40e39b3147`
- PR #400 remains Draft and diverged/stale relative to current `main`; the signed-command verifier is still not integrated into the worker.
- PR #405 remains Draft and stale; the canonical worker workflow still has `permissions: contents: write` and the worker code retains a direct Git push path. This is a separate, unresolved security blocker.
- Issue #301 remains the controlling Contour A workstream. The current map Contents reader has returned an empty body with a non-empty blob SHA; do not rewrite the map based on that reader limitation.
- Contour A remains **NOT_PROVEN / BLOCKED**. No qualification, deployment, or acceptance is established. Contour B remains gated on independent Contour A acceptance.

## Next step

Re-fetch the current refs and inspect the exact commits that removed the two smoke workflows; then address the more material unresolved worker boundary: issuer/capability admission and artifact-only publication, with exact-head tests and a separately authorized publisher. Do not inject a broad PAT into the worker or model process. Keep all secret and provider operations inside an authorized, narrowly scoped dispatcher/publisher boundary.

