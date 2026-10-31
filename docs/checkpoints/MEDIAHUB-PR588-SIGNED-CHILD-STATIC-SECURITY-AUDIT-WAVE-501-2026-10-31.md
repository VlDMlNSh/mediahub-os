# Wave 501 — PR #588 signed child static security audit

- Date: 2026-10-31
- Target: PR #588 exact HEAD `0d83e2033eb97e9661816706186cf059b4ae9713`
- Base: `main` SHA `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`
- Status: **PRELIMINARY STATIC AUDIT COMPLETE / REPLAY CONTROL BLOCKED / CONTROLLER INTEGRATION NOT IMPLEMENTED / INDEPENDENT REVIEW NOT VERIFIED / NO DISPATCH**
- This is an orchestrator source audit, not an independent Gemini review or formal GitHub approval.

## 1. Source identity and exact-head evidence

PR #588 remains OPEN / DRAFT / UNMERGED, 10 commits ahead and 0 behind main, with 10 changed files. Exact target SHA was re-read from PR metadata and compared to main using GitHub compare API.

Source blobs:
- `.github/workflows/gemini-pr-readonly-review-wave471.yml`: `85174e24b7d213ce7d90a4bd215ec4fbac32c605`.
- `tests/test_gemini_pr_readonly_review_wave471_contract.py`: `3ac7428a3054334842f4774f1fee3f49027cf51a`.
- `tests/test_gemini_child_signed_dispatch_runtime_contract.py`: `4ffb6d28e835814937bb4668dd3b2306df4426af`.
- Main controller `.github/workflows/gemini-batch-dispatch-controller.yml`: `0a1246f6755020faf8b7e48d07bfff790bbaece3`.

Five required ruleset workflow executions reported terminal SUCCESS on the exact PR #588 SHA:
- Astra Verify run 41016734247.
- Astra Cloud Runtime Validation run 41016734246.
- AI Factory verification run 41016734258.
- Provider contract verification run 41016734368.
- Gemini workflow contract validation (Wave 284) run 41016734271.
- Non-launching controller probe run 41016734294: probe/assertion succeeded; admission and dispatch skipped.

Formal PR reviews: 0. Inline review threads: 0. Independent A3 review: NOT VERIFIED.

## 2. Positive source properties

The child:
- Requires workflow_dispatch inputs for UUIDv4 dispatch ID, numeric PR number, full lowercase base/head SHAs, fixed task and HMAC signature.
- Restricts execution to the expected repository and `refs/heads/main`.
- Checks HMAC-SHA256 using constant-time comparison.
- Requires an open PR based on main, exact base/head SHA equality and same-repository head.
- Verifies authorization before the job that maps the Gemini API key.
- Checks out the immutable head SHA with `persist-credentials: false`, fetches full history, and builds a base..head patch plus changed-file list and provenance manifest.
- Grants contents:read and pull-requests:read; the Gemini tool allowlist is read-only.
- Pins external GitHub Actions to full commit SHAs.
- Instructs the model to treat patch/repository content as untrusted and prohibits edits, dispatch, external provider calls, merge, deployment and unsupported test claims.

These are source-level observations, not runtime qualification.

## 3. Blocking findings

### B1 — No durable replay receipt / atomic claim

The child validates UUIDv4 and HMAC but does not persist or atomically claim the dispatch ID. The concurrency group serializes matching PR/head jobs with `cancel-in-progress: false`; serialization is not deduplication. A repeated valid dispatch can therefore start another review run.

Required remediation:
- Use a durable repository-controlled receipt/claim keyed at minimum by repository + PR number + head SHA + dispatch ID (or a deliberately defined idempotency key).
- Atomically transition absent → claimed before model credentials are available.
- Define terminal states and expiry/retention.
- On duplicate, return the original receipt/result and do not invoke Gemini again.
- Test simultaneous duplicate requests and crash windows around claim, dispatch and receipt finalization.
- Do not implement a best-effort first-page workflow-run search as the sole durable replay control.

### B2 — Existing controller cannot construct the child request

The main controller's signed payload currently binds `workflow_file`, `dispatch_id`, `target_sha`, `task`, `base_ref`, and `scope`. The PR child independently requires `pr_number` and `base_sha` in its signed payload. The current generic dispatch input builder does not provide these fields.

