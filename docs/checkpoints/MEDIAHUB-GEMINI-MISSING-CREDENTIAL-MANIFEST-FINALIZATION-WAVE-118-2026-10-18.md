# Gemini Missing-Credential Manifest Finalization — Wave 118

Date: 2026-10-18
Status: IMPLEMENTED ON PR BRANCH / EXACT-HEAD CI PENDING AT LAST CHECK / NOT APPROVED

## Objective

Close the source-confirmed gap where both Gemini read-only workflows could upload an evidence manifest left at `PREPARED` / `NOT_STARTED` when `GEMINI_API_KEY` was absent.

## Source state and changes

- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301), still OPEN.
- Implementation PR: [#334](https://github.com/VlDMlNSh/mediahub-os/pull/334), OPEN / DRAFT / UNMERGED.
- Candidate HEAD after this pass: `e195849fcd8174e6fad87da28c7b42e2256b82f4`.
- Compare to live `main`: DIVERGED, 44 ahead / 2 behind; observed main HEAD `c06015e0b1526e0aaa6a522306052b077455aba5`; merge base `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`.
- Helper blob `scripts/mark_gemini_missing_credential.js`: `359c7d1f96ee8753da373fd5de6d77e6b7be6aac`.
- Helper regression test blob `scripts/test_gemini_missing_credential.js`: `a3090be9e605a9cd1ee2dd5c085be7ff4712962b`.
- Workflow contract test blob `scripts/test_gemini_readonly_workflows.py`: `3d1ed3bc1c059f8219cea7f0287bf39c551170e0`.
- Primary workflow blob `.github/workflows/gemini-readonly-audit.yml`: `0ba7c6590bef30b600920274729f5d9c8a1f50fe`.
- Retry workflow blob `.github/workflows/gemini-readonly-audit-retry.yml`: `dc1b31d101cd5f1961a047621d1503a697e24a89`.

## Implementation

Both workflows now invoke the secret-independent helper before exiting with code 30 when `GEMINI_API_KEY` is missing. The helper accepts only the expected `PREPARED` / `NOT_STARTED` state, atomically writes a terminal `BLOCKED_MISSING_CREDENTIAL` status with provider status `MISSING_CREDENTIAL`, records `failure_class=missing_credential` and `finished_at`, and leaves output digest/byte count null. It refuses to rewrite a manifest that is already in another state.

A Node regression test checks the emitted manifest, timestamp, atomic replacement/no leftover temporary file, and rejection of an already-terminal state. The Python workflow contract suite runs this test and checks that both workflows invoke the helper before exiting. No provider call is needed to test this path.

## CI evidence

After the new source was pushed, current-head runs were observed:
- [Astra Cloud Runtime Validation #39072860900](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39072860900): completed/success.
- [Astra Verify #39072860885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39072860885): in progress at last poll.
- [Gemini Read-only Workflow Contract #39072860984](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39072860984): pending at last poll.

Therefore the helper implementation is read back from GitHub, but its CI/test outcome is NOT YET VERIFIED. Do not infer success from a queued or in-progress run.

## Canonical map limitation

The canonical map blob was re-read at `4798bd288451000d6eff5bcb8f7f0855942f7181` using the blob API because the Contents API returned an empty body. The blob contained 1,048,405 characters / 7,172 lines, leaving insufficient safe margin for an additive map entry under the contents endpoint's payload constraints. This pass does not rewrite or truncate the map. A supplemental navigation addendum is provided and linked from the updated checkpoint.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Safety and disposition

No Gemini provider call, credential read, manual dispatch, merge, deployment, queue admission or Contour A acceptance occurred. PR #334 remains Draft. Its 44-ahead / 2-behind divergence, independent security review, protection-rule read-back and other Issue #301 admission gates remain open. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT PRODUCTION-ACCEPTED.

## Next bounded action

Poll the exact-head runs above. If all relevant checks pass, record their final conclusions and consider the next isolated gap: provider-outcome state-machine/manifest tests for invalid JSON, HTTP 429/non-2xx, transport errors, empty/oversized output and success digest. Then obtain independent review and reconcile branch drift without loss before promotion.
