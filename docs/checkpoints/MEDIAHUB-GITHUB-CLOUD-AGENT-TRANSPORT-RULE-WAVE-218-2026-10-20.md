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


## Read-back verification

Read-back from the canonical documentation branch after writes:
- Dedicated policy blob SHA: `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap blob SHA: `d54870c68633c3ff49f992647d46ea5fc7219a05`.
- Continuation checkpoint blob SHA: `28722e5eff8650402ed28b653772660bb17a8248`.
- Map addendum blob SHA: `c2a4513c9a4eccb7bfcee8119fd2d837edd75986`.
- This report before this read-back append: `541e1b8788aee2796fc00064b7f26dad8ad42a9e`.
- Controller workflow on `main` read-back SHA: `99e5a87825aeb239568f96ecef004a102ff3e53b`; content references `secrets.MEDIAHUB_GITHUB_TOKEN`.
- Issue #301 comment ID: `6287381098`.
