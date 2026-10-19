# MediaHub Contour A — worker checkout credential minimization (Wave 176)

- Date: 2026-10-19
- Status: DRAFT IMPLEMENTATION CANDIDATE; dedicated static regression test now explicitly executed successfully in exact-head CI; independent review and qualification remain outstanding.
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
- Candidate head commit at initial report: `77352fc1224372b94e0a7d9b92288ca86b059cc2`; Wave 176 follow-up commit adds explicit CI invocation, resulting head `ad18328f940c2573707efd919778e8118e8c9723`.
- Branch comparison against `main` after CI wiring: ahead 3, behind 0, three changed files (`.github/workflows/astra-distributed-local-worker.yml`, `.github/workflows/astra-verify.yml`, and `ops/qualification/test_worker_workflow_credential_policy.py`).
- Read-back inspection verified exactly three checkout steps, three explicit `persist-credentials: false` settings, zero `persist-credentials: true` settings, no `contents: write`, and three static tests with no third-party test dependency.
- PR-triggered workflow runs at exact head when queried: [Astra Cloud Runtime Validation](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39222837361) and [Astra Verify](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39222837322) were both `in_progress`. No passing CI is claimed. The unit test has not been executed in an isolated local environment in this pass.

## Security impact and limits

This reduces the worker workflow's GitHub permission and removes the checkout action's persisted Git credential from all three checkouts. It does not establish that the job can never access another credential, and does not fix the separate FCC auth token passed into the Claude subprocess. It does not provide OS or network isolation, define issuer/capability authority, validate the bootstrap publisher's provenance, or independently qualify the worker. No real credential was accessed; no worker dispatch, provider call, host change, merge, deployment, or qualification occurred.

## CI recheck (2026-10-19)

Exact PR-head commit `77352fc1224372b94e0a7d9b92288ca86b059cc2` has two associated pull-request workflow runs, both completed successfully:
- [Astra Cloud Runtime Validation](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39222837361), run ID `39222837361`, job `validate` (`117961956367`) succeeded.
- [Astra Verify](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39222837322), run ID `39222837322`, job `verify` (`117961956042`) succeeded.

On the updated candidate HEAD `ad18328f940c2573707efd919778e8118e8c9723`, [Astra Verify run 39223502183](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39223502183) completed successfully. Job `verify` (`117964107846`) shows step `Worker workflow credential policy regression tests` completed with conclusion `success`; the executed command is `python -m unittest ops.qualification.test_worker_workflow_credential_policy`. [Astra Cloud Runtime Validation run 39223502235](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39223502235) also completed successfully. These CI results validate the candidate's automated checks, not independent security review or Contour A qualification.

## Next gates

1. Add mutation/negative-fixture coverage to prove the static policy tests reject a workflow that restores `contents: write` or `persist-credentials: true`.
2. Independently review workflow permission reduction, checkout behavior, and test assertions. Confirm no downstream step relies on checkout's persisted credential.
3. Establish the FCC authentication contract before changing the model subprocess environment. Continue synthetic-secret negative tests and explicit environment allowlisting as a separate change.
4. Keep PR #375 Draft until checks and independent review pass. Do not merge on CI alone.
5. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**; Contour B remains gated.
