# MediaHub OS — Wave 381: dispatch-unique Gemini child branches

- Date: 2026-10-22
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Code base / immutable review target: `11d04d2f2687e9ba9215e4b67af2e450516960bb`
- Controller source blob on base: `28874450099e70b0f9d276600e6452c1b8e1b1a6`

## Problem statement

Wave 379 demonstrated that each child workflow had a unique signed `dispatch_id`, but the child prompt only requested a “dedicated branch” without specifying a branch name tied to that dispatch. The role profiles are fixed, and repeated dispatches could therefore reuse branch names or collide with prior PRs. This did not cause the observed Agent 3 HTTP 503/tool failure; this change addresses a separate reproducibility and branch-isolation gap.

## Bounded change prepared

On branch `fix/gemini-dispatch-unique-branches-wave381-20261022`:

- Agent 1 prompt now requires `contour-a/agent-1-${{ inputs.dispatch_id }}`.
- Agent 2 prompt now requires `contour-a/agent-2-${{ inputs.dispatch_id }}`.
- Agent 3 prompt now requires `contour-a/agent-3-${{ inputs.dispatch_id }}`.
- Each prompt prohibits branch reuse across dispatches and requires the dispatch ID in the PR body.
- Added `test_child_branch_names_are_unique_per_signed_dispatch` to the existing `tests/test_gemini_transport_controller_contract.py`, which is already in the controller contract validation path filter and test command.

The controller's signed payload and HMAC schema are unchanged. No new task input, provider route, secret, permission, workflow dispatch path, merge authority or deployment authority was added. This is a prompt-level guardrail with a static contract test, not a cryptographic enforcement of the model's chosen branch name.

## Verification status

- Changes were written through GitHub Contents API and are awaiting PR exact-head CI.
- The changed files must be re-read from the branch and blob SHAs recorded before claiming source verification.
- No local test execution is claimed in this environment.
- No Gemini controller or child workflow was dispatched by this pass.
- No secret was read, no server was operated, and no PR was merged.
- CI, independent review, runtime behavior and acceptance: NOT VERIFIED until evidence arrives.

## Acceptance criteria

1. Existing HMAC payload/authorizer interoperability tests remain unchanged and pass.
2. The new contract test confirms all three child prompts use role-specific branch prefixes plus signed dispatch ID.
3. Existing controller trigger-path coverage includes the modified child workflows and test file.
4. Exact-head CI passes; a reviewer independently confirms that no authority, credential, or dispatch-gate boundary changed.
5. Subsequent runtime evidence confirms branches and PRs actually use the requested unique names; prompt assertions alone do not prove model compliance.

## Next step

Open a PR and wait for exact-head CI/review. Do not rerun the three-agent controller until the branch-isolation change is verified; do not treat a passing static prompt test as runtime qualification.
