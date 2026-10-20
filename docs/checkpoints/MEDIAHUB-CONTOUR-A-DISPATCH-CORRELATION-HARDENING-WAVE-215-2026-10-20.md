# MediaHub OS Contour A — Dispatch correlation hardening (Wave 215)

Date: 2026-10-20

## Status

Implemented a narrow hardening change to the proposed GitHub Actions batch controller and verified the saved file by GitHub Contents API read-back. This is source-level verification only. No workflow dispatch was initiated; no new run IDs, artifacts, or agent PRs were produced. No merge, deployment, qualification, or acceptance is claimed.

## Canonical references

- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Current continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Controller PR: https://github.com/VlDMlNSh/mediahub-os/pull/408

## Evidence

- Main HEAD used for comparison: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`
- Controller branch: `feat/contour-a-gemini-github-dispatch-controller-wave-213-2026-10-20`
- Controller update commit: `a1ad2b003909289a57a08ecdc56a1bb864948c82`
- Controller blob SHA after read-back: `cb75ca90467775eafb8766fe3bba8871bfcff934`
- Branch comparison after changes: 7 commits ahead, 0 behind `main`.
- Wave 214 credential gate report blob after update: `02f82f0de76a0a7d7402ba9bd99636c53ba42476`
- Canonical map Contents API response was empty despite a known blob SHA; this is treated as a connector/read limitation, not an empty map. No canonical map mutation was attempted.

## Change

Before dispatch, the controller now snapshots the latest run ID for each of the three child workflows. The monitor filters for `workflow_dispatch` runs on `main` created after the batch start and with IDs greater than the per-workflow baseline. If more than one candidate is visible, it fails closed instead of selecting the newest and risking false correlation.

This narrows the identified race but does not establish an immutable correlation token. A concurrent dispatch can still cause the controller to fail closed, which is preferable to silently recording the wrong run.

## Not yet verified

- YAML parser / actionlint result: NOT RUN.
- GitHub Actions CI for this controller: NOT VERIFIED.
- Actual controller invocation: NOT RUN.
- Current validity of user-reported GitHub API secrets: NOT VERIFIED; values were not accessed.
- New Gemini run IDs, artifacts, or Draft PRs: NONE from this wave.
- Prior successful runs remain historical evidence only.

## Next action

Run a suitable static workflow linter and review the complete diff. Then, subject to repository protections and review gates, integrate the controller and execute one controlled batch. Verify the controller run, all three exact child run IDs and conclusions, job steps, artifacts, and agent Draft PRs. Never auto-merge agent output.

Contour A remains NOT_PROVEN / BLOCKED pending the project's required deployment and independent acceptance gates.
