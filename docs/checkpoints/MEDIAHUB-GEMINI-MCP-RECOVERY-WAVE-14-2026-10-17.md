# MediaHub OS — Gemini MCP Recovery Wave 14

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: remediation prepared in PR; runtime re-execution pending
- Diagnostic run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38972774167
- Diagnostic artifact: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38972774167/artifacts/12077208897
- Workflow under remediation: `.github/workflows/gemini-autonomous-engineering.yml`
- Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Evidence-backed diagnosis

The run's GitHub Actions job concluded `success`, but the downloaded artifact recorded:
- `response: ""`
- 8 model requests, one `MALFORMED_FUNCTION_CALL` API error
- 3 tool calls, 0 successful and 3 failed
- 0 added lines and 0 removed lines

The MCP server's startup instruction requires `get_me` first. The workflow's previous `includeTools` list omitted `get_me`, creating a mismatch between server instructions and the visible tool set. The model subsequently attempted `update_topic`, which is absent from the configured allowlist. The official action did not convert the empty response/tool failure into a failed job.

A second source-of-truth mismatch was identified: canonical project documents live on ref `docs/mediahub-chat-tree-map-20261012`, while the engineering workflow checks out `main`. The prompt previously asked the agent to read canonical docs without telling it to use the documentation ref.

## Remediation included in the proposed change

1. Add `get_me` to the GitHub MCP allowlist and state the complete permitted tool-name set.
2. Instruct the agent to read Bootstrap, Project Map, Master Roadmap, and continuation checkpoint from `docs/mediahub-chat-tree-map-20261012`; implementation sources and new branches use `main`.
3. Pin Gemini CLI to observed version `0.64.0` for repeatability.
4. Reduce max session turns from 30 to 16.
5. Disable local telemetry file collection so the uploaded artifact omits telemetry logs.
6. Add a validator requiring a parseable JSON artifact, non-empty response, at least one successful tool operation, and a successful `create_pull_request` operation. A workflow run with empty output or no PR should now fail visibly.

## Boundaries

- No merge or deployment performed.
- No tests or qualification run.
- No API key value or other secret read.
- The new configuration has not yet been executed; runtime behavior and acceptance remain pending.
- Queue processing remains one bounded CAF item per dispatch. Each PR requires independent review before the next queue item is accepted as completed.

## Next step

Review and merge the remediation PR through normal governance. Then dispatch one bounded CAF-Q-003 recovery pass, inspect the artifact and validator result, and continue with the next queue item only after reviewing the resulting PR.
