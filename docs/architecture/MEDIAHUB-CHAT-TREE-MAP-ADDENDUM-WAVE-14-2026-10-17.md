# MediaHub OS — Chat Tree Map Addendum, Wave 14: Gemini MCP Recovery

- Date: 2026-10-17
- Status: remediation PR prepared; runtime re-execution pending.
- Main implementation PR: https://github.com/VlDMlNSh/mediahub-os/pull/303
- Diagnostic run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38972774167
- Diagnostic artifact: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38972774167/artifacts/12077208897
- Main-branch checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/fix/gemini-mcp-tooling-wave-14/docs/checkpoints/MEDIAHUB-GEMINI-MCP-RECOVERY-WAVE-14-2026-10-17.md
- Manual guide in remediation branch: https://github.com/VlDMlNSh/mediahub-os/blob/fix/gemini-mcp-tooling-wave-14/docs/checkpoints/MEDIAHUB-GEMINI-AUTONOMOUS-ENGINEERING-MANUAL-LAUNCH-WAVE-13-2026-10-17.md

## New project state

The first run of the new Gemini engineering workflow returned GitHub Actions success while the artifact recorded an empty model response, three failed tool calls, zero successful tool calls, zero changed lines, and a `MALFORMED_FUNCTION_CALL` API error.

The evidence-backed configuration mismatch: the GitHub MCP server instructs clients to call `get_me` first, but the previous `includeTools` list omitted `get_me`. The agent then attempted `update_topic`, which was unavailable in the configured tool set. The workflow also used `main` as its checkout while canonical project documents are maintained on `docs/mediahub-chat-tree-map-20261012`.

## Remediation proposal

The implementation PR adds the required `get_me` tool, restricts tool use to the configured allowlist, points canonical-document reads to the documentation ref, pins Gemini CLI to observed version `0.64.0`, reduces the session-turn budget, disables local telemetry artifact collection, and makes the workflow fail when the response is empty, tool operations all fail, or successful PR creation is absent.

## Queue protocol

The worker processes one bounded CAF queue item per dispatch and creates a PR. Continue with the next queue item after the previous result receives independent review. The queue is not advanced automatically by an unbounded self-triggering loop. Tests, qualification, runtime acceptance, merge, and deployment remain pending.

## Next step

Review implementation PR #303. After normal governance merges the remediation, dispatch a single CAF-Q-003 recovery task, inspect the new artifact and validator result, review the resulting PR, then continue to the next open CAF queue item.
