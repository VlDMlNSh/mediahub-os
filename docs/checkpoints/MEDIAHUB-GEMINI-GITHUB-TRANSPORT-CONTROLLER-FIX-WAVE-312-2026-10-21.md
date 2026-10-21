# Gemini GitHub API transport controller correction — Wave 312 (2026-10-21)

## Required architecture

- Gemini Agents 1–3 are launched exclusively through the approved GitHub Actions controller using GitHub REST workflow dispatch and repository secret `MEDIAHUB_GITHUB_TOKEN` scoped only to the controller's dispatch/monitor steps.
- The transport token is never passed to child workflows, Gemini, prompts, model processes, logs, summaries, or artifacts. Child workflows receive only their own provider key.
- Server 3 / Alamo is exclusively for local Claude Code and browser-agent work. It is not a Gemini transport or fallback.

## Implementation in this PR

- Restores controller-side GitHub API dispatch/monitoring for the three fixed child workflows.
- Defaults to a no-secret probe. Model dispatch requires both `mode=agents` and explicit `confirm=yes`.
- Snapshots run IDs before dispatch and refuses ambiguous run correlation.
- Resolves `main` once and passes one immutable commit SHA to all three child checkouts.
- Keeps child workflows as direct `workflow_dispatch` targets with per-agent provider-secret isolation and pinned external actions.
- Clarifies that the immutable checkout SHA is not a valid Pull Request base; agent PRs must target branch `main`.
- Adds/updates static tests for the transport boundary, probe, child contracts and SHA pinning.

## Verification evidence

- Corrective PR: https://github.com/VlDMlNSh/mediahub-os/pull/431
- The final PR head `4764c74f6b3373fdb09117d3bc02576a39668a4f` has completed CI successfully. Runs:
  - [Controller/probe run 39600173791](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600173791): no-secret probe succeeded; `dispatch-and-verify` was skipped; no Gemini agents launched.
- [Cloud Runtime Validation 39600173792](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600173792): succeeded.
- [Astra Verify 39600173765](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600173765): succeeded.
- [Gemini workflow contract validation 39600173823](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600173823): succeeded.
- [No-secret caller-context probe 39600173779](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600173779): succeeded; caller-context denial assertion passed.
- No Gemini agent was dispatched by this correction. No secret value was read or exposed. No formal independent security review is yet recorded.

## Status and next gate

Status: IMPLEMENTED IN DRAFT PR; exact-head CI SUCCEEDED at `4764c74f6b3373fdb09117d3bc02576a39668a4f`; independent security review and effective repository/org governance confirmation still pending; NOT MERGED; NOT QUALIFIED; Gemini agent-mode NOT RUN.

Next step: obtain a genuine independent security review, confirm effective repository/org governance and the `MEDIAHUB_GITHUB_TOKEN` fine-grained permissions (`Actions: write`, minimum additional read access only as required), then merge only after required checks pass. Do not start agent-mode until these gates are satisfied.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
