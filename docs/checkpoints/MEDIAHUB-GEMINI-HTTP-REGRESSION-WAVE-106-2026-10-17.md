# Provider-Free Gemini HTTP Response Regression — Wave 106

- Date: 2026-10-17
- Scope: PR #334 candidate branch `security/gemini-readonly-hardening-20261017`.
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
- PR: [#334](https://github.com/VlDMlNSh/mediahub-os/pull/334).

## Implementation

- Extracted bounded HTTP response collection into `scripts/gemini_http_response.js`, shared by the primary workflow and a provider-free local test harness.
- The reader enforces a byte ceiling, rejects `aborted` and `error` response events, and only resolves after the HTTP response reaches `end` and `res.complete` is not false.
- The primary workflow awaits the shared reader before HTTP status/JSON/output validation and before writing `agent-output/gemini-audit.md`.
- Added `scripts/test_gemini_http_response.js`, using a local loopback HTTP server and temporary files only. It exercises:
  1. Complete valid JSON response — output is written.
  2. Non-2xx response — no output artifact.
  3. Response over the configured test limit — rejected, no output artifact.
  4. Truncated response with an incomplete declared Content-Length — rejected, no output artifact.
- The Python contract suite runs this Node.js harness. No provider key is loaded and no external provider endpoint is contacted.

## Candidate revision and blobs

- PR head: `166c49bd5231c4ab94fce02ebd2c2ed6ceb35b7b`.
- Primary workflow blob: `e233f808077a622b9ac51b1cf3be7ccc3259eb82`.
- Shared response reader blob: `adb3d27307cd5ad078a8c622cbeaaebd40f903ec`.
- Local HTTP harness blob: `5656d2563676d85ff83ed99905c5d4d0216c648f`.
- Python contract suite blob: `809a1ddcf07f40af297182576f1a13fb652243e1`.
- PR merge-ref validation commit: `6d13d5156855a81c522bd33e29ba9fb5eb2aee3d`, which merges the candidate head above into the current PR base for CI validation.

## CI evidence

All three PR merge-ref workflow runs completed successfully:

- [Gemini Read-only Workflow Contract #39068528671](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068528671) — actionlint and least-privilege/security regression tests passed, including the local HTTP harness.
- [Astra Cloud Runtime Validation #39068528613](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068528613) — success.
- [Astra Verify #39068528583](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068528583) — success.

The first CI attempt on the intermediate ref failed because the static test still expected the abort listener to remain inline in the workflow after it had been moved to the shared module. That assertion was updated to verify the shared module and call ordering; the subsequent three runs above passed.

## Limits and disposition

- PR #334 remains **OPEN / DRAFT / UNMERGED**. CI success is not independent security review or runtime qualification.
- The local harness proves behavior of the shared response reader plus the workflow-equivalent output gate. It does not invoke the Gemini provider, inspect secrets, exercise the hosted workflow's secret environment, or prove all production socket schedules.
- No provider calls, credential reads, queue admission, merge, deployment, or Contour A acceptance occurred.
- Next: request independent security review of PR #334 and confirm branch protection / required review state. Do not promote this draft solely on green CI.
