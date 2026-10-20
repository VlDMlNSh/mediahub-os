# MediaHub OS — controller-only cloud-agent route verification and sync, Wave 231

- Date: 2026-10-20
- Status: DOCUMENTATION / POLICY READ-BACK VERIFIED; NO AGENT DISPATCH; NOT A TECHNICAL EXCLUSIVITY PROOF
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Sole approved launch/API path

For every cloud-agent launch or cloud-agent API launch in MediaHub OS, the only permitted route is:

`GitHub-hosted Actions controller .github/workflows/gemini-batch-dispatch-controller.yml → the three fixed-scope child workflows`.

The controller uses repository secret `MEDIAHUB_GITHUB_TOKEN` for GitHub REST API dispatch and run monitoring. Direct launch from SentinelX, server shell, local CLI, ad-hoc scripts, unrelated workflows, or any alternate transport is prohibited. No fallback and no paid fallback without explicit governance authorization. The credential must never be read, logged, passed to a model/agent, or placed in prompts/artifacts.

## Read-back evidence

- Policy: `docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md`, blob `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap: `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md`, blob `77368971b90071812f82c384cdd3be813513a5dc`; section 1A explicitly states the controller-only route and disallows direct child-workflow dispatch.
- Controller on `main`: `.github/workflows/gemini-batch-dispatch-controller.yml`, blob `99e5a87825aeb239568f96ecef004a102ff3e53b`. Read-back confirms `workflow_dispatch`, explicit `confirm == 'yes'` gate, secret reference `secrets.MEDIAHUB_GITHUB_TOKEN`, three child dispatch operations, and fail-closed checks. No secret value was accessed.
- Current PR #420: https://github.com/VlDMlNSh/mediahub-os/pull/420 — head `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`; 13 commits ahead / 0 behind main `80be45a70732b1d568164571d4273a6397792c3b`; Draft/unmerged; submitted review list empty at this read.
- Exact-head CI: Astra Cloud Runtime Validation [run #39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891) SUCCESS; Astra Verify [run #39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885) SUCCESS.
- Canonical map read attempt returned empty content at blob `baa715602545461fc24afc9e8a8e1d83d9099425`; it was not overwritten. The map addendum is the current navigation record.

## Limits / unresolved gates

- This confirms that the approved route is consistently documented and the controller source contains the expected gates; it does NOT prove that every alternative GitHub dispatch entry point is technically disabled.
- PR #420 still needs independent review and an authorized controlled failure-path test proving sanitized diagnostic upload after Gemini action failure.
- No agent was dispatched in this wave; no token value was read; no merge, deployment, or Contour A qualification is claimed.

## Next bounded step

Audit all repository workflow dispatch entry points and permissions for technical enforcement of controller-only execution. Keep PR #420 Draft until independent review and the authorized controlled failure-path test are complete. Do not dispatch a child workflow directly or rerun the failed Gemini agent outside the controller.

## Navigation

- [Transport policy](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md)
- [Bootstrap](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md)
- [Current checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
