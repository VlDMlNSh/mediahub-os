# MediaHub OS — Wave 85: CI closeout and dependency-lock decision

- Date: 2026-10-17
- Status: **FINAL-HEAD CI VERIFIED; LOCKFILE NOT YET IMPLEMENTED; PR REMAINS DRAFT**
- PR: https://github.com/VlDMlNSh/mediahub-os/pull/337
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## 1. Fresh evidence

- PR #337 live snapshot at the Wave 85 write: open, Draft, unmerged, GitHub reported mergeable=true; head observed as `96963cb2701021d7eda85285d9bad1f2f42fa080`. This was the PR snapshot before the Wave 85 report commit.
- PR base: `docs/mediahub-chat-tree-map-20261012`, base SHA `8083cd61dbe348e18ab7db3e09b2769529bdcfda`.
- Fresh compare against the actual PR base on the subsequent Wave 86 check: **18 commits ahead / 18 behind**, status `diverged`, merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`. This supersedes the earlier 17-ahead count. Do not equate this count with divergence against `main`.
- `main` HEAD observed as `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`; a previous branch API read reported `protected=false`.
- PR review endpoint returned an empty array: no submitted review is recorded.
- Final-head run https://github.com/VlDMlNSh/mediahub-os/actions/runs/39043810272 is `completed / success`, job `117428432389`. The schema validation step, including positive and negative fixtures, completed successfully.
- Wave 85 report commit `7776c02ae54f712ba0da4ee7a38e11d0293475d9` triggered run https://github.com/VlDMlNSh/mediahub-os/actions/runs/39044943058, which completed `success`; job `117431696468`, including schema validation, succeeded.
- Workflow file: `.github/workflows/cloud-agent-schema-validation.yml`; read-back blob SHA observed before the report-only commits: `c0bca0c1994e9888b223c316f1bc3e7b50f5097e`.
- Wave 85 report blob SHA before this correction: `0169143a3f7240e650aaf979bef9c6f391ecef6d`.

## 2. Interpretation

The CI result verifies that the tested workflow revision ran its current validation checks successfully. It does not demonstrate exhaustive schema mutation coverage, production admission behavior, independent review, qualification, deployment, or Contour A acceptance.

The dependency install still resolves `jsonschema[format]==4.23.0` with transitive versions selected at install time. Exact pinning of the top-level package is not a complete dependency lock. `pip freeze` is not a reliable lock-generation strategy by itself because its output depends on the environment from which it is collected.

## 3. Dependency-lock decision

Do not hand-author transitive pins from memory and do not label a generated environment snapshot as a portable lock. The next implementation should:

1. Declare the sole direct requirement `jsonschema[format]==4.23.0` in a dedicated input file.
2. Select a pinned, maintained lock generator (for example, `pip-tools`) and pin its own version in the generation environment.
3. Generate a complete transitive lock with hashes in a clean Python 3.12 environment matching the workflow runner; review environment markers and platform-specific distributions.
4. Change CI to install from the checked-in hash-verified lock with `pip install --require-hashes -r <lockfile>`.
5. Verify a clean install and the existing schema/fixture suite on a fresh workflow run. Keep the generator input and generated lock together and document the deliberate regeneration procedure.

This report does not claim that a lockfile has been created or that dependency installation is hermetic.

## 4. Integration and qualification gates

- Do not merge PR #337: it remains Draft, has no independent review, and diverges from its base (18 ahead / 18 behind at the latest compare).
- Resolve branch history only after a file-level comparison and preservation check; do not rebase/merge solely to reduce the ahead/behind count.
- Main branch protection was reported disabled by the branch API; recheck before any future integration.
- Issue #301 gates remain open: A0 issuer/verifier lifecycle, R-06 audit/privacy authority, accepted runner/workspace/network manifest, independent schema review, and qualification of the bounded read-only worker/queue path.
- No provider invocation, credential access, dispatch, deployment, or Contour B work is authorized by this validation result.

## 5. Read-back / source integrity limitation

The canonical map was successfully retrieved by its Git blob SHA `e1eb74740b2429b10a6025fcb1a8289f5958316d`; the Contents API wrapper had returned an empty body. The map identifies itself as an inventory, not full acceptance. This wave does not modify the canonical map or checkpoint. The report is an evidence record on the PR branch only, not canonical acceptance.

## 6. Next step

Implement the lock in a bounded follow-up on this branch, using a pinned lock generator in a clean Python 3.12 environment, then verify hash-checked installation and the existing fixtures. Separately obtain independent review and perform a deliberate file-level reconciliation with the documentation base before considering promotion.
