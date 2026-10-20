# MediaHub OS — Worker token mitigation compatibility gate (Wave 237)

- Date: 2026-10-20
- Status: **EXACT-HEAD CI GREEN; OPERATIONAL COMPATIBILITY GAP CONFIRMED; NOT QUALIFIED**
- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- PR under review: https://github.com/VlDMlNSh/mediahub-os/pull/405
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Live refs and checks

- `main` HEAD remains `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`.
- PR #405 remains OPEN/Draft, head `59951fb247a6251b1693d5f0bc807c96480f7424`, base main `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`, 2 commits ahead / 0 behind; GitHub reports mergeable but this is not a security approval.
- Exact-head Astra Verify run `39377730257` and Astra Cloud Runtime Validation run `39377730292` both completed SUCCESS. This proves those CI workflows passed, not that a live worker dispatch or publication path is qualified.
- Issue #301 remains OPEN. PR #388 (`815fa4af497a593f321ee692f64f53a12dcad061`) and PR #404 (`75ce935bd54003b63086bb990496cee1ddc96d3b`) remain OPEN/Draft.
- Wave 236 report blob `c4d8dc7c7ce9203c61fdf79cbb2eff995f7447a2`; continuation checkpoint blob before this update `b9978ca997f966c1d3fc0c9baa2520a0c5366826`.

## New compatibility finding

Re-read `ops/qualification/run_distributed_local_worker.py` at main, blob `dfa6bdfc5b2bd728f51ded9bd21b4de9db127cd1`. Lines 663–680:
1. `git add -A`
2. `git commit`
3. `git push origin HEAD:refs/heads/{branch}`
4. `git ls-remote` verifies the pushed ref and SHA.

Re-read PR #405 workflow `.github/workflows/astra-distributed-local-worker.yml`, blob `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`. It grants `contents: read` and sets `persist-credentials: false` on all three checkout steps. This correctly reduces token authority, but means the checkout token no longer provides credentials for the worker's direct push. Unless a self-hosted runner has another ambient Git/SSH credential, the current worker will fail at push verification. Ambient credentials have not been inspected, and no runtime dispatch was made. The new workflow test only asserts least-privilege settings; it does not test the full worker push behavior.

This is an explicit security/operability incompatibility, not a reason to restore write permissions. Keep PR #405 Draft and do not call the worker qualified.

## Actions recorded

- Added PR conversation comment `6284510831` documenting the direct-push compatibility gap and recommended artifact-only handoff.
- No worker was dispatched; no host, secret, provider credential, or external execution environment was accessed.
- No PR was merged, no deployment occurred, and no acceptance gate changed.

## Required next implementation slice

1. Refactor worker to produce a deterministic, content-addressed result/diff artifact only; remove worker-side `git push` and remote-ref verification.
2. Keep artifact upload as untrusted transport, not as authorization.
3. Add a separately authorized publisher that verifies accepted issuer/capability bindings, target SHA, task identity, artifact digest, replay/revocation state, cancellation and recovery semantics before any write.
4. Add negative tests for unsigned, wrong-target, altered, replayed, revoked and cancelled artifacts; test that the worker cannot publish directly.
5. Re-run exact-head CI, inspect effective runner credential sources without revealing values, then request independent security review.

Contour A remains **NOT_PROVEN / BLOCKED**; Contour B remains gated. The canonical map remains unmodified at blob `2187b4ca50792fe073f0979442c0f73432a2f6f9`. Connected Contents reads still return empty content for that blob; do not infer emptiness or perform a rewrite until the full blob/tree is obtained and verified via an alternate authorized Git Data API path.
