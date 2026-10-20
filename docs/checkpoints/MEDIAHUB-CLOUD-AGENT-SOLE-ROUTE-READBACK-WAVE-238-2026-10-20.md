# MediaHub OS — sole cloud-agent route read-back audit (Wave 238)

Date: 2026-10-20
Status: DOCUMENTATION SYNC VERIFIED; TECHNICAL EXCLUSIVITY NOT PROVEN

## Result

The sole policy-authorized cloud-agent/API launch route remains the GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` invoking its three fixed-scope child workflows. The controller's REST dispatch/monitoring uses repository secret `MEDIAHUB_GITHUB_TOKEN`. Direct launches through SentinelX, server shells, local CLI, ad-hoc scripts, unrelated workflows, or alternate transports are prohibited. Do not expose the token to model/agent processes, artifacts, prompts, or logs.

## Read-back evidence

- Binding policy, canonical docs branch `docs/mediahub-chat-tree-map-20261012`: `docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md`, blob SHA `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap, same branch: `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md`, blob SHA `77368971b90071812f82c384cdd3be813513a5dc`.
- Controller on `main`: `.github/workflows/gemini-batch-dispatch-controller.yml`, blob SHA `99e5a87825aeb239568f96ecef004a102ff3e53b`.
- Child workflow blobs on `main`: Agent 1 `09523d809530ae5b7bf528eab5fa53bc5deaf92d`; Agent 2 `259c8c82b8d90a39e1c90e65390e469b241b5581`; Agent 3 `91b5397001e088dfae2f450ee77c9c23118b5601`.
- All three mainline child workflow files still declare `workflow_dispatch`. Therefore policy exclusivity is persisted, but technical exclusion of direct child invocation is **NOT PROVEN**. Effective Actions policy and token-principal type have not been established from available evidence.
- Latest recorded governance proposal is Wave 236; no governance disposition was evidenced in the latest Issue #301 comments read for this pass. Do not redesign the current REST dispatch contract without that disposition.
- PR #420 remains a separate Draft/unmerged change set. Its prior exact-head CI success does not prove sole-route enforcement or controlled failure-path artifact behavior.

## Actions in this wave

- Re-read the binding policy, Bootstrap, controller, all three child workflow files, current checkpoint and map addendum from GitHub.
- Confirmed policy/bootstrap blob SHAs and the three child workflow refs.
- No agent was dispatched; no workflow was triggered; no secret value was read; no workflow code was changed; no merge, deployment, or Contour A qualification occurred.
- Updated the report, map addendum, checkpoint and Issue #301 to preserve this distinction and avoid implying technical enforcement.

## Next bounded step

Obtain an explicit governance disposition on Wave 236 options before any change to the workflow invocation architecture. Until then, keep cloud-agent dispatch unused and continue independent work. Do not claim technical exclusivity until direct invocation is demonstrably prevented or effective policy evidence proves it.

## Navigation

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Binding cloud-agent transport policy](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Current checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Map addendum](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md)
- [Governing Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #420](https://github.com/VlDMlNSh/mediahub-os/pull/420)
