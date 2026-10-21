# MediaHub OS — hash-lock verification and schema CI Wave 87

- Date: 2026-10-17
- Work branch: `contour-a-schema-validation-wave81-20261017`
- PR: [#337 — Wave 81: Add pinned cloud-agent schema validation workflow](https://github.com/VlDMlNSh/mediahub-os/pull/337)
- Scope: verify Wave 86 lock-generation evidence, read back the lock and workflow, confirm current-head CI, and record remaining integration gates.
- Status: committed lock text matches successful generator output, and hash-enforced schema CI passes on the current PR head; lock-generation provenance has an unresolved `--no-index` configuration discrepancy, so full reproducibility is not yet qualified.

## 1. Evidence checked

### Lock generation

- Workflow: [Generate cloud-agent schema dependency lock](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39045574488)
- Run ID: `39045574488`; result: `completed / success`.
- Generator input commit: `287fc64638a6ddd968912441f123b6c933c124be`.
- Generator toolchain from the run log: Python `3.12.15`, `pip-tools 7.4.1`, pip `24.3.1`.
- Logged input SHA-256: `1056b740383d453db32b92c7f24170a952eadf5ffafaaa7875ad58329c313916`.
- Logged generated-lock SHA-256: `8ca73afc0d357018760c86c2ed6e7d0c5226e8677f6e3197fa6f1064321f4681`.
- Workflow artifact: `cloud-agent-schema-validation-lock-287fc64638a6ddd968912441f123b6c933c124be`, artifact ID `12105503066`, API-reported digest `sha256:4e8f45a9e2bfb1c27e4a91dd27ca46584d125fd2c9b765c2fa3cd7f937146cdf`, expiry `2026-10-24T15:33:46Z).
- The lock text emitted in the successful workflow log was reconstructed from the log and compared byte-for-byte with the current committed lock content. Both have 14,985 characters; exact text comparison passed. The workflow artifact itself was not downloaded in this pass; its existence and metadata were verified separately.
- Lock file read-back blob SHA: `f6abb557b75373821945aee719a19a86bf2a4d8c`.
- Direct-input read-back blob SHA: `46aa24e6ab56bc0bc1c69e29ffa778e7f2c74635`.

### Current-head schema CI

- Current checked head: `1d23683aace97f88610b42bc9070fef72fef455b`.
- Successful run: [39045708468](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39045708468), job ID `117433883463`, status `completed / success`.
- A second run on the same head also succeeded: [39045704331](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39045704331).
- Read-back validator workflow blob SHA: `33008092a1302a50a1674d1a1646686a2bb638a8`.
- The workflow installs from the lock using `python -m pip install --disable-pip-version-check --no-input --require-hashes -r requirements/cloud-agent-schema-validation.lock`. The log confirms the hash-locked install completed successfully.
- The job's schema-fixture stage passed for all three v0.2 artifacts: task envelope, agent registry, and evidence manifest. Logged passing classes include positive fixtures, empty-object rejection, nested required-field rejection (37 / 25 / 36 cases respectively), additional-property rejection, enum rejection, invalid date-time rejection, cross-artifact consistency, and a negative cross-artifact task-ID mismatch. No fixture-stage failure was logged in this successful run.

## 2. Repository and governance state

- PR #337 remains open and Draft; no review submissions were returned. It is not merged.
- Current comparison with canonical docs branch `docs/mediahub-chat-tree-map-20261012`: `27 ahead / 18 behind`; merge base `8083cd61dbe348e18ab7db3e09b2769529bdcfda`. This is branch divergence, not evidence of a merge conflict-free or governance-approved integration.
- PR #332 remains open, non-Draft, unmerged.
- PR #333 remains open, Draft, unmerged; GitHub currently reports it as not mergeable.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains open. Its stated gates include A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy authority, an accepted runner/workspace/network target manifest, independent schema review, and qualification of the bounded read-only worker/queue path.
- Historical schema-validation runs on intermediate commits include failures/cancellations; the final checked head above has successful runs. Do not describe every attempt as green.

## 3. Wave 86 report correction

The Wave 86 report was accurate at the time it was written, but its statement that no lock had been read back or committed is now superseded by the evidence in this Wave 87 report. Keep Wave 86 as a historical snapshot; use this report for the later verified state.

## 4. Lock-generation provenance caveat

The generated lock header emitted by the successful generator run records a `pip-compile` command containing `--no-index`, while the checked-in workflow's visible compile invocation does not pass that flag. The workflow log also shows the generated lock was emitted and its logged SHA-256 was recorded, and the committed file matches that emitted text byte-for-byte; however, the source of the effective `--no-index` option has not been explained. Before calling dependency generation reproducible, inspect runner-level pip configuration/environment and the complete `pip-compile` invocation/environment, then regenerate in a controlled environment with explicit index policy and compare results. The hash-locked install passing proves the current lock can be installed in the observed runner, not that lock generation is independent of hidden runner configuration.

## 5. What is still not proven

- The artifact ZIP was not downloaded and independently unpacked; the current lock was matched to the complete lock text emitted by the successful generator log, and artifact metadata was verified.
- No independent code/security review of PR #337 is recorded.
- Branch reconciliation and integration approval are still outstanding.
- This does not qualify the full autonomous environment, authorize provider dispatch, prove secret-hygiene across every workflow, or close Issue #301.
- No merge, deployment, credential access, external model invocation, task dispatch, or Contour B work was performed.

## 6. Next bounded step

1. Explain and eliminate the `--no-index` provenance discrepancy; explicitly define the package-index policy and regenerate the lock under a controlled environment. Download and inspect artifact `12105503066` if the available GitHub connector exposes a safe artifact-download path; compare the extracted file with the committed lock and the recorded SHA-256.
2. Review the full PR diff file-by-file, especially schema-validator behavior, workflow triggers, token permissions, action pins, and dependency provenance.
3. Reconcile the 27/18 branch divergence only after a file-level conflict/loss review; re-run CI on the resulting head.
4. Obtain independent review and resolve Issue #301 authority/runner qualification gates before any promotion or merge decision.

## Canonical navigation

- [Canonical project map](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- [Bootstrap instruction](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md)
- [Current continuation checkpoint](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/mediahub-next-continuation-checkpoint-2026-10-12-current.md)
- [Master Development Roadmap](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
- [PR #337](https://github.com/VlDMlNSh/mediahub-os/pull/337)
- [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
