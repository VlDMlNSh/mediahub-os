# CAF-Q-003 / Wave 40 — Gemini MCP Adapter Remediation

- Date: 2026-10-17
- Status: **CHANGE PROPOSED / READ-BACK VERIFIED / RUNTIME RE-DISPATCH PENDING**
- Contour: A (Developer Fabric)
- Base ref: `main`
- Base commit observed before branch creation: `72cd8b66d5544b89a26275cd67312584c793ff02`
- Branch: `fix/gemini-mcp-remove-list-commits-wave-40`

## Evidence

- Workflow run [39019037870](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019037870), job [117356960181](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39019037870/job/117356960181), completed with conclusion `success`.
- The run created [PR #310](https://github.com/VlDMlNSh/mediahub-os/pull/310) on branch `caf-q-003-mcp-recovery-pass`, head commit `acf66bcc35f8a0eae454271d6210f7d97d38fe4b`.
- PR #310's evidence file records `mcp_github_list_commits` failing with `Invalid input: expected record, received array`; file reads, branch creation, file creation, and PR creation succeeded in the run.
- The run proves the configured workflow can complete one bounded task and open a PR. It does not prove repeated-run reliability, quota availability, or full tool compatibility.

## Change

- Remove `list_commits` from the GitHub MCP allowlist.
- Use the already demonstrated `get_file_contents` operation for the initial connectivity check by reading `GEMINI.md` from `main`.
- Retain only the four MCP operations required by the bounded flow: file read, branch creation, file creation/update, and PR creation.
- Preserve the existing fail-closed validator requiring valid output, a non-empty response, at least one successful tool operation, and successful PR creation.

## Acceptance criteria

1. Workflow YAML and embedded MCP settings are reviewed by read-back.
2. Allowlist contains only the four required operations and valid JSON punctuation.
3. A separately authorized manual dispatch completes successfully and creates a reviewable PR.
4. Repeated runs and provider quota behavior are recorded separately before claiming durable operational reliability.

## Verification

- Workflow file read back from branch after edits.
- Confirmed `list_commits` is absent from `includeTools`; first connectivity check now uses `get_file_contents`.
- Static content inspection only. No tests, workflow dispatch, provider call, installation, qualification, deployment, merge, or runtime change performed in this pass.

## Remaining gaps

- Runtime confirmation of this revised allowlist is pending a manual workflow dispatch.
- Gemini free-tier quota remains provider-controlled and can interrupt future runs.
- The workflow action currently references mutable tag `google-github-actions/run-gemini-cli@v0`; immutable action pinning should be a separate source-reviewed hardening task.
- The canonical project map and Master Roadmap remain the navigation/priority authorities; this recovery record does not alter product architecture or acceptance state.
