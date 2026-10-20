# MediaHub OS Contour A — map addendum, GitHub Transport Wave 217

Date: 2026-10-20

This addendum records the GitHub-hosted controller integration and runtime dispatch. It supplements, but does not replace, the canonical map.

- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Wave 217 evidence report: [MEDIAHUB-CONTOUR-A-GITHUB-TRANSPORT-CONTROLLER-WAVE-217-2026-10-20.md](../checkpoints/MEDIAHUB-CONTOUR-A-GITHUB-TRANSPORT-CONTROLLER-WAVE-217-2026-10-20.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Controller PR #408 merged as `27edfd5f04c6704ee7136c6cc73cf46f9731beb7`.
- Workflow input fix PR #411 merged as `7d86e852bf5837bc7dcf650327b22c1b27886efa`.
- Controller run [39396582084](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396582084) successfully executed the dispatch step using `MEDIAHUB_GITHUB_TOKEN`.
- Child runs: Agent 1 [39396593650](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396593650) SUCCESS with PR [#413](https://github.com/VlDMlNSh/mediahub-os/pull/413); Agent 2 [39396596067](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396596067) IN_PROGRESS at report time; Agent 3 [39396598015](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396598015) SUCCESS with PR [#414](https://github.com/VlDMlNSh/mediahub-os/pull/414).
- Do not mark the batch complete until the controller and Agent 2 finish. Agent-produced PRs remain proposals and require independent review.
- The canonical map Contents API returned empty content despite its known blob SHA. It was not overwritten; this addendum is the safe navigation update pending a reliable full-file read.


## Wave 218 — persistent cloud-agent transport rule (2026-10-20)

- Binding owner-directed policy: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md](MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md).
- Bootstrap section 1B now mandates the GitHub-hosted Actions controller and `MEDIAHUB_GITHUB_TOKEN`; direct SentinelX/server/local CLI agent launches are prohibited.
- Wave report: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-RULE-WAVE-218-2026-10-20.md](../checkpoints/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-RULE-WAVE-218-2026-10-20.md).
- Runtime batch: controller dispatch succeeded but monitor failed because Agent 2 failed actionable-PR validation; Agent 1 and Agent 3 jobs succeeded. See report for exact run IDs.
- Canonical map file itself was not overwritten due to empty Contents wrapper output; this addendum records navigation and evidence safely.
