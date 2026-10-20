# MediaHub OS — Gemini failure-handling review, Wave 220

Date: 2026-10-20
Status: Evidence review recorded; workflow implementation not changed.

## Scope

Inspect current main-branch Gemini agent workflows and the failed Agent 2 run. Identify a minimal, testable next change without dispatching more agents or switching transport.

## Source refs and evidence

- Agent 2 workflow on `main`: `.github/workflows/gemini-agent-2.yml`, blob SHA `259c8c82b8d90a39e1c90e65390e469b241b5581`.
- Agent 1 workflow on `main`: `.github/workflows/gemini-autonomous-engineering.yml`, blob SHA `09523d809530ae5b7bf528eab5fa53bc5deaf92d`.
- Agent 3 workflow on `main`: `.github/workflows/gemini-agent-3.yml`, blob SHA `91b5397001e088dfae2f450ee77c9c23118b5601`.
- Failed Agent 2 run: [39396596067](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396596067); job ID `118540763883`.
- Agent 2 task was bounded to read `GEMINI.md`, compare workflow files, and create one evidence checkpoint/PR.
- The job log records a call to unconfigured tool `update_topic`, repeated `mcp_github_get_file_contents` errors, exhaustion of Gemini free-tier input-token quota for `gemini-3.5-flash-lite`, and `FatalTurnLimitedError`. No usable stdout JSON artifact was available to the post-step validator.
- Each of the three inspected workflows sets `upload_artifacts: 'true'` inside the Gemini CLI action, then validates `gemini-artifacts/stdout.log` in a separate step gated by `if: success()`. The validator therefore does not run after an action failure; the action's own artifact-upload step was skipped in the observed failed run.
- Existing prompt text already says to stop repeated guessing on tool errors. The runtime trace shows that prompt guidance alone did not prevent repeated calls.

## Findings

1. The observed failure is a combination of a tool-selection/configuration violation, repeated MCP failures, provider quota exhaustion, and the session turn limit. Do not attribute the incident to quota alone.
2. Existing output validation fails closed when there is no valid output/PR record. Preserve that behavior.
3. The next workflow change should add an outer diagnostic artifact-upload step with `if: always()`, guarded so missing files do not mask the original failure. It should upload only non-secret diagnostic files produced by the action and must not fabricate a successful result.
4. Add explicit prompt language: on the first MCP error, record the exact tool/error; do not call an unlisted tool; do not repeat the same failed call; if required evidence cannot be fetched, stop and return a concise blocker. This is a behavioral guard, not a substitute for runtime enforcement.
5. Keep the approved GitHub-hosted controller transport and existing provider credential boundaries. Do not use a paid fallback and do not re-dispatch Agent 2 until a reviewed change is merged and the relevant checks pass.

## Verification status

- Source content and blob SHAs read from GitHub.
- Failed job log inspected directly.
- No workflow edits, branch creation, PR creation, dispatch, merge, deployment, tests, or secret inspection performed in this wave.
- Mainline workflow changes remain a proposal and require independent review plus exact-head CI.

## Next bounded step

Prepare a minimal PR changing all three child workflows consistently: add best-effort failure diagnostics under `if: always()`, strengthen tool-error stop rules, and add YAML/workflow validation. Preserve the existing fail-closed success validator. Do not merge or rerun agents until CI and review evidence are available.
