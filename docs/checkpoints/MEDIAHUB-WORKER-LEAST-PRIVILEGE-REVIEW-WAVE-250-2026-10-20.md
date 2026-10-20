# Wave 250 — Worker least-privilege PR review and publication boundary

- Date: 2026-10-20
- Status: **REVIEW EVIDENCE RECORDED; PR #405 IS DEFENSE IN DEPTH ONLY; ARTIFACT-ONLY HANDOFF NOT IMPLEMENTED; CONTOUR A NOT PROVEN / BLOCKED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301

## 1. Refs and current review scope

- `main` HEAD: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.
- Canonical docs HEAD before this update: `f02d5b3366e75d3e6851b00e6d27b0c7851867d4`.
- PR #405 head: `59951fb247a6251b1693d5f0bc807c96480f7424`; open, Draft, unmerged; base `main`.
- PR #405 exact-head workflow runs returned by the commit-run query:
  - Astra Verify run `39377730257`: completed, SUCCESS.
  - Astra Cloud Runtime Validation run `39377730292`: completed, SUCCESS.
- The combined-status endpoint returned an empty status list for the PR head. This is not itself a passing result; the two named workflow runs above are the concrete evidence.
- PR #375, #388, #400, #401, #402, #403 and #404 are still open Draft/unmerged in the latest metadata read. Their state does not authorize integration.

## 2. What PR #405 changes — exact patch

PR #405 changes only:
- `.github/workflows/astra-distributed-local-worker.yml`: `permissions.contents` from `write` to `read`, and all three checkout steps from `persist-credentials: true` to `false`.
- `tests/test_distributed_local_worker.py`: a regression test asserts read-only workflow token permissions and exactly three non-persisting checkout steps.

It does **not** modify `ops/qualification/run_distributed_local_worker.py`.

## 3. Current worker source — read-back evidence

- Worker path: `ops/qualification/run_distributed_local_worker.py@main`.
- Blob SHA: `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`; read-back length 33,485 characters.
- Lines 664–680 still stage changes, create a Git commit, run `git push origin HEAD:refs/heads/{branch}`, then verify with `git ls-remote` and fail if push/remote SHA verification fails.
- In the reviewed worker file, task parsing is not equivalent to cryptographic issuer authorization. This source still has no integrated issuer signature, capability expiry/revocation, or replay validation path.
- Because the workflow change removes the standard checkout credential and reduces the job token to read-only, a direct push is expected to fail unless some other credential mechanism is available. The source review did not establish whether runner/host-level credentials exist. Do not assume the push is impossible merely because checkout persistence is disabled.

## 4. Security decision

PR #405 is a useful least-privilege mitigation and has two successful named checks on its exact head, but it is **not** an artifact-only worker/publisher implementation and is not sufficient evidence for Contour A qualification. Do not mark the publisher boundary resolved or merge solely from these checks.

Required follow-up:
1. Define/confirm the canonical task-envelope issuer, capability semantics, expiry, revocation, replay store, and cancellation/recovery contracts before binding the worker to an authority.
2. Remove worker-side Git add/commit/push from the execution path. Worker output should be a bounded artifact plus manifest (base SHA, allowed paths, modes, sizes, digests, task identity, provenance); the publisher must independently validate it.
3. Give only the trusted publisher write authority. Validate exact base SHA, manifest schema, digest, path allowlist, symlinks/traversal, modes/size, duplicate JSON keys, stale/replayed task IDs, signature and revocation. Reject by default.
4. Add negative tests for missing/forged/expired/revoked signatures, replay, base mismatch, modified digest, forbidden path, symlink/traversal, malformed manifest, and publication failure. Run checks on exact head and preserve Draft until independent review passes.
5. Verify whether any self-hosted runner or host-level SSH credentials can authenticate Git pushes; inspect credential sources without printing secret values.

## 5. Regional execution finding remains separate

GitHub App/API dispatch relocates the control-plane request; it does not make runner egress location disappear. A1/A2/A3 are configured with `runs-on: ubuntu-latest`, without a country pin or a fixed egress IP in workflow source. Provider eligibility and the actual egress route must be qualified from the runner, without trying to mask location or bypass provider restrictions. This regional question is separate from the worker/publisher trust boundary.

## 6. Disposition

- PR #405: useful hardening candidate; keep Draft pending full worker/publisher boundary and host credential review.
- A1/A2/A3: no new dispatch is claimed in this pass.
- Contour A: **NOT PROVEN / BLOCKED**.
- Contour B: remains gated on Contour A deployment and independent acceptance.

Related reports:
- [Wave 248 — worker/publisher boundary source review](MEDIAHUB-WORKER-PUBLISHER-BOUNDARY-SOURCE-REVIEW-WAVE-248-2026-10-20.md)
- [Wave 249 — GitHub-hosted runner regional boundary](MEDIAHUB-GITHUB-HOSTED-RUNNER-REGIONAL-BOUNDARY-WAVE-249-2026-10-20.md)
- [Wave 246 — Gemini dispatch credential scope](MEDIAHUB-GEMINI-DISPATCH-CREDENTIAL-SCOPE-REVIEW-WAVE-246-2026-10-20.md)
