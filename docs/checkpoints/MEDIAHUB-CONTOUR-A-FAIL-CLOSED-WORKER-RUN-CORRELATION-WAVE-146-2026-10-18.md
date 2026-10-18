# MediaHub OS — Fail-Closed Worker Run Correlation — Wave 146

Date: 2026-10-18
Repository: VlDMlNSh/mediahub-os
Status: IMPLEMENTED ON DRAFT PR; ASSOCIATED GITHUB WORKFLOW CHECKS SUCCESSFUL; NOT MERGED; CONTOUR A NOT QUALIFIED.

## Scope

A bounded fix for the run-correlation defect identified in Wave 144. It does not close the A0 signature/freshness/replay or evidence-provenance findings.

## Change

Draft PR #358: https://github.com/VlDMlNSh/mediahub-os/pull/358
Branch: `fix/wave-146-fail-closed-worker-run-correlation`
Base: `main` at `c06015e0b1526e0aaa6a522306052b077455aba5`
Latest observed PR head: `6206e4bcef5ad81262a4bd082230f52885ef599e`

Queue file:
- Path: `runtime/mediahub_runtime/autonomous_queue.py`
- Read-back blob SHA: `7ef01df586b3cb0f30c456025a0d543f2d2dd2b7`
- Changes: require a non-empty valid command ID before dispatch; capture dispatch start time; match exact workflow display title rather than substring fragments; reject stale/malformed run rows; fail closed if more than one exact fresh match exists.

Tests:
- Path: `tests/test_worker_run_correlation.py`
- Read-back blob SHA: `8f57133b7afe14415adf9a6e629cfae44316ae77`
- Seven test cases cover exact match, empty ID, substring collision, stale run, duplicate exact runs, invalid run ID, and unsupported executor.

## CI evidence

GitHub reports the following completed checks associated with commit `6206e4bcef5ad81262a4bd082230f52885ef599e`:
- Astra Cloud Runtime Validation — run 39116323624 — conclusion `success`: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39116323624
- Astra Verify — run 39116323626 — conclusion `success`: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39116323626

The connector confirms workflow-level success on the commit. This report does not claim that the individual new test module was independently run outside CI; CI logs/test selection should be checked before acceptance.

## Security limits remaining

- A workflow title is correlation metadata, not authorization.
- The queue path still needs explicit validation of the canonical A0 signed command envelope (HMAC, freshness, node/target binding and replay).
- Run selection must still bind to authoritative GitHub-derived workflow path, event, source ref/SHA, job/attempt and artifact digest.
- No real worker dispatch was performed for testing.
- PR remains draft, open and unmerged. No deployment or qualification state changed.

## Source review / read-back

The PR diff was inspected after creating the draft. The queue file and test file were re-read from the feature branch. An intermediate source-edit defect in the helper insertion was detected in the PR diff and corrected before the latest read-back; the final file no longer contains the duplicated function definition.

## Next step

Review CI logs and the new unit-test selection; then implement a separate bounded change for A0 envelope verification and authoritative run/artifact provenance. Do not merge PR #358 solely on green workflow status; require security review and branch protection.
