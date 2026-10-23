# MediaHub OS — Claude FCC cloud/local executor Wave 421 report

Date: 2026-10-23
Status: **PARTIALLY VERIFIED; NOT QUALIFIED; NOT ACCEPTED**

## Scope

Bounded work: reconcile the GitHub-hosted Claude Code → FCC → OpenRouter free-only + pinned ECC route, and separately qualify local Claude Code → FCC → Ollama Llama on `Voktors-Mini.Dlink`. No paid fallback, no secret disclosure, no merge, no production authorization.

## Immutable repository evidence

- Main target SHA: `fbbdc9a06ef344cd57aae13b230a042af76bbc60`.
- Working PR: [#530](https://github.com/VlDMlNSh/mediahub-os/pull/530), branch `contour-a/claude-fcc-admission-router-20261023`; at verification time head `c44992c82cb5f32802557f0241b0225f478d0122`, open draft, unmerged, no formal review, combined status contexts empty.
- Router policy blob before this report update: `e249333c1c0ce6c1c586a5f498dbfd3979418f6e`. It declares cloud FCC/OpenRouter Free-only and local FCC Ollama model `llama3.2:3b`; this is policy, not runtime qualification.
- ECC source pin: `affaan-m/ECC@c05b2d6614f62f6db0047669aa4eefb223d478f9`, plugin version 2.2.3. ECC is guidance only; no hooks/MCPs/independent authority installed.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md

## Exact-head CI

For PR head `c44992c82cb5f32802557f0241b0225f478d0122`, all six workflows succeeded:
- Provider contract [39923968535](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39923968535), job `120315707254`.
- AI Factory [39923968707](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39923968707), job `120315708327`.
- Astra Verify [39923968523](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39923968523), job `120315707536`.
- Astra agent [39923968509](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39923968509), job `120315707363`.
- Cloud Runtime [39923968552](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39923968552), job `120315707324`.
- FCC admission [39923968627](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39923968627): jobs `120315708308`, `120315708593`, `120315708594`, `120315708742` succeeded; dispatch-gate `120315710239` and bounded-worker `120315710742` skipped by design.
- This report commit advances PR head and invalidates the above exact-head claim for the new head until CI is re-run. Do not merge on the strength of prior-head checks.

## Local runtime evidence — SentinelX host

Host ID: `host_5f7264034bdf0b51`, `Voktors-Mini.Dlink`.

- FCC process `15499` listens on `127.0.0.1:8082`; health HTTP 200. Admin config reports `HOST=127.0.0.1`, `PORT=8082`. This corrects the earlier inaccurate inference that this listener was bound to all interfaces.
- Current admin read-back: `MODEL=ollama/qwen3:4b`, `OLLAMA_BASE_URL=http://127.0.0.1:11434`, `PROXY_AUTH_ENABLED=false`. Secret value was not emitted.
- A deliberately invalid unauthenticated POST to `/v1/messages` returned HTTP 422, not HTTP 401. This proves request validation is reachable without authentication; auth is not enforced on that request path.
- A partial admin POST attempted to set `MODEL=ollama/llama3.2:3b` and `PROXY_AUTH_ENABLED=true`; the API returned `applied=true`, but read-back remained unchanged. The configuration mutation is **NOT APPLIED / NOT VERIFIED**. No token was printed or changed.
- Ollama `llama3.2:3b` direct inference returned exact marker `MEDIAHUB_LOCAL_LLAMA_OK`, `done=true`, `eval_count=8`, total duration `8478378166 ns` (~8.48 s). FCC model catalog contains aliases `anthropic/ollama/llama3.2:3b` and `claude-3-freecc-no-thinking/ollama/llama3.2:3b`; default remains Qwen. This is Ollama-only evidence, not FCC-routed Claude Code qualification.

## Cloud route / controller

- Cloud OpenRouter provider invocation: **NOT RUN**. PR review and route admission are incomplete.
- Fresh `/next` comment on Issue #301: [6361110709](https://github.com/VlDMlNSh/mediahub-os/issues/301#issuecomment-6361110709). Controller run ID and three child run/job IDs for this comment are **NOT VERIFIED**; the available event-run query returned no runs and agent-browser disconnected. No dispatch/success is inferred from the comment.
- Historical bounded smoke [39905084056](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39905084056) only proves a prior free-route connectivity/marker check, not coding ability or provider qualification.

## Blockers and next step

1. Diagnose why FCC admin apply returns success but read-back does not change. Inspect the exact config manager prepare/commit contract and admin UI payload; do not try alternate undocumented fields.
2. Establish auth enabled and prove unauthenticated `/v1/messages` returns HTTP 401 before sending any valid inference request. Keep listener loopback-only.
3. Apply the local Llama default only after the config contract is understood; verify admin read-back and an authenticated FCC-routed marker request.
4. For cloud: obtain independent review of PR #530, run exact-head CI after this report commit, then use only the approved owner-gated workflow for a free-only smoke. No paid fallback.
5. Verify latest controller/child run IDs via Actions before claiming agent execution.

No merge, no provider call this wave, no runtime qualification, no production authorization, no Contour A acceptance.
