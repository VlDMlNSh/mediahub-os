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
- The implementation code was present at `4764c74f6b3373fdb09117d3bc02576a39668a4f`. After documentation-only commits, exact PR head `cf7c42578b81f7212d25db44ed71a9b046b841c2` also completed all triggered checks successfully. Runs:
  - [Controller/probe run 39600342389](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600342389): no-secret probe succeeded; `dispatch-and-verify` was skipped; no Gemini agents launched.
- [Cloud Runtime Validation 39600342340](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600342340): succeeded.
- [Astra Verify 39600342341](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600342341): succeeded.
- [Gemini workflow contract validation 39600342385](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600342385): succeeded.
- [No-secret caller-context probe 39600342405](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39600342405): succeeded; caller-context denial assertion passed.
- Earlier exact code-head validation runs are listed in workflow history; latest exact-head CI confirms these checks also pass after the documentation-only updates.
- No Gemini agent was dispatched by this correction. No secret value was read or exposed. No formal independent security review is yet recorded.

## Status and next gate

Status: IMPLEMENTED IN DRAFT PR; exact-head CI SUCCEEDED at `4764c74f6b3373fdb09117d3bc02576a39668a4f`; independent security review and effective repository/org governance confirmation still pending; NOT MERGED; NOT QUALIFIED; Gemini agent-mode NOT RUN.

Next step: obtain a genuine independent security review, confirm effective repository/org governance and the `MEDIAHUB_GITHUB_TOKEN` fine-grained permissions (`Actions: write`, minimum additional read access only as required), then merge only after required checks pass. Do not start agent-mode until these gates are satisfied.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
