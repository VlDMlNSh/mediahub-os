# Wave 472 — strengthen PR review child contract tests (2026-10-29)

## Status

- Change: **COMMITTED on draft PR #588**, not merged.
- Exact-head CI for `11074b6240361b2943643922d49417bee9601262`: Astra Verify `40844640479` and Astra Cloud Runtime Validation `40844640409` completed **SUCCESS**. The check-runs API returned only 2 contexts total, so the other Ruleset-required contexts remain **NOT VERIFIED** and the complete required set is not established.
- Independent review: **NOT VERIFIED**; no formal review submissions or inline threads were returned on latest check.
- Controller integration: **NOT IMPLEMENTED**. Do not manually dispatch the child workflow.
- Contour A: **NOT ACCEPTED**. Contour B: **GATED**.

## Immutable refs

- `main`: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- PR #588 head: `11074b6240361b2943643922d49417bee9601262`.
- Workflow blob SHA: `85174e24b7d213ce7d90a4bd215ec4fbac32c605`.
- Test blob SHA: `3ac7428a3054334842f4774f1fee3f49027cf51a`.
- Branch compare: `feat/pr-scoped-readonly-review-wave471` is ahead 5, behind 0; changes remain isolated from `main`.

## Work in this pass

Extended `tests/test_gemini_pr_readonly_review_wave471_contract.py` with checks that authorization is a dependency of the review job, the model API key is not exposed to the authorization job, missing HMAC fails closed, external actions are pinned to full commit SHAs, and jobs do not grant write permissions or persist checkout credentials.

The previous static test suite had already caught and corrected an over-broad assertion. The newly added checks have been committed, but exact-head CI is queued, so they have not yet been proven by CI. These are static structural assertions, not behavioral tests of HMAC/API/dispatch handling.

## Required-checks gate revalidated

The active repository ruleset `MediaHub-main-autonomous-merge` (`26108066`) requires these five exact status contexts: `Astra Cloud Runtime Validation`, `AI Factory verification`, `provider contract verification`, `Astra Verify`, and `Gemini workflow contract validation (Wave 284)`. For exact PR head `11074b6240361b2943643922d49417bee9601262`, the GitHub check-runs endpoint returned only two checks: `verify` and `validate`, both SUCCESS. The classic commit status endpoint reports `pending` with zero legacy statuses. Therefore the five named required contexts are **not demonstrated on this exact head** and the full required-check gate is **NOT VERIFIED**. Do not merge or mark ready for merge.

## Remaining blockers

1. Wait for exact-head CI and inspect any failure logs; do not call full CI green until all required Ruleset contexts are confirmed.
2. Add behavioral tests for malformed PR numbers, invalid HMAC, wrong/changed base and head SHA, duplicate request/idempotency, missing secret, inaccessible PR, and rejected/ambiguous dispatch.
3. Implement a bounded controller path that fetches the open PR, verifies `base=main` and exact immutable base/head SHAs, signs the PR-specific payload with `MEDIAHUB_DISPATCH_HMAC_KEY`, and dispatches only the dedicated child. Reconcile duplicate and ambiguous dispatch outcomes; preserve owner-only bridge and fail-closed gates.
4. Obtain independent review before enabling any dispatch route.

No child workflow was dispatched, no agent was launched, no secret was read, and no merge/deployment/qualification occurred in this pass.

## Links

- PR #588: https://github.com/VlDMlNSh/mediahub-os/pull/588
- Issue #301 report: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
