# MediaHub OS — cloud-agent route enforcement options (Wave 234)

Date: 2026-10-20  
Status: **POLICY VERIFIED / TECHNICAL EXCLUSIVITY OPEN / NO AGENT DISPATCH**

## Objective

Verify persistence of the only permitted cloud-agent/API launch path, re-check PR #420 and its exact-head CI, and evaluate a non-invasive technical enforcement option without changing the accepted transport contract or triggering agents.

## Binding rule and read-back

- The sole permitted cloud-agent/API launch path remains GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` → the three fixed-scope child workflows.
- Controller REST dispatch/run monitoring uses repository secret `MEDIAHUB_GITHUB_TOKEN`. The value was not read, copied, logged, or exposed.
- Direct launch from SentinelX, a server/local shell, local CLI, ad-hoc script, unrelated workflow, or any alternate transport is prohibited. If controller transport is blocked, continue independent work and record the blocker; do not fall back.
- Binding policy: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md), blob SHA `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap section 1A/1B: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), blob SHA `77368971b90071812f82c384cdd3be813513a5dc`.
- Controller on main: `.github/workflows/gemini-batch-dispatch-controller.yml`, blob SHA `99e5a87825aeb239568f96ecef004a102ff3e53b`. It has an explicit `confirm=yes` guard and calls the three children through GitHub REST API.
- Child workflows on main still expose `workflow_dispatch`: A1 blob `09523d809530ae5b7bf528eab5fa53bc5deaf92d`; A2 `259c8c82b8d90a39e1c90e65390e469b241b5581`; A3 `91b5397001e088dfae2f450ee77c9c23118b5601`. Therefore, the rule is binding policy, but technical exclusivity remains **not proven**.

## PR #420 and exact-head CI

- PR: [#420](https://github.com/VlDMlNSh/mediahub-os/pull/420), branch `contour-a/gemini-failure-diagnostics-wave221`.
- Latest branch head observed: `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`; compare against main `80be45a70732b1d568164571d4273a6397792c3b`: 13 ahead / 0 behind.
- Exact-head [Astra Cloud Runtime Validation #39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891): success; job `validate` ID `118561301997`.
- Exact-head [Astra Verify #39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885): success; job `verify` ID `118561301487`. Steps including pinned-version actionlint, compile, cloud-admission unit tests and signed-command smoke test succeeded.
- PR review API and inline review-thread API returned no submitted reviews / no threads at read-back. PR remains Draft and unmerged. CI does not prove the controlled failure-path diagnostic behavior or controller-only route exclusivity.
- PR description now records diagnostic uploader pinned to immutable upstream commit `actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9` (v7.0.2). This is proposal-branch content, not merged mainline.

## Technical enforcement option reviewed

Official GitHub documentation describes workflow execution protections that can restrict allowed actors and events for selected workflow paths:
- [About Actions policies](https://docs.github.com/en/actions/concepts/about-actions-policies)
- [Governing execution of workflows](https://docs.github.com/en/actions/how-tos/administer/control-workflow-execution)
- [REST API for Actions policies](https://docs.github.com/en/rest/actions/policies)

This suggests a repository/organization policy could restrict the child workflow paths and/or allowed actors/events. It is **not yet evidence that such a policy is enabled or available for this repository**. The identity/type behind `MEDIAHUB_GITHUB_TOKEN` and the repository's configured Actions policy/plan are not visible from workflow source alone. If the token represents a human user, an actor allowlist for that user would not distinguish controller use from direct API use by the same identity. Do not claim this option establishes exclusivity until the actual principal and applied policy are independently verified.

The alternative is to convert the child workflows to `workflow_call` and call them as static jobs from the controller, with explicit per-child provider-secret passing and no `secrets: inherit`. That removes direct child `workflow_dispatch` entry points, but conflicts with the current policy's requirement for controller REST child-dispatch. This transport contract must not be silently changed; an explicit owner/governance change-control decision is required before that redesign is implemented.

## Safety and disposition

- No cloud agent dispatched; no workflow manually triggered.
- No secret value read or exposed.
- No workflow/code change to the transport, no merge, deployment, or qualification.
- The only approved launch route is persisted in the policy and Bootstrap and is restated in Issue #301.
- **Open gates:** establish an enforceable controller-only boundary; independent review of PR #420; separately authorized controlled failure-path artifact test.
- Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains blocked.

## Synchronization

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Map addendum: [MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md)
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- Continuation checkpoint: [mediahub-next-continuation-checkpoint-2026-10-12-current.md](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
