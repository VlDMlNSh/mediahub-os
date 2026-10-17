# Gemini Contract CI Path-Filter Hardening — Wave 119

Date: 2026-10-18
Status: SOURCE CHANGE READ BACK / EXACT-HEAD CI PENDING / NOT APPROVED

## Objective

Make changes to the missing-credential manifest finalizer and its regression test reliably trigger the dedicated Gemini workflow-contract CI. Previously the validation workflow path filters watched the main workflow files and the Python test driver, but not the new helper or its standalone Node test. A helper-only change could therefore miss the contract workflow trigger.

## Live project refs and governing evidence

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`.
- Bootstrap blob SHA read this pass: `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Canonical map blob SHA read this pass: `4798bd288451000d6eff5bcb8f7f0855942f7181`; Contents API returned empty, so historical/current content was read through blob fetch in prior pass. Do not treat empty Contents response as empty map.
- Checkpoint blob SHA read this pass: `a1437086c2e98c743d3d2f0b17a3bd37c9fae7a8`.
- Master Roadmap blob SHA read this pass: `462466162f23242e170cd1f25395e6c899b5ddc3`.
- Governing [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN; it states that the queue is documentary rather than a live scheduler and that provider calls, dispatch, merge and deployment require their independent gates.

## Change made

On PR #334 branch `security/gemini-readonly-hardening-20261017`:

- Updated `.github/workflows/gemini-readonly-workflow-validation.yml` so both `push.paths` and `pull_request.paths` include:
  - `scripts/mark_gemini_missing_credential.js`
  - `scripts/test_gemini_missing_credential.js`
- Added `test_manifest_finalizer_changes_trigger_contract_ci` to `scripts/test_gemini_readonly_workflows.py`. It asserts that each path is present in both path filters and that the intended branch filters remain present.

## Read-back SHAs

- Workflow path filters blob: `c64504ed0107a63898c162405ed7d3fcfe70722b`.
- Contract test blob: `9585f9a091a881a51a4dfd28294dbb5847674d47`.
- PR #334 exact candidate HEAD: `1e66aae968c51dc232acc07723a965c3bd80cb6d`.

## Exact-head CI observed at last poll

- [Gemini Read-only Workflow Contract #39073129356](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39073129356): status pending, conclusion null; job list returned empty. Targeted contract tests/actionlint are NOT VERIFIED.
- [Astra Cloud Runtime Validation #39073129357](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39073129357): in progress; job `validate` was still installing test dependencies.
- [Astra Verify #39073129372](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39073129372): in progress; job `verify` was still installing a torrent test dependency.
- These generic runs are not substitutes for the dedicated contract job.

## Branch and PR state

PR [#334](https://github.com/VlDMlNSh/mediahub-os/pull/334) is OPEN / DRAFT / UNMERGED. Live compare to `main` HEAD `c06015e0b1526e0aaa6a522306052b077455aba5` is DIVERGED, 47 ahead / 2 behind; merge base `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`. PR metadata says mergeable, but that does not remove the branch-reconciliation or independent-review gates.

## Disposition and safety

The path-filter/test change is implemented and read back from GitHub. The dedicated contract CI has not yet provided executable evidence for it. No provider call, secret read, manual dispatch, merge, deployment, queue admission, or Contour A acceptance occurred. Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT PRODUCTION-ACCEPTED.

## Next bounded action

Poll the exact-head Gemini contract run and the generic checks. If the dedicated run remains pending with no jobs, investigate its workflow/trigger/concurrency state without manually dispatching the provider workflow. Once contract CI is green, expand executable provider-result/manifest tests, then obtain independent review and reconcile the 47-ahead / 2-behind branch losslessly.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
