# Wave 394 — Gemini controller gate reconciliation (2026-10-22)

## Scope and immutable references

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Main HEAD at inspection: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`
- Canonical documentation branch at inspection: `343eeb760b1d49df8371db674e51ffc5942701a9`
- Functional Baseline 2.0 blob: `1147ecd39cfe6f0e6ba2d7a62b6bf68c71c0e24f` (accepted canonical reference)
- Controller workflow blob on main: `28874450099e70b0f9d276600e6452c1b8e1b1a6`
- Current controller-related evidence comment: [Issue #301 comment Wave 393](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6350710036)
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Reconciled repository state

- PR #493 is merged; its evidence is now indexed in the canonical map/checkpoint.
- PR #421 (controller-only `workflow_call` proposal) is merged, but the current main controller and three child workflows have since evolved. Current source must be treated as authoritative rather than assuming the old PR implementation remains active.
- PR #437 is merged at `7cbbc0025ce01b8c476d512cfc5e12dc35fd952c`; the current main controller blob is `28874450099e70b0f9d276600e6452c1b8e1b1a6`.
- PR #441 remains OPEN, head `9f40b90c3106662cfcc337c48f29e4794fa713dc`, base `ad99e1bebfeda0da799da94dd83a8f2e50a9acd0`, `mergeable=false`, no formal reviews returned, and exact-head check/status APIs returned empty results. Its formal review and CI are **NOT VERIFIED**.
- Issue #301 remains OPEN. Owner-approved Option B is recorded in issue comment [#6289586838](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6289586838); approval allowed implementation in a PR only and did not itself authorize dispatch, merge, deployment, or qualification.

## Current controller facts read from main

- Controller blob: `28874450099e70b0f9d276600e6452c1b8e1b1a6`.
- Controller has `workflow_dispatch` and `issue_comment` triggers; its probe is a reusable workflow with no secrets and no model invocation.
- Agent admission requires either explicit `workflow_dispatch` mode `agents` with `confirm=true`, or an exact owner `/next` comment on Issue #301, plus `MEDIAHUB_GEMINI_BATCH_ENABLED=true`.
- Controller reads `MEDIAHUB_GITHUB_TOKEN` and `MEDIAHUB_DISPATCH_HMAC_KEY`, resolves and pins a 40-character target SHA, signs three fixed-scope tasks, then POSTs GitHub Actions workflow-dispatch requests to the three child workflow files.
- Current child workflow blobs:
  - Agent 1 `.github/workflows/gemini-autonomous-engineering.yml`: `155a02159912ca371e6f826c51325ca269857aad`
  - Agent 2 `.github/workflows/gemini-agent-2.yml`: `fff1820a6b97d379b23674f36bd62227b7d4dec2`
  - Agent 3 `.github/workflows/gemini-agent-3.yml`: `781df56e8aa7c75ba453c08378611857862b2e44`
- Each of those three children still declares `workflow_dispatch`. Therefore the previously approved Option B property — children callable only by the controller via `workflow_call`, with no direct child dispatch trigger — is **not satisfied by current main**. Do not launch or use direct child dispatch to work around this discrepancy.
- The controller's successful non-secret probe is not evidence that the three-child dispatch path passed admission/security gates. Latest main check runs include successful general Verify and the unrelated OpenRouter catalog probe, but the controller event run on this main SHA was skipped; exact controller-specific gate success is **NOT VERIFIED**.
- The most recent formal PR review endpoint for #441 returned `[]`; the status/check-run endpoints for its head returned no records. Empty results are not PASS.
- No Gemini controller or child run was initiated in this pass. No secret values were read. No provider inference or remote host command was run.

## Disposition

**CONTROLLER-ONLY GOVERNANCE: NOT SATISFIED ON CURRENT MAIN / PR #441 REVIEW AND CI: NOT VERIFIED / GEMINI AGENTS 1–3: NOT RUN / CONTOUR A: NOT ACCEPTED.**

This is a source-state discrepancy to resolve, not permission to dispatch. The next implementation step is to reconcile the current controller transport with the recorded Option B decision in a focused code PR, including source-bound tests proving no direct child entry point, explicit secret mapping, controller caller guard, HMAC integrity, and positive/negative trigger-context behavior. Require independent review and exact-head CI before any agent dispatch. Do not use REST child dispatch as an alternative to the approved workflow_call-only design.

## Evidence links

- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #421](https://github.com/VlDMlNSh/mediahub-os/pull/421)
- [PR #437](https://github.com/VlDMlNSh/mediahub-os/pull/437)
- [PR #441](https://github.com/VlDMlNSh/mediahub-os/pull/441)
- [Wave 393 issue evidence](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6350710036)
- [Canonical chat tree map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
