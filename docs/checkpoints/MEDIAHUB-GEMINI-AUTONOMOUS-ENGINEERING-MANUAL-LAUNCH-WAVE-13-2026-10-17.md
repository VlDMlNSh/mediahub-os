# MediaHub OS — Gemini Autonomous Engineering: Manual Launch Guide

- Status: proposed workflow component; activation and execution require repository-side review and the first manual run.
- Contour: A — Developer Fabric only.
- Workflow: `.github/workflows/gemini-autonomous-engineering.yml`
- Official action: https://github.com/google-github-actions/run-gemini-cli
- GitHub MCP server: https://github.com/github/github-mcp-server

## What this adds

A manually dispatched, bounded Gemini engineering worker using the official Google Gemini CLI GitHub Action and GitHub MCP tools. It receives one explicit task, reads the project’s authoritative documents, creates a dedicated branch, applies a scoped change through GitHub tools, and opens a Pull Request. It has no automatic issue/comment trigger, no schedule, and no merge/deploy step.

This is autonomy for task execution and PR preparation, not an always-running daemon. GitHub Actions is the execution infrastructure; the MediaHub application servers are not on the request path for Gemini API calls.

## Prerequisites

1. Repository Actions are enabled.
2. `Settings → Secrets and variables → Actions` contains repository secret `GEMINI_API_KEY`. Reuse the existing secret if present; never paste its value into a workflow, issue, or chat.
3. Optional repository variable `GEMINI_MODEL` contains a model ID supported by the account. If absent, the official action selects its default model.
4. Repository Actions permissions permit the workflow's job-level `contents: write` and `pull-requests: write` grants. Organization policy may restrict these permissions.
5. The workflow is present on the default branch before the first manual launch.

The workflow grants write access only to the task's GitHub Actions token for branch/file/PR operations. It does not grant repository administration, secret management, merge, deployment, or infrastructure permissions. Review repository rulesets and Actions policy before enabling it.

## Manual launch

1. Open https://github.com/VlDMlNSh/mediahub-os/actions/workflows/gemini-autonomous-engineering.yml
2. Select **Run workflow**.
3. Select branch `main` as the workflow ref.
4. Keep `base_ref` set to `main` and `scope` set to `contour-a`.
5. Enter one bounded task with concrete acceptance criteria and relevant MediaHub IDs. Prefer a task from the active CAF-Q queue and cite the canonical source documents.
6. Click **Run workflow**.
7. Open the new run and inspect the logs and uploaded artifacts. Then review the Pull Request, changed files, source refs, claims, and remaining gaps.
8. Merge only through the repository's normal independent review and governance process. This workflow never merges automatically.

## Suggested first task

`Perform one bounded source-evidence pass for CAF-Q-003: read the current Gemini workflow files and the latest cloud-agent operational evidence, compare the implementation against the current Google action documentation, and produce a source-bound remediation proposal. Reuse existing components. Make documentation-only changes for this first run; preserve all historical IDs; identify each claim by path/ref/SHA; do not run tests or invoke any additional provider.`

## Troubleshooting

- Missing `GEMINI_API_KEY`: add the repository secret in Actions settings, then rerun.
- Permission denied while creating a branch or PR: inspect repository/org Actions token policy and rulesets; do not broaden permissions beyond the required branch and PR operations.
- Gemini API quota/model error: inspect the run's status and the configured model; keep the key private.
- No PR created: inspect the action logs and artifact, then dispatch a smaller task with explicit acceptance criteria.

## Evidence and limitations

The repository already contains read-only Gemini audit workflows and historical successful execution evidence for run `38952885501`. This new workflow is a separate proposed write-capable engineering lane. Its successful configuration, first execution, PR quality, repeatability, and qualification remain unproven until independently reviewed against run-bound evidence.
