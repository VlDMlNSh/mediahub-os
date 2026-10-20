# Canonical map addendum — Wave 288 (2026-10-20)

## Reusable-workflow token permission ceiling

- **Report:** [Wave 288 permission-ceiling audit](../checkpoints/MEDIAHUB-GEMINI-REUSABLE-WORKFLOW-PERMISSION-CEILING-AUDIT-WAVE-288-2026-10-20.md).
- [Canonical project map](MEDIAHUB-CHAT-TREE-MAP.md); [continuation checkpoint](../checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md); [Master Roadmap](../checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md); [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- PR #421 remains OPEN / DRAFT / UNMERGED at head `3141a44370694d78f76779243adb548318a745d7`, base `80be45a70732b1d568164571d4273a6397792c3b`, 61 ahead / 0 behind. Submitted independent reviews: zero.
- Controller blob `da1d0254a993adcc224d5859a9a97bf609abd710` sets top-level `permissions: {}`; child jobs request `contents: write`, `pull-requests: write`, `issues: read` and pass `github.token` to GitHub MCP. Reusable workflows cannot elevate the caller token's permissions. The source contract therefore conflicts with the intended GitHub write operations; runtime behavior has not been tested.
- PR #426 is a separate draft negative-context probe at head `6caf55977260e808a055c8c4b9a04d68eb050d8c`; it does not prove the trusted positive caller path.
- **Disposition:** BLOCKED pending independent security review, least-privilege token design, and no-credential positive-context qualification. No dispatch, provider call, test, merge, deployment, or acceptance.
- **Next:** independently verify token-ceiling semantics and design the minimal permission model before editing or dispatching. Do not merge PR #421 and #426 together.
