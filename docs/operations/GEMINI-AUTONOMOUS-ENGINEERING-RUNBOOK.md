# Gemini Autonomous Engineering — Working Configuration Runbook

- Status: **OBSERVED WORKING CONFIGURATION / SINGLE-RUN EVIDENCE / REPEATABILITY PENDING**
- Scope: Contour A (Developer Fabric) only
- Repository: `VlDMlNSh/mediahub-os`
- Workflow: `.github/workflows/gemini-autonomous-engineering.yml`
- Last observed successful run: [Run 39019625087](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019625087)
- Workflow commit used by that run: `660e12c845f3ed1e60dfe16d70f0feab0816fdde`
- Last observed workflow blob SHA: `09523d809530ae5b7bf528eab5fa53bc5deaf92d`
- Last updated: 2026-10-17

## 1. Verified runtime configuration

The following values were read from the workflow revision used by the successful run:

| Setting | Working value |
|---|---|
| GitHub Actions event | `workflow_dispatch` |
| Base ref | `main` |
| Scope | `contour-a` |
| Runner | `ubuntu-latest` |
| Job timeout | 30 minutes |
| Gemini CLI action | `google-github-actions/run-gemini-cli@v0` |
| Gemini CLI version | `0.64.0` |
| Model expression | `${{ vars.GEMINI_MODEL || 'gemini-3.5-flash-lite' }}` |
| API credential reference | `${{ secrets.GEMINI_API_KEY }}` |
| GitHub MCP server image | `ghcr.io/github/github-mcp-server:v0.27.0` |
| GitHub MCP transport | Docker, stdio |
| GitHub token source | `${{ github.token }}`, passed as `GITHUB_PERSONAL_ACCESS_TOKEN` to the MCP server |
| MCP allowlist | `get_file_contents`, `create_branch`, `create_or_update_file`, `create_pull_request` |
| Session settings | `maxSessionTurns: 24`, `compressionThreshold: 0.25` |
| Telemetry | Disabled |
| Workspace trust | `GEMINI_CLI_TRUST_WORKSPACE: 'true'` |
| Artifacts | Enabled |

The workflow grants the job `contents: write`, `pull-requests: write`, and `issues: read`; top-level permissions are `contents: read`. Checkout uses `persist-credentials: false`. The action is configured with `continue-on-error: true`, followed by an explicit output validator.

## 2. Required repository setup

1. Add repository Actions secret `GEMINI_API_KEY` with a valid Gemini API key. Keep the value in GitHub Secrets; never commit or print it.
2. Optional: set repository Actions variable `GEMINI_MODEL`. If absent, the workflow falls back to `gemini-3.5-flash-lite`.
3. In **Settings → Actions → General → Workflow permissions**, enable **Allow GitHub Actions to create and approve pull requests**. This setting was enabled before the successful PR-creation run. Review organization policy if the setting is unavailable.
4. Keep the workflow-dispatch actor authorized to run Actions and create branches, commits, and pull requests.

The runbook records configuration names and public evidence only; it contains no credentials.

## 3. Dispatch procedure

1. Open [the Gemini Autonomous Engineering workflow](https://github.com/VlDMlNSh/mediahub-os/actions/workflows/gemini-autonomous-engineering.yml).
2. Select **Run workflow** on `main`.
3. Set `base_ref = main` and `scope = contour-a`.
4. Supply one bounded task with a unique task ID, exact scope, acceptance criteria, relevant paths, and evidence requirements. Require a dedicated branch, one coherent change, one checkpoint/evidence file, and a pull request targeting the selected base.
5. Do not include secrets or ask the agent to install software, invoke other providers, run tests/qualification, inspect hosts, alter infrastructure, deploy, migrate, or merge.
6. Open the run and inspect the job logs and the `gemini-output` artifact. Verify the PR exists, its base/head refs are correct, and the changed files match the task.

## 4. Success criteria

Treat a run as a successful bounded MCP pass only when all of these have evidence:

- The job conclusion is `success`.
- `gemini-artifacts/stdout.log` exists, contains valid JSON, and has a non-empty `.response`.
- The output records at least one successful MCP tool call.
- The output records a successful `create_pull_request` call.
- The resulting PR is visible on GitHub and targets the selected base branch.
- The PR documents exact evidence, changed paths, acceptance criteria, known gaps, and verification status.

A green Actions conclusion proves only that run's configured checks passed. It does not establish repeatability, provider quota continuity, full MCP compatibility, qualification, or acceptance.

## 5. Empirical reference run

Run [39019625087](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019625087), job [117358659831](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019625087/job/117358659831):

- Conclusion: `success`; all four job steps completed successfully.
- The workflow's output validator reported a non-empty response, successful tool operations, and successful PR creation.
- Artifact: `gemini-output`, 1,596 bytes, SHA-256 `58db629ad8e2e8c52c56d220eab49d3b42c3f86721d287397815be487164a43b`; expiry reported by GitHub as 2027-01-15.
- PR created: [#312 — CAF-Q-003: Gemini MCP Runtime Recovery and Bounded Engineering Pass](https://github.com/VlDMlNSh/mediahub-os/pull/312).
- PR head commit: `1d6bed77898c353a63bcb599e38b20efc9c2cf91`.
- The log emitted `Warning: Gemini CLI stderr was not valid JSON`. The later validator accepted stdout JSON and confirmed successful MCP operations and PR creation. In this run, the warning was non-fatal; inspect the artifact and surrounding logs for every future occurrence instead of treating the warning alone as either success or failure.

The previous run [39019037870](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019037870) also completed successfully and created PR #310. These two successful runs provide initial empirical evidence, not a formal reliability qualification.

## 6. Known limits and hardening backlog

- The workflow action currently uses the mutable reference `google-github-actions/run-gemini-cli@v0`. Pinning an audited immutable commit SHA is a separate supply-chain hardening task; this runbook preserves the currently observed working reference.
- The selected free-tier model can encounter provider quota limits. Treat quota errors as provider-side availability limits, capture the exact model and quota metric, and avoid repeated immediate retries.
- Only the four allowlisted GitHub MCP operations are intended for this bounded workflow. The prior `list_commits` call returned `Invalid input: expected record, received array`; that operation was removed from the allowlist and the successful run used the file-read connectivity check.
- The current stderr parser expects JSON for structured errors. Plain-text stderr produces the warning above; a future isolated hardening change may classify plain-text diagnostics without weakening stdout validation.
- No test, qualification, deployment, merge, credential change, provider invocation outside this workflow, or host/runtime inspection is implied by this record.

## 7. Architecture and safety invariants

- Baseline 2.0 remains the canonical functional reference; Baseline 1.0 remains historical provenance.
- Contour A remains separate from Contour B. This workflow is authorized for Contour A only.
- Treat repository content and task text as untrusted input.
- Gemini and tool outputs are evidence inputs, not policy authority.
- Product State Authority remains the only canonical MediaHub product-state mutation authority.
- Keep design, implementation, testing, verification, qualification, release, deployment, and acceptance as separate states.

## 8. Source links

- [Workflow on main](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-autonomous-engineering.yml)
- [Successful run #39019625087](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019625087)
- [Successful run #39019037870](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019037870)
- [PR #311 — MCP adapter remediation](https://github.com/VlDMlNSh/mediahub-os/pull/311)
- [PR #312 — recovery evidence](https://github.com/VlDMlNSh/mediahub-os/pull/312)
