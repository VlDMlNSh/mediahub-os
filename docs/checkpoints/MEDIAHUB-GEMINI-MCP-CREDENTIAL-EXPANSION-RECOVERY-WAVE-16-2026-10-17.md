# MediaHub OS — Gemini MCP Credential Expansion Recovery Wave 16

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: targeted configuration remediation prepared; runtime confirmation pending
- Diagnostic run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38976095754
- Diagnostic artifact: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38976095754/artifacts/12079316446
- Prior remediation: https://github.com/VlDMlNSh/mediahub-os/pull/305
- Workflow source: .github/workflows/gemini-autonomous-engineering.yml

## Evidence

The Wave 15 prompt update reached `main`, and the next dispatch still ended with an empty model response. The artifact records 3 failed tool calls, 0 successful calls, and `INVALID_STREAM`. The first attempted tool name was `mcp_github_get_me`; stderr reports `Tool "mcp_github_get_me" not found`.

The official Gemini CLI documentation specifies the `mcp_{serverName}_{toolName}` naming convention and confirms that MCP tools are discovered from the configured server: https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md

The workflow currently configures the GitHub MCP server environment with `"GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"`. A documented Gemini CLI issue describes MCP discovery failures involving sensitive environment-variable expansion and tokens being redacted: https://github.com/google-gemini/gemini-cli/issues/18302. The available artifact does not contain an explicit server-discovery diagnostic, so the credential-expansion failure is a leading evidence-supported hypothesis, rather than a proven runtime root cause.

## Change in this wave

- Keep the model-facing tool names in the documented `mcp_github_*` format.
- Pass the workflow-scoped `github.token` directly into the GitHub MCP server's explicit environment configuration, avoiding the intermediate `GITHUB_TOKEN` environment-variable expansion path.
- Preserve the existing `includeTools` allowlist and workflow permission boundaries.

## Verification and boundaries

- Inspected the failed run's job log and downloaded artifact.
- Confirmed the configured prompt and MCP environment mapping from the current `main` workflow.
- Change prepared on a dedicated branch and submitted for review.
- Runtime confirmation remains pending. No workflow rerun, tests, qualification, deployment, or acceptance are claimed.

## Acceptance criteria

1. MCP discovery exposes `mcp_github_get_me` and the other allowlisted tools.
2. At least one MCP call succeeds.
3. Gemini creates a reviewable PR for its bounded task.
4. The workflow validator passes with a non-empty response and successful PR creation.

## Next step

Review the proposed configuration change, then dispatch one bounded Contour A task and inspect the artifact plus workflow logs. If discovery still fails, capture explicit MCP server startup/discovery diagnostics before selecting another remediation.
