# Wave 476 — PR #588 replay and default-branch bootstrap blockers

**Date:** 2026-10-30  
**Status:** READ-ONLY SOURCE AUDIT / EVIDENCE RECONCILIATION  
**Canonical code target:** `0d83e2033eb97e9661816706186cf059b4ae9713`  
**Base / main:** `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`  
**PR:** [#588](https://github.com/VlDMlNSh/mediahub-os/pull/588) — OPEN / DRAFT / UNMERGED

## 1. Scope

Revalidated the moving PR head after Wave 475, reviewed the new synthetic-key HMAC authorization tests and the PR-specific child authorization workflow, and checked whether the child can currently be dispatched from the default branch. No code or workflow changes were made in this pass; this report records a bounded review of the current head and the remaining control-plane blockers.

## 2. Exact-head status

At the time of this pass PR #588 was OPEN / DRAFT / UNMERGED at `0d83e2033eb97e9661816706186cf059b4ae9713`, based on main `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`. The compare endpoint reports 10 commits ahead, 0 behind, with main as merge-base. The changed-file set contains ten files.

The active ruleset [MediaHub-main-autonomous-merge / 26108066](https://github.com/VlDMlNSh/mediahub-os/rules/26108066) requires these five exact contexts; all five completed SUCCESS on this exact head:

| Required context | Run | Result |
|---|---:|---|
| Astra Verify | [41016734247](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016734247) | SUCCESS |
| Astra Cloud Runtime Validation | [41016734246](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016734246) | SUCCESS |
| AI Factory verification | [41016734258](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016734258) | SUCCESS |
| provider contract verification | [41016734368](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016734368) | SUCCESS |
| Gemini workflow contract validation (Wave 284) | [41016734271](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016734271) | SUCCESS |

The Gemini validation job was `123934650485`; its steps show successful execution of actionlint, legacy/reusable/controller transport contracts, the executable child HMAC authorization suite, controller path coverage and the Wave 474 required-context regression contract.

The non-launching controller probe [41016734294](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016734294) completed SUCCESS. Its `dispatch_and_monitor` job was SKIPPED. This is probe evidence only; no child or agent was dispatched.

## 3. Synthetic-key authorization coverage now present

The latest commit `0d83e2033eb97e9661816706186cf059b4ae9713` adds PR-child authorization behavior to `tests/test_gemini_child_signed_dispatch_runtime_contract.py` (blob `4ffb6d28e835814937bb4668dd3b2306df4426af`). The new cases execute the actual authorization shell/Python script with a synthetic test key and a stubbed `gh api` response. They cover:

- valid signed inputs and exact open-PR metadata;
- missing HMAC key, invalid signature, wrong event/repository/ref;
- malformed PR number, base/head SHA and UUIDv4;
- task tampering before metadata lookup;
- closed PR, non-main base, changed base/head SHA and foreign head repository.

The child workflow is `.github/workflows/gemini-pr-readonly-review-wave471.yml`, blob `85174e24b7d213ce7d90a4bd215ec4fbac32c605`. It uses HMAC over workflow file, dispatch ID, PR number, base/head SHA and fixed task; it validates exact open-PR metadata before the model job. The review job has read-only repository permissions, checks out the exact head with `persist-credentials: false`, and uploads the diff/manifest inputs.

## 4. Blocking findings

### B1 — No durable replay protection

The child validates the signed `dispatch_id`, but the authorizer has no durable one-time receipt or atomic claim for that identifier. It performs signature/context/PR validation and then emits the PR/SHA outputs. Replaying the same valid signed request while the PR remains open at the same base/head therefore has no source-level duplicate barrier. The new tests do not exercise replay: they verify acceptance and rejection conditions, but no prior-use state is recorded or consulted.

**Disposition:** REQUIRES IMPLEMENTATION. Keep child read-only; the controller should own an atomic durable receipt/claim keyed by dispatch ID and bound to PR number, base SHA, head SHA and fixed task. Reconcile a lost/ambiguous dispatch response by exact dispatch ID and child run ID; never blindly retry an uncertain POST. Receipt-write failure or ambiguous receipt state must fail closed.

### B2 — Child workflow not dispatchable from the current default branch

The child workflow exists in PR #588 but is absent from `main` (the default-branch file lookup returned 404). GitHub's current documentation states that a `workflow_dispatch` workflow must exist on the default branch before the event can trigger it: [Manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow?tool=webui), [Events that trigger workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows).

The existing default-branch controller still exposes only its existing `probe`, `agents`, and FCC-pinned `review` route; it does not sign or dispatch this PR-specific child. The current controller review route remains pinned to FCC target `074f20eb495666946a14410ab88d566aaa754f24`, not an arbitrary PR.

**Disposition:** BLOCKED until the child and reviewed controller route are integrated to the default branch through the project's independent-review and merge gates. Do not manually dispatch the PR-only child.

### B3 — Secret-name presence NOT VERIFIED

The child source references `MEDIAHUB_DISPATCH_HMAC_KEY` and `GEMINI_API_KEY_2`, and the model variable `GEMINI_MODEL`. The controller references `MEDIAHUB_GITHUB_TOKEN` and `MEDIAHUB_DISPATCH_HMAC_KEY`. The connected GitHub interface rejected the Actions secret/variable listing endpoints; no values were requested or read. Presence and exact repository/environment scope therefore remain NOT VERIFIED. No aliases or secret renames were attempted.

### B4 — Independent review remains absent

PR #588 has zero formal review submissions and zero inline review threads. The local/source review in this wave is not a qualified independent A3 review. The workflow cannot be used to review its own pre-merge branch until it is available on the default branch; use a separately qualified reviewer path for the bootstrap review.

## 5. Current disposition

- Exact five-context required CI on `0d83e2033eb97e9661816706186cf059b4ae9713`: **PASS**.
- Controller no-secret/non-launching probe: **PASS**; dispatch job **SKIPPED**.
- PR-child HMAC negative/positive behavioral tests: **PASS in CI**.
- Replay resistance / durable one-time receipt: **NOT IMPLEMENTED / NOT VERIFIED**.
- Controller-owned PR-child routing: **NOT IMPLEMENTED**.
- Default-branch workflow availability: **BLOCKED** (child file absent from main).
- Exact live secret-name availability: **NOT VERIFIED**.
- Independent A3 review: **NOT VERIFIED** (0 reviews, 0 threads).
- Child dispatch / agent execution / provider call / secret read: **NOT RUN**.
- Merge / deployment / qualification / acceptance: **NOT performed**.
- Contour A: **NOT ACCEPTED**. Contour B: **GATED**.

Do not mark PR #588 ready or merge based on green CI alone.

## 6. Next bounded action

1. Prepare the controller-side PR review contract separately: fetch PR metadata; freeze and HMAC-bind PR number, base/head SHA, fixed task and dispatch ID; atomically claim a durable one-time receipt before POST; reconcile accepted/ambiguous dispatch outcomes by exact ID/run metadata; preserve the child as read-only.
2. Add synthetic-key tests for duplicate/replayed IDs, receipt-write conflicts, concurrent claims, lost/ambiguous POST reconciliation, malformed GitHub API responses and changed PR head between authorization and dispatch.
3. Resolve the default-branch bootstrap using a qualified independent reviewer before merging the child/controller route. Do not self-approve or bypass governance.
4. Verify exact secret-name availability and scope without reading values.
5. Rerun all five required contexts on the final immutable head and obtain independent A3 review.

## Links

- PR #588: https://github.com/VlDMlNSh/mediahub-os/pull/588
- Wave 475 report: [MEDIAHUB-PR588-READONLY-SOURCE-REVIEW-WAVE-475-2026-10-30.md](MEDIAHUB-PR588-READONLY-SOURCE-REVIEW-WAVE-475-2026-10-30.md)
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
