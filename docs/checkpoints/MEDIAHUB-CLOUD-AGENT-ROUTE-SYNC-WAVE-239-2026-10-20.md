# MediaHub OS — sole cloud-agent API route synchronization, Wave 239

Date: 2026-10-20  
Status: DOCUMENTATION SYNC VERIFIED; TECHNICAL DIRECT-DISPATCH EXCLUSION NOT PROVEN

## Purpose

Revalidate the persisted rule that the GitHub-hosted Actions controller is the only policy-authorized launch path for any MediaHub OS cloud-agent/API execution, and synchronize the current evidence into the canonical documentation branch and governing Issue #301.

## Sole policy-authorized route

**GitHub-hosted Actions controller** `.github/workflows/gemini-batch-dispatch-controller.yml` → its three fixed-scope child workflows. The controller uses repository secret `MEDIAHUB_GITHUB_TOKEN` only for GitHub REST workflow dispatch and run monitoring. The credential must never be read, logged, decoded, placed in prompts/artifacts, or exposed to Gemini/child processes.

Direct launches from SentinelX, server shells, local CLI, ad-hoc scripts, unrelated workflows, or alternate transports are prohibited. If the approved route is unavailable, continue independent work and record the blocker; do not fall back. No paid fallback without explicit governance authorization.

## Read-back evidence

Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.

- Binding policy: [MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md), blob SHA `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.
- Bootstrap: [MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md), blob SHA `77368971b90071812f82c384cdd3be813513a5dc`. Section 1A explicitly calls the controller → three fixed-scope children the sole permitted cloud-agent/API launch route.
- Controller on `main`: `.github/workflows/gemini-batch-dispatch-controller.yml`, blob SHA `99e5a87825aeb239568f96ecef004a102ff3e53b`.
- Main child workflow blobs: Agent 1 `09523d809530ae5b7bf528eab5fa53bc5deaf92d`; Agent 2 `259c8c82b8d90a39e1c90e65390e469b241b5581`; Agent 3 `91b5397001e088dfae2f450ee77c9c23118b5601`.
- All three main child workflows still declare `workflow_dispatch`, and none declares `workflow_call`. Therefore the rule is persisted as policy, but technical exclusion of direct child-workflow dispatch remains **NOT PROVEN**. Effective repository/organization Actions policy and the `MEDIAHUB_GITHUB_TOKEN` principal type remain unknown because the available GitHub connector did not expose the Actions permissions endpoint. Do not claim enforcement beyond the evidence.
- The canonical map path was fetched; the Contents API returned empty content with blob SHA `baa715602545461fc24afc9e8a8e1d83d9099425`. This is an API retrieval limitation, not evidence that the map is empty or missing. Use the current map addendum for synchronized continuation notes and retain the canonical map link.

## PR #420 current evidence

[PR #420 — sanitized Gemini failure diagnostics](https://github.com/VlDMlNSh/mediahub-os/pull/420) remains Draft/unmerged at head `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`, 13 commits ahead / 0 behind main base `80be45a70732b1d568164571d4273a6397792c3b`.

Read-back branch blob SHAs:
- Agent 1 workflow: `89ded6bd650b6f14ab419151762dc3d4f2804a0d`
- Agent 2 workflow: `7a067fd7093a31c243c9e1f0e2caeec701f29c18`
- Agent 3 workflow: `d0e2e21d15523757293100f10a72e5e85232b7a2`
- Astra Verify: `9b38238e59c45d06bffca5198ef1bd764c5fc467`

The three child workflow files retain `job_id`, do not contain the obsolete `job:$job_id` expression, and pin the diagnostic artifact uploader to `actions/upload-artifact@cf430e030ddbb5b0abf93d22962f4752f3646cd9`. Astra Verify includes actionlint v1.7.7.

Exact-head CI:
- [Astra Cloud Runtime Validation #39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891): completed successfully.
- [Astra Verify #39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885): completed successfully.
- GitHub review API returned no submitted reviews at this read-back.

Open gates: independent review; authorized controlled failure-path test proving sanitized metadata uploads after a Gemini action failure without masking the failure; acceptance of the artifact action pin under repository supply-chain policy. Do not rerun Agent 2 or merge PR #420 before these gates are met.

## This wave's actions and limits

- Re-read the binding policy, Bootstrap, current checkpoint, map addendum, Master Roadmap, controller, all three main child workflows, PR #420 branch workflows, review submissions, exact-head CI runs, and Issue #301 comments.
- No cloud agent dispatched; no workflow triggered; no secret value read; no workflow code changed; no merge, deployment, or Contour A qualification.
- No governance disposition accepting the proposed dispatch-exclusivity options was found in the latest Issue #301 comments. Do not redesign the current REST-child-dispatch contract without the required explicit governance/change-control decision.

## Next bounded step

Obtain the required governance disposition on dispatch exclusivity (prove enforceable Actions restrictions/principal, explicitly approve a least-privilege controller-only `workflow_call` redesign with explicit per-child secret passing and no `secrets: inherit`, or keep agent dispatch unused). Independently obtain PR #420 review and authorize a controlled failure-path test only after the relevant gates are satisfied.

## Canonical navigation

- [Canonical project map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Current map addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md)
- [Current continuation checkpoint](mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Bootstrap](../architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Binding cloud-agent transport policy](../architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md)
- [Governing Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
