# Gemini Provider Outcome and Manifest Matrix — Wave 120

Date: 2026-10-18
Status: IMPLEMENTED / READ BACK / EXACT-HEAD CI PASS / INDEPENDENT REVIEW STILL REQUIRED

## Objective

Close the source-level gap identified in Waves 115–119: the HTTP response reader had executable coverage, but the two inline workflow handlers duplicated provider outcome and manifest finalization logic. This pass extracts that lifecycle into one shared, testable helper used by both workflows and adds a provider-outcome manifest matrix.

## Sources of truth and live refs

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap blob SHA read this pass: `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Canonical map blob SHA: `4798bd288451000d6eff5bcb8f7f0855942f7181` (1,048,405 characters; Contents API returned empty, so the blob API was used; map itself was not rewritten to avoid truncation).
- Canonical checkpoint blob SHA at the start of this documentation update: `acba9c24aa53a9e08ba351a8da4a43c993f63b1f`.
- Master Roadmap blob SHA: `462466162f23242e170cd1f25395e6c899b5ddc3`.
- Baseline 2.0 read from `main`, blob SHA `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f`.
- Governing [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN. It still separates implementation evidence from controlled dispatch, qualification and acceptance.

## Implementation

On [PR #334](https://github.com/VlDMlNSh/mediahub-os/pull/334), candidate HEAD `5f97db332e817169f9b138f3958e2db1c64086ad`:

1. Added `scripts/gemini_provider_outcome.js`, used by both primary and single-attempt retry workflows.
2. Added `scripts/test_gemini_provider_outcome.js`.
3. Updated `scripts/test_gemini_readonly_workflows.py` to execute the new matrix and assert workflow integration/path filters.
4. Updated `.github/workflows/gemini-readonly-workflow-validation.yml` so the new helper and test trigger contract CI on both `push.paths` and `pull_request.paths`.
5. Both workflows now use the shared helper to persist terminal outcomes; no automatic POST retry or provider/key fallback was added.

The executable matrix covers HTTP 429, HTTP 503, invalid JSON, empty output, over-limit output, transport failure, oversized transport response and successful output. Failure cases assert terminal `FAILED` manifest state, null output digest/byte count and no output artifact. Success asserts the exact output SHA-256 and byte count and retains the untrusted-advisory marker.

## Read-back blob SHAs

- `scripts/gemini_provider_outcome.js`: `e200943217d483eb6e41531a46a69de7f7ee9d53`.
- `scripts/test_gemini_provider_outcome.js`: `6ccb7ef38d91ffdb1e42ff41be1d694deeac16fc`.
- `scripts/test_gemini_readonly_workflows.py`: `f6acbdc6a05eae821b297df61be1aa16aad21fb1`.
- `.github/workflows/gemini-readonly-audit.yml`: `d95bd0086b22dab9be878bd469df2afccdc79c99`.
- `.github/workflows/gemini-readonly-audit-retry.yml`: `b581ccd6b6ee3dfd76908107b8884ac7c06ceb5d`.
- `.github/workflows/gemini-readonly-workflow-validation.yml`: `d031dfdff90e11fcd42f793cda33ce9dd038bdae`.

All changed source files were fetched again from GitHub after writing. Earlier exact-head CI attempts correctly caught stale source assertions after extraction; those assertions were updated, then the final exact-head run below passed.

## Exact-head CI evidence

All three runs correspond to candidate HEAD `5f97db332e817169f9b138f3958e2db1c64086ad`:

- [Gemini Read-only Workflow Contract #39073826467](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39073826467) — SUCCESS. Immutable checkout SHA verification, actionlint, and all Python security-contract tests passed, including the provider-outcome manifest matrix.
- [Astra Cloud Runtime Validation #39073826470](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39073826470) — SUCCESS.
- [Astra Verify #39073826473](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39073826473) — SUCCESS.

The combined commit-status endpoint returned an empty statuses array; the workflow run/job records above are the positive evidence.

## PR and branch disposition

PR #334 remains OPEN / DRAFT / UNMERGED. Latest live compare against `main` HEAD `c06015e0b1526e0aaa6a522306052b077455aba5` is DIVERGED, 63 ahead / 2 behind, merge base `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`. PR metadata says mergeable, but that does not establish lossless reconciliation or satisfy protection/independent-review gates.

A source-bound COMMENT review was recorded against exact HEAD (review ID `5560323518`). It is explicitly not independent approval.

## Safety and remaining gates

No Gemini provider call, secret read, manual workflow dispatch, queue admission, merge, deployment or Contour A acceptance occurred. The source/test pass does not qualify provider access or autonomous dispatch. A0 issuer/verifier/ingress/lease/cancel/recovery, R-06 audit/privacy authority, accepted runner/workspace/network target manifest, independent schema/authority review and queue qualification remain open under Issue #301.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT PRODUCTION-ACCEPTED**.

## Next bounded action

Obtain independent security review of the exact diff. Then reconcile the 63-ahead / 2-behind branch against live `main` without losing changes, re-read the resulting diff and rerun all required checks on the new exact SHA. Keep PR #334 Draft until those gates pass.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
