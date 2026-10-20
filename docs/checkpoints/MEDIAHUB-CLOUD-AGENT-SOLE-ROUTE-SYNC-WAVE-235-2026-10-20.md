# MediaHub OS — cloud-agent sole-route persistence and synchronization, Wave 235

Date: 2026-10-20  
Status: **POLICY PERSISTENCE VERIFIED / TECHNICAL EXCLUSIVITY NOT PROVEN / NO DISPATCH**

## Objective

Re-verify that the sole permitted cloud-agent/API launch route is durably recorded, and synchronize the latest project state into the canonical documentation branch and governing Issue #301.

## Sole permitted route — binding project rule

**The only permitted cloud-agent/API launch path is:**

GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` → its three fixed-scope child workflows.

The controller performs REST dispatch and run monitoring using the repository secret `MEDIAHUB_GITHUB_TOKEN`. The secret value must never be read, logged, copied into prompts/artifacts, or passed to Gemini/agent processes. Direct launch from SentinelX, server shell, local CLI, ad-hoc script, unrelated workflow, or any alternate transport is prohibited. If the approved controller is blocked, continue independent work and record the blocker; do not silently fall back.

### Read-back evidence

- Binding policy: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md), blob SHA `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), blob SHA `77368971b90071812f82c384cdd3be813513a5dc`; its owner-directed section explicitly labels this the only permitted route.
- Controller on `main`: `.github/workflows/gemini-batch-dispatch-controller.yml`, blob SHA `99e5a87825aeb239568f96ecef004a102ff3e53b`.
- Three child workflow blobs on `main` remain:
  - Agent 1 `.github/workflows/gemini-autonomous-engineering.yml`: `09523d809530ae5b7bf528eab5fa53bc5deaf92d`
  - Agent 2 `.github/workflows/gemini-agent-2.yml`: `259c8c82b8d90a39e1c90e65390e469b241b5581`
  - Agent 3 `.github/workflows/gemini-agent-3.yml`: `91b5397001e088dfae2f450ee77c9c23118b5601`
- Read-back confirms all three child workflows still declare `workflow_dispatch`. Therefore the route is the **only policy-authorized path**, but technical exclusion of direct child dispatch remains **NOT PROVEN**. This distinction is mandatory; do not overstate enforcement.

## Current proposal PR #420

- PR: [#420 — sanitized Gemini failure diagnostics](https://github.com/VlDMlNSh/mediahub-os/pull/420), Draft/unmerged.
- Latest revision reported in the PR description: `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`; compare says 13 commits ahead / 0 behind base `80be45a70732b1d568164571d4273a6397792c3b`.
- Exact-head [Astra Cloud Runtime Validation #39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891) and [Astra Verify #39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885) both completed successfully.
- Review API returned no submitted reviews at read-back. CI does not establish sanitized artifact upload behavior under an actual Gemini failure and does not establish controller-only dispatch.
- The PR proposal pins `actions/upload-artifact` to `cf430e030ddbb5b0abf93d22962f4752f3646cd9` (v7.0.2). This remains proposal-branch content, not merged mainline.

## Next engineering decision and gates

1. Inspect non-secret Actions execution policy and determine the identity/principal behind `MEDIAHUB_GITHUB_TOKEN`, without reading the token value.
2. If a repository/organization policy cannot demonstrably exclude direct child dispatch, prepare a controller-orchestrated `workflow_call` redesign with static child jobs, explicit per-agent provider-secret passing (no `secrets: inherit`), minimal permissions, and preserved fail-closed validation. Because this changes the existing REST-child-dispatch contract, do not implement it without the required owner/governance change-control decision.
3. Keep PR #420 Draft until independent review and a separately authorized controlled failure-path test are complete.
4. Do not dispatch agents during this pass. No secret was read; no workflow was triggered; no code was merged; no deployment or Contour A qualification is claimed.

## Canonical synchronization

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Map addendum: [MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md)
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- Continuation checkpoint: [mediahub-next-continuation-checkpoint-2026-10-12-current.md](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
