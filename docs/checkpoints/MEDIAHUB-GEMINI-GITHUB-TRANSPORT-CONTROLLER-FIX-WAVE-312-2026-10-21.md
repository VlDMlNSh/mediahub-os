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
- The earlier exact-head validation for controller commit `5676bf402c807d069d1374a9321b12743fb72854` passed:
  - [Controller/probe run 39599892909](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39599892909): no-secret probe succeeded; dispatch job skipped.
  - [Cloud Runtime Validation 39599892899](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39599892899): validation job succeeded.
  - [Astra Verify 39599892964](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39599892964): verification job succeeded.
  - [Gemini workflow contract validation 39599892953](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39599892953): contract tests succeeded.
- Those runs predate the final prompt clarification commits in this PR. Exact final-head CI must be checked separately before merge.
- No Gemini agent was dispatched by this correction. No secret value was read or exposed. No formal independent security review is yet recorded.

## Status and next gate

Status: IMPLEMENTED IN DRAFT PR; prior intermediate checks passed; final-head CI and independent security review pending; NOT MERGED; NOT QUALIFIED; Gemini agent-mode NOT RUN.

Next step: verify CI for the final PR head, obtain a genuine independent security review, confirm effective repository/org governance and token permissions, then merge only after required checks pass. Do not start agent-mode until these gates are satisfied.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
