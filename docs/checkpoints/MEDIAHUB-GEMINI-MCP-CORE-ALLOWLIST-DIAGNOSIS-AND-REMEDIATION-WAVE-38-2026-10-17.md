# MediaHub OS — Gemini MCP Core-Allowlist Diagnosis and Remediation, Wave 38

- Date: 2026-10-17
- Parent wave: [Wave 37 post-merge Gemini diagnostic and cloud-agent portability](MEDIAHUB-POST-MERGE-GEMINI-DIAGNOSTIC-AND-CLOUD-AGENT-PORTABILITY-WAVE-37-2026-10-17.md)
- Main SHA reviewed: `6c2e8dbdee81c798b64e65546e7ded07093f100a`
- Current Gemini workflow blob at review: `9be13613ae79f316ca410c16c6e69e2aea7283a4`
- Status: **SOURCE-BOUND ROOT-CAUSE MATCH / PR PROPOSED / PROVIDER RUNTIME ACCEPTANCE PENDING**

## 1. Decision

The latest failed Gemini dispatch matches a documented Gemini CLI policy interaction: the workflow config explicitly contains `"tools": { "core": [] }`, while CLI version `0.64.0` is requested. Gemini CLI issues [#28361](https://github.com/google-gemini/gemini-cli/issues/28361) and Google Action issue [#532](https://github.com/google-github-actions/run-gemini-cli/issues/532) describe how an explicitly configured empty core-tool allowlist creates a wildcard deny that also hides or excludes MCP tools from active tool declarations from CLI v0.41.0 onward. This produces tool-call attempts followed by `Tool "... " not found`, despite MCP discovery/registration logs.

The exact MediaHub configuration, tool-registration warnings, absent successful tool calls and final validation failure are consistent with this documented cause. The configuration-level cause is source-supported; runtime repair is awaiting CI/review and a separately authorized runtime acceptance event.

## 2. Exact current evidence

| Evidence | Observation |
|---|---|
| Main | `6c2e8dbdee81c798b64e65546e7ded07093f100a` |
| Workflow | `.github/workflows/gemini-autonomous-engineering.yml`, blob `9be13613ae79f316ca410c16c6e69e2aea7283a4` |
| Gemini dispatch | [Run 38977205621](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38977205621), conclusion `failure` in final action-result validator |
| Artifact | `gemini-output`, ID `12079328104`, size 1,714 bytes, digest `sha256:2411b20d32d6e68ce21f9bae75282416f101df55028e7b052fbb931a73e0854a` |
| Structured response | 3 model requests, 0 API errors, 2 tool calls, 0 successes, 2 failures; no branch, PR or commit |
| Failed calls | `mcp_github_get_me`; `mcp_github_get_file_contents`; both returned “Tool ... not found” |
| Astra Verify | [Run 38976598150, attempt 2](https://github.com/VlDMlNSh/mediahub-os/actions/runs/38976598150), completed `success`; all 11 steps passed |

This was a read of existing GitHub run evidence. No new model/provider call or Gemini workflow dispatch was initiated by this wave.

## 3. Proposed minimal source remediation

[PR #307 — allowlist GitHub MCP tools without enabling core tools](https://github.com/VlDMlNSh/mediahub-os/pull/307) changes only the `tools.core` allowlist:

```json
{
  "tools": {
    "core": ["mcp_github_*"]
  }
}
```

The actual workflow edit is one line:
- Removed: `"tools": { "core": [] }`
- Added: `"tools": { "core": ["mcp_github_*"] }`

This follows the workaround reported by upstream issue #28361. It permits the fully-qualified tools for the configured GitHub MCP server while keeping ordinary core tools outside the allowlist. Existing server-side `includeTools`, runner, token permissions, task prompt, validation step, model setting and PR-only workflow remain unchanged.

- Branch: `fix/gemini-mcp-core-allowlist-wave-38`
- Head commit: `5ae969763ff7ccbd22052efbd2661cf7bbdd7fd3`
- Workflow blob after read-back: `ed1ec965abc70041024afd4a1fc6ab17c6594fe7`
- PR base: `main` at `6c2e8dbdee81c798b64e65546e7ded07093f100a`
- PR status at creation: OPEN / UNMERGED

## 4. Adjacent upstream defect

The official Google Action copies its own `.github/commands/*` into the workspace. Current upstream copies include slash-command prompts with bare or stale MCP method names, as reported in [issue #510](https://github.com/google-github-actions/run-gemini-cli/issues/510). The direct MediaHub engineering prompt already specifies fully-qualified `mcp_github_*` names, so #510 is a second, adjacent hazard for tasks that invoke those copied slash commands. It is tracked separately from the current direct-prompt failure.

## 5. Safety and authority boundary

- Preserve server-side `includeTools` as the narrow API-operation allowlist.
- Preserve least-privilege GitHub job permissions, immutable source SHAs, sanitized artifacts, output validation, and PR-only promotion.
- Do not enable unbounded shell/file tools as a workaround.
- Treat all agent output as untrusted; successful execution, verification and qualification remain distinct.
- No credentials or raw secret values were accessed, and no workflow run was dispatched by this wave.
- No merge, release, deployment, infrastructure change, queue activation or agent promotion occurred.
- The existing 16-item activation queue remains documentary. A0 issuer/lifecycle, MH-12 credential-store contract, R-06 audit/privacy, accepted target manifest and independent fabric qualification remain open.

## 6. Acceptance checklist

1. Review PR #307 and require the normal CI checks.
2. Re-read the exact merged workflow revision only after an authorized merge decision.
3. For a separately authorized and eligible provider acceptance event, require: tools listed in the runtime registry; at least one successful read-only MCP call; valid structured response; artifact provenance; branch/PR result matching the task scope; no secret disclosure; and clear final status.
4. Add a negative-path check showing that non-allowlisted core tools remain unavailable.
5. Audit upstream copied slash-command prompt names as a separate, source-pinned change.

## 7. Sources

- Gemini CLI naming and discovery reference: https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md
- Gemini CLI core allowlist / MCP exclusion issue: https://github.com/google-gemini/gemini-cli/issues/28361
- Google Action issue reporting `tools.core: []` behavior: https://github.com/google-github-actions/run-gemini-cli/issues/532
- Google Action bundled prompt naming issue: https://github.com/google-github-actions/run-gemini-cli/issues/510
- GitHub secure use / immutable action pinning guidance: https://docs.github.com/en/actions/reference/security/secure-use

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
