# MediaHub Wave 502 — Alamo hosted-runner execution-state correction and Gemini replay design audit

**Date:** 2026-10-31  
**Disposition:** PRELIMINARY AUDIT COMPLETE; runtime qualification and implementation remain NOT VERIFIED  
**Canonical code target:** `main` = `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`  
**Canonical documentation base:** `docs/mediahub-chat-tree-map-20261012` = `d9a289b9113f7567711b641a7017eb814d6c259d`  
**Governing issue:** [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## 1. Scope and immutable evidence

This pass corrects the interpretation of PR #610's successful check runs and tightens the replay-resistance requirements for PR #588. It does not dispatch Gemini, call a model provider, read secrets, merge, deploy, or qualify any runtime.

- PR #610: [open PR](https://github.com/VlDMlNSh/mediahub-os/pull/610), head `e099b99ba5a190a0d44ee03a2c0ff20a43732cb7`, base `main` at `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- PR #588: [open PR](https://github.com/VlDMlNSh/mediahub-os/pull/588), head `0d83e2033eb97e9661816706186cf059b4ae9713), base `main` at `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Main controller: `.github/workflows/gemini-batch-dispatch-controller.yml`, blob `0a1246f6755020faf8b7e48d07bfff790bbaece3`.
- PR #610 runner workflow: `.github/workflows/mediahub-alamo-fcc-claude-runner.yml`, blob `5878d6e91f52fb97342437078e5aa86d5252435a`.
- PR #610 runner contract test: `tests/test_mediahub_alamo_fcc_runner_contract.py`, blob `99d3af7a33f61e715e95cedf5d401acd2c392c86`.
- Active main ruleset: `MediaHub-main-autonomous-merge`, ID `26108066`; five required status contexts, zero required approving reviews, and required review-thread resolution.

## 2. Correction: PR #610 did not run Ollama, FCC, or Claude Code

The prior progress message stated that the Alamo candidate workflow had executed successfully. That statement was too broad and is corrected here.

Workflow run [41187561063](https://github.com/VlDMlNSh/mediahub-os/actions/runs/41187561063) was triggered by **pull_request**, not `workflow_dispatch`. Its jobs show:

| Job | Result | What actually ran |
|---|---|---|
| `dispatch-gate` | SUCCESS | PR event was denied live-run admission |
| `workflow-contract` | SUCCESS | Checkout, Python setup, static runner contract tests |
| `alamo-local-fcc-claude` | SUCCESS | Only the explicit PR skip-record step; all installation, Ollama, FCC, Claude Code, smoke and artifact-upload steps were SKIPPED |

Run artifacts: **none**. The `alamo-local-fcc-claude` job's green conclusion is a successful skip path, not a successful runtime smoke.

The workflow source explicitly makes the live installation and inference steps conditional on `workflow_dispatch`. No owner-dispatched live run was found in this evidence set. Therefore:
- Hosted Runner capacity: NOT VERIFIED by a live run.
- Ollama local model inference: NOT RUN.
- FCC installation/authentication: NOT RUN.
- Claude Code through FCC: NOT RUN.
- Runtime evidence artifact: NOT PRODUCED.
- Alamo equivalence: NOT VERIFIED (the PR itself correctly preserves this status).

PR #610 currently has zero formal reviews and zero inline review threads. It remains OPEN / UNMERGED. Do not mark its runtime acceptance gates complete.

## 3. PR #588: replay protection — refined finding

The main controller has a limited duplicate guard for owner `/next` issue-comment events: it queries recent controller workflow runs and looks for the source comment ID in the display title. This guard is not a durable, atomic receipt protocol.

Observed limitations:
1. It applies to the issue-comment route only; manual `workflow_dispatch` mode is not covered by this source-comment guard.
2. The lookup is a bounded workflow-run history query (first page, up to 100 results), not an authoritative receipt store.
3. The check-then-dispatch sequence is not an atomic claim. Concurrent/retried requests can race.
4. It is keyed to the source comment ID, not to a canonical signed PR-review operation identity binding repository, PR number, immutable base SHA, immutable head SHA, task ID and dispatch ID.
5. It does not durably model CLAIMED → DISPATCH_ACCEPTED/UNKNOWN → CHILD_RUN_BOUND → TERMINAL states or reconcile an ambiguous dispatch response from a durable record.
6. It does not provide a child-side one-time claim for the new PR-review child.

Thus the precise status is: **limited issue-comment duplicate suppression exists; durable atomic replay protection for the PR-scoped child remains NOT IMPLEMENTED / NOT VERIFIED.**

PR #588's own description correctly says the child is not integrated into the controller and must not be dispatched. The child is still absent from `main`; controller `review` mode remains pinned to the historical FCC review target. PR #588 remains OPEN / DRAFT / UNMERGED. Five required CI contexts were previously reported successful at its exact head, but independent A3 review remains NOT VERIFIED and the default-branch bootstrap is unresolved.

## 4. Required durable receipt contract before controller integration

Do not treat GitHub Actions concurrency groups, workflow history, artifacts, or cache entries as an atomic idempotency ledger.

The controller integration design must select and qualify one durable primitive with a server-enforced conditional create/compare-and-set operation. Candidate directions:

- **Append-only Git ref receipt ledger:** a deterministic receipt key, with atomic create-only refs for claim and subsequent immutable event records. This requires a narrowly scoped credential, explicit ref namespace governance, deletion/update protection, retention/recovery tests, and proof that the credential cannot alter application branches. Do not enable this path until those permission and ruleset properties are verified.
- **Dedicated transactional store:** a durable key-value/database record with conditional insert or compare-and-set, strict service identity, minimal scoped access, retention and backup. This requires an approved service and independent qualification.

A receipt identity must bind at least:
`repository_id + PR_number + base_sha + head_sha + fixed_task_id + dispatch_id`.
The canonical digest must be computed over a deterministic serialization. The signed request must bind the same fields. A claim must be created before any provider credential becomes available.

Minimum state machine:
- `CLAIMED`: unique key atomically acquired; only one caller can win.
- `DISPATCH_PENDING`: controller is preparing the GitHub API dispatch.
- `DISPATCH_ACCEPTED`: API returned definitive acceptance.
- `DISPATCH_UNKNOWN`: timeout/transport error leaves acceptance ambiguous; do not blindly redispatch.
- `CHILD_RUN_BOUND`: exact child run ID and workflow identity correlated to the same dispatch ID and target tuple.
- `SUCCEEDED`, `FAILED`, `CANCELLED`, `TIMED_OUT`, `REJECTED`: terminal outcomes, with immutable event evidence.
- Recovery/retry must first reconcile the existing receipt and child run; a new provider invocation is forbidden while the prior dispatch outcome is ambiguous.

Minimum behavioral test matrix:
- two concurrent identical claims: exactly one wins;
- same dispatch ID with changed PR/base/head/task: reject;
- exact replay after success/failure/cancel: no second child/provider invocation;
- timeout after API accepted but before response: reconcile existing child run, never blindly resend;
- crash after claim but before dispatch: recover without creating a second claim;
- crash after dispatch but before child-run binding: reconcile by dispatch ID and exact target tuple;
- expired/unknown receipt, missing child run, duplicate matching child runs: fail closed and report NOT VERIFIED;
- malformed UUID, signature mismatch, wrong repo/ref, closed PR, wrong base, foreign head repo, changed base/head: reject before model credentials;
- missing/empty artifact, missing digest, mismatched manifest/patch digest, failed/cancelled/skipped model step: never report PASS.

No live secrets or provider calls are needed for these synthetic-key tests.

## 5. Governance and execution disposition

The active main ruleset currently requires these five contexts: Astra Cloud Runtime Validation, AI Factory verification, provider contract verification, Astra Verify, and Gemini workflow contract validation (Wave 284). The same ruleset currently requires zero approving reviews. This does not satisfy the project's separate requirement for genuine independent A3 review; absence of a branch-protection requirement is not evidence of review.

No secret values were accessed. Presence/scope of `MEDIAHUB_GITHUB_TOKEN`, `MEDIAHUB_DISPATCH_HMAC_KEY`, `GEMINI_API_KEY_2`, `GEMINI_MODEL` and relevant admission variables remains NOT VERIFIED. No controller or child dispatch was performed in this wave.

| Area | Status |
|---|---|
| PR #610 workflow-contract CI | SUCCESS |
| PR #610 live Alamo/FCC/Claude run | NOT RUN |
| PR #610 artifact | NOT PRODUCED |
| PR #610 independent review | NOT VERIFIED |
| PR #588 required CI (previous exact-head evidence) | SUCCESS |
| PR #588 controller integration | NOT IMPLEMENTED |
| PR #588 child on default branch | ABSENT |
| PR-scoped durable atomic replay receipt | NOT IMPLEMENTED |
| Limited owner /next history guard | IMPLEMENTED; bounded/non-atomic |
| Gemini dispatch/provider inference | NOT RUN |
| Contour A | NOT ACCEPTED |
| Contour B | GATED |

## 6. Next bounded step

Build a non-production replay-receipt prototype and deterministic synthetic-key behavioral test suite on an isolated branch. First compare the append-only Git-ref design with a transactional store against credential scope, atomicity, retention, deletion protection, recovery and auditability. Do not modify the trusted controller or expose Gemini credentials until the primitive is qualified and independently reviewed.

Related:
- [PR #588](https://github.com/VlDMlNSh/mediahub-os/pull/588)
- [PR #610](https://github.com/VlDMlNSh/mediahub-os/pull/610)
- [PR #611](https://github.com/VlDMlNSh/mediahub-os/pull/611)
- [PR #612](https://github.com/VlDMlNSh/mediahub-os/pull/612)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Canonical map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
