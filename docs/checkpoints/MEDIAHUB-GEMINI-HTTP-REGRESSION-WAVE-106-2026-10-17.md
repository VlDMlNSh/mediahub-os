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


## Follow-up correction — Wave 107 (2026-10-17)

A post-wave source audit found that the JavaScript template embedded in the primary workflow used double-escaped newline sequences for joining candidate text and framing the Markdown artifact. That would preserve literal backslash-`n` text rather than write actual line breaks. Corrected both expressions and strengthened the local HTTP harness to return two text parts and assert the artifact contains an actual newline between them.

- Current PR candidate head: `1e052519f85afb1e9d3b58eb6d05cb45e81c2d73`.
- Primary workflow blob: `7465ad56496669ea576822109ca34afb47632596`.
- HTTP harness blob: `ade921ade649ddfda42c280759c8455d5e502304`.
- The earlier Wave 106 CI results apply to merge-ref `6d13d5156855a81c522bd33e29ba9fb5eb2aee3d`, not to this follow-up head. CI for the follow-up head has not yet been confirmed in the available workflow-run query; do not treat the earlier green runs as evidence for this revision.
- PR #334 remains OPEN / DRAFT / UNMERGED; no provider calls, secret access, queue admission, merge, deployment, or Contour A acceptance.

Next: confirm CI on the exact follow-up head and continue seeking independent security review.

- Follow-up exact-head CI passed on `1e052519f85afb1e9d3b58eb6d05cb45e81c2d73`: [Gemini Read-only Workflow Contract #39068814327](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068814327), [Astra Verify #39068814332](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068814332), and [Astra Cloud Runtime Validation #39068814337](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39068814337) all succeeded.


## Wave 108 — shared HTTP response reader across both workflows (2026-10-18)

Source audit found that the retry workflow maintained a second response-body parser. It enforced a byte cap and handled `aborted`, but did not explicitly verify `res.complete` before resolving on `end`. This was a consistency and fail-closed assurance gap; it was not confirmed as an exploitable vulnerability.

Changes:
- Retry workflow now imports and uses the shared `scripts/gemini_http_response.js` bounded reader, matching the primary workflow.
- Removed duplicate inline stream parsing from the retry workflow.
- Updated contract tests to require both workflows to use the shared helper and prohibit reintroduction of the old inline response parser.

Evidence on exact candidate HEAD `e1f35cb47eab05f573c38a4c2a507c9d832ca3cc`:
- Retry workflow blob: `ad6d82b6eca40b4c9923ac5fc6485fa103e4d24b`.
- Contract tests blob: `f3ebfab5e0729e498872cceedc0ed3c0dc89c0d4`.
- Shared reader blob: `adb3d27307cd5ad078a8c622cbeaaebd40f903ec`.
- [Gemini Read-only Workflow Contract #39069449788](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39069449788) — success.
- [Astra Verify #39069449749](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39069449749) — success.
- [Astra Cloud Runtime Validation #39069449848](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39069449848) — success.

PR #334 remains OPEN / DRAFT / UNMERGED. No review submissions or inline review threads were present in the latest review audit. Repository collaborator permission metadata confirms administrator access for the authenticated owner, but the available GitHub integration does not expose branch protection/ruleset read endpoints; required-review protection is therefore unverified, not assumed absent or present. No provider calls, secret reads, workflow dispatch, queue admission, merge, deployment, or Contour A acceptance.

Next: obtain independent security review; verify branch protection through an authorized GitHub settings/API path before considering readiness changes.


### Wave 108 follow-up — shared response contract and summary correctness (2026-10-18)

A deeper review of both manual audit workflows found that the retry workflow still had a separate inline HTTP reader. It could accept an incomplete response at the `end` event without checking HTTP message completion. Both workflows now use `scripts/gemini_http_response.js`, which rejects aborted/incomplete responses and enforces the same hard response-byte cap.

The pass also corrected two output-format/runtime defects:
- The primary workflow's GitHub step-summary template used double-escaped newlines; it now emits actual Markdown line breaks.
- The retry workflow's summary referenced an undefined `attempts` variable; it now uses the recorded `manifest.attempts` value.

Regression coverage checks the shared reader is used by both workflows, both artifacts use real newlines, and the retry summary references the recorded attempt count. The local HTTP harness remains provider-free.

Latest verified PR head: `eab691df37b1e9d0a54d67a80c8c558a40d685df`.
- Primary workflow blob: `cb42b1094adbad802bbc764f7a36b453fcb518ea`.
- Retry workflow blob: `df8c2cdf5a344f400cdbbd9997aec82cf38870f2`.
- Contract test blob: `831d59559eef41783f3758ce883d895acc1526b0`.
- [Gemini Read-only Workflow Contract #39069711066](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39069711066) — success (10 tests passed).
- [Astra Verify #39069710934](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39069710934) — success.
- [Astra Cloud Runtime Validation #39069711045](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39069711045) — success.

The earlier intermediate failing runs were inspected and are not counted as passes. PR #334 remains OPEN / DRAFT / UNMERGED. No independent security review submissions or inline review threads were present. Branch protection/ruleset settings remain unverified because the available GitHub integration actions do not expose those settings. No provider calls, secret reads, dispatch, queue admission, merge, deployment, or Contour A acceptance.


## Wave 109 — current-state revalidation (2026-10-18)

- Re-fetched PR #334, Issue #301, exact-head workflow runs, review submissions, and inline review threads.
- PR #334 remains OPEN / DRAFT / UNMERGED at HEAD `eab691df37b1e9d0a54d67a80c8c558a40d685df`; base SHA `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`.
- Exact-head CI remains green: [Contract #39069711066](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39069711066), [Astra Verify #39069710934](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39069710934), [Cloud Runtime Validation #39069711045](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39069711045).
- No GitHub review submissions or inline threads were returned. Branch-protection/ruleset configuration remains unverified because the available GitHub integration has no corresponding read action.
- Current-source spot-check confirmed immutable `github.sha` checkout, main-only manual dispatch, read-only token permissions, disabled persisted checkout credentials, fixed context profiles, and shared bounded/incomplete-response rejection.
- No provider call, secret read, workflow dispatch, queue admission, merge, deployment, or Contour A acceptance.
- Details and explicit next gate: [Wave 109 addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-109-2026-10-18.md).
