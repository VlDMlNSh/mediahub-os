# MediaHub OS — governance request for controller-only cloud-agent invocation, Wave 240

Date: 2026-10-20  
Status: OPTION A CHECKED; REQUIRED GITHUB ENFORCEMENT EVIDENCE UNAVAILABLE THROUGH CURRENT CONNECTION; OPTION B REQUESTED, NOT APPROVED OR IMPLEMENTED

## Decision context

The binding project rule permits only the GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` to launch the three fixed-scope cloud-agent child workflows. The controller uses repository secret `MEDIAHUB_GITHUB_TOKEN` for REST dispatch/monitoring. Direct SentinelX/server/local CLI/ad-hoc/alternate transports remain prohibited.

Binding policy blob: `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.  
Bootstrap blob: `77368971b90071812f82c384cdd3be813513a5dc`.  
Controller on `main` blob: `99e5a87825aeb239568f96ecef004a102ff3e53b`.

## Option A — verification attempt and result

Attempted read-only retrieval of repository Actions settings endpoints:
- `GET https://api.github.com/repos/VlDMlNSh/mediahub-os/actions/permissions`
- `GET https://api.github.com/repos/VlDMlNSh/mediahub-os/actions/permissions/workflow`
- `GET https://api.github.com/repos/VlDMlNSh/mediahub-os/actions/permissions/selected-actions`
- `GET https://api.github.com/repos/VlDMlNSh/mediahub-os/actions/workflows/...`

The available GitHub connector rejected these endpoint URLs as unsupported/not allowed. This is a connector limitation, not proof that GitHub itself denies the requests or that any specific Actions policy is configured. The repository rulesets endpoint returned an empty list, but that alone does not establish effective Actions restrictions, classic branch protection, workflow-dispatch eligibility, or the principal type/permissions of `MEDIAHUB_GITHUB_TOKEN`. The credential value was not accessed.

Read-back of the three child workflows on `main` confirms they still expose `workflow_dispatch`:
- Agent 1 blob: `09523d809530ae5b7bf528eab5fa53bc5deaf92d`
- Agent 2 blob: `259c8c82b8d90a39e1c90e65390e469b241b5581`
- Agent 3 blob: `91b5397001e088dfae2f450ee77c9c23118b5601`

Therefore Option A cannot be confirmed from the evidence available in this connection. Technical exclusion of direct child invocation remains **NOT PROVEN**. No direct child dispatch was attempted.

## Option B — governance approval requested, not yet accepted

Request explicit owner/governance approval to design and implement a controller-only reusable-workflow model:
1. Convert each child workflow to `workflow_call` only; remove its direct `workflow_dispatch` entry point.
2. Have the approved controller call each child as a reusable workflow, preserving fixed task scopes, explicit confirmation, fail-closed behavior, concurrency controls, and audit records.
3. Pass only the specific provider secret(s) required by each child, explicitly named in the call. Never use `secrets: inherit`; never pass `MEDIAHUB_GITHUB_TOKEN` to a child/model process.
4. Give the controller and each child only the minimum required GitHub token permissions; preserve separation between transport credentials and provider credentials.
5. Revise evidence correlation because child invocations would become jobs within the controller run rather than separately dispatched workflow runs. Record controller run ID, child job IDs, outcomes, artifact digests and commit provenance; fail closed if any child lacks valid evidence.
6. Before merging, require independent review, actionlint/workflow-contract tests, positive/negative tests for dispatch exclusivity and secret boundaries, and exact-head CI. Do not trigger cloud agents as part of this design-only change.

This is an architecture/contract change from REST-dispatched child workflow runs to reusable workflow jobs. It must not be implemented or treated as approved until the owner/governance disposition is explicit.

## Current disposition and safety

- Existing binding policy remains in force; the sole approved route is the current controller → fixed-scope children.
- Because direct-dispatch exclusion is not proven and Option B is not yet approved, do not launch cloud agents until governance decides or the required repository-admin evidence for Option A is supplied.
- No agent dispatched, no workflow triggered, no secret read, no workflow code changed, no merge/deployment/qualification.
- PR #420 remains Draft/unmerged; its independent review and authorized controlled failure-path test are separate open gates.

## Navigation

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Current map addendum: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md
- Current checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Binding transport policy: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md
- Governing Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
