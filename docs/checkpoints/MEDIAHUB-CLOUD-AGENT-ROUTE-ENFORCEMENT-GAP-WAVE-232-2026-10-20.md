# MediaHub OS Contour A — cloud-agent route enforcement gap (Wave 232)

Date: 2026-10-20  
Status: **POLICY VERIFIED; TECHNICAL EXCLUSIVITY NOT YET ENFORCED / NOT QUALIFIED**

## Objective

Verify persistence of the owner-directed cloud-agent launch path, confirm current workflow triggers, and synchronize this finding with the canonical documentation branch and governing Issue #301.

## Confirmed policy and source evidence

- Binding policy: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md), blob SHA `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap rule: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), blob SHA `77368971b90071812f82c384cdd3be813513a5dc`.
- Sole **permitted** route: GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` → fixed-scope child workflows. The controller uses repository secret `MEDIAHUB_GITHUB_TOKEN` for GitHub API dispatch/monitoring. Controller blob on `main`: `99e5a87825aeb239568f96ecef004a102ff3e53b`.
- Read-back of the three child workflow files on `main` shows that all still declare `on.workflow_dispatch`:
  - Agent 1 `.github/workflows/gemini-autonomous-engineering.yml`, blob `09523d809530ae5b7bf528eab5fa53bc5deaf92d`.
  - Agent 2 `.github/workflows/gemini-agent-2.yml`, blob `259c8c82b8d90a39e1c90e65390e469b241b5581`.
  - Agent 3 `.github/workflows/gemini-agent-3.yml`, blob `91b5397001e088dfae2f450ee77c9c23118b5601`.

## Critical distinction

The route is persisted as the only approved policy. However, the child workflows' own `workflow_dispatch` triggers remain present on `main`. Therefore this pass does **not** prove technical exclusivity: an actor with sufficient GitHub Actions permissions may still be able to start a child workflow directly. Documentation alone cannot disable that route. No direct child dispatch was attempted.

## Current related PR

PR [#420](https://github.com/VlDMlNSh/mediahub-os/pull/420) remains a Draft proposal, not merged, at head `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`; compare reports 13 commits ahead / 0 behind main `80be45a70732b1d568164571d4273a6397792c3b`. Exact-head checks:
- [Astra Cloud Runtime Validation #39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891): success.
- [Astra Verify #39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885): success, including actionlint.
No submitted reviews were present at the latest read-back. Independent review and an authorized controlled failure-path test remain outstanding.

## Decision / next bounded step

Do not claim the controller path is technically exclusive yet. Design and review a minimal enforcement change that removes direct child dispatch entry points while preserving one explicit controller entry point, fixed scopes, secret isolation, and observable run correlation. A candidate is to convert children to reusable `workflow_call` workflows and have the approved controller/orchestrator invoke them, but validate GitHub Actions semantics and permissions before implementation. Do not launch agents, merge PR #420, read secrets, use an alternate transport, or promote Contour A qualification in this pass.

## Synchronization

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Map addendum: [MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md)
- Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

This report records project-relevant state and decisions from this pass, not a verbatim chat transcript archive.
