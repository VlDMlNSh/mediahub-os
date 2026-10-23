# MediaHub Claude FCC + ECC Cloud Route and Local Llama Executor — Wave 429

Date: 2026-10-23  
Status: **PARTIALLY VERIFIED / CLOUD QUALIFICATION NOT ACCEPTED / LOCAL FCC EXECUTION BLOCKED**

## Objective

Continue two isolated paths without weakening Astra authority:

1. GitHub-hosted Claude Code → pinned Free Claude Code (FCC) → OpenRouter concrete `:free` model, no paid fallback, with pinned ECC guidance.
2. `Voktors-Mini.Dlink` local Claude Code → FCC → Ollama `llama3.2:3b` + ECC guidance.

Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](../architecture/MEDIAHUB-CHAT-TREE-MAP.md).  
Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301  
Cloud qualification issue #496: https://github.com/VlDMlNSh/mediahub-os/issues/496

## Immutable source and policy evidence

- Observed `main` SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- PR #530 is merged at merge commit `4fe1486e2062d276c4dba2ab8c9ed97f261e9086`; its head was `e4a2e1cb9961e806f3351addf0569a1ed22f85b0`. Merge status is verified, but this is not evidence of independent review or live provider qualification.
- PR #563 is merged. Exact-head workflows `39962161538` (Astra Cloud Runtime Validation), `39962161549` (Astra Verify), and `39962161545` (FreeLLMAPI Live Qualification) concluded success; the live `qualify` job was skipped for the PR event. This remains separate from Claude FCC qualification.
- Main router policy blob: `e249333c1c0ce6c1c586a5f498dbfd3979418f6e`. It names `fcc_openrouter_free` for cloud Claude, `fcc_ollama` + `llama3.2:3b` on `Voktors-Mini.Dlink` for local Claude, allowlists the FCC workflow as cloud transport, and sets `paid_fallback: false`.
- Main FCC workflow blob: `384eee5209d2ec129ff2d0e92e953d3cad0fa863`. Its manual dispatch requires `confirm=true`, exact current workflow SHA, `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE=true`, and presence of `OPENROUTER_API_KEY`; the OpenRouter response must return a concrete model ID ending in `:free`. No provider request was made in this pass.
- ECC upstream remains pinned to `affaan-m/ECC@c05b2d6614f62f6db0047669aa4eefb223d478f9` (plugin version 2.2.3 verified in earlier evidence). ECC is guidance only; hooks/MCP servers do not gain control-plane authority.

## Fresh controller dispatch — comment 6367501128

Controller run: https://github.com/VlDMlNSh/mediahub-os/actions/runs/39971768646  
Target SHA: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.

- Admission job `120477175602`: **SUCCEEDED**.
- Dispatch/monitor job `120477216256`: **FAILED** because two child workflows failed their bounded engineering postcondition.
- Agent 1 run [39972135815](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39972135815): jobs `120477293947` and `120477338042` **SUCCEEDED**. Artifact `gemini-output`, ID `12509693220`, digest `sha256:01dace26df848e94c975ca930df59ee50c4d5509cba970dadb490ce52b8a06ad`. It created report-only PR #584: https://github.com/VlDMlNSh/mediahub-os/pull/584.
- Agent 2 run [39972138796](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39972138796): signature job `120477308550` **SUCCEEDED**; bounded task `120477360663` **FAILED**. Artifact ID `12509681909`, digest `sha256:332807d3a1afa8005cf3d71752b684c2b154035d980e0ebe01e0c1f6beaf440b`.
- Agent 3 run [39972142422](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39972142422): signature job `120477318032` **SUCCEEDED**; bounded task `120477358298` **FAILED**. Artifact ID `12509373521`, digest `sha256:75d08cdd216c937ed9021d151e24e2cfff81d0da5e026a5f4698828e2c963c80`.
- Both Agent 2/3 artifacts were downloaded and inspected. They contain a non-empty response, but the response says a PR is active while the tool telemetry contradicts that claim: `create_branch` failed and `create_pull_request` failed for both; only `create_or_update_file` succeeded. The final child step correctly failed because there was no successful `create_pull_request` tool result. Do not count the claimed PRs as created by these child runs.
- The requested branch names already exist: `agent-2-contract-verification-20261023`, `agent-3-security-provenance-audit-20261023` (verified by branch search). This is consistent with branch/PR collisions from the queued repeated /next runs; exact existing-PR mapping for these failed attempts is **NOT VERIFIED**.
- Agent 2 artifact's claimed evidence blob: `61b672992045801b58802acbe3c0d8d17a1c50a2`. Agent 3 artifact's claimed checkpoint blob: `e39a26f2191d71c5228f87dc9c056810a6342dc6`. Their artifact content must not be treated as accepted repo evidence without branch/PR read-back and independent verification.
- The Gemini child runner emitted free-tier input-token quota errors and retry messages in Agent 1 stderr; Agent 1 eventually completed. Quota pressure is observed, not a reason to switch to a paid route.

