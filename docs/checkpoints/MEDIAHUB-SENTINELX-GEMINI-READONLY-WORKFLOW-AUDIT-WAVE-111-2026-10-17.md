# MediaHub OS — SentinelX Host and Gemini Read-only Workflow Audit, Wave 111

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: **HOST REACHABLE / LOCAL GEMINI INVOCATION BLOCKED / PR #334 SOURCE-HARDENING CANDIDATE HAS CI EVIDENCE / CONTOUR A NOT QUALIFIED**
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Governing tracker: https://github.com/VlDMlNSh/mediahub-os/issues/301
- Working branch for this report: `docs/mediahub-sentinelx-gemini-audit-wave111-20261017`

## Scope and method

This pass revalidated SentinelX host state, repository refs, Issue #301, PR #333 and the existing Gemini read-only workflow-hardening candidate PR #334. GitHub source was read from explicit refs. No secret values were read; no provider API request, workflow dispatch, rerun, merge, deployment or credential rotation occurred.

## SentinelX / third Mac

- Live host list contains one operational host: `host_5f7264034bdf0b51`, `Voktors-Mac-mini.local`, SentinelX agent 0.22.0, macOS 23.6 / arm64. Ping returned `pong=true`.
- The Free plan enforces one active host. `mh-dev-01` and `mh-dev-02` are user-disabled; do not treat them as available.
- Host repo checkout `/Users/voktor/mediahub-os` is clean on `main` at `1d45bbccbbbd27309c39cb9e9351bb291cdb47a8`; its remote tracking ref for the canonical docs branch is `97d19bc423caca159c916ca9112eee77a18d10cd`. The local checkout is not the canonical docs ref.
- SentinelX file operations expose only `/Users/voktor/sentinelx/workspace` (rw) and `/Users/voktor/sentinelx/config.yaml` (rw). Direct filesystem API access to the repository is denied by policy. This pass did not widen the allowlist or mutate the host repository.
- Gemini CLI package 0.64.0 is cached under npm's npx cache, but the `node` executable is absent from the agent's execution PATH and no Gemini OAuth credentials, Gemini settings file or gcloud ADC file was present at the checked standard paths. Therefore a local Gemini CLI invocation is **not currently executable/authenticated** on this host. This is an environment readiness result, not a provider failure.

## Live GitHub state

- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`, HEAD `97d19bc423caca159c916ca9112eee77a18d10cd`.
- Canonical map blob at that ref: `5a94a4e22e0c636aba2a6f1efc48cacd69c7fc93`. Contents API returned empty content for this large file; fetching the blob by SHA returned 1,037,980 characters, confirming the file is not empty.
- Bootstrap blob: `fe9f09ff6b1913bab833db93d442111062b2fd15`.
- Current continuation checkpoint blob before this update: `6a4fe5955389e961585de31ef8eb0053abf0f174`.
- Master Roadmap blob: `462466162f23242e170cd1f25395e6c899b5ddc3`.
- Issue #301 is OPEN and was updated at `2026-10-17T19:26:29Z`. Its latest governance packet still leaves D-CA-01 through D-CA-06 OPEN/BLOCKED/UNKNOWN. These upstream decisions remain blockers for admission, queue execution and Contour A acceptance.
- PR #333 remains OPEN/DRAFT/UNMERGED, head `a83030bc6449109626b072dc0a090a59709b4a5b`, base `a0c432273914fa5c4bd9e756736f9c9b72b41a77`, merge state `DIRTY`; GitHub reported no checks for this head. No merge attempted.
- PR #334 remains OPEN/DRAFT/UNMERGED, head `517b76d7f52f05fa145ae7fb44b3bba541f72267`. Compare against current `main` (`c06015e0b1526e0aaa6a522306052b077455aba5`) is DIVERGED: 6 ahead / 2 behind, merge base `fbe30881c0ecc5e07a66ec1d5538c2c06171982b`. Exact-head workflow runs `39039099296` (Gemini Read-only Workflow Contract), `39039099324` (Astra Verify), and `39039099350` (Astra Cloud Runtime Validation) are completed/success. The PR has no recorded review submissions; these CI results are not independent security acceptance.
- PRs #338 and #339 remain open draft candidates. PR #339 is the documentation/acceptance-matrix branch; no independent reviews were returned. Do not infer acceptance from CLEAN merge-state metadata.

## Source audit of PR #334

Read-back source identities:
- `.github/workflows/gemini-readonly-audit.yml`: blob `39082ca0a82ab6882f51164cd38f952ef560d77e`.
- `.github/workflows/gemini-readonly-audit-retry.yml`: blob `7649dadd8d30120e658f67c65e838940a984e7ec`.
- `.github/workflows/gemini-readonly-workflow-validation.yml`: blob `8ad3cbddbf99954607dd7aa47c25aaacfa94dc7b`.
- `scripts/test_gemini_readonly_workflows.py`: blob `2967add7dc49418372cb88c9fbc63b89edfb5de5`.

Confirmed positive controls in both read-only workflows:
- Manual dispatch restricted to `main`; checkout uses `github.sha`, full-SHA-pinned `actions/checkout`, and `persist-credentials: false`; checkout SHA is compared with `github.sha`.
- Only two fixed context profiles are selectable; paths are fixed in workflow source, symlinks are rejected, per-file size is capped at 100 KB, aggregate context at 200 KB, and task input at 2,000 bytes.
- Fixed model `gemini-3.5-flash-lite`; maximum output 4,096 tokens and 100 KB; output is labelled untrusted advisory content. HTTP error response bodies are suppressed. The retry workflow limits attempts to three and does not automatically retry HTTP 429 or switch model/provider.
- Evidence manifest records source/workflow identity, task digest, context file hashes, model, action pins, provider status and output digest. Artifacts have 14-day retention.
- Workflow contract test source checks full-SHA action pins, least-privilege permissions, immutable checkout, fixed context, model/output bounds, quota retry behavior and retention. The exact-head CI runs above passed.

Residual review items (not CI failures):
1. Both workflows use `secrets.GEMINI_API_KEY || secrets.GOOGLE_API_KEY`. This is same-provider credential fallback rather than a model/provider fallback, but it obscures which configured credential was selected; decide whether the contract should require one explicit secret name and record a non-secret credential-source identifier.
2. The retry path retries network transport failures and HTTP 500/502/503/504, but not HTTP 408 or 425. Decide whether these are intentionally excluded and encode the decision in tests; do not broaden retries to 429 without an explicit quota policy.
3. Static tests are text-pattern tests. They do not execute the workflow wrapper, validate a sample evidence manifest against a formal schema, simulate secret-safe error handling, or prove artifact completeness on partial failure. Add focused unit tests for manifest lifecycle and error branches before qualification.
4. The runbook/source does not establish provider quota, current secret availability, repeatability or independent Contour A qualification. No model invocation was made in this pass.

## Disposition and next step

- Host connection: VERIFIED.
- Local Gemini invocation on third Mac: BLOCKED by missing Node runtime on PATH and absent standard local auth files; no credentials were exposed.
- PR #334: promising source-hardening candidate with exact-head CI PASS; still lacks independent review and is diverged from current `main`.
- PR #333: DIRTY and no checks reported; do not integrate.
- Issue #301 governance gates: OPEN/BLOCKED/UNKNOWN. Contour A remains **NOT QUALIFIED / NOT DEPLOYED / NOT PRODUCTION-ACCEPTED**.
- Next bounded action: independently review PR #334's workflow source/tests, resolve the secret-source and retry-policy decisions, add executable wrapper tests, and reconcile its two-commit divergence only after preserving the exact source provenance. Do not dispatch a provider call until the applicable source/authority gates are satisfied.

