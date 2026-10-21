# MediaHub OS — Gemini Controller Signed GitHub API Dispatch Repair, Wave 312

- Date: 2026-10-21
- Status: **IMPLEMENTED ON DRAFT PR / CI VERIFIED ON EXACT PR HEAD / NOT INTEGRATED / NOT QUALIFIED**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Controller repair PR: https://github.com/VlDMlNSh/mediahub-os/pull/432
- Competing transport PR requiring reconciliation: https://github.com/VlDMlNSh/mediahub-os/pull/431

## Objective and architecture

Restore the owner-required Gemini transport: the approved GitHub Actions controller dispatches and monitors all three fixed Gemini child workflows through the GitHub API using `MEDIAHUB_GITHUB_TOKEN`. The token is confined to the controller workflow step and is not mapped into child workflows, Gemini prompts, provider jobs, summaries, or artifacts. Alamo/server 3 remains reserved for local Claude Code and browser work; it is not Gemini transport.

## Exact source evidence

- Main/base commit: `f16e5bae202a78584f273132e7f88c6e25d3142e`.
- Controller repair PR #432 exact head at verification: `ea637eb55c87d44f0ce22730588e744c7470ee1d`.
- Controller blob: `3268dbf08cbcf4869b6ec608c9d61c34ac213154`.
- Agent 1 child blob: `a4160266e4da8dce00862936c6d4a3a7c17026f5`.
- Agent 2 child blob: `71adf89707c45fbfabdcfdb35fe0381d4583d647`.
- Agent 3 child blob: `507aa2cadefb3e8bdd8d210713c011152b202529`.
- Controller transport contract test blob: `5182b5f0e12a37c756342298642d100a9d4edbd0`.
- Reusable-workflow security contract test blob: `ec1cd102afa273d67a6a24ac68e5ee47bc09ae1e`.
- Caller-context probe contract test blob: `980d3868a2f9adbac842da7802289f4755f5e083`.

The controller defaults to a non-launching probe and requires both `mode=agents` and `confirm=yes`, additionally gated to `refs/heads/main`. It resolves and validates one immutable target SHA, dispatches only three fixed workflow filenames, signs each bounded task with HMAC, and fails closed when a child run cannot be uniquely correlated or does not succeed. Each child checks the signed payload before the provider/model job and checks out the shared target SHA. No child has the transport token or a nested-dispatch route.

## Exact-head verification evidence

All five checks returned success for PR #432 head `ea637eb55c87d44f0ce22730588e744c7470ee1d`:

- Astra Verify: [run 39604609752](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609752)
- Gemini workflow contract validation: [run 39604609734](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609734)
- Astra Cloud Runtime Validation: [run 39604609921](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609921)
- Non-launching caller-context probe: [run 39604609755](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609755)
- Controller probe and assertion: [run 39604609766](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39604609766). The probe and assertion succeeded; `dispatch_and_monitor` was **SKIPPED**. This is not a trusted agent dispatch or provider invocation.

Earlier exact-head runs exposed legacy tests that still encoded the obsolete reusable-`workflow_call` contract; the test suite was updated to assert the new signed API-dispatch architecture, and the latest exact-head CI is green. No agent-mode dispatch was run.

## Governance, security, and executor status

- PR #432 remains OPEN/DRAFT/UNMERGED. Formal review API currently returns **zero submitted reviews**. A green CI run is not independent security approval.
- PR #431 is also open and changes overlapping controller/child paths. It restores API transport but does not establish the same HMAC child-authorization gate. Keep PRs separate until independent review determines the safe integration candidate; do not merge either automatically.
- Availability, scope and rotation policy for repository secrets `MEDIAHUB_GITHUB_TOKEN` and `MEDIAHUB_DISPATCH_HMAC_KEY` were not inspected. The PAT's effective Actions permissions and organization/repository policy remain unverified. No secret value was read.
- Gemini Agents 1–3: **NOT RUN**. Controller agent-mode dispatch: **NOT RUN**. No provider/model invocation, child run IDs, agent artifacts, or agent artifact digests exist for this pass.
- Claude Code on Alamo/server 3: **NOT RUN**; the designated host and approved non-paid route are not positively identified. Browser lane: **NOT RUN** for the same host-identity/capability reason.
- Issue #301 remains OPEN. Contour A remains **NOT QUALIFIED / NOT ACCEPTED**. Contour B remains gated.

## Next bounded step

Obtain a formal independent security review of PR #432 against the controller and all three child workflow blobs, including replay/partial-dispatch behavior, secret availability/permissions, exact-main policy and provenance. Reconcile the overlapping PR #431 without losing its useful evidence. Only after governance/security gates pass should a trusted `mode=probe` run verify the positive main-controller context; agent mode remains blocked until all stated gates are accepted.

The canonical map itself was not changed and remains authoritative at https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md.
