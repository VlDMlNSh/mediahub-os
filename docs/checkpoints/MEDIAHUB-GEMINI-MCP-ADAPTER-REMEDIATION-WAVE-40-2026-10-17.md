# Gemini MCP Adapter Remediation — Wave 40

- Date: 2026-10-17
- Status: **PROPOSED / STATIC READ-BACK VERIFIED / RUNTIME RE-DISPATCH PENDING**
- Contour: A (Developer Fabric)
- Related successful run: [39019037870](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019037870)
- Related job: [117356960181](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019037870/job/117356960181)
- Evidence PR: [#310](https://github.com/VlDMlNSh/mediahub-os/pull/310)
- Remediation PR: [#311](https://github.com/VlDMlNSh/mediahub-os/pull/311)
- Proposed branch: `fix/gemini-mcp-remove-list-commits-wave-40`
- Proposed head after final edit: `f4bcc4d0bf137445ff413ae27ccd39b2d0f3f262`

## Confirmed findings

1. Run 39019037870 completed successfully, passed the workflow's output validator, and created PR #310.
2. `mcp_github_list_commits` failed with `Invalid input: expected record, received array`.
3. File retrieval, branch creation, file creation/update, and PR creation succeeded in that run.
4. PR #310's recovery evidence was corrected to record successful PR creation and distinguish one-run success from durable repeatability.
5. The workflow currently uses `google-github-actions/run-gemini-cli@v0`, Gemini CLI `0.64.0`, GitHub MCP server `v0.27.0`, and a configurable Gemini model defaulting to `gemini-3.5-flash-lite`.

## Proposed remediation

- Remove `list_commits` from the configured MCP tool allowlist.
- Begin with the proven `get_file_contents` operation reading `GEMINI.md` from `main`.
- Keep the allowlist to four operations required for the bounded flow: `get_file_contents`, `create_branch`, `create_or_update_file`, `create_pull_request`.
- Preserve fail-closed output validation, artifact upload, and the existing Contour A-only scope.

## Verification and limits

- Workflow content was read back from the remediation branch after edits; the allowlist has valid comma placement and excludes `list_commits`.
- Evidence file in PR #310 was read back with successful PR creation status.
- No workflow dispatch or tests were run for the proposed change. The runtime acceptance gate remains open pending owner-triggered dispatch after PR review/merge.
- Free-tier quota remains provider-controlled. One successful run does not establish sustainable quota, guaranteed availability, or multi-run reliability.
- The mutable `@v0` action reference remains a separate supply-chain hardening item. Pinning it requires a source-bound review of the official action and its transitive behavior.

## Next step

Review PR #311. After authorized merge, manually dispatch the workflow from `main` with a bounded Contour A task. Verify the initial file-read tool call, successful PR creation, artifact contents, and exact output validator result. Record a second successful run before claiming repeatable operation.

No merge, deployment, tests, provider invocation, installation, qualification, credential modification, host/runtime inspection, or infrastructure change was performed as part of this documentation pass.
