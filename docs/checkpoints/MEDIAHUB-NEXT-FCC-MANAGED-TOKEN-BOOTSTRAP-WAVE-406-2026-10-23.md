# Wave 406 — FCC managed-token bootstrap remediation (2026-10-23)

## Result

A bounded code correction was prepared in draft PR [#506](https://github.com/VlDMlNSh/mediahub-os/pull/506). The confirmed defect was that the workflow supplied a run-scoped `ANTHROPIC_AUTH_TOKEN` only through the process environment, while the pinned FCC configuration loader excludes that variable from process-level overrides and validates the API bearer token against its managed settings.

This report records implementation and CI evidence only. It does not qualify the provider route or accept Contour A.

## Immutable target and provenance

- Base `main` before the fix: `85e74ec24b862a5f6427ad5dca7d050df89c224c`.
- FCC source commit: `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`.
- Worker source: [pinned FCC loader](https://github.com/Alishahryar1/free-claude-code/blob/3d2ae2306752dbdf504714a5489bcfcf69b2d04a/src/free_claude_code/config/loader.py), which explicitly skips `ANTHROPIC_AUTH_TOKEN` in process overrides.
- Auth source: [pinned FCC dependencies](https://github.com/Alishahryar1/free-claude-code/blob/3d2ae2306752dbdf504714a5489bcfcf69b2d04a/src/free_claude_code/api/dependencies.py), which checks bearer auth against `settings.proxy_auth_token`.
- Original failure: [workflow run #39882471966, job #120182870408](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39882471966/job/120182870408). OpenRouter returned a concrete `:free` model, but FCC readiness failed with HTTP 401.
- Fix branch: `fix/fcc-managed-auth-token-20261023`.
- Fix PR: [#506](https://github.com/VlDMlNSh/mediahub-os/pull/506), draft, open.
- PR head SHA: `a8cef5fbad56c93573e309c6048ffd8a0f675053`.
- Workflow blob SHA at PR head: `4a1e7c2014fe3d6a1b23f8d90403c10814d20907`.
- Contract-test blob SHA at PR head: `9ebbae8775c7db87629010dbc4741aed1f96f072`.

## Changes

1. Seed a temporary `FCC_ENV_FILE` with only the run-scoped proxy token so FCC's supported one-time import writes it into managed configuration.
2. Set `umask 077` and file mode `0600`; the token file is neither printed nor uploaded.
3. Keep proxy authentication enabled and retain the free-only OpenRouter route, empty workspace and restricted Claude tool allowlist.
4. Make the readiness probe distinguish HTTP 401 from startup/connectivity failure without disclosing server logs.
5. Extend the workflow contract tests to require the managed-token bootstrap and safe failure classification.

## Exact-head verification

At the last read-back on 2026-10-23:

- [FCC workflow contract tests](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39883095467/job/120184843387): **SUCCEEDED**.
- [Pinned FCC install smoke](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39883095467/job/120184843407): **SUCCEEDED**.
- [Astra Verify](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39883095452/job/120184842850): **SUCCEEDED**.
- [Astra Cloud Runtime Validation](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39883095533/job/120184843061): **SUCCEEDED**.
- PR-triggered live dispatch jobs `dispatch-gate` and `bounded-worker`: **SKIPPED**, as required for a pull request; no provider request was made by these jobs.
- Combined commit status endpoint: **PENDING / zero status contexts** at the last check. Do not summarize this as all required status contexts passing.
- Formal PR reviews: empty list; independent security review **NOT VERIFIED**.
- PR #506 remains draft and unmerged.

## Safety and acceptance

- No auth bypass, no disabled proxy auth, no paid Anthropic credential, and no paid fallback was added.
- No live worker rerun was performed.
- Effective account billing/quota, runtime Claude marker, output artifact digest and end-to-end free-route qualification remain **NOT VERIFIED**.
- Contour A remains **NOT ACCEPTED**.
- Gemini controller dispatch remains outside this pass and must continue to respect its separate governance gates.

## Next bounded step

Obtain independent review of PR #506 and reconcile the pending/empty combined-status state. Only after those gates are evidenced may an authorized owner run one bounded FCC worker dispatch and preserve run ID, request ID, selected `:free` model, artifact digest and billing/quota evidence.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
