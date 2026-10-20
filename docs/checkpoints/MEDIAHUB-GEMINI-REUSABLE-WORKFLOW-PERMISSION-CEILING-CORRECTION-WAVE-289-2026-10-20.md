# MediaHub Contour A — correction to Wave 288 permission-ceiling finding (Wave 289)

**Date:** 2026-10-20  
**Status:** Corrective audit; source-level; no workflow dispatch, provider/model invocation, secret access, tests, merge, or deployment.

## Correction

Wave 288 incorrectly concluded that controller-level `permissions: {}` necessarily prevents child reusable workflows from receiving the explicitly requested token permissions. That conclusion was based on the workflow-level declaration alone and failed to account for permissions declared on the calling jobs.

The inspected controller `.github/workflows/gemini-batch-dispatch-controller.yml` has workflow-level `permissions: {}`, but each reusable-workflow calling job separately declares its own `permissions` block (including `contents: write`, `pull-requests: write`, and `issues: read`). In GitHub Actions, a job-level permissions declaration sets the token permissions for that job; for a reusable-workflow call, the caller job's permissions are the relevant upper bound passed to the called workflow. Thus the top-level empty map alone does **not** establish the claimed write-permission mismatch. The Wave 288 blocker must be withdrawn.

This correction does not prove the whole transport works. Remaining verification must inspect every actual caller job, every child job's permissions, repository/org Actions policy, secret availability, MCP token usage, and exact-head workflow evidence. The previously recorded caller-context probe failure remains a separate, unresolved fact; it cannot be attributed to this permissions claim without direct evidence.

## Current GitHub evidence

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- PR #421: https://github.com/VlDMlNSh/mediahub-os/pull/421 — OPEN / DRAFT / UNMERGED; head `3141a44370694d78f76779243adb548318a745d7`; base `80be45a70732b1d568164571d4273a6397792c3b`; independent submitted reviews: zero.
- PR #426: https://github.com/VlDMlNSh/mediahub-os/pull/426 — OPEN / DRAFT / UNMERGED; head `6caf55977260e808a055c8c4b9a04d68eb050d8c`.
- Issue #301 remains the governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Controller blob previously inspected: `da1d0254a993adcc224d5859a9a97bf609abd710`; reusable engineering child blob: `f67d62b721bcd8b86ef3a9491db5db2f50de6b1d`.
- Documentation branch head before this correction: `43e7800b7a90773c2755baab143998cd2c38ecf0`; verified tree SHA: `7a7012cfd310f888f20b98b8382f381306155392`.

## Disposition

**Wave 288 permission-ceiling conclusion withdrawn.** Do not treat the empty workflow-level permissions map as proof that child writes are denied. The controller architecture remains unqualified for independent reasons: PR #421 has no independent review, the actual trusted positive caller context is not established, and PR #426 covers only the negative-context path. No dispatch or provider/model call was performed during this corrective pass.

## Next bounded action

Perform a source-to-runtime permissions matrix for each controller job and called workflow, then inspect exact-head run records for the existing non-launching probe failure. Keep model/provider jobs unreachable. If source permissions are consistent, investigate the probe startup failure from its actual job/run evidence rather than assuming a token-ceiling cause. Keep PR #421 and #426 separate and unmerged pending review and governance gates.
