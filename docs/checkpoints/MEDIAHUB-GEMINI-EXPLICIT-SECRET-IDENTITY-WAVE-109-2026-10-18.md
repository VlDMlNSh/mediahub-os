# Gemini explicit secret identity and workflow contract — Wave 109 (2026-10-18)

## Result

Removed implicit secret-name fallback from both read-only Gemini workflows. Both now consume only the explicitly named `GEMINI_API_KEY` secret. Added a regression test that fails if either workflow reintroduces `secrets.GOOGLE_API_KEY` or a logical-OR secret fallback.

This closes a source-contract inconsistency; it does not establish that a provider call is authorized, that the secret exists, or that Contour A is qualified.

## Candidate source evidence

- PR: [#334](https://github.com/VlDMlNSh/mediahub-os/pull/334), branch `security/gemini-readonly-hardening-20261017`.
- Exact candidate HEAD after changes: `b8938e2c8a6b53a9856611beb4e2c91b9b47e7eb`.
- Primary workflow blob: `f2183d1ee19af66f4669b70f38a762ede4c4239f` — [source](https://github.com/VlDMlNSh/mediahub-os/blob/security/gemini-readonly-hardening-20261017/.github/workflows/gemini-readonly-audit.yml).
- Retry workflow blob: `0909d6039875bb33033a618dbb4b672ce1a85ead` — [source](https://github.com/VlDMlNSh/mediahub-os/blob/security/gemini-readonly-hardening-20261017/.github/workflows/gemini-readonly-audit-retry.yml).
- Contract-test blob: `f6b2ea1e8d7bd45f0c96c0b8a3f1a9058506e59d` — [source](https://github.com/VlDMlNSh/mediahub-os/blob/security/gemini-readonly-hardening-20261017/scripts/test_gemini_readonly_workflows.py).
- Shared bounded HTTP reader remains `adb3d27307cd5ad078a8c622cbeaaebd40f903ec`.

## Verification

Read-back after writes confirmed:
- Both workflows contain `GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}`.
- Neither workflow contains `secrets.GOOGLE_API_KEY`.
- The regression test checks explicit key identity and rejects fallback syntax.

Exact-head GitHub Actions runs for `b8938e2c8a6b53a9856611beb4e2c91b9b47e7eb`:
- [Gemini Read-only Workflow Contract #39070239298](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39070239298) — success.
- [Astra Verify #39070239407](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39070239407) — success.
- [Astra Cloud Runtime Validation #39070239344](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39070239344) — success.

## Governance and unresolved gates

- PR #334 remains OPEN / DRAFT / UNMERGED.
- Live comparison against `main`: diverged, candidate ahead 39 / behind 2; merge base `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`; observed main HEAD `c06015e0b1526e0aaa6a522306052b077455aba5`. Reconcile this divergence losslessly before integration.
- No submitted independent review or inline review thread was returned.
- Branch-protection/ruleset settings remain UNVERIFIED: available GitHub integration actions do not expose a read operation for these settings. Do not infer configuration from CI results.
- No provider call, workflow dispatch, credential read, queue admission, merge, deployment, or Contour A acceptance occurred in this pass.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN; A0 issuer/lifecycle, R-06 audit/privacy, accepted target manifest and independent qualification gates remain unresolved.

## Next step

Obtain independent security review and authorized branch-protection/ruleset read-back; reconcile PR #334's 39-ahead / 2-behind divergence without losing either side, then rerun checks on the reconciled exact head. Keep the PR draft until those gates are evidenced.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).
Wave 109 navigation: [Wave 109 addendum](../architecture/MEDIAHUB-CHAT-TREE-MAP-ADDENDUM-WAVE-109-2026-10-18.md).
