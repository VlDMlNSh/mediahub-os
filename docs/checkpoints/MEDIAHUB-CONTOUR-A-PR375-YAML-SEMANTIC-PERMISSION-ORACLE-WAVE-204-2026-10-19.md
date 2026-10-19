# MediaHub OS Contour A — PR #375 YAML semantic permission oracle (Wave 204)

- Date: 2026-10-19
- Candidate PR: https://github.com/VlDMlNSh/mediahub-os/pull/375
- Governing issue: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Status: Draft candidate; no governance decision or security acceptance implied.

## Scope

Replaced the regex-oriented source inspection in `ops/qualification/test_worker_workflow_credential_policy.py` with PyYAML parsing. The test oracle inspects the parsed workflow and job permission mappings, rejects write permissions and write-all grants, and checks the three parsed `actions/checkout` steps for `persist-credentials: false`. It includes mutation tests for workflow-level write, job-level block/flow/quoted write, write-all, persisted checkout credentials, missing checkout, and invalid YAML.

The existing Astra Verify workflow already installs PyYAML before running tests, so this candidate adds no new package-install step. No workflow dispatch, worker execution, secret access, host command, Gemini/provider call, or runtime configuration change was performed.

## Exact-head evidence

- Candidate branch: `security/contour-a-worker-checkout-credential-minimization-wave176-20261019`.
- Candidate commit after syntax correction: `40ca9a2eabf69949134c941babd2624559f0cb1f`.
- Test blob read back at that exact commit: `67a9589b16332f1a07ee9ce7b73662d2ce23d237`.
- The intermediate commit `5d88a4506c02b3ec34d6549ba9d075ed35446113` failed Astra Verify at compileall because one new test assertion had an unclosed parenthesis. This failure was inspected from job logs, fixed in the next commit, and not hidden.
- Exact corrected-commit CI: [Astra Verify run 39294040201](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39294040201), job `verify` / `118201803921`, SUCCESS. Compile, Worker workflow credential policy regression tests, Cloud admission unit tests, and Signed command smoke test all succeeded.
- Exact corrected-commit cloud runtime validation: [Astra Cloud Runtime Validation run 39294040541](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39294040541), job `validate` / `118201804833`, SUCCESS.
- PR #375 was re-read after the correction: OPEN / Draft / unmerged; `head_sha=40ca9a2eabf69949134c941babd2624559f0cb1f`.
- Local offline validation of the semantic oracle and synthetic mutations passed 9 tests; the exact-commit CI above independently confirms the committed test file passed in the repository workflow.

## Interpretation and limitations

This closes the narrow test-oracle gap for the tested YAML forms and confirms CI on the corrected candidate SHA. It does not prove GitHub's complete permission evaluation semantics, server-side authorization, protection from duplicate-key parser ambiguities, safe output publication, trusted publisher provenance, FCC secret isolation, OS/network isolation, issuer/capability governance, or independent security acceptance. The workflow continues to use `contents: read` and `persist-credentials: false`; the unresolved direct `git push` path must not be treated as solved.

## Next action

Keep PR #375 Draft and unmerged. Independently review the semantic oracle and the worker's output-publication path; agree the issuer/capability contract through governance before implementing a trusted publisher. Reconcile the canonical map and continuation checkpoint with this report using read-back SHA evidence.

**Contour A remains NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED. Contour B remains gated.**
