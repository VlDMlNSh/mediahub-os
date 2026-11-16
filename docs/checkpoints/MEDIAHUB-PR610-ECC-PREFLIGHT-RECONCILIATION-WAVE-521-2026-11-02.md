# MediaHub OS — PR #610 ECC preflight reconciliation and documentation freshness — Wave 521

Date: 2026-11-02

## Scope and disposition

Read-only source and governance reconciliation of the merged Runner 1 implementation, the overlapping PR #610 candidate, the owner-directed two-runner proposal, the current Gemini controller, and the canonical documentation branch. This report proposes preservation of selected PR #610 changes; it does not merge, cherry-pick, dispatch, qualify, deploy, or accept any runtime.

## Immutable repository refs

- Repository: https://github.com/VlDMlNSh/mediahub-os
- `main` HEAD: `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0` (PR #623 merge).
- Runner 1 workflow on main: blob `12b684bbd3d475d64cac7e37bbaf64c65ce40529`.
- Runner 1 contract tests on main: blob `a3cf0c8fffbe5fd049144619d388354b4704b1d8`.
- Gemini controller on main: blob `0a1246f6755020faf8b7e48d07bfff790bbaece3`.
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`, observed HEAD `d9a289b9113f7567711b641a7017eb814d6c259d`.
- Canonical map blob: `75f62685459ec99ebf8be478f4e9096cdb842b1d`; checkpoint blob: `fd312ded05dd1898bd36d776a9669bb02920720d`; Master Roadmap blob: `ea7e94e921045253f3e6494438e197c4bafae3a0`; Bootstrap blob: `75f30750183efe8c6877368e9f0ada48f8e81ea7`.

## Finding 1 — PR #610 is not a pure duplicate

PR #610 remains open. Its latest evidence report identifies working head `cac44b8a867945d4b544c3e46bd819bc42373f36`. Comparing that ref with current main returns `diverged`, 92 commits ahead and 2 behind, with merge base `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`. A whole-branch merge or cherry-pick is therefore unsafe.

The overlapping source paths are materially different:

| File | Current main | PR #610 candidate |
|---|---|---|
| Runner workflow | `12b684bbd3d475d64cac7e37bbaf64c65ce40529` | `dd6a577f6c704b0453fcd5b05754d10967f8babb` |
| Contract tests | `a3cf0c8fffbe5fd049144619d388354b4704b1d8` | `2cf879635b68008b90af2e1ae0ec831f1b5a65a1` |

The PR #610 workflow adds two distinct pull-request-only checks absent from the current main version:

1. `ecc-profile-preflight`: checks out ECC at commit `c05b2d6614f62f6db0047669aa4eefb223d478f9`, verifies the MIT license and three selected skill blobs (verification-loop, security-review, search-first), assembles advisory guidance, and explicitly avoids installing ECC plugins, hooks, MCP servers, or another control plane.
2. `fcc-claude-install-preflight`: checks out FCC at immutable commit `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`, verifies its entry points, installs pinned Claude Code `2.1.282`, and checks the preflight without provider credentials or inference.

The candidate test file has 10 tests, including ECC-guidance-only assertions, the PR preflight gates, and Ollama systemd/process isolation. Current main has 9 tests and includes a separate FCC settings assertion covering absent cloud credentials, proxies and fallbacks. That main coverage must be preserved; replacing the main test file with PR #610's version would lose it.

PR #610 also contains a Wave 509 terminology correction and branch-only Wave 496/497/498/500 addenda, a continuation prompt, and other historical evidence. These are unique documentary changes, not reasons to merge the entire diverged branch.

**Decision:** retain PR #610 as an evidence/source candidate; do not merge it wholesale. The smallest useful follow-up is a new branch from current main that selectively ports the two preflight jobs and their tests while preserving all current-main assertions. Require exact-head CI and an independent formal review before considering merge.

## Finding 2 — CI evidence must be scoped to the exact ref

The Wave 510 report records 10/10 contract tests and successful ECC and FCC/Claude installation preflights on implementation SHA `d217d2de332b07b30866635750aac910375525a5`. PR #610's current body also records five required contexts and a successful runner workflow on a later branch SHA. However, the connected exact-SHA workflow-run and combined-status lookups for `cac44b8a867945d4b544c3e46bd819bc42373f36` returned empty results in this pass. Therefore current exact-head CI is **NOT VERIFIED by this recheck**; prior report/body claims are preserved as historical evidence, not promoted to a fresh PASS.

PR #623 is merged at main SHA above. Wave 520 records six successful PR-head workflow runs, but the Ollama runner was a pull-request no-op: live Ollama installation, model pull/inference, FCC service, Claude Code invocation, and artifact upload were skipped. Runner 1 source integration and contract CI are established; live runtime qualification is **NOT RUN**.

## Finding 3 — canonical documentation is stale

The canonical documentation branch HEAD is `d9a289b9113f7567711b641a7017eb814d6c259d`, not main. Read-back of its current files shows:

- Map blob `75f62685459ec99ebf8be478f4e9096cdb842b1d` begins with Wave 477 (2026-10-30) and contains no Wave 520 or Wave 523 entry.
- Continuation checkpoint blob `fd312ded05dd1898bd36d776a9669bb02920720d` begins with Wave 392 (2026-10-22).
- Master Roadmap blob `ea7e94e921045253f3e6494438e197c4bafae3a0` begins with Wave 458 (2026-10-29).
- The Wave 520 report exists on its working documentation branch and in open PR #627, but is not indexed in the canonical map/checkpoint.

This is a verified documentation freshness gap. This Wave 521 report and its index/checkpoint entries are therefore proposed on a separate documentation branch based on the exact canonical branch HEAD. The canonical branch remains unchanged until review and merge.

## Finding 4 — two-runner and Gemini admission remain blocked

PR #625 proposes Runner 1 (Ollama/FCC/Claude Code/ECC) and Runner 2 (three isolated Gemini agents on one Ubuntu host). It remains an unaccepted documentation proposal. Its body and the Wave 520 report disagree on the candidate PR head (`01efb5e6264b4cb84aee1d9c0c162be77cd1f264` versus `2c06a56eb2f3a5f265a5f558f3d02a80221eb022`); exact current head is **DISPUTED / NOT VERIFIED**. Formal reviews are zero and exact-head CI was not established.

Main's Gemini controller currently dispatches three separate child workflows to separate `ubuntu-latest` jobs. It does not implement the owner-requested co-located Runner 2 with three isolated containers/workspaces.

The controller source references `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY`, and `MEDIAHUB_GEMINI_BATCH_ENABLED`. Source references do not prove secret/variable presence, effective scope, token permissions, or governance. No secret values were accessed. No trusted-main no-secret probe was verified. The available GitHub connector exposes no workflow-dispatch action, so this pass did not dispatch the probe or agent workflows. An Issue #301 owner `/next` comment is a launch-capable path, not a safe substitute for the missing probe and review gates.

Gemini Agents 1/2/3: **NOT RUN**. Controller run ID, child run/job IDs, artifacts and artifact digests: **NONE FOR THIS PASS**.

## Required next work

1. Create a source branch from current main and selectively port PR #610's ECC and FCC/Claude PR preflight jobs plus focused tests; preserve current-main FCC configuration and no-fallback assertions.
2. Re-run the five required ruleset contexts and the runner contract suite on the exact new head; obtain an independent formal APPROVED review.
3. Reconcile PR #610's unique Wave 509 terminology/addendum material separately from runtime code; do not merge the diverged branch wholesale.
4. Reconcile PR #625's exact head and obtain independent review plus exact-head CI before treating the two-runner placement as accepted.
5. Implement and test the same-host Runner 2 design only after the controller's existing HMAC, replay, least-privilege and isolation contracts are preserved.
6. Verify secret/variable metadata and effective token scope without reading values; run the authorized non-launching trusted-main probe before any Gemini batch.
7. Keep live Runner 1 smoke owner-gated and separate from PR CI. Do not claim runtime qualification from no-op checks.

## Status

- Runner 1 source integration: **MERGED**.
- Runner 1 live runtime: **NOT RUN / NOT QUALIFIED**.
- PR #610 unique ECC/FCC preflight: **IDENTIFIED / NOT PORTED**.
- PR #610 full-branch integration: **BLOCKED / UNSAFE AS A WHOLE**.
- Canonical map/checkpoint/roadmap freshness: **STALE; update proposed in this documentation PR**.
- Runner 2 same-host implementation: **NOT IMPLEMENTED**.
- Gemini controller admission and security review: **NOT VERIFIED**.
- Gemini Agents 1/2/3: **NOT RUN**.
- Contour A: **NOT ACCEPTED**. Contour B: **GATED**.

## Canonical navigation

- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [PR #610](https://github.com/VlDMlNSh/mediahub-os/pull/610)
- [PR #623](https://github.com/VlDMlNSh/mediahub-os/pull/623)
- [PR #625](https://github.com/VlDMlNSh/mediahub-os/pull/625)
- [PR #627](https://github.com/VlDMlNSh/mediahub-os/pull/627)

This report is a proposed documentation update only. It is not a runtime qualification certificate, controller authorization, topology acceptance, or merge approval.
