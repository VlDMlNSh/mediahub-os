# MediaHub Contour A — reusable-workflow permission ceiling audit (Wave 288)

**Date:** 2026-10-20  
**Class:** Read-only source, GitHub ref, PR metadata, and review-state audit. No dispatch, provider/model invocation, secret access, tests, merge, or deployment.

## Finding

The current PR #421 candidate configures the controller workflow with top-level `permissions: {}`, while each reusable child job requests `contents: write`, `pull-requests: write`, and `issues: read`. The child engineering jobs pass `github.token` to the GitHub MCP server and include write-capable tools such as branch/file/PR creation.

GitHub Actions reusable-workflow permission semantics make the caller's GITHUB_TOKEN permission set an upper bound: a called workflow cannot elevate permissions above the caller. Therefore the current controller's empty token permission ceiling conflicts with the intended write-capable child operations. Depending on the actual MCP implementation, the Gemini action may run but GitHub write operations through that token will be denied. This is a source-contract incompatibility, not proof of a live runtime failure; no workflow was dispatched to test it.

## Exact refs and evidence

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301 — OPEN.
- PR #421: https://github.com/VlDMlNSh/mediahub-os/pull/421 — OPEN / DRAFT / UNMERGED; head `3141a44370694d78f76779243adb548318a745d7`; base `80be45a70732b1d568164571d4273a6397792c3b`; 61 commits ahead / 0 behind; mergeable reported true; submitted review list is empty.
- Controller blob `.github/workflows/gemini-batch-dispatch-controller.yml`: `da1d0254a993adcc224d5859a9a97bf609abd710`. Top-level `permissions: {}`; three reusable jobs request write permissions.
- Child `.github/workflows/gemini-autonomous-engineering.yml`: `f67d62b721bcd8b86ef3a9491db5db2f50de6b1d`. Workflow-level permissions are `contents: read`; engineer job requests write capabilities and supplies `GITHUB_TOKEN: ${{ github.token }}` to GitHub MCP.
- Child source has immutable action/container pins and caller-context guard, but those protections do not change the GITHUB_TOKEN ceiling.
- PR #426: https://github.com/VlDMlNSh/mediahub-os/pull/426 — OPEN / DRAFT / UNMERGED; head `6caf55977260e808a055c8c4b9a04d68eb050d8c`; a non-launching negative-context probe only. It is not a positive trusted-controller runtime proof.
- PR #421 independent submitted reviews: zero. The latest Wave 287 CI evidence is tied to the same exact head, but CI success does not substitute for review or establish positive-path qualification.

## Disposition

**BLOCKED — permission ceiling and independent review remain unresolved.** Do not dispatch Gemini, merge, or claim qualification. Do not casually change the controller ceiling: any permission change must be reconciled with least privilege and the accepted authority contract.

## Next bounded action

Have an independent reviewer validate the reusable-workflow token-ceiling interpretation and propose the smallest least-privilege design. Candidate approaches should explicitly separate (a) a no-credential context probe, (b) any provider invocation, and (c) GitHub write authority. Verify the exact required permissions and secret/token route from source and platform semantics before changing the workflow. Then obtain positive trusted-controller context evidence with all model/provider jobs unreachable. Keep PR #421 and #426 separate and unmerged until review and governance gates are satisfied.

## Non-actions

No workflow dispatch or rerun; no Gemini/provider call; no secret/host access; no test execution; no merge/rebase/cherry-pick; no deployment, qualification, or acceptance.
