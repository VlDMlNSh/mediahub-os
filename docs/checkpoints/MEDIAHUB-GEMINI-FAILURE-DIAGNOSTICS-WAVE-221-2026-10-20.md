# MediaHub OS — Gemini failure diagnostics, Wave 221

Date: 2026-10-20
Status: Draft PR opened; CI pending at time of report. No merge or qualification.

## Objective

Address the Agent 2 failure evidence from run [39396596067](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396596067): repeated MCP read errors, free-tier quota exhaustion, and no usable stdout artifact for the fail-closed validator.

## Implementation proposal

Draft PR: [#420 — preserve sanitized Gemini failure diagnostics](https://github.com/VlDMlNSh/mediahub-os/pull/420)
Head branch: `contour-a/gemini-failure-diagnostics-wave221`
PR head commit: `2016c1c99a44cbf9b700d0a1eba777a9964fed09`
Base at PR creation: `main` @ `80be45a70732b1d568164571d4273a6397792c3b`.

Changed child workflows:
- `.github/workflows/gemini-autonomous-engineering.yml` — blob SHA `e3de99ec9299b33a9c12e126aba785d55cfb71d9`.
- `.github/workflows/gemini-agent-2.yml` — blob SHA `75d9db95a9ccb75e5dfaba373f6d6ac77883fe11`.
- `.github/workflows/gemini-agent-3.yml` — blob SHA `b730bfb426450cda45a4252db6b4e370959e2061`.

The proposed workflow change:
1. Adds an `if: always()` step that emits a small JSON diagnostic artifact containing run/attempt IDs, job/step outcomes, stdout presence and JSON-validity booleans, response-presence boolean, and tool-name success/failure counts.
2. Uploads only this sanitized diagnostic metadata with a seven-day retention. Raw stdout, tool arguments/results, and repository content are not copied into the new diagnostic artifact.
3. Makes the prompt stop rule explicit: after a GitHub MCP call fails, record the exact tool/error; do not repeat the same call, try aliases, or invoke tools outside the allowlist.
4. Leaves the existing success validator in place; missing/invalid output, no successful tool operation, or no successful PR creation must still fail the job.

## Verification and current status

- All three changed files were fetched again from the feature branch. The diagnostic and upload steps, strict stop rule, and original success validator were present in read-back.
- PR #420 was created as Draft; it has three changed files and is not merged.
- At first CI read, workflow runs `39399830230` (Astra Cloud Runtime Validation) and `39399830302` (Astra Verify) were `in_progress`. These are not yet a green result and do not independently prove YAML or runtime behavior.
- No Gemini agents were re-dispatched. No paid fallback, alternate transport, merge, deployment, secret read, or Contour A acceptance occurred.

## Review caveats

- The diagnostic artifact intentionally omits raw Gemini stdout to avoid copying potentially sensitive model/tool content. Detailed runtime cause must still be investigated through access-controlled GitHub Actions logs.
- This pass has not demonstrated the new step against a real failed Gemini run. Runtime behavior remains unverified until CI passes and a controlled, authorized test demonstrates that the metadata artifact is uploaded after an action failure.
- `actions/upload-artifact@v4` is referenced by tag, not immutable commit SHA. Supply-chain pinning remains a separate review concern; this PR does not claim to resolve it.

## Next step

Review PR #420 and its exact-head CI. Fix any workflow syntax or expression errors before considering a controlled failure-path test. Do not merge automatically and do not re-dispatch Agent 2 before the workflow change is reviewed and accepted.


## CI read-back update (2026-10-20)

- Exact PR head `2016c1c99a44cbf9b700d0a1eba777a9964fed09` has two associated GitHub Actions runs completed successfully:
  - [Astra Cloud Runtime Validation #39399830230](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39399830230), job `validate` / `118551486243`, conclusion `success`.
  - [Astra Verify #39399830302](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39399830302), job `verify` / `118551487161`, conclusion `success`.
- These runs cover the repository's contract/runtime and verification suites, but the job step lists do not show a dedicated GitHub Actions workflow-lint or failure-path test. Therefore, CI is green for the associated checks; workflow syntax/runtime behavior of the new step is not yet independently demonstrated.
- Both runs report no downloadable artifacts; they are verification runs, not Gemini child workflow executions.
