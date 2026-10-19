# MediaHub OS Contour A — PR #375 job-level permission oracle review (Wave 200)

- Date: 2026-10-19
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Previous checkpoint: [Wave 199 exact-commit CI verification](MEDIAHUB-NEXT-CONTINUATION-CHECKPOINT-WAVE-199-2026-10-19.md)
- Candidate PR: [#375](https://github.com/VlDMlNSh/mediahub-os/pull/375)
- Candidate branch: `security/contour-a-worker-checkout-credential-minimization-wave176-20261019`

## Finding

A source-level review of the PR's static credential-policy oracle found a false-negative gap: it rejected a top-level `contents: write` permission but did not reject a job-level `permissions: contents: write` override. GitHub Actions permits job-level permission blocks, so checking only the top-level indentation was insufficient to assert that no job regained write authority.

## Bounded change

- Updated `ops/qualification/test_worker_workflow_credential_policy.py` to reject `contents: write` at any indentation level.
- Added a synthetic negative fixture that inserts `permissions: contents: write` under a worker job and asserts the policy oracle rejects it.
- During read-back, found that the first generated edit had over-escaped the Python regex and fixture newline strings. Corrected those escapes in a follow-up commit before concluding this pass.
- Final test blob read back by immutable SHA: `1d003b1d33fa31ec44d4cc8220747e3c4982b8b6`.
- Final correction commit: [`c9383017d9255c637df81cf5811c8d8ea32737e3`](https://github.com/VlDMlNSh/mediahub-os/commit/c9383017d9255c637df81cf5811c8d8ea32737e3). Preceding initial candidate commit: [`db19e9b5c35bbb4db6d56e6a215e1b7502490568`](https://github.com/VlDMlNSh/mediahub-os/commit/db19e9b5c35bbb4db6d56e6a215e1b7502490568).
- Candidate branch comparison against `main`: 8 commits ahead, 0 behind; three changed paths. The branch includes prior candidate history, so this is not a claim that all eight commits are new in this wave.

## Verification and limits

- Read-back verified the final blob SHA and the corrected regex/fixture text.
- No CI run was returned for correction commit `c9383017d9255c637df81cf5811c8d8ea32737e3` at the time of this check. The new test has **not** been claimed as executed or passing; await exact-commit CI.
- PR #375 remains open and Draft/unmerged. No independent review submissions were found in the reviewed PR review list.
- This is a static regression-oracle improvement, not a complete workflow authorization boundary. It does not replace a trusted publisher, solve output publication after removing worker write access, or establish issuer/capability enforcement, OS/network isolation, FCC token propagation, branch protection, or independent security acceptance.
- No worker dispatch, provider call, secret access, host command, merge, deployment, or qualification occurred.

## Next step

Verify the exact `c9383017d9255c637df81cf5811c8d8ea32737e3` PR CI result and inspect the job-level negative fixture's execution. Then obtain independent review and resolve the trusted publication path before considering integration. Continue MCP OCI digest provenance and brokered-write governance work separately.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains gated.
