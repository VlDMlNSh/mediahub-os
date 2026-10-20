# MediaHub OS — governance approval request and synchronization (Wave 242)

Date: 2026-10-20
Status: governance decision pending; no Option B approval inferred.

## Purpose

Synchronize the current cloud-agent launch gate and provide the exact owner response needed to authorize Option B. This report records the request and verification status; it is not itself a governance decision.

## Verified transport rule

The only policy-authorized cloud-agent/API launch route is the GitHub-hosted Actions controller `.github/workflows/gemini-batch-dispatch-controller.yml` → its three fixed-scope child workflows. The controller uses repository secret `MEDIAHUB_GITHUB_TOKEN` for GitHub REST dispatch and monitoring. The token must never be read, logged, placed in artifacts/prompts, or exposed to child agents/models. Direct SentinelX/server/local CLI/ad-hoc/unrelated-workflow/alternate launch routes are prohibited.

Read-back:
- Binding transport policy: blob SHA `7441e2059c5a7b987c559f822c1764047d0150d4`.
- Bootstrap: blob SHA `69a11d27c591dac859a097734f9eda3df80f29de`, section 1A.
- Controller on main: blob SHA `99e5a87825aeb239568f96ecef004a102ff3e53b`.
- Canonical map URL: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Governance status

Option A was attempted first but cannot be verified using the available GitHub connection: Actions permission endpoints were not readable; an empty `/rulesets` response does not prove effective restrictions; the three main child workflows still expose `workflow_dispatch`; and the effective restrictions/principal associated with `MEDIAHUB_GITHUB_TOKEN` remain unconfirmed. This is **insufficient evidence**, not proof that controls are absent.

The explicit Option B governance request is already recorded at:
https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6289444269

The latest synchronization comment states the hold:
https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6289488182

No explicit approval/rejection of Option B was present in the latest Issue #301 comments inspected. Therefore:
- Option B remains **REQUESTED, NOT APPROVED**.
- Cloud-agent dispatch remains **ON HOLD**.
- Do not implement the `workflow_call` redesign until an authorized governance comment explicitly approves it.
- No agent was dispatched, no workflow was triggered, no secret value was accessed, and no merge/deployment/Contour A qualification is claimed.

## Option B design boundary, if approved

1. Child workflows become `workflow_call`-only; remove their standalone `workflow_dispatch` entry points.
2. The existing controller remains the sole manually invoked entry point, preserving explicit confirmation, fixed task scopes, ambiguity checks, and fail-closed validation.
3. Pass only explicitly named, child-specific provider secrets. Never use `secrets: inherit`; never pass `MEDIAHUB_GITHUB_TOKEN` to child jobs or model processes.
4. Preserve least privilege and record controller run ID, child job IDs/conclusions, artifact digests, exact refs and commit provenance.
5. Before merge: independent review, actionlint, positive/negative workflow-contract tests, secret-boundary tests, exact-head CI, and documented rollback. A design/implementation approval does not authorize live agent dispatch, automatic merge, deployment, or qualification.

## Exact owner response to post on Issue #301

```text
APPROVE OPTION B — I explicitly authorize implementation of the controller-only reusable-workflow design for MediaHub OS Contour A in a separate working branch and pull request.

Scope: convert the three fixed-scope Gemini child workflows to workflow_call-only and remove their workflow_dispatch triggers; update the existing GitHub-hosted controller to invoke them as reusable jobs while preserving explicit confirmation, fixed scopes, ambiguity checks, and fail-closed validation. Pass only explicitly named child-specific provider secrets; do not use secrets: inherit; do not expose MEDIAHUB_GITHUB_TOKEN to child jobs or model processes. Retain least-privilege permissions and auditable run/job/artifact/commit provenance.

Required before merge: independent review, actionlint, positive and negative workflow-contract tests, secret-boundary and dispatch-exclusivity tests, and exact-head CI.

This approval authorizes design and implementation in a separate PR only. It does NOT authorize cloud-agent dispatch, secret access beyond the existing approved purpose, automatic merge, deployment, or Contour A qualification. Those require their own applicable gates and explicit authorization.
```

Post the approval as a new comment on the governing issue, not by editing the earlier request:
https://github.com/VlDMlNSh/mediahub-os/issues/301

## PR #420 status

- Draft proposal head: `c6b57ee3c8c748b86025f23fbb928cf6e0f2ddcc`.
- Base observed in the comparison: `main` at `80be45a70732b1d568164571d4273a6397792c3b`; proposal is 13 commits ahead / 0 behind.
- Exact-head Astra Cloud Runtime Validation run [39402774891](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774891): SUCCESS.
- Exact-head Astra Verify run [39402774885](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39402774885): SUCCESS.
- Review API returned no submitted reviews at last read. Independent review and an authorized controlled failure-path test remain open. PR remains Draft/unmerged.

## Next step

Owner/governance must post the explicit approval above (or choose a different disposition) on Issue #301. Until then, continue independent non-agent work and do not dispatch cloud agents or change the REST-child-dispatch contract.

## Navigation

- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Map addendum: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-217-2026-10-20.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Transport policy: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-GITHUB-CLOUD-AGENT-TRANSPORT-POLICY.md
- Governing issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
