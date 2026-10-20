# MediaHub OS — sole cloud-agent route persistence and sync audit (Wave 237)

- Date: 2026-10-20
- Status: **DOCUMENTARY REVALIDATION COMPLETE / TECHNICAL EXCLUSIVITY NOT PROVEN**
- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Binding launch route

The only policy-authorized launch path for any MediaHub OS cloud-agent/API invocation is:

`.github/workflows/gemini-batch-dispatch-controller.yml` on GitHub-hosted Actions → the three fixed-scope child workflows. The controller uses repository secret `MEDIAHUB_GITHUB_TOKEN` for GitHub REST dispatch and run monitoring. No direct SentinelX/server-shell/local-CLI/ad-hoc/unrelated-workflow/alternate transport is allowed. Do not expose the token to Gemini or artifacts; do not use a paid fallback.

## Re-read evidence

- Policy: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md), blob SHA `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), blob SHA `77368971b90071812f82c384cdd3be813513a5dc`; section 1A explicitly repeats the single approved route.
- Controller on `main`: blob SHA `99e5a87825aeb239568f96ecef004a102ff3e53b`.
- Child workflow files on `main` still declare `workflow_dispatch`: Agent 1 `09523d809530ae5b7bf528eab5fa53bc5deaf92d`; Agent 2 `259c8c82b8d90a39e1c90e65390e469b241b5581`; Agent 3 `91b5397001e088dfae2f450ee77c9c23118b5601`.
- Therefore policy exclusivity is preserved in the canonical docs, but technical exclusion of direct child invocation is **not proven**. Effective Actions policy and the principal type behind `MEDIAHUB_GITHUB_TOKEN` remain unknown; no secret value was read.
- PR [#420](https://github.com/VlDMlNSh/mediahub-os/pull/420) remains Draft/unmerged at `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`, 13 commits ahead / 0 behind base `80be45a70732b1d568164571d4273a6397792c3b`. Exact-head Astra Cloud Runtime Validation [#39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891) and Astra Verify [#39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885) are recorded as successful. PR review API returned no submitted reviews. These CI runs do not prove route exclusivity or the sanitized failure-path behavior.
- No agent was dispatched in this wave. No workflow was triggered; no credential was read; no workflow code was changed; no merge, deployment, or Contour A qualification is claimed.

## Governance boundary and next step

Wave 236's options remain proposals, not accepted decisions:
A. establish enforceable repository/organization policy and principal evidence;
B. after explicit governance approval, redesign the children as controller-only `workflow_call` workflows, passing only each child's explicitly required provider secret (never `secrets: inherit`) and preserving minimal permissions/correlation/fail-closed validation; or
C. leave dispatch unused and continue independent work.

Do not change the current REST-dispatch architecture without the applicable governance decision. The next bounded step is to obtain a documented governance disposition and, if option B is selected, prepare a separately reviewed implementation plan. Continue independent work while blocked.

## Navigation

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Wave 236 governance proposal](MEDIAHUB-CLOUD-AGENT-DISPATCH-EXCLUSIVITY-GOVERNANCE-PROPOSAL-WAVE-236-2026-10-20.md)
- [PR #420](https://github.com/VlDMlNSh/mediahub-os/pull/420)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
