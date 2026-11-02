# MediaHub owner-directed two-runner topology contract reconciliation — Wave 522

Date: 2026-11-02

## Purpose

Reconcile the current owner-directed two-runner proposal (PR #625 / Wave 517) against the controlling Issue #301, local routing Issue #296, GitHub-hosted Claude executor Issue #496, current Bootstrap, Master Roadmap and current Gemini controller source. This is a documentation/contract audit only.

## Immutable source refs

- PR #625 candidate HEAD: `2c06a56eb2f3a5f265a5f558f3d02a80221eb022`; base: `d9a289b9113f7567711b641a7017eb814d6c259d`.
- PR #625 compare: one commit ahead, zero behind; six changed files, 186 insertions, zero deletions.
- Canonical Bootstrap blob: `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Canonical Master Roadmap blob: `ea7e94e921045253f3e6494438e197c4bafae3a0`.
- Canonical checkpoint blob: `fd312ded05dd1898bd36d776a9669bb02920720d`.
- Current main Runner 1 workflow blob: `12b684bbd3d475d64cac7e37bbaf64c65ce40529`.
- Current main Gemini controller blob: `0a1246f6755020faf8b7e48d07bfff790bbaece3`.
- PR #623 merge commit: `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`.

## Contract reconciliation

### Issue #301 — cloud-agent fabric

Issue #301 prioritizes GitHub-hosted ephemeral workers, outbound HTTPS, runtime-only credential injection, no fixed egress assumptions, and explicit provider/data-route controls. It requires exact source refs, standards validation, independent review, immutable provenance and distinct execution/verification/qualification/acceptance states. The two-runner proposal is compatible as a target topology only if it retains these controls. It does not authorize dispatch or deployment.

### Issue #296 — Ollama/FCC route

Issue #296 requires an actual Ollama identity and model tag, a separately identified physical host/runtime, pinned and verified components, local-only fail-closed routing, no Anthropic/paid/cloud fallback, separate FreeLLMAPI route evidence, redacted tests and independent verification. PR #625 preserves the core non-paid/no-fallback conditions in the proposed Runner 1 placement, but does not provide live runtime evidence. The merged Runner 1 workflow is a source candidate only; live install/inference/FCC/Claude execution remains NOT RUN.

### Issue #496 — Claude Code placement

Issue #496 explicitly targets Claude Code on GitHub-hosted ephemeral runners, prohibits server 3/local host execution for that cloud lane, and requires provider route, terms, quota, budget, pinned actions/profile, non-launching contract tests, and explicit admission gates before dispatch. This supports the owner-directed Runner 1 placement and demonstrates that the old canonical Bootstrap's server-3-only binding is stale. PR #625's Bootstrap patch correctly replaces the placement rule while preserving non-paid/no-fallback and governance constraints.

### Current Bootstrap and controller

The current canonical Bootstrap still contains the historical separate server-3/Alamo placement language. PR #625 proposes a scoped supersession of that host-binding only; its new Bootstrap text preserves Wave 272/273 route requirements, controller-secret isolation and no alternate Gemini transport.

The current main Gemini controller blob `0a1246f6755020faf8b7e48d07bfff790bbaece3` dispatches three child workflows to three independent `ubuntu-latest` runner allocations. It does not provide one shared Runner 2 host. PR #625 correctly marks co-location NOT IMPLEMENTED and requires an architectural controller/worker change plus container, credential, resource and provenance boundaries.

## PR #625 file and evidence review

Changed files are:
1. `docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md`
2. `docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md`
3. `docs/architecture/MEDIAHUB-TWO-UBUNTU-RUNNER-TOPOLOGY-OWNER-DIRECTION-WAVE-517-2026-11-02.md`
4. `docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md`
5. `docs/checkpoints/MEDIAHUB-OWNER-DIRECTED-TWO-UBUNTU-RUNNER-TOPOLOGY-WAVE-517-2026-11-02.md`
6. `docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md`

The proposal is documentation-only; it does not change workflow/controller code. The PR currently has zero formal reviews and zero inline review threads. Exact-head workflow-run lookup returned no runs; exact-head CI is NOT VERIFIED. It must not be described as accepted or canonical yet.

## Stale statements requiring correction before acceptance

The Wave 517 documents/PR description cite PR #623 as an unmerged code candidate and reference older candidate SHA `4ded07da6c262aa47fdca19289e5479a1580318d`. PR #623 is now MERGED at `41c13e1c2b17ac48dc51c9963a9cda140f79ddb0`. The historical candidate SHA may remain as provenance, but the current status text must say merged source / contract CI only / live runtime NOT RUN. Do not use the old candidate SHA as current main HEAD or as evidence of runtime qualification.

The proposal also says Runner 1 and Runner 2 are Ubuntu roles. This is a target requirement, not proof of provisioned persistent Ubuntu VMs. Actual runner identity, lifecycle (hosted ephemeral vs self-hosted persistent), architecture, CPU/RAM/disk, labels and egress remain NOT VERIFIED.

## Disposition

- Owner-directed target topology: **SUPPORTED BY ISSUE #301/#296/#496; PROPOSED, NOT CANONICAL**.
- Bootstrap server-3-only placement: **STALE; supersession proposed in PR #625, not yet merged**.
- Runner 1 source: **MERGED**; runtime qualification **NOT RUN**.
- Runner 2 single-host co-location: **NOT IMPLEMENTED**.
- Gemini dispatch: **NOT RUN / BLOCKED pending all controller gates**.
- PR #625 exact-head CI and independent review: **NOT VERIFIED**.
- Contour A: **NOT ACCEPTED**; Contour B: **GATED**.

No workflow dispatch, provider call, secret read, runner provisioning, merge, deployment or qualification occurred.

## Required next step

1. Correct stale PR #623 state/SHA references in the Wave 517 report and PR #625 description without rewriting historical candidate provenance.
2. Obtain exact-head CI and independent formal review for PR #625; keep it non-canonical until merged.
3. Implement the Runner 2 same-host isolated-agent design as a separate reviewed code change only after controller contracts, trusted-main no-secret probe, metadata-only secret/variable scope and branch governance gates are verified.
4. Qualify Runner 1 only after permitted non-paid FCC route and runtime evidence are established.

## References

- [PR #625 — owner-directed two-runner topology](https://github.com/VlDMlNSh/mediahub-os/pull/625)
- [PR #623 — merged Runner 1 source](https://github.com/VlDMlNSh/mediahub-os/pull/623)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Issue #296](https://github.com/VlDMlNSh/mediahub-os/issues/296)
- [Issue #496](https://github.com/VlDMlNSh/mediahub-os/issues/496)
- [Canonical map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Canonical Bootstrap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Master Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
