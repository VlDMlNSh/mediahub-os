# MediaHub OS — Wave 381: dispatch-unique Gemini child branches

- Date: 2026-10-22
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Code base / immutable review target: `11d04d2f2687e9ba9215e4b67af2e450516960bb`
- Controller source blob on base: `28874450099e70b0f9d276600e6452c1b8e1b1a6`
- PR: [#482](https://github.com/VlDMlNSh/mediahub-os/pull/482)
- Initial code-only CI target SHA: `cd76cc9c58a192aaae3f38a2ea6a34b5f32ea460`.
- Follow-up documentation commits advanced the PR head; final-head CI must be checked against the latest PR head.

## Problem statement

Wave 379 demonstrated that each child workflow had a unique signed `dispatch_id`, but the child prompt only requested a “dedicated branch” without specifying a branch name tied to that dispatch. The role profiles are fixed, and repeated dispatches could therefore reuse branch names or collide with prior PRs. This did not cause the observed Agent 3 HTTP 503/tool failure; this change addresses a separate reproducibility and branch-isolation gap.

## Bounded change prepared

On branch `fix/gemini-dispatch-unique-branches-wave381-20261022`:

- Agent 1 prompt requires `contour-a/agent-1-${{ inputs.dispatch_id }}`.
- Agent 2 prompt requires `contour-a/agent-2-${{ inputs.dispatch_id }}`.
- Agent 3 prompt requires `contour-a/agent-3-${{ inputs.dispatch_id }}`.
- Each prompt prohibits branch reuse across dispatches and requires the dispatch ID in the PR body.
- Added `test_child_branch_names_are_unique_per_signed_dispatch` to `tests/test_gemini_transport_controller_contract.py`, already covered by the controller contract validation workflow.

The controller's signed payload and HMAC schema are unchanged. No new task input, provider route, secret, permission, workflow dispatch path, merge authority or deployment authority was added. This is a prompt-level guardrail with a static contract test, not a cryptographic enforcement of the model's chosen branch name.

## Exact-head verification evidence

Initial code-only PR #482 head `cd76cc9c58a192aaae3f38a2ea6a34b5f32ea460` had the following successful workflow results. Because documentation-only commits later advanced the PR head, these runs are historical evidence for that source-equivalent state, not final-head verification:

- [Astra Verify run 39812234965](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39812234965): job 119941296295 completed / success.
- [Gemini workflow contract validation run 39812235006](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39812235006): job 119941296681 completed / success. Logs show the transport-controller contract suite ran 12 tests and returned OK; signed-dispatch runtime contract suite ran 11 tests and returned OK; trigger-path suite ran 2 tests and returned OK.
- [Astra Cloud Runtime Validation run 39812235012](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39812235012): job 119941296879 completed / success.
- [Controller no-secret PR probe run 39812234998](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39812234998): probe/assertion jobs succeeded; admission and dispatch jobs were skipped as expected. No Gemini child workflow was launched.
- [Reusable workflow caller-context probe run 39812235105](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39812235105): observation and denial assertion completed / success.

The combined-status endpoint returned an empty statuses array; the workflow-run evidence above is the available exact-head CI evidence. Formal PR review submissions are empty and independent review remains NOT VERIFIED. GitHub reports the PR mergeable, but it is not merged. Final-head CI remains NOT VERIFIED until checks run against the latest head SHA.

## Acceptance status and limits

- Static workflow/controller contract CI: PASS for the listed runs.
- HMAC payload, admission flag, allowlists, permissions and provider routing: unchanged in this patch.
- Actual model compliance with the requested branch name: NOT VERIFIED until a later authorized runtime dispatch produces matching branches/PRs.
- Independent review and acceptance: NOT VERIFIED.
- No local test execution is claimed.
- No secret was read, no server was operated, and no PR was merged.
- No Gemini controller or child workflow was dispatched by this pass.

## Next step

Obtain independent review of PR #482. Do not rerun the three-agent controller until review/merge governance permits it; a passing static prompt test does not constitute runtime qualification.
