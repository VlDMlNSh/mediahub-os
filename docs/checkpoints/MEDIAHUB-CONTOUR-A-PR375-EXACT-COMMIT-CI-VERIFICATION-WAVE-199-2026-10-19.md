# MediaHub OS Contour A — PR #375 exact-commit CI verification (Wave 199)

- Date: 2026-10-19
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Prior wave: [Wave 198 regression review](MEDIAHUB-CONTOUR-A-PR375-CREDENTIAL-POLICY-REGRESSION-REVIEW-WAVE-198-2026-10-19.md)
- Candidate PR: [#375](https://github.com/VlDMlNSh/mediahub-os/pull/375)
- Candidate branch: `security/contour-a-worker-checkout-credential-minimization-wave176-20261019`
- Candidate commit verified: [`a617a960346756a6b3098ee974d74327f9088f5e`](https://github.com/VlDMlNSh/mediahub-os/commit/a617a960346756a6b3098ee974d74327f9088f5e)

## Result

Wave 198 had left the focused unit test and exact-commit CI unverified. This pass queried workflow runs associated with the corrected test commit and fetched the job-step results.

| Check | Run | Job | Result |
|---|---|---|---|
| Astra Verify | [39244658819](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39244658819) | `verify`, job 118033550386 | SUCCESS |
| Astra Cloud Runtime Validation | [39244658804](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39244658804) | `validate`, job 118033549945 | SUCCESS |

The Astra Verify step list explicitly reports **Worker workflow credential policy regression tests — completed / success** (step 7), followed by Cloud admission unit tests and signed command smoke test, all successful. The commit queried for these PR-triggered runs is `a617a960346756a6b3098ee974d74327f9088f5e`. The fetched commit metadata confirms the same SHA and commit title. This is exact-commit CI evidence, not independent security acceptance or release approval.

## Change reviewed

The existing draft PR test file now:
- requires exactly three checkout blocks in the worker workflow policy oracle;
- rejects a synthetic mutation that removes two checkout steps;
- retains negative fixtures for elevated contents permission and persisted checkout credentials.

The final test blob remains `8cf3697d0aaf02d31c3359b6f2c8ed5283087b6f`. The workflow candidate blob remains `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`; no production workflow YAML was changed in this pass.

## Limits and outstanding gates

- PR #375 remains OPEN and Draft according to the latest retrieved PR metadata; it is not merged.
- The change narrows GitHub token exposure but may affect the existing worker push path. A trusted, reviewed publisher replacement is still required before integration.
- FCC token propagation, OS/network isolation, A0 issuer/capability lifecycle, R-06, target manifest, repository protection, independent review and governance disposition remain open.
- The separate Gemini workflow brokered-write boundary and MCP OCI tag-to-manifest provenance remain unresolved.
- No dispatch, provider calls, secret access, host commands, merge, deployment, or qualification occurred.

## Next action

Obtain independent review for PR #375 and settle the trusted publication path before considering integration. In parallel, continue authoritative MCP image digest provenance and governance evidence work. Keep the PR Draft/unmerged until all applicable gates are satisfied.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains gated until Contour A is deployed and independently accepted.
