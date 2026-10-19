# MediaHub Contour A — worker checkout credential minimization (Wave 176)

- Date: 2026-10-19
- Status: DRAFT IMPLEMENTATION CANDIDATE; CI IN PROGRESS AT REPORT TIME; NOT QUALIFIED.
- Candidate PR: [#375](https://github.com/VlDMlNSh/mediahub-os/pull/375), open Draft, base `main`.
- Governing tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301).
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).

## Change scope

Created branch `security/contour-a-worker-checkout-credential-minimization-wave176-20261019` from `main` at `c06015e0b1526e0aaa6a522306052b077455aba5`. Changed only two files:

1. `.github/workflows/astra-distributed-local-worker.yml`: top-level `permissions.contents` changed from `write` to `read`; all three `actions/checkout@v4` steps changed to `persist-credentials: false`.
2. `ops/qualification/test_worker_workflow_credential_policy.py`: added three dependency-free static regression tests for explicit read-only repository permission, no write-permission marker, and disabled persisted credentials on every checkout.

## Provenance and read-back

- Source workflow blob before edit: `f650f2416c19dc75b4a0eeec037661c0c6169910`.
- Candidate workflow blob after edit: `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`.
- Candidate test blob after edit: `4b3787368758f2dba4abd85325025cfbfbe59e9b`.
- Candidate head commit: `77352fc1224372b94e0a7d9b92288ca86b059cc2` (test-file commit; workflow change is the preceding commit).
- Branch comparison against `main`: ahead 2, behind 0, two changed files.
- Read-back inspection verified exactly three checkout steps, three explicit `persist-credentials: false` settings, zero `persist-credentials: true` settings, no `contents: write`, and three static tests with no third-party test dependency.
- PR-triggered workflow runs at exact head when queried: [Astra Cloud Runtime Validation](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39222837361) and [Astra Verify](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39222837322) were both `in_progress`. No passing CI is claimed. The unit test has not been executed in an isolated local environment in this pass.

## Security impact and limits

This reduces the worker workflow's GitHub permission and removes the checkout action's persisted Git credential from all three checkouts. It does not establish that the job can never access another credential, and does not fix the separate FCC auth token passed into the Claude subprocess. It does not provide OS or network isolation, define issuer/capability authority, validate the bootstrap publisher's provenance, or independently qualify the worker. No real credential was accessed; no worker dispatch, provider call, host change, merge, deployment, or qualification occurred.

## Next gates

1. Wait for and inspect exact-head CI for commit `77352fc1224372b94e0a7d9b92288ca86b059cc2`; execute the static test in an isolated test environment when available.
2. Independently review the workflow permission reduction, checkout behavior, and test assertions. Confirm no downstream step relies on checkout's persisted credential.
3. Establish the FCC authentication contract before changing the model subprocess environment. Continue synthetic-secret negative tests and explicit environment allowlisting as a separate change.
4. Keep PR #375 Draft until checks and independent review pass. Do not merge on CI alone.
5. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**; Contour B remains gated.