## PR #584 and exact-head CI

- PR #584 head: `f3ccef41b7d35a4ca9a2a80da2e54f016af7a027`, report-only. Its Astra Cloud Runtime Validation run `39972829407` and Astra Verify run `39972829450` returned `action_required`; job arrays were empty through the available API. Therefore exact-head CI is **NOT VERIFIED**, not PASS.
- Formal PR reviews for #584: none. Combined commit status contexts: empty. Do not merge.
- PRs #569–#581 are also open reports/changes from prior controller waves; the inspected Astra Verify and Cloud Runtime checks on these heads are `action_required`, with no formal reviews and empty combined status contexts. Do not treat these repeated PRs as accepted.

## Local FCC runtime — BLOCKED

Host: `Voktors-Mini.Dlink`, SentinelX host ID `host_5f7264034bdf0b51`.

- Current report and prior live checks agree that FCC is listening on loopback `127.0.0.1:8082`, but process-owned config still reports `MODEL=ollama/qwen3:4b` and `PROXY_AUTH_ENABLED=false`.
- Unauthenticated `GET /v1/models` returned HTTP 200; an unauthenticated malformed `/v1/messages` request returned HTTP 422, not 401. Bearer authentication is therefore not enforced.
- Direct Ollama inference with `llama3.2:3b` previously returned `MEDIAHUB_LOCAL_LLAMA_OK`; this proves direct model inference only. It does not qualify FCC-routed Claude Code or ECC execution.
- The LaunchAgent plist `/Users/voktor/Library/LaunchAgents/com.mediahub.fcc-server.plist` is outside the active SentinelX writable file-operation allowlist. No shell bypass was used. A controlled persistent change requires owner-authorized addition of this exact file to the allowlist, then config write/read-back and restart verification.
- Required acceptance before any local coding task: FCC binds only to loopback; auth enabled; model `ollama/llama3.2:3b`; unauthenticated request returns 401; authenticated local model-list and bounded marker request succeed; logs contain no credentials.

## Disposition and next bounded step

- Cloud Claude route policy: **MERGED / STATIC CONTRACT ONLY**.
- Cloud OpenRouter request: **NOT RUN**; no live qualification or acceptance.
- Local direct Ollama Llama inference: **VERIFIED**; FCC-routed Claude Code/ECC task: **NOT RUN**.
- Agent 1 bounded pass: **SUCCEEDED** as a report-only PR; PR #584 remains **NOT VERIFIED / NOT ACCEPTED**.
- Agent 2 and Agent 3 bounded passes: **FAILED** at branch/PR creation postconditions; their evidence responses are not accepted.
- Controller wave: **FAILED**; no automatic rerun is authorized by this report.

Next: stop accumulating distinct `/next` comments until the serialized controller backlog is reconciled; repair the child-task branch naming/idempotency so each run has a unique, source-correlated branch and does not collide with existing PRs; independently inspect Agent 2/3 evidence and rerun only after that repair. Separately obtain owner authorization for the exact FCC LaunchAgent plist allowlist entry and verify effective auth before local execution. No merge, provider call, runtime qualification, or Contour A acceptance is claimed.

Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
