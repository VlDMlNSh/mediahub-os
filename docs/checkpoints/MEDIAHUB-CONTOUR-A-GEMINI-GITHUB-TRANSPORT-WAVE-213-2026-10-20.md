# MediaHub OS Contour A — GitHub transport batch controller (Wave 213)

Date: 2026-10-20
Status: implementation proposal on a feature branch; NOT MERGED, NOT DISPATCHED, and NOT QUALIFIED.

## Purpose
Add a narrowly scoped, manually triggered GitHub-hosted controller that dispatches the three existing Gemini workflows through the GitHub Actions REST API and waits for run completion. The controller uses the run-scoped `github.token` with `actions: write`; it does not read, print, or copy Gemini provider secret values. Each child workflow continues to consume its own configured provider secret at runtime.

## Source facts rechecked
- Current `main` HEAD at inspection: `1324f2f9e558a99c1d3e06eb9d955c0827214fe2`.
- [Agent 1 workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-autonomous-engineering.yml): `GEMINI_API_KEY`.
- [Agent 2 workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-2.yml): `GEMINI_API_KEY_2`.
- [Agent 3 workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-3.yml): `GEMINI_API_KEY_3`.
- Each child workflow declares `workflow_dispatch`, fixed `main` base choice, `contour-a` scope choice, isolated Draft PR output, and output validation.
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) requires a controlled dispatch and exact run/job/artifact evidence; its existence does not itself authorize dispatch.
- Existing assignments #378–#380 contain per-task guardrails against dispatching workflows. This controller therefore uses three separate transport/evidence tasks rather than representing those guarded assignments as dispatched.

## Controller behavior
- Manual `workflow_dispatch` only, with explicit confirmation input defaulting to `no`.
- Fixed task text and fixed `main` ref; no arbitrary user-supplied prompt, base branch or scope.
- Requests the three existing child workflow dispatches using `github.token`; expects HTTP 204.
- Finds matching post-start `workflow_dispatch` runs, records run IDs and URLs in the GitHub Actions step summary, polls for terminal state, and fails unless all three conclude `success`.
- Uses a 45-minute job timeout and a bounded 35-minute polling window.
- No merge/deploy step and no secret-management step.

## Security / residual limits
- This is a proposed GitHub-hosted control path, not proof that the repository's current token permissions permit dispatch. That is only proven by a successful controller run after merge.
- The controller does not inspect or validate provider secret values. A successful child workflow and its artifact/tool-call validation are required; even that is not Contour A qualification.
- GitHub Actions may require repository policy settings or workflow permissions to permit dispatch with `GITHUB_TOKEN`. If the dispatch POST is rejected, the controller fails closed and suppresses response bodies from logs.
- Run correlation is based on workflow path, `workflow_dispatch`, `main`, and creation time after the batch start. Avoid concurrent manual dispatches during a batch; inspect run IDs/artifacts before acceptance.
- Agent-produced Draft PRs are untrusted proposals. Do not merge automatically.
- No credentials were read or tested by this chat session. No child Gemini runs were started by this chat session.

## Verification state
- Workflow source inspection: COMPLETE.
- Controller static review: authored; not executed by GitHub Actions yet.
- YAML/actionlint validation: NOT RUN in this session.
- Gemini dispatch and provider authentication: NOT VERIFIED by this session.
- Contour A: NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED.

## Next step
Review and merge this PR through the repository's normal governance. Then open the controller workflow on `main`, choose `confirm=yes`, and run it. Collect its summary and all three run IDs, inspect job logs/artifacts and resulting Draft PRs, and record provider/authentication outcomes without exposing secret values.

## Canonical map
[MediaHub OS canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)


## Additional historical execution evidence discovered during this wave

The repository's Actions API exposes a prior three-agent batch on 2026-10-20, before this controller PR was created. These are real historical runs, but they were NOT initiated by this chat session or by this Wave 213 controller:

| Agent | Run | Job | Conclusion | Artifact | Artifact digest |
|---|---:|---:|---|---:|---|
| Gemini 1 | [39370191589](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370191589) | 118456086050 | success | 12240818397 | `sha256:6ba571f563e38fd9df2be5d5ca23da0c59e446661528284ac22b428dfde93d3e` |
| Gemini 2 | [39370202615](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370202615) | 118456119718 | success | 12241545147 | `sha256:a800276ca454550d19930b03a62169cdfe45786e96beabf59d9194b54098644f` |
| Gemini 3 | [39370217605](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39370217605) | 118456166571 | success | 12240363870 | `sha256:6d91dc54e57aebb3720674c86466e0fa37cc3f69c525a5c94bb0b5c14fceeccd` |

All three were `workflow_dispatch` runs on source HEAD `25033753415fcbecdc7b2fe53085ed1bf2e4b8b4`. Their job summaries show the Gemini CLI action and the actionable-output validator completed successfully; each published a non-expired `gemini-output` artifact. This is strong evidence that the configured workflows, provider credentials at that time, GitHub MCP tool call validation, and artifact publishing worked in that earlier batch. It does not prove the credentials remain valid now or that Wave 213 dispatched anything.

The repository's current report in [PR #404](https://github.com/VlDMlNSh/mediahub-os/pull/404) also records successful Gemini runs and Draft PR outputs [#401](https://github.com/VlDMlNSh/mediahub-os/pull/401), [#402](https://github.com/VlDMlNSh/mediahub-os/pull/402), and [#403](https://github.com/VlDMlNSh/mediahub-os/pull/403), with independent review caveats. Agent output remains untrusted and those PRs were not accepted by this wave.

## Current-session execution result

No new run was started from this chat session: the GitHub connector exposes no workflow-dispatch mutation, and the available browser profiles have no recorded GitHub sign-in. The controller in PR #408 remains the proposed next step; it must be reviewed and merged under normal repository governance, then invoked through GitHub Actions with `confirm=yes`. Do not claim the historical runs were launched by this session.


## Pull-request checks observed during this wave

On controller PR #408 head `8fa1793a720f9fdfdb3aecc5d735963ccf72b002`, the repository reported:
- [Astra Verify run #39391451564](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39391451564), job #118523694886: `success`.
- [Astra Cloud Runtime Validation run #39391451551](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39391451551), job #118523694833: `success`.

Both were tied to that exact head SHA. They cover the repository's current verification and runtime-validation suites, but neither executes this new controller or dispatches Gemini. Dedicated actionlint/YAML lint for the new workflow has not been run in this session, and runtime behavior remains unverified until the controller is merged and manually dispatched.
