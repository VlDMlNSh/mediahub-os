# MediaHub OS — cloud-agent single-path transport verification, Wave 227

Date: 2026-10-20
Status: POLICY PERSISTENCE VERIFIED; CURRENT PR STATE REFRESHED; NO AGENT DISPATCH

## Objective
Verify that the owner-directed cloud-agent launch transport is persisted in GitHub and explicitly remains the sole permitted launch path for all MediaHub OS cloud-agent API/workflow launches. Synchronize this finding into the dated report, map addendum, current continuation checkpoint, and governing Issue #301.

## Verified policy sources
- Canonical documentation ref: `docs/mediahub-chat-tree-map-20261012`.
- Transport policy: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md), read-back blob SHA `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), read-back blob SHA `d54870c68633c3ff49f992647d46ea5fc7219a05`, section 1B.
- The rule is explicit: ONLY `.github/workflows/gemini-batch-dispatch-controller.yml` and its fixed-scope GitHub-hosted child workflows may launch cloud agents. The controller must use repository secret `MEDIAHUB_GITHUB_TOKEN` for GitHub REST dispatch and monitoring. No direct SentinelX/server/local CLI/ad-hoc/alternate transport. The credential must never be logged, exposed to, or passed into model/agent processes.
- Governing Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) contains the owner-directed policy comment [#6287381098](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6287381098). A later synchronization comment [#6288415115](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6288415115) records Wave 226 report/map/checkpoint hashes and the same single-path constraint.

## Live engineering-state refresh
- `main` HEAD observed: `80be45a70732b1d568164571d4273a6397792c3b`.
- PR [#420](https://github.com/VlDMlNSh/mediahub-os/pull/420), branch `contour-a/gemini-failure-diagnostics-wave221`, remains a proposal: `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`, 13 commits ahead / 0 behind `main`. Search result shows it remains Draft/unmerged; review API returned zero submitted reviews.
- Exact-head CI evidence recorded in Wave 226 remains: [Astra Cloud Runtime Validation #39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891) and [Astra Verify #39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885) succeeded on that PR head. These static checks do not prove the sanitized artifact uploads after a real Gemini-step failure.
- PR #420 remaining gates: genuine independent review and an authorized controlled failure-path test. Do not rerun Agent 2 before those gates. No agent was dispatched during this verification; no secret was read; no merge/deployment/qualification is claimed.

## Synchronization result and limits
The launch-path rule is saved in two canonical documentation sources and governing Issue #301; this is not merely a chat-only instruction. The policy does not technically disable every alternate path in GitHub; it is the binding project rule and must be enforced by workflow permissions/repository controls where feasible. Do not describe it as technically enforced everywhere unless separate evidence proves that enforcement.

Canonical project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Next step
Continue independent engineering while obtaining independent review of PR #420. Then, only through the approved GitHub-hosted controller/child-workflow path and after authorization, run a bounded controlled failure-path test. No alternate transport, no silent fallback, no agent redispatch in this wave.
