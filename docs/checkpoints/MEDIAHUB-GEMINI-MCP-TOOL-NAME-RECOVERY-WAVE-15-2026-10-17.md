# MediaHub OS — Gemini MCP Tool Name Recovery Wave 15

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: prompt/tool-name remediation prepared; runtime rerun pending
- Diagnostic run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38975571838
- Diagnostic artifact: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38975571838/artifacts/12079250907
- Workflow source: .github/workflows/gemini-autonomous-engineering.yml
- Parent workflow commit: 99e7c0598bdc2f69201958aeb983f64c04504990

## Evidence

The workflow validator failed with `Gemini returned an empty response`. Inspection of artifact `gemini-output` established:
- `response` was empty.
- Gemini CLI recorded 3 failed tool calls and 0 successful tool calls.
- The attempted names were `get_me`, `github:get_me`, and `github:github__get_me`.
- `stderr.log` reported `Tool "get_me" not found`, followed by equivalent failures for the two aliases.
- The Gemini CLI startup output registered tools with names such as `mcp_github_get_me`, `mcp_github_create_branch`, and `mcp_github_create_or_update_file`.
- The model stream ended with `INVALID_STREAM: Model stream ended with malformed function call`.

This is a second, more specific naming mismatch after the Wave 14 allowlist change: the MCP server allowlist uses server-side names, while Gemini CLI exposes registered tools with the `mcp_github_` prefix. The prompt used server-side names when directing the model how to invoke tools.

## Remediation in this change

Update the workflow prompt to call the exact Gemini CLI-registered names:
- `mcp_github_get_me`
- `mcp_github_get_file_contents`
- `mcp_github_search_code`
- `mcp_github_list_commits`
- `mcp_github_create_branch`
- `mcp_github_create_or_update_file`
- `mcp_github_create_pull_request`
- `mcp_github_list_pull_requests`
- `mcp_github_search_pull_requests`
- `mcp_github_issue_read`
- `mcp_github_search_issues`

The MCP server-side `includeTools` values remain unchanged because those are names used by the upstream server configuration. This change corrects the model-facing invocation contract.

## Verification and boundaries

- Artifact and workflow logs inspected.
- Workflow change written to a dedicated branch and read-back verification pending.
- No workflow rerun, tests, qualification, merge, deployment, or acceptance performed.
- Runtime confirmation requires a new dispatch and a successful tool call followed by PR creation and validator success.

## Next step

Review and merge the remediation PR through repository governance. Dispatch one bounded CAF-Q-003 task and inspect the artifact. Continue the queue only after a reviewable PR and its evidence exist.
