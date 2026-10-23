# MediaHub OS — Claude FCC Admission and Local Executor Readiness (Wave 419)

- Date: 2026-10-23
- Status: **IMPLEMENTED ON WORKING BRANCH / NOT VERIFIED / NOT ACCEPTED**
- Base/main target SHA: `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- Working branch: `contour-a/claude-fcc-admission-router-20261023`
- Parent tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Claude executor tracker: [Issue #496](https://github.com/VlDMlNSh/mediahub-os/issues/496)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Canonical documentation branch remains `docs/mediahub-chat-tree-map-20261012`; this working branch is not canonical or accepted.

## Scope

Owner requested parallel setup of (1) GitHub-hosted Claude Code → pinned FCC → OpenRouter free-only route with ECC-derived workflow discipline, and (2) local Claude Code → FCC → Ollama executor using the existing ECC skill surface. No provider call, secret value read, merge, deployment, or qualification was performed in this pass.

## Cloud route changes proposed on this branch

- Updated `.github/workflows/mediahub-fcc-free-claude-worker.yml` (new blob SHA `9fbd6987d91449a4fd8c88474d508b886e835362`): the existing bounded workflow is explicitly treated as the Claude route admission controller; live execution now requires owner dispatch, `refs/heads/main`, explicit `confirm=true`, exact 40-character `target_sha == github.sha`, `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE=true`, and presence of `OPENROUTER_API_KEY`. Claude Code installation is pinned to `2.1.282`; FCC source remains pinned at `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`. The route still requires a concrete returned model ID ending in `:free`, unsets paid Anthropic/fallback credentials, uses an empty isolated workspace and read-only plan-mode tools, and records the target SHA in the evidence metadata.
- Updated `.github/ai/model-router.yml` (new blob SHA `5a785ca8f30996494d7ff3ae86189986b9f7d827`) to allow only the existing Gemini controller and the explicitly owner-gated Claude FCC admission workflow as cloud transports. Direct provider API calls remain disabled, paid fallback remains false, and unknown routes fail closed.
- Updated `scripts/verify_ai_factory.py` (blob SHA `28440a2342e00d2e3fd14821dea3cdeec0508a7e`), `tests/test_mediahub_fcc_free_claude_workflow_contract.py` (blob SHA `4415c292db4b8579c4086e1713242ac5c68dceac`) and `tests/ai/test_provider_selector.py` (blob SHA `b37e4c5cbc0aaa0dd144ab3e1e1fbc1431930052`) to enforce explicit cloud-controller allowlisting, the owner/ref/SHA gates, the separate cloud-free and local-Ollama Claude routes, pinned Claude Code and no-paid-fallback policy.

## Local executor evidence

- SentinelX host identity confirmed: `Voktors-Mini.Dlink`, host ID `host_5f7264034bdf0b51`, agent `0.23.30`, architecture `arm64`; the configured capability mode is allowlist-based.
- Installed runtime inventory: Claude Code `2.1.282`, FCC `6.2.69`, Ollama `0.34.4`, OmniRoute `16.3.1`; existing ECC skills include `ecc-guide`, `configure-ecc`, `verification-loop` and others.
- Ollama endpoint `127.0.0.1:11434` returned HTTP 200 and model `qwen2.5-coder:1.5b` is present.
- FCC environment file has mode `0600`; non-secret settings identify `HOST=127.0.0.1`, `PORT=18093`, `MODEL=ollama/qwen2.5-coder:1.5b`, `PROXY_AUTH_ENABLED=true`, `OLLAMA_BASE_URL=http://127.0.0.1:11434`, and `REASONING_POLICY=off`. No FCC listener was bound on port 18093 during the check. A restart/health-check attempt was initiated through SentinelX but the remote session disconnected before returning a result; it is **NOT VERIFIED** and must not be assumed to have applied.
- Existing Astra local worker requires an immutable target SHA, clean workspace, explicit task envelope, declared node/executor/verifier, scoped paths, tests, and verifier. No unsigned task was submitted and no model inference was made.

## Verification and blockers

- Static content and blob SHA read-back: performed for the three edited source files.
- Contract tests, `verify_ai_factory.py`, YAML/workflow validation and exact-head CI: **NOT RUN / NOT VERIFIED** on this branch yet.
- Cloud provider probe/smoke: **NOT RUN**. Router admission is only proposed until PR review and exact-head checks pass.
- Local FCC health: **NOT VERIFIED**; the configured port was unreachable and SentinelX returned intermittent `duplicate_session/agent_disconnected`.
- ECC stays an executor guidance/profile only. No ECC controller, unrestricted hooks, provider credentials or independent authority are introduced.
- No merge, deployment, runtime qualification or Contour A acceptance.

## Next step

Run exact-head CI and independent review for the admission-policy PR. In parallel, revalidate the local FCC service on the exact approved host; only after `/health` and authenticated local `/v1/models` checks pass should the existing Astra issuer produce a bounded signed local task. Do not call OpenRouter until the route-policy PR is reviewed/accepted and its controller gates are live.