Required remediation:
- Add a distinct fixed PR-review controller mode; do not mutate the existing FCC review task.
- Resolve PR metadata from GitHub API, require open/same-repository/base-main, capture immutable base/head, and recheck exact metadata before signing.
- Sign the exact child schema including PR number, base SHA, head SHA, fixed task, dispatch ID and workflow identity.
- Do not accept arbitrary task text, caller-supplied repository, or caller-supplied file paths.
- Keep the existing general three-agent batch and FCC-specific review route behavior unchanged.

### B3 — Child workflow is absent from default branch

A direct default-branch lookup for `.github/workflows/gemini-pr-readonly-review-wave471.yml` returned 404. The child currently exists only on PR #588. It must not be manually dispatched from the PR branch. The default-branch bootstrap dependency is therefore unresolved.

Required remediation:
- First complete the required independent review and all integration gates for the bootstrap change.
- Integrate the minimal child workflow onto main only through the normal protected/reviewed path.
- Re-read the exact main file and blob SHA after integration before enabling controller dispatch.
- Do not use a PR-only workflow_dispatch as a substitute.

## 4. Additional verification gaps

- The child manifest records PR/base/head and changed-file names but does not include per-file blob identities or a digest of the generated patch inside the manifest. Add deterministic patch digest and file blob identities (or explicitly document why the artifact digest is the sole binding).
- The artifact upload is unconditional after the Gemini step, but no independent runtime evidence exists that a review artifact was produced, retained, downloaded and inspected. Artifact digest/run provenance must be verified by the controller after execution.
- Static contract tests are source-string assertions. The PR-specific child has no dedicated executable synthetic-key authorization suite in the inspected test file. The shared executable child suite currently enumerates only the pre-existing four child workflows and does not include this PR-review child.
- Exact presence/scope of `MEDIAHUB_DISPATCH_HMAC_KEY`, `GEMINI_API_KEY_2`, `GEMINI_MODEL`, `MEDIAHUB_GITHUB_TOKEN` and the admission variable remains NOT VERIFIED. No secret values were accessed.

## 5. Required negative/behavioral tests before controller use

1. Valid synthetic-key request succeeds against mocked GitHub PR metadata.
2. Invalid HMAC, altered task, altered PR number, altered base/head, malformed SHA, malformed UUID and malformed PR number fail before Gemini credentials are exposed.
3. Closed PR, wrong base, foreign head repository and changed PR head/base are rejected.
4. Duplicate and concurrent dispatch IDs produce exactly one model invocation.
5. Crash after claim, API timeout, accepted dispatch with lost response, and missing child run reconcile without duplicate dispatch.
6. Child run with failed/cancelled/skipped/empty Gemini result cannot produce PASS.
7. Missing/expired/malformed artifact, empty patch, missing changed-file list and manifest/patch digest mismatch fail closed.
8. Every result binds repository, PR number, base/head SHA, controller run ID, child run/job IDs, artifact name and digest.

## 6. Disposition and next step

| Gate | State |
|---|---|
| PR #588 five required workflow executions | SUCCESS |
| Controller no-secret probe | SUCCESS; dispatch SKIPPED |
| Source review by this orchestrator | PRELIMINARY COMPLETE |
| Independent A3 review | NOT VERIFIED |
| Durable replay protection | BLOCKED / NOT IMPLEMENTED |
| Controller PR/base/head/HMAC route | NOT IMPLEMENTED |
| Default-branch child workflow | ABSENT |
| Secret/variable presence and scope | NOT VERIFIED |
| Gemini child dispatch | NOT RUN |
| Qualification / acceptance | NOT ACCEPTED |

Next bounded engineering packet: implement only the durable replay receipt contract and its synthetic-key concurrency/crash tests on a dedicated branch, then separately implement controller PR metadata binding/signing. Preserve the default-branch bootstrap and independent review gates. Do not dispatch Gemini until all blockers close.

## 7. Scope

No repository runtime, secret, provider, infrastructure or workflow dispatch was changed. No Gemini agent, model inference, live smoke, merge, deployment, qualification or acceptance occurred.
