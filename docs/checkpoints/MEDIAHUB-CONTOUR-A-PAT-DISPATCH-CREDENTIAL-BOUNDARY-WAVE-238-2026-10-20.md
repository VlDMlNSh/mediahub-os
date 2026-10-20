# MediaHub OS — PAT_DISPATCH credential-boundary review (Wave 238)

- Date: 2026-10-20
- Status: **SECRET EXISTENCE/CONFIGURATION NOT INDEPENDENTLY VERIFIED; NO DISPATCH; SECURITY GATE OPEN**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Worker hardening PR: https://github.com/VlDMlNSh/mediahub-os/pull/405
- Contour A tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Prior compatibility report: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-CONTOUR-A-WORKER-TOKEN-COMPATIBILITY-GATE-WAVE-237-2026-10-20.md

## User-provided change

The repository owner reports creating a fine-grained personal access token with broad read/write permissions and storing it as GitHub Actions secret `PAT_DISPATCH`. This is user-reported state only: this pass did not read secret values or verify secret metadata, workflow exposure, or a successful dispatch. Secret values must never be copied into logs, artifacts, task JSON, model prompts, or repository files.

## Revalidated source evidence

- `main` HEAD: `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- PR #405 remains OPEN/Draft, head `59951fb247a6251b1693d5f0bc807c96480f7424`, base `main`; compare reports 2 commits ahead / 0 behind.
- Exact-head CI: Astra Verify run `39377730257` SUCCESS; Astra Cloud Runtime Validation run `39377730292` SUCCESS. These runs validate the PR head, not the existence or permissions of `PAT_DISPATCH`, a live dispatch, or publication.
- Workflow blob `c24ad16ab8ed59fd4dbad9538063f63a933eab2c` grants `contents: read` and has `persist-credentials: false` on all three checkout steps.
- Worker source blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1` still contains worker-side `git push origin HEAD:refs/heads/{branch}` followed by `git ls-remote` verification.
- Regression-test blob `12f25f684f0b37cf6d34d5c905394f9e0664fbf2` asserts least-privilege checkout settings but does not exercise a live push or publisher boundary.

## Security disposition

Do **not** wire a broad PAT into the worker job or expose it to the agent/model subprocess. The worker executes generated or task-influenced code and handles mutable workspace content; any credential in that trust boundary can be exfiltrated or misused. A green CI result is not evidence that the secret is correctly scoped or safely consumed.

Preferred design:
1. Worker runs with read-only repository access and emits a bounded, content-addressed artifact plus provenance metadata; it has no repository-write credential and no direct-push code.
2. A separate publisher receives only the artifact and immutable task/target metadata. It independently verifies issuer/capability, target SHA, task scope, artifact digest, replay/revocation, cancellation and recovery state before writing.
3. Prefer GitHub's short-lived `GITHUB_TOKEN` with narrowly scoped job permissions or a GitHub App installation token limited to the required repository and operation. Keep dispatch authority separate from contents-write authority where possible.
4. If a PAT is temporarily unavoidable, replace the broad token with a repository-scoped fine-grained token limited to only the specific permissions and operations needed, give it an expiry, rotate/revoke the broad token after replacement, and ensure only the publisher job can access it. Do not test by printing or otherwise exposing the secret.
5. Add negative tests proving the worker cannot publish and that unsigned, altered, wrong-target, replayed, revoked or cancelled artifacts are rejected.

## Actions and non-actions

- Re-read PR #405 metadata, workflow, worker source, tests, prior Wave 237 report, Issue #301, compare metadata and exact-head workflow runs.
- No secret value or host credential was accessed; no worker was dispatched; no provider was called; no merge, deployment, or qualification was performed.
- The canonical map's connected Contents read still returns empty content for blob `2187b4ca50792fe073f0979442c0f73432a2f6f9`; this is a reader limitation, not evidence that the map is empty. The map was not changed.

## Gate and next step

Contour A remains **NOT_PROVEN / BLOCKED**. Keep PR #405 Draft. Next implementation slice: remove worker-side direct push and hand off a deterministic artifact to a separately authorized publisher; add adversarial tests and verify publisher-only secret exposure before any controlled dispatch. Contour B remains gated until Contour A deployment and independent acceptance.
