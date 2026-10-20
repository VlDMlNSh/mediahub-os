# MediaHub OS — permanent GitHub cloud-agent transport rule (Wave 218)

Date: 2026-10-20
Status: RULE RECORDED; TRANSPORT BATCH PARTIALLY SUCCESSFUL

## Owner direction implemented

All MediaHub OS cloud-agent launches must use only the GitHub-hosted Actions controller workflow `.github/workflows/gemini-batch-dispatch-controller.yml` and its fixed-scope child workflows. The controller uses repository secret `MEDIAHUB_GITHUB_TOKEN` for GitHub REST API dispatch and run monitoring. Direct launches from SentinelX/server/local CLI, ad-hoc scripts, or alternate transports are prohibited unless this rule is explicitly changed through owner direction and applicable governance/change control.

Rule recorded in:
- [Dedicated transport policy](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md)
- [Bootstrap instruction](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), section 1B
- [Map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md)
- [Continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Runtime evidence

- Controller [39396582084](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396582084): job 118540718853; dispatch step SUCCESS; monitoring step FAILURE.
- Agent 1 [39396593650](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396593650): job 118540757771 SUCCESS; PR [#413](https://github.com/VlDMlNSh/mediahub-os/pull/413) created.
- Agent 2 [39396596067](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396596067): job 118540763883 FAILURE at “Validate Gemini produced an actionable PR result”. The Gemini CLI action step itself concluded SUCCESS.
- Agent 3 [39396598015](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39396598015): job 118540769364 SUCCESS; Draft PR [#414](https://github.com/VlDMlNSh/mediahub-os/pull/414) created.
- Batch is not fully successful because Agent 2 did not produce the required actionable PR result. API dispatch through MEDIAHUB_GITHUB_TOKEN is evidenced. No secret value was read or logged.

## Verification limits and next step

The canonical map itself was not overwritten because the Contents wrapper returned an empty body for the large map; the map addendum is used instead. This rule does not establish Contour A acceptance or accept agent outputs. No agent PR was merged. Next: read back all changed files and record blob SHAs, inspect Agent 2 logs, and independently review PRs #413/#414. Future agent launches remain restricted to the approved controller and MEDIAHUB_GITHUB_TOKEN.
