# MediaHub OS Contour A — controller caller-ref guard review (Wave 253)

Date: 2026-10-20
Status: REVIEW FINDING RECORDED / PR NOT ACCEPTED

## Scope
Independent read-only review of Draft PR #421 implementing the owner-approved Option B design: controller-only GitHub Actions reusable workflows. No cloud-agent dispatch, provider call, merge, deployment, or qualification was performed.

## Exact repository evidence
- Repository: `VlDMlNSh/mediahub-os`
- Main HEAD observed: `80be45a70732b1d568164571d4273a6397792c3b`
- PR branch: `contour-a/workflow-call-controller-governance-wave243`
- PR candidate commit: `436c6d386289c77538382f76d7d6102aaa28acbb`
- Compare `main...PR branch`: `ahead`, 11 ahead / 0 behind; merge base equals main HEAD.
- Controller blob on candidate: `da1d0254a993adcc224d5859a9a97bf609abd710`
- Agent 1 child blob: `41eac32ed8baaf76f05d024c682998e67b497713`
- Agent 2 child blob: `e2abd0c881c65c312f7607746065417325bab877`
- Agent 3 child blob: `49f41783235af15a5bf62aa9cf2aafbdf8a40a42`
- Contract test blob: `327ab69071048c627109352322fbef8adcbadcee`
- Exact candidate workflow runs [Astra Cloud Runtime Validation #39414529957](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39414529957) and [Astra Verify #39414529912](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39414529912) are both recorded as completed SUCCESS. This does not establish that the caller-ref guard is secure.

## Finding — blocking authorization gap
Each child workflow currently checks:
- `github.event_name == 'workflow_dispatch'`
- `contains(github.workflow_ref, '/.github/workflows/gemini-batch-dispatch-controller.yml@')`

The path check does not constrain the ref suffix. A controller workflow dispatched from an arbitrary branch can therefore satisfy the path predicate; the called child receives a provider secret and a write-capable `github.token`. This does not prove the child caller is the trusted controller on the approved ref. The current test only checks for the path substring and does not reject a feature-branch caller ref.

## GitHub review action
A formal `REQUEST_CHANGES` review submission was rejected by GitHub because the connected identity is the PR author. A review finding was instead recorded as [PR #421 comment 6289801576](https://github.com/VlDMlNSh/mediahub-os/pull/421#issuecomment-6289801576). The comment requests an exact trusted controller ref policy and negative tests. It also notes that `actions/checkout@v4`, `google-github-actions/run-gemini-cli@v0`, and `ghcr.io/github/github-mcp-server:v0.27.0` are mutable references; immutable provenance remains open.

## Disposition
- PR #421: DRAFT / NOT ACCEPTED; do not merge until the caller-ref guard and negative tests are corrected and independently reviewed.
- Cloud-agent dispatch: ON HOLD. Passing CI is not permission to launch agents.
- No secrets were read, printed, or changed.
- No agent/workflow was launched.
- No mainline or documentation-branch merge/rebase/cherry-pick was attempted.

## Next bounded action
Correct the child guard to allow only the approved controller workflow ref, add positive and negative caller-ref fixtures (including an untrusted branch), run exact-head CI/actionlint, and obtain independent review. Separately pin external actions and container images to reviewed immutable refs. Only then re-evaluate the dispatch gate; do not dispatch during validation.

## Navigation
- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Draft PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
