# MediaHub OS Contour A — controller-only Gemini workflow implementation, Wave 243

Date: 2026-10-20
Status: IMPLEMENTATION PROPOSAL / DRAFT PR; NOT MERGED, NOT QUALIFIED

## Governance authority

Owner explicitly approved Option B for implementation in a separate PR at [Issue #301 comment 6289586838](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6289586838). The approval does not authorize live cloud-agent dispatch, merge, deployment, or Contour A qualification.

Option A remains unproven: effective repository Actions restrictions and the principal permissions for `MEDIAHUB_GITHUB_TOKEN` could not be confirmed through the available GitHub connection. This wave proceeds under the explicit Option B implementation approval only.

## Implementation PR

- [Draft PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
- Branch: `contour-a/workflow-call-controller-governance-wave243`
- Exact checked commit: `436c6d386289c77538382f76d7d6102aaa28acbb`
- Base: `main` at `80be45a70732b1d568164571d4273a6397792c3b`
- Compare: 11 commits ahead / 0 behind at the last comparison.
- PR state: open Draft, unmerged; no submitted reviews were present at the last review-list read.

## Scope implemented

1. The three child workflows now declare `workflow_call` instead of standalone `workflow_dispatch`.
2. Child jobs include a fail-closed caller-context guard requiring the `workflow_dispatch` event and the controller workflow path.
3. The manual controller now calls the three local reusable workflows as fixed-scope jobs. It preserves explicit `confirm: yes`, fixed `main` base and `contour-a` scope, and an aggregate fail-closed summary.
4. Each child receives only its matching provider secret by explicit mapping. `secrets: inherit` is not used. The controller no longer performs REST child dispatch/run polling and no longer references `MEDIAHUB_GITHUB_TOKEN`.
5. Added positive/negative contract tests and pinned actionlint invocation in Astra Verify.
6. No cloud-agent workflow was dispatched during this wave; no secret value was read.

## Read-back blob SHAs

These files were fetched again from the PR branch after writes:

- Controller `.github/workflows/gemini-batch-dispatch-controller.yml`: `da1d0254a993adcc224d5859a9a97bf609abd710`
- Agent 1 `.github/workflows/gemini-autonomous-engineering.yml`: `41eac32ed8baaf76f05d024c682998e67b497713`
- Agent 2 `.github/workflows/gemini-agent-2.yml`: `e2abd0c881c65c312f7607746065417325bab877`
- Agent 3 `.github/workflows/gemini-agent-3.yml`: `49f41783235af15a5bf62aa9cf2aafbdf8a40a42`
- Astra Verify `.github/workflows/astra-verify.yml`: `00cd78c453655b8e092b1f73615866dc32fdc0d6`
- New reusable-workflow contract tests: `327ab69071048c627109352322fbef8adcbadcee`
- Updated controller contract tests: `161fc5a1d02b9d99ddf9819ab39a803981f05d67`

## CI evidence

Exact checked commit `436c6d386289c77538382f76d7d6102aaa28acbb):

- [Astra Cloud Runtime Validation run 39414529957](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39414529957): **success**.
- [Astra Verify run 39414529912](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39414529912): **success**. The run included actionlint, compileall, Gemini reusable-workflow contract tests, the full Python unit-test discovery, and signed-command smoke test.

An earlier CI attempt failed because required reusable-workflow inputs also declared defaults, and then because existing controller tests still expected the former REST-dispatch job. Both demonstrated issues were corrected; the later exact-commit CI above passed. This does not replace independent review or a runtime caller-guard test.

## Remaining gates and limitations

- Independent review is still required, especially for the semantics of `github.workflow_ref` in the reusable-workflow guard, secret flow, and permission ceiling.
- Add or verify a controlled negative caller-context test without launching Gemini.
- PR #421 remains Draft/unmerged. Do not merge automatically.
- Live agent dispatch remains **ON HOLD** until independent review and integration gates pass and a separate authorization for a real agent run is recorded.
- No deployment, release, qualification, or Contour A acceptance is claimed.

## Canonical navigation

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Map addendum](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Binding transport policy](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Governing Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
