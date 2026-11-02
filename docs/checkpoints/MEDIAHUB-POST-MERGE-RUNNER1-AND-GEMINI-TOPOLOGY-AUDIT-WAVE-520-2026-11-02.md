# MediaHub post-merge Runner 1 and Gemini topology audit — Wave 520

Date: 2026-11-02

## Scope

Bounded post-merge verification of Runner 1 PR #623, its exact-head Actions evidence, the still-open PR #610 overlap, the owner-directed two-runner proposal PR #625, documentation PR #626, and the current Gemini controller topology. No runtime dispatch, provider call, secret read, host mutation, merge, deployment, qualification, or acceptance was performed.

## Immutable refs and repository state

- Repository: https://github.com/VlDMlNSh/mediahub-os
- PR #623 is **MERGED**. Head: `504507a4335e353e8adac90d755f002ff476f33b`; merge commit: `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`; base recorded by PR: `af200c4323bd4cb7cfa4c47dab4accc10049d1ec`.
- Runner 1 workflow on main has blob SHA `12b684bbd3d475d64cac7e37bbaf64c65ce40529`.
- Gemini controller on main has blob SHA `0a1246f6755020faf8b7e48d07bfff790bbaece3`.
- Canonical documentation branch remains `docs/mediahub-chat-tree-map-20261012`; working documentation PRs are not canonical until merged.

## PR #623 — merged source, no live runtime qualification

Six PR-head workflow runs at the PR head completed SUCCESS:

| Workflow | Run ID | Job ID | Result |
|---|---:|---:|---|
| Provider contract verification | 41390337694 | 125100107720 | SUCCESS |
| Gemini workflow contract validation | 41390337866 | 125100108291 | SUCCESS |
| Astra Verify | 41390337860 | 125100108231 | SUCCESS |
| AI Factory verification | 41390337755 | 125100108516 | SUCCESS |
| Ollama local inference runtime | 41390337883 | 125100108594 / 125100108928 / 125100126198 | SUCCESS, PR no-op only |
| Astra Cloud Runtime Validation | 41390337707 | 125100107761 | SUCCESS |

The Ollama workflow run explicitly followed the pull-request path. The live job's marker step succeeded; FCC checkout, capacity/install, ECC checkout, Ollama installation, model pull/inference, FCC service, Claude Code installation/invocation, and evidence upload were all **SKIPPED**. The separate contract test job succeeded. Therefore PR #623 establishes source integration and deterministic contract CI, not live Ollama inference, FCC 401/200, Claude invocation, persistence, or Ubuntu runner qualification.

PR #623 has zero formal submitted reviews and zero inline review threads. Merge status is not independent security review or runtime acceptance.

## PR #610 — unresolved overlapping candidate

PR #610 remains OPEN at head `cac44b8a867945d4b544c3e46bd819bc42373f36`, with base metadata `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`. Its changed files include the same Runner 1 workflow and contract-test paths as merged PR #623, plus historical architecture/checkpoint material. It is not safe to treat it as a second implementation or merge it without a path/commit-level unique-change reconciliation against current main. Its one recorded review is a COMMENTED review authored by the repository owner, not an independent approval. No merge or cherry-pick was performed.

## PR #625 and #626 — documentation proposals

- PR #625 remains OPEN, head `2c06a56eb2f3a5f265a5f558f3d02a80221eb022`, base `d9a289b9113f7567711b641a7017eb814d6c259d`, with zero formal reviews and zero inline threads. It proposes the owner-directed topology: Runner 1 Ubuntu with Ollama/FCC/Claude Code/ECC; Runner 2 Ubuntu with three isolated Gemini agents. It is a proposal, not an accepted topology or deployed infrastructure.
- PR #626 remains OPEN, head `7c94e83b859917d8b066c34ac9204a61ac3fab47`, base `d9a289b9113f7567711b641a7017eb814d6c259d`, with zero formal reviews and zero inline threads. Its Wave 519 report correctly described PR #623 as open at the time, but that status is now stale after PR #623 merged. This Wave 520 report supersedes that single status observation; PR #626 itself is not updated or accepted by this report.
- Exact-head CI for PR #625 and PR #626 was not established by the available PR-triggered workflow-run lookup; mark NOT VERIFIED, not PASS.

## Gemini controller topology and admission

- Controller source blob on main: `0a1246f6755020faf8b7e48d07bfff790bbaece3`.
- The controller currently launches three separate child workflows; the child workflows declare independent `runs-on: ubuntu-latest` jobs. This is not one co-located Runner 2 host with three isolated containers.
- The controller source references `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY`, and `MEDIAHUB_GEMINI_BATCH_ENABLED`; this source evidence does not prove that repository/org secret and variable metadata are present, correctly scoped, or authorized. Secret values were not accessed.
- No successful trusted-main no-secret probe or independent security review was verified in this pass.
- Gemini Agent 1/2/3: **NOT RUN**. No controller run ID, child run/job IDs, artifacts, or provider invocations exist for this pass.

## Architecture and governance constraints

The canonical Bootstrap on the documentation branch still identifies the separate Alamo/local Claude executor route and prohibits silently substituting a GitHub-hosted runner. PR #625 proposes superseding that placement constraint in line with the newer owner-directed Runner 1 topology, but the proposal is unmerged and has no independent review. Until the applicable route contract is formally reconciled and accepted, do not infer that the Claude-on-Ubuntu runtime path is authorized merely because its workflow source is merged.

## Status

- PR #623 source integration: **MERGED**.
- PR #623 deterministic exact-head contract CI: **SUCCESS**.
- Runner 1 live Ollama/FCC/Claude runtime: **NOT RUN**.
- PR #610 overlap disposition: **OPEN / NOT RECONCILED**.
- Runner 2 same-host co-location: **NOT IMPLEMENTED**.
- Gemini dispatch: **BLOCKED / NOT RUN**.
- Secret/variable metadata and effective governance: **NOT VERIFIED**.
- PR #625 / #626 independent review and exact-head CI: **NOT VERIFIED**.
- Contour A: **NOT ACCEPTED**. Contour B: **GATED**.

## Next bounded work

1. Reconcile PR #610 unique changes against current main; do not merge duplicate Runner 1 workflow/test paths.
2. Update PR #626's Wave 519 status note with this Wave 520 post-merge evidence, or close it in favor of a consolidated evidence PR after reviewing its full diff.
3. Implement and independently test a single-host Runner 2 controller design with three isolated agent containers, retaining immutable target SHA, HMAC envelopes, replay protection, per-agent workspaces/quotas, and controller-secret isolation.
4. Complete independent controller security review, trusted-main non-launching probe, and metadata-only verification of required secrets/variables before any Gemini batch dispatch.
5. Resolve the canonical Claude placement contract against the owner-directed Runner 1 topology before live Claude invocation.

## Canonical references

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #610](https://github.com/VlDMlNSh/mediahub-os/pull/610)
- [PR #623](https://github.com/VlDMlNSh/mediahub-os/pull/623)
- [PR #625](https://github.com/VlDMlNSh/mediahub-os/pull/625)
- [PR #626](https://github.com/VlDMlNSh/mediahub-os/pull/626)
