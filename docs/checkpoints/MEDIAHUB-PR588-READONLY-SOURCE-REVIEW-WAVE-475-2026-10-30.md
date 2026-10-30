# MediaHub OS — PR #588 read-only source review and CI trigger follow-up (Wave 475)

**Date:** 2026-10-30  
**Disposition:** PRELIMINARY STATIC REVIEW COMPLETE; INDEPENDENT REVIEW NOT VERIFIED  
**Repository:** `VlDMlNSh/mediahub-os`  
**Canonical documentation branch:** `docs/mediahub-chat-tree-map-20261012`  
**Code branch:** `feat/pr-scoped-readonly-review-wave471`  
**PR:** [#588](https://github.com/VlDMlNSh/mediahub-os/pull/588), OPEN / DRAFT / UNMERGED  
**Immutable reviewed head:** `c65897f2a4ff594b69a98ce739aace244147c926`  
**Base/main:** `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`  
**Branch relation:** 8 ahead / 0 behind, merge base equals main.

## 1. Purpose and scope

This pass performed a read-only, source-level review of all nine files in the current PR diff. It is an internal preliminary review, not an independent A3 review or formal PR review.

The pass also closed a CI-gate defect found after Wave 474: path-filtered workflows that publish required status contexts may be absent on unrelated PRs. All five required workflows now run for every PR targeting `main`; their PR triggers no longer use `paths` or `paths-ignore`. The Astra Verify push-only filter remains unchanged.

## 2. Exact changed-file inventory

| File | Blob SHA |
|---|---|
| `.github/workflows/astra-cloud.yml` | `14f37463670129bee5e84bb7e632751a2beca088` |
| `.github/workflows/astra-verify.yml` | `7a70ff2b0e7b058fcf1ee9fd59a53628df864141` |
| `.github/workflows/gemini-pr-readonly-review-wave471.yml` | `85174e24b7d213ce7d90a4bd215ec4fbac32c605` |
| `.github/workflows/gemini-workflow-contract-validation-wave284.yml` | `7e7b809013361245677a310403aabc2150af7aaf` |
| `.github/workflows/mediahub-ai-factory-verification.yml` | `93e731afcbff0a99dd1c41d62b202dcfa3dc1fa6` |
| `.github/workflows/mediahub-provider-contract-verification.yml` | `3194a046efa62ebf7932bca124ad28fc4bb6c513` |
| `tests/test_gemini_controller_trigger_path_coverage_contract.py` | `35ccdc10d2eb983a5e9e3184d974b1714282e46c` |
| `tests/test_gemini_pr_readonly_review_wave471_contract.py` | `3ac7428a3054334842f4774f1fee3f49027cf51a` |
| `tests/test_ruleset_required_contexts_wave474_contract.py` | `fe91f629af1b8cf2aaf623ad7ab6d143b5320e5e` |

## 3. Exact-head CI evidence

Active ruleset: `MediaHub-main-autonomous-merge`, ID `26108066`, enforcement ACTIVE. Its five exact required contexts were all present and SUCCESS on PR head `c65897f2a4ff594b69a98ce739aace244147c926`:

| Required context | Workflow run / job | Result |
|---|---:|---|
| Astra Verify | [41016101267](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016101267) / 123932662277 | SUCCESS |
| Astra Cloud Runtime Validation | [41016101271](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016101271) / 123932662331 | SUCCESS |
| Gemini workflow contract validation (Wave 284) | [41016101312](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016101312) / 123932662449 | SUCCESS |
| AI Factory verification | [41016101268](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016101268) / 123932662244 | SUCCESS |
| provider contract verification | [41016101355](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016101355) / 123932662460 | SUCCESS |

The Gemini validation job passed actionlint, legacy/Wave 292 caller-context checks, reusable-workflow, transport, executable old-child HMAC, controller-trigger and new ruleset-context tests. Astra Verify compile, full unit suite and signed-command smoke test passed. Astra Cloud tests passed. AI Factory and provider contract jobs passed.

Controller no-secret PR probe [41016101286](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41016101286): probe and caller-context assertion SUCCESS; admission and `dispatch_and_monitor` SKIPPED. No Gemini child agent was dispatched.

## 4. Static review findings

### F-01 — BLOCKER: workflow-dispatch bootstrap sequencing is unresolved

The PR-scoped child currently exists only on the PR branch, not on `main`. GitHub documents that a `workflow_dispatch` workflow only receives events when its workflow file exists on the default branch. The trusted controller runs from `main`, so it cannot yet use this file as a dispatchable child before the file is integrated into the default branch.

Therefore this child cannot provide its own independent review for the PR that introduces it. Use a separately qualified reviewer or establish a separately approved bootstrap sequence; do not manually dispatch or merge around this dependency.

Reference: [GitHub Actions — Triggering a workflow](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).

### F-02 — BLOCKER: replay protection is not enforced by the child

The HMAC binds a UUIDv4 `dispatch_id`, PR number, base SHA, head SHA, fixed task, workflow filename, base ref and scope. The child verifies the signature and rechecks PR state/base/head/repository before the model-credential job. It does not, however, consume or persist a one-time dispatch ID. Its concurrency group is keyed by PR/head and is not a durable replay ledger.

Before enabling a controller route, implement durable idempotency and ambiguous-dispatch reconciliation in the trusted controller, with a verifiable request receipt and run correlation. Do not rely on concurrency alone to suppress replay.

### F-03 — BLOCKER: behavioral coverage for the new child is absent

`tests/test_gemini_pr_readonly_review_wave471_contract.py` is structural/static. The existing executable HMAC runtime suite `tests/test_gemini_child_signed_dispatch_runtime_contract.py` enumerates four previous child workflows and does not execute the PR-scoped child authorizer. Thus the green “executable child HMAC” CI step does not prove this new child's HMAC or PR-metadata behavior.

Add an isolated behavioral harness for the actual PR-child authorizer, with a stubbed `gh api` response and synthetic test key. Cover valid signature, missing/invalid HMAC, malformed IDs, wrong repository/ref, closed or fork PR, changed base/head SHA, fixed-task mismatch, duplicate/replay and ambiguous controller dispatch. No network access or real secret is needed for these tests.

### F-04 — NOT VERIFIED: secret-name configuration

The child references `MEDIAHUB_DISPATCH_HMAC_KEY` and `GEMINI_API_KEY_2`. Secret values were not read. The presence/availability of both exact secret names in GitHub settings was not independently verified in this pass. This blocks a dispatch trial until their exact names are checked against live repository configuration and the project contract.

### F-05 — WATCH: static ruleset mapping can drift

The new regression test hard-codes the five required contexts and workflow/job mapping. It matches the current live ruleset and exact-head check-runs, but does not fetch the remote ruleset. A later ruleset change must update the mapping or add a separately trusted configuration-drift check.

## 5. Positive controls verified

- All five required check contexts are published under the exact current ruleset names.
- All five required PR workflows target `main` and have no PR `paths` or `paths-ignore` filter; their required jobs are not conditional.
- PR-scoped child permissions are read-only (`contents: read`, `pull-requests: read`); checkout uses a full-SHA pinned action and `persist-credentials: false`.
- Model credentials are mapped only in the review job, after successful authorization.
- Authorization checks full immutable SHAs, open PR state, base branch, same-repository head, fixed task and HMAC before model execution.
- Five required CI contexts and the non-launching controller probe are proven on the exact reviewed head.

## 6. Governance disposition

- PR #588: OPEN / DRAFT / UNMERGED; base main unchanged.
- Formal review submissions: 0. Inline review threads: 0.
- Independent A3 review: NOT VERIFIED. This static inspection is not independent acceptance.
- PR-specific controller integration: NOT IMPLEMENTED.
- Gemini Agent 1/2/3 dispatch: NOT RUN.
- Child workflow dispatch: NOT RUN.
- Provider inference / secret-value access: NOT RUN.
- Merge / deployment / qualification / acceptance: not performed.
- Contour A: NOT ACCEPTED. Contour B: GATED.

Do not mark the PR ready or merge solely on green CI. The exact-head CI gate is PASS; independent review, anti-replay and bootstrap/integration gates remain open.

## 7. Next bounded action

1. Resolve the default-branch bootstrap path with a qualified independent reviewer; the new child cannot dispatch until its workflow file is on the default branch.
2. Add synthetic-key behavioral tests for the actual new authorizer.
3. Implement controller-owned PR review routing with durable idempotency and ambiguous-outcome reconciliation; bind immutable PR/base/head and the fixed task.
4. Verify exact live secret-name availability without reading values.
5. Obtain independent A3 review of the full diff and controller change; rerun all five required contexts on the final immutable head.

## Links

- PR #588: https://github.com/VlDMlNSh/mediahub-os/pull/588
- Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Bootstrap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md
- Master Roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
