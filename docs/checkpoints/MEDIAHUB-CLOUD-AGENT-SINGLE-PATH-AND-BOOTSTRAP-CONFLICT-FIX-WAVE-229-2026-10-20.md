# MediaHub OS — cloud-agent single-path and bootstrap conflict fix, Wave 229

Date: 2026-10-20
Status: DOCUMENTATION SYNC VERIFIED; NO AGENT DISPATCH; NO TECHNICAL ENFORCEMENT CLAIM

## Objective
Verify that the sole permitted cloud-agent API launch path is durable in GitHub and remove a conflicting instruction in the canonical bootstrap that could be read as authorizing direct child-workflow dispatch.

## Source-bound findings
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Transport policy was read back at blob `18c27e3f3be100da54b256cdc7d97a36e1fd753e`: [mandatory GitHub cloud-agent transport policy](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md).
- Before this wave, Bootstrap blob `d54870c68633c3ff49f992647d46ea5fc7219a05` contained section 1A language directing direct launch of three separate GitHub Actions workflows at each `/next`. This conflicted with the policy's controller-only route.
- Controller source on `main` was read back at blob `99e5a87825aeb239568f96ecef004a102ff3e53b`: [gemini-batch-dispatch-controller.yml](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-batch-dispatch-controller.yml). It requires explicit `confirm: yes`, dispatches the three fixed-scope child workflows using `secrets.MEDIAHUB_GITHUB_TOKEN`, correlates run IDs and fails closed on ambiguity/non-success.
- Child workflow Agent 2 on `main` was read back at blob `259c8c82b8d90a39e1c90e65390e469b241b5581`; it is a child workflow and not an alternative launch transport.

## Change and verification
- Replaced Bootstrap section 1A so the controller → fixed-scope child workflow chain is the only allowed cloud-agent/API launch route. Explicitly disallowed direct SentinelX/server/local CLI/ad-hoc/alternate dispatch; specified no fallback, no paid fallback without authorization, and strict secret isolation.
- Bootstrap update commit: `7e15cc9ba7235703f56ddfc3235e62eaf9b3ef39`.
- Bootstrap new blob SHA, verified by a fresh read-back: `77368971b90071812f82c384cdd3be813513a5dc`.
- Read-back assertions confirmed the new controller-only statement is present and the contradictory direct-three-workflow instruction is absent.
- The policy document remains unchanged at blob `18c27e3f3be100da54b256cdc7d97a36e1fd753e`.

## Scope limits
- This is a binding project policy and bootstrap instruction. It does **not** prove that GitHub technically disables every direct child-workflow dispatch path. Workflow permissions/repository controls must be separately reviewed before claiming technical enforcement.
- No cloud agent was dispatched. No secret value was read. No paid provider, alternate transport, merge, deployment, or Contour A qualification was used or claimed.
- PR #420 remains a separate Draft proposal with independent review and authorized controlled failure-path test still outstanding (see current PR for live state).

## Canonical navigation
- Map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Transport policy: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301

## Next step
Review repository controls to determine whether direct child-workflow dispatch can be technically constrained without breaking controller operation; obtain independent review of PR #420 and only then conduct the authorized bounded failure-path test through the controller.
