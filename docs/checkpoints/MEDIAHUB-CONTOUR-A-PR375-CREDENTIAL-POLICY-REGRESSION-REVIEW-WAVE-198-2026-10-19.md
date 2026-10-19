# MediaHub OS Contour A — PR #375 credential-policy regression review (Wave 198)

- Date: 2026-10-19
- Canonical branch: `docs/mediahub-chat-tree-map-20261012`
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Governing issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Candidate PR: [#375](https://github.com/VlDMlNSh/mediahub-os/pull/375)
- Candidate branch: `security/contour-a-worker-checkout-credential-minimization-wave176-20261019`

## Scope and exact source evidence

This pass reviewed the existing draft PR #375, rather than creating a parallel security candidate. Current PR state was fetched from Issue/PR metadata: OPEN; last updated `2026-10-19T11:26:29Z`. The candidate workflow blob remains `c24ad16ab8ed59fd4dbad9538063f63a933eab2c`. The pre-change test blob was `c24897e827b70941fc9b4f154fd0aa1b31b801cc`.

The workflow reduces `contents` permission to `read` and sets `persist-credentials: false` on three checkout steps. This narrows one credential exposure path, but the PR description says no tests had been executed in its earlier pass and identifies other open trust-boundary gaps. It does not provide a replacement trusted publisher for worker output.

## Finding: the static oracle did not require all three checkout steps

The original `policy_violations()` rejected a missing checkout block only when zero checkout steps were found. It did not require the expected three worker checkouts. A source-level mutation experiment confirmed the issue: the original policy oracle returned no violations for a synthetic workflow retaining only one valid checkout step. This was a synthetic text check only; it did not execute a workflow or mutate repository source.

### Bounded correction applied to the existing draft candidate

Updated `ops/qualification/test_worker_workflow_credential_policy.py` on the PR #375 branch:

- Require exactly three checkout blocks in the static policy oracle.
- Add `test_rejects_missing_checkout_steps`, which removes two checkout blocks in a synthetic fixture and asserts the policy rejects the mutation.
- No production workflow YAML was changed in this wave.

Change evidence:
- Original test blob: `c24897e827b70941fc9b4f154fd0aa1b31b801cc`
- First correction commit: `165171506850fda0335fa49028cbe5a680178352`, test blob `6bf4181c60131858f1d7496f1779cfed05d7add3`
- Regex fixture correction commit: `a617a960346756a6b3098ee974d74327f9088f5e`
- Final read-back test blob: `8cf3697d0aaf02d31c3359b6f2c8ed5283087b6f`
- Final read-back confirms the exact-three assertion and missing-checkout negative fixture are present.

The first edit's negative-fixture regex was found malformed during read-back and corrected in the second commit before finalizing this report. This illustrates why read-back was required.

## Verification status

- Source-level mutation experiment: PASS for the defect reproduction (original oracle failed to reject one-checkout mutation); correction is present by read-back.
- Python unit test suite: NOT RUN in this environment.
- Workflow/CI run for the new commit `a617a960346756a6b3098ee974d74327f9088f5e`: no PR-triggered run was returned by the connector at the time of check. Do not claim CI success.
- No worker dispatch, provider call, secret/credential access, host command, merge, deployment or qualification occurred.
- The PR's exact current head is not asserted from the connector's limited run response; the two commits above are confirmed write/read-back evidence.

## Remaining limits

1. The three-checkout count is a contract for the current three-node workflow; if topology changes, the expected count and fixture must be deliberately reviewed together.
2. Static regex tests do not parse YAML semantics or prove GitHub token authority is contained across subprocesses.
3. `contents: read` may prevent the existing worker push behavior; PR #375 itself has no replacement trusted publisher. Do not merge until the intended output publication path and its authority are reviewed.
4. FCC token propagation/environment isolation, OS/network isolation, A0 issuer/capability lifecycle, R-06, target manifest, repository protection and independent security/governance disposition remain separate gates.
5. The Gemini workflow brokered-write proposal and exact MCP OCI image provenance remain unresolved; this narrow test improvement does not close them.

## Outcome and next action

The regression oracle was strengthened in the existing draft PR and read back by blob SHA. CI is still unverified for the new commit. Next: retrieve a fresh authoritative PR head/status/check snapshot, run the focused unit test and relevant CI on that exact SHA, then request independent review. Keep PR #375 Draft/unmerged until a trusted publisher replacement and all required authority gates are resolved.

Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT INDEPENDENTLY ACCEPTED**. Contour B remains gated.
