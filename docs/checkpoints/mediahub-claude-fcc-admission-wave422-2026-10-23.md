# MediaHub OS — Claude FCC cloud + local Llama admission report (Wave 422)

Date: 2026-10-23  
Status: **PARTIALLY VERIFIED / BLOCKED**  
Working branch: `contour-a/claude-fcc-admission-router-20261023`  
Canonical documentation branch (unchanged): `docs/mediahub-chat-tree-map-20261012`

## Scope

Advance two independent routes without crossing authority boundaries:

1. GitHub-hosted Claude Code → pinned Free Claude Code (FCC) → OpenRouter free-only route, with ECC guidance pinned to an immutable source.
2. Local Claude Code → FCC → Ollama `llama3.2:3b` on approved host `Voktors-Mini.Dlink`.

No provider invocation, merge, deployment, qualification, or acceptance is implied by policy/code checks.

## Immutable repository refs and CI

- `main` HEAD: `fbbdc9a06ef344cd57aae13b230a042af76bbc60`.
- PR #530: https://github.com/VlDMlNSh/mediahub-os/pull/530
- Current observed PR head: `076ed5bd55cec5cf5c6c58370b9dec7a66a80cdc`.
- PR state: OPEN, DRAFT, NOT MERGED.
- Exact-head checks all completed successfully:
  - Provider contract: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39928213627
  - AI Factory verification: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39928213644
  - Astra agent verification: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39928213589
  - Cloud Runtime Validation: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39928213665
  - FCC free-route admission controller: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39928213688
  - Astra Verify: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39928213661
- Formal PR reviews: **NONE**. Combined commit status contexts: **EMPTY**. These are NOT VERIFIED, not PASS. Do not merge.
- Router policy blob on working branch: `.github/ai/model-router.yml`, SHA `e249333c1c0ce6c1c586a5f498dbfd3979418f6e`.
  - Cloud route: `fcc_openrouter_free`, free-only, no paid fallback, fail-closed.
  - Local route: `fcc_ollama`, model `llama3.2:3b`, host `Voktors-Mini.Dlink`.
- FCC upstream source pinned to `Alishahryar1/free-claude-code@3d2ae2306752dbdf504714a5489bcfcf69b2d04a`.
- ECC source pinned to `affaan-m/ECC@c05b2d6614f62f6db0047669aa4eefb223d478f9`; plugin version 2.2.3 confirmed at that immutable commit. ECC is guidance only; no hooks, MCP servers, or independent control-plane authority are enabled.

## Local executor evidence

Host: `Voktors-Mini.Dlink`; SentinelX host ID `host_5f7264034bdf0b51`.

- FCC `/health` at `127.0.0.1:8082`: HTTP 200.
- Admin configuration read-back:
  - `HOST=127.0.0.1`
  - `PORT=8082`
  - `MODEL=ollama/qwen3:4b`
  - `OLLAMA_BASE_URL=http://127.0.0.1:11434`
  - `PROXY_AUTH_ENABLED=false`
- An intentionally malformed unauthenticated request to `/v1/messages` returned HTTP 422 rather than HTTP 401. Therefore proxy authentication is **NOT ENFORCED**. FCC is blocked for any coding task until authentication is configured and verified.
- A previous admin apply returned HTTP 200 with `applied=true` and `valid=true`, but read-back did not reflect the requested model/auth changes. Treat apply/read-back as a failure; do not trust the optimistic response.
- Ollama `llama3.2:3b` direct inference returned `MEDIAHUB_LOCAL_LLAMA_OK`, `done=true`, `eval_count=8`, `total_duration_ns=8478378166` (~8.48 s). FCC model catalog exposes `anthropic/ollama/llama3.2:3b` and `claude-3-freecc-no-thinking/ollama/llama3.2:3b`, but default model remains Qwen.
- Direct Ollama inference is verified; **FCC-routed Claude Code/ECC execution is NOT RUN**.
- During this pass, host script calls repeatedly failed with SentinelX `duplicate_session/agent_disconnected` or timeout while inspecting the FCC admin apply schema. No configuration changes were made and no credentials were read or printed.

## Cloud route and controller

- No OpenRouter request/provider call was made in this pass.
- Latest fresh `/next` comment on Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6361829435
- Controller run ID and three child run/job IDs for that comment: **NOT VERIFIED**. Available connector queries did not enumerate issue-comment event runs; browser automation on the host disconnected. Do not claim dispatch or child-agent execution based only on the comment.
- Cloud route qualification remains **NOT ACCEPTED** pending independent review, controller evidence, and a separately authorized bounded free-only runtime smoke.

## Canonical source refs

- Bootstrap blob: `75f30750183efe8c6877368e9f0ada48f8e81ea7`.
- Canonical map blob: `78fa7dfa02357fe9e95645843e583f8802867d78`. Contents API returned empty content for this path; retrieval by blob SHA was not supported by the connector. The canonical map was not changed.
- Canonical checkpoint blob at pass start: `573c26ccb7e1b18b09e7b37e684f2dba18dc5026`.
- Master Roadmap blob: `4b45b4bfeb5fcbf2dd409fb98241832283982c95`.
- Canonical map link: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Next bounded step

1. Restore stable SentinelX session and read the exact FCC admin apply schema.
2. Make a controlled FCC configuration change only when its persistence/restart path is understood; set loopback binding, enable proxy auth, and select `ollama/llama3.2:3b`.
3. Verify read-back, verify unauthenticated `/v1/messages` returns 401, and verify authenticated model listing/inference. Until then, do not send coding tasks to FCC.
4. Reconcile controller run ID and all three child run/job IDs for Issue #301 comment `6361829435`.
5. Obtain independent review on PR #530. Re-run exact-head CI after any new code changes. No merge or cloud provider call before required gates pass.

## Change provenance

This report is an unaccepted working-branch artifact, not a change to the canonical documentation branch and not a runtime qualification certificate.
