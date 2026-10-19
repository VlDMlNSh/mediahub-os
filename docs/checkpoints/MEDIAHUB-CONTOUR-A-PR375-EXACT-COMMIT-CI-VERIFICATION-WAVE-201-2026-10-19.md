# MediaHub OS Contour A — PR #375 exact-commit CI verification (Wave 201)

- Date: 2026-10-19
- Canonical branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous checkpoint: [Wave 200](MEDIAHUB-NEXT-CONTINUATION-CHECKPOINT-WAVE-200-2026-10-19.md)
- Candidate PR: [#375](https://github.com/VlDMlNSh/mediahub-os/pull/375)
- Candidate commit: [`c9383017d9255c637df81cf5811c8d8ea32737e3`](https://github.com/VlDMlNSh/mediahub-os/commit/c9383017d9255c637df81cf5811c8d8ea32737e3)

## Objective

Close Wave 200's narrowly scoped uncertainty: whether the corrected job-level `permissions: contents: write` negative fixture was exercised by PR CI for the exact correction commit, rather than relying on successful checks from its parent commit.

## Verified evidence

- PR #375 was re-read and reported OPEN / Draft / unmerged; its current head is `c9383017d9255c637df81cf5811c8d8ea32737e3`, base `main` at `c06015e0b1526e0aaa6a522306052b077455aba5`.
- The exact-commit workflow-run query for `c9383017d9255c637df81cf5811c8d8ea32737e3` returned:
  - [Astra Verify run 39289137450](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39289137450), job `verify` / `118184887310`, SUCCESS.
  - [Astra Cloud Runtime Validation run 39289137423](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39289137423), job `validate` / `118184886994`, SUCCESS.
- The Astra Verify job's step summary explicitly marks **Worker workflow credential policy regression tests** SUCCESS, followed by Cloud admission unit tests and signed command smoke test, also SUCCESS.
- The correction commit metadata and diff were fetched by SHA. The test file was read back from the PR branch with blob SHA `1d003b1d33fa31ec44d4cc8220747e3c4982b8b6`; the corrected matcher rejects `contents: write` at any indentation and the synthetic job-level permission fixture inserts the override under a worker job.
- PR changed paths are exactly `.github/workflows/astra-distributed-local-worker.yml`, `.github/workflows/astra-verify.yml`, and `ops/qualification/test_worker_workflow_credential_policy.py`.

## Disposition

**Wave 200's exact-commit CI gap is closed for this candidate commit.** This is CI evidence for the static regression test, not independent security acceptance or release qualification.

PR #375 remains Draft and unmerged. The candidate reduces the workflow token to `contents: read` and disables persisted checkout credentials, while the worker implementation on `main` still contains a direct `git push` path. A trusted, independently reviewed publisher/output-publication path has not been demonstrated. The issuer/capability lifecycle, R-06, accepted target manifest, FCC token propagation, OS/network isolation, repository protection/review settings, and independent security review remain open. No governance decision is inferred.

No worker dispatch, provider call, secret access, host command, merge, deployment, or qualification occurred in this wave.

## Next action

Keep PR #375 Draft/unmerged. Obtain independent review and resolve the trusted publisher/output-publication path without restoring broad ambient write credentials. Separately continue authoritative MCP image tag-to-manifest provenance and brokered-write governance. Do not promote Contour A until its required gates are independently satisfied.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains gated until Contour A is deployed and independently accepted.
