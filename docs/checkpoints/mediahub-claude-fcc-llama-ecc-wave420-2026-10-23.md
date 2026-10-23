# MediaHub OS — Cloud Claude FCC + Local LLaMA FCC + ECC (Wave 420)

- Date: 2026-10-23
- Status: **POLICY / PROFILE IMPLEMENTED ON DRAFT PR; LATEST CI NOT VERIFIED; LOCAL RUNTIME BLOCKED**
- Base/main SHA: `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- PR: [#530 — Claude FCC free-route admission](https://github.com/VlDMlNSh/mediahub-os/pull/530)
- PR code head verified in this update: `28ad807045f246897bf11df82da90ee32588cfdb`
- Working branch: `contour-a/claude-fcc-admission-router-20261023`
- Parent tracker: [Issue #301](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- Claude executor tracker: [Issue #496](https://github.com/VlDMlNSh/mediahub-os/issues/496)
- Canonical map: [MEDIAHUB-CHAT-TREE-MAP.md](https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md)
- Canonical documentation branch remains `docs/mediahub-chat-tree-map-20261012`; this PR branch is not canonical or accepted.

## Cloud Claude FCC / OpenRouter free-only route

The draft PR proposes a separate, owner-gated Claude admission workflow. It is not a direct provider API caller. Gates require dispatch from `refs/heads/main`, owner actor, explicit `confirm=true`, exact full `target_sha == github.sha`, `MEDIAHUB_ALLOW_FCC_FREE_CLAUDE=true`, and presence of `OPENROUTER_API_KEY`. It pins FCC source at `3d2ae2306752dbdf504714a5489bcfcf69b2d04a` and Claude Code at `2.1.282`, requires a concrete returned model ID ending `:free`, disables paid Anthropic fallback, uses a run-scoped FCC token and an empty workspace, and records the target SHA. No live provider request was made during this pass.

## ECC profile

- Official upstream: [affaan-m/ECC](https://github.com/affaan-m/ECC)
- Pinned source commit/tag target: `c05b2d6614f62f6db0047669aa4eefb223d478f9` (manifest at this ref reports ECC `2.2.3`).
- License: MIT; LICENSE blob `b832b6f642312312367c07688dc7426db40a82ed`.
- Selected, blob-pinned skills:
  - `skills/verification-loop/SKILL.md`: `d7eb1fa239fd8c0ba8ae2d31a3c34d1f01741ef9`
  - `skills/security-review/SKILL.md`: `3f26b0df65661425de4e5c40c295e04edcad7a83`
  - `skills/search-first/SKILL.md`: `3d2669e71ba54afba95defb05080253058190600`
- The workflow assembles only those skill texts as prompt guidance. ECC hooks, MCP servers, plugins, installer side effects and independent orchestration are not enabled. A PR-only `ecc-profile-preflight` job checks the exact upstream commit and blobs without provider credentials.
- The PR-only ECC preflight has now passed on code head `28ad807045f246897bf11df82da90ee32588cfdb` (run `39922262095`, job `120310166318`).

## Local Claude-FCC-LLaMA executor

- Approved host: `Voktors-Mini.Dlink`, SentinelX host ID `host_5f7264034bdf0b51`, agent `0.23.30`, allowlist-based capabilities.
- `llama-server` responds on loopback `127.0.0.1:8081`: `/health` HTTP 200 and `/v1/models` HTTP 200. The model advertised by the server is `/Users/voktor/Library/Application Support/MediaHub/models/qwen2.5-coder-1.5b-instruct/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf`.
- The legacy FCC env file was briefly changed to the `llamacpp` provider, but the running service did not adopt those settings; the file was restored atomically to its prior Ollama-backed `qwen2.5-coder:1.5b` configuration (mode `0600`). No secret value was printed or copied into the repository.
- The user LaunchAgent plist `com.mediahub.fcc-server.plist` was created, validated, bootstrapped, then unloaded after the config-precedence issue. FCC still responds at default loopback port `8082`; configured `18093` remains unavailable. `lsof` verified Python PID `15499`, owned by `voktor`, bound only to `127.0.0.1:8082`. An unauthenticated request to `http://127.0.0.1:8082/v1/models` returned HTTP 200 and listed only Ollama Qwen aliases, not `llama3.2:3b`. `ollama show llama3.2:3b` now succeeds, but FCC does not yet advertise that model. Effective managed auth/provider settings remain unverified; `~/.fcc/.env` is mode `0600`, and the settings inspection timed out through SentinelX. Treat local FCC as **BLOCKED / NOT VERIFIED**; do not submit a task or use the endpoint until authentication and model routing are corrected.
- No local model inference, signed-task submission or qualification occurred.

## Verification / exact evidence

Latest source blobs on the PR branch at time of this report:
- Router `.github/ai/model-router.yml`: `e249333c1c0ce6c1c586a5f498dbfd3979418f6e`
- Cloud FCC workflow: `384eee5209d2ec129ff2d0e92e953d3cad0fa863`
- AI Factory verifier: `e8a4a62dc480b23b5db452fe4a47527e3f44137a`
- Routing tests: `fcfc37d046a9670c793c7282f9c0c9369d6fdae1`
- FCC workflow contract tests: `86f4c641225a0192b600d7462a5cfb15d51df49e`

On PR code head `28ad807045f246897bf11df82da90ee32588cfdb`, all six workflows succeeded: provider contract `39922262324` / job `120310054497`; AI Factory `39922262275` / job `120310054635`; Astra agent boundary `39922262305` / job `120310054433`; Cloud Runtime `39922261963` / job `120310053515`; Astra Verify `39922262337` / job `120310054731`; FCC admission workflow `39922262095` — contract tests `120310166102`, ECC source/skill preflight `120310166318`, install-smoke `120310166374`, managed-auth preflight `120310166383` all SUCCEEDED. Dispatch gate `120310167194` and bounded worker `120310168373` were SKIPPED as expected on the PR event, so no provider inference occurred. This verifies code head `28ad807...`, not the report-only follow-up created by this edit, and does not establish independent review or qualification. No formal PR review exists; PR #530 remains draft/open/unmerged.

A fresh `/next` comment was created on Issue #301 (comment ID `6360168955`). The controller run ID and all three child run/job IDs could not be independently retrieved in this pass, so Gemini dispatch outcome is **NOT VERIFIED**; no agent success is claimed.

## Governance and next step

- Astra remains the sole control plane and claim/promotion/qualification authority. ECC is guidance only.
- Cloud free-route policy is proposed, not accepted; no provider inference, merge, deployment or production authorization.
- Exact-head CI, including `ecc-profile-preflight`, passed on code head `28ad807...`; the report-only follow-up still needs its own checks.
- Obtain independent security/governance review before any live cloud provider call.
- In parallel, resolve FCC managed-config precedence and enforce authentication. The desired repo route is `fcc_ollama` with `llama3.2:3b` on `Voktors-Mini.Dlink`; only after the active FCC endpoint authenticates and advertises that model should the existing Astra issuer submit a bounded signed task.
