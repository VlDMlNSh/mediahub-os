# MediaHub OS — project map addendum, Wave 188 (2026-10-19)

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](MEDIAHUB-CHAT-TREE-MAP.md)
- Wave 188 report: [Gemini workflow token-authority review](../checkpoints/MEDIAHUB-CONTOUR-A-GEMINI-WORKFLOW-TOKEN-AUTHORITY-REVIEW-WAVE-188-2026-10-19.md)
- Previous checkpoint: [Wave 187](../checkpoints/MEDIAHUB-NEXT-CONTINUATION-CHECKPOINT-WAVE-187-2026-10-19.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

Wave 188 identified a design-level authority gap in all three Gemini workflows. Although the configured MCP tool list is limited to branch creation, file create/update, PR creation, and file reading, the job token has repository-level `contents: write` and `pull-requests: write`. Prompts request a dedicated branch and documentation-only work, but the inspected workflow itself does not enforce a branch namespace, fixed ref/path allowlist, or post-run validation of PR base and changed paths. No exploit or direct write was observed; workflows were not dispatched, and branch-protection rules were not audited.

This is a proposal for governance/change control, not an accepted contract. Proposed direction: broker writes through a server-side constrained path/ref allowlist; validate PR base, branch, and changed paths; reduce token authority; and resolve immutable action/image provenance before dispatch. Main HEAD remains `c06015e0b1526e0aaa6a522306052b077455aba5`. PR #374/#375/#376 remain Draft; SentinelX has zero connected hosts; Codex Tasks has no registered environments.

No workflow or permission was changed. No Gemini dispatch, secret read, host command, manual test, merge, deployment, or qualification occurred. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**.
