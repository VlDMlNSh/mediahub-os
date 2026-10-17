# Wave 127 — execute Gemini provider lifecycle regression tests in CI

Date: 2026-10-18  
Repository: [VlDMlNSh/mediahub-os](https://github.com/VlDMlNSh/mediahub-os)  
Candidate PR: [#334](https://github.com/VlDMlNSh/mediahub-os/pull/334)  
Candidate branch: `security/gemini-readonly-hardening-20261017)

## Objective

Close a verification gap in the Gemini read-only workflow hardening candidate: the dedicated HTTP, missing-credential and provider-outcome Node.js regression tests existed, but the validation workflow did not execute them.

## Change

Updated `.github/workflows/gemini-readonly-workflow-validation.yml` to execute, after the Python workflow-contract tests:

- `node scripts/test_gemini_http_response.js`
- `node scripts/test_gemini_missing_credential.js`
- `node scripts/test_gemini_provider_outcome.js`

The job remains read-only (`contents: read`), checks out the immutable event SHA, and does not read provider credentials or call Gemini. No workflow dispatch or provider invocation was performed.

## Evidence and verification

- Candidate commit: [`8b75963be33425718f381390bfcfdf997ab3b3ca`](https://github.com/VlDMlNSh/mediahub-os/commit/8b75963be33425718f381390bfcfdf997ab3b3ca)
- Parent candidate: `822cd023015f72002b850ee20f8047aff24080fe`
- Changed workflow blob SHA after read-back: `4a365141243d60e5c3cf2815aaede8857b55346f`
- Read-back confirmed all three Node test commands are present.
- Exact-HEAD [Gemini Read-only Workflow Contract run #39076578738](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39076578738): completed/success. The `actionlint`, Python contract-test and executable Node regression-test steps all completed/success.
- Exact-HEAD [Astra Verify run #39076578839](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39076578839): completed/success.
- Exact-HEAD [Astra Cloud Runtime Validation run #39076578899](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39076578899): completed/success.
- Live comparison: `main` HEAD `c06015e0b1526e0aaa6a522306052b077455aba5`; candidate HEAD `8b75963be33425718f381390bfcfdf997ab3b3ca`; 71 commits ahead, 0 behind; merge base is current main HEAD.
- PR #334 remains OPEN / DRAFT / UNMERGED and reports mergeable=true. The current review submissions do not establish independent security approval.
- Rulesets endpoint returned an empty list; branch-protection read returned HTTP 403 / resource not accessible. Protection requirements therefore remain unverified, not presumed disabled.

## Scope and disposition

This pass improves automated regression coverage; it does not establish provider runtime qualification or Contour A acceptance. No secret was read, no Gemini call/dispatch occurred, and no merge, deployment or queue admission occurred.

## Blockers

1. Independent security review of the exact current candidate HEAD is still required.
2. Authorized read-back of applicable branch-protection requirements is unavailable to the current integration.
3. Issue #301 still requires the remaining Contour A issuer/ingress/lease/cancel/recovery and R-06 authority gates, standards-compliant Draft 2020-12 schema validation with negative fixtures, and an authoritative runner/workspace/network target manifest.

## Next step

Continue Issue #301 with the next bounded, source-verifiable Contour A acceptance gap while keeping PR #334 in Draft until independent review and repository-protection requirements are evidenced.

Canonical project map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md) on [`docs/mediahub-chat-tree-map-20261012`](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md).
