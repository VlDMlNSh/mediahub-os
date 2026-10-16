# MediaHub OS — Gemini Autonomous Engineering: Manual Launch and Recovery Guide

- Status: remediation proposed in Wave 14; runtime confirmation is pending.
- Contour: A — Developer Fabric only.
- Workflow: `.github/workflows/gemini-autonomous-engineering.yml`
- Official action: https://github.com/google-github-actions/run-gemini-cli
- Official GitHub MCP server: https://github.com/github/github-mcp-server
- Diagnostic run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38972774167
- Diagnostic artifact: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38972774167/artifacts/12077208897

## Incident finding

The diagnostic run reported GitHub Actions `completed/success`, while the Gemini artifact recorded an empty `response`, three failed tool calls, zero successful tool calls, zero changed lines, and a `MALFORMED_FUNCTION_CALL` API error. The action step's exit status alone therefore overstated task success.

The logs show the GitHub MCP server's startup instruction requested `get_me`, while the configured `includeTools` list excluded that tool. A later attempt called `update_topic`, which is absent from the allowlist. This is a concrete tool-discovery/configuration mismatch. The workflow remediation adds `get_me`, explicitly limits tool names, pins the observed Gemini CLI version, reduces the session-turn budget, disables local telemetry artifact collection, and adds a post-run gate that requires a non-empty response, at least one successful tool call, and successful PR creation.

## Prerequisites

1. GitHub Actions are enabled for the repository.
2. Repository secret `GEMINI_API_KEY` exists under **Settings → Secrets and variables → Actions → Secrets**. Keep its value private.
3. Optional repository variable `GEMINI_MODEL` contains a model ID supported by the account. The fallback remains `gemini-3.5-flash-lite`, which answered requests in the diagnostic run.
4. Repository and organization Actions policies allow the workflow's `contents: write` and `pull-requests: write` job permissions.
5. The remediation PR has been reviewed and merged into `main` before dispatching the revised workflow.

## Manual launch

The revised workflow must first be reviewed and merged into `main` through normal governance. Runtime behavior remains pending until a new run produces a non-empty response, passes the validator, and creates a reviewable PR.

1. Open https://github.com/VlDMlNSh/mediahub-os/actions/workflows/gemini-autonomous-engineering.yml
2. Select **Run workflow** and choose branch `main`.
3. Keep `base_ref=main` and `scope=contour-a`.
4. Enter one bounded task with concrete acceptance criteria and the CAF queue ID.
5. Click **Run workflow**.
6. Open the run summary and the `gemini-output` artifact.
7. Confirm the validator step passed, a dedicated branch and PR exist, and the PR contains source refs, exact files, rationale, known gaps, and pending verification.
8. Review and merge through the repository's independent governance process only.

## Suggested first recovery task

`Resume CAF-Q-003 as one bounded Contour A pass. Read the current canonical map, bootstrap instruction, Master Development Roadmap, latest continuation checkpoint, and primary sources. Reuse stable GitHub components. Identify the next evidence-backed remediation item, preserve historical IDs and Baseline 2.0 authority, make the smallest coherent change on a dedicated branch, and open a PR. State exact source paths/refs/SHAs and verification still pending. Stop before tests, qualification, merge, or deployment.`

## Queue operation

The workflow intentionally processes one bounded queue item per dispatch and creates a reviewable PR. Continue the CAF queue by dispatching the next explicitly identified item after reviewing the previous PR. A successful Actions status is necessary but insufficient: the validator must also pass, and the PR and artifact must be inspected. This design avoids an unbounded self-triggering loop and preserves independent review between queue items.

## Troubleshooting

- **Missing secret:** configure `GEMINI_API_KEY` as a repository Actions secret.
- **MCP `get_me` failure:** verify `get_me` remains in the server allowlist and inspect the artifact's `stderr.log`.
- **Malformed function call:** inspect `stdout.log` and `stderr.log`; keep the tool allowlist small and use only listed tool names.
- **No PR:** the new validator fails the job if PR creation has no successful tool record. Inspect the artifact before dispatching again.
- **Permission error:** review the repository/org Actions token policy and rulesets. Avoid widening permissions beyond the stated branch and PR operations.
- **Model/quota error:** inspect the run's error output and configured model; keep the API key private.

## Evidence and limits

- Diagnostic run `38972774167`: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38972774167
- Diagnostic artifact `12077208897`: https://github.com/VlDMlNSh/mediahub-os/actions/runs/38972774167/artifacts/12077208897
- The action and MCP server are existing upstream components; this remediation reuses them.
- Workflow source changes and documentation are implementation artifacts. Runtime behavior, successful PR creation, repeatability, qualification, and acceptance remain pending until a revised run produces evidence and is independently reviewed.
