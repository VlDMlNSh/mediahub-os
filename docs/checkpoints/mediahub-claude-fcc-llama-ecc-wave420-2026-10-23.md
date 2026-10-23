# MediaHub OS — Cloud Claude FCC + Local LLaMA FCC + ECC (Wave 420)

- Date: 2026-10-23
- Status: **POLICY / PROFILE IMPLEMENTED ON DRAFT PR; LATEST CI NOT VERIFIED; LOCAL RUNTIME BLOCKED**
- Base/main SHA: `fbbdc9a06ef344cd57aae13b230a042af76bbc60`
- PR: [#530 — Claude FCC free-route admission](https://github.com/VlDMlNSh/mediahub-os/pull/530)
- PR head observed before this report: `64bfba5efe6f5b5759854379b4f1c903a2e0c85c`
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
- This new preflight was added after the prior green CI set; its latest execution is **NOT VERIFIED** until the CI run for current PR head is observed.

## Local Claude-FCC-LLaMA executor

- Approved host: `Voktors-Mini.Dlink`, SentinelX host ID `host_5f7264034bdf0b51`, agent `0.23.30`, allowlist-based capabilities.
- `llama-server` responds on loopback `127.0.0.1:8081`: `/health` HTTP 200 and `/v1/models` HTTP 200. The model advertised by the server is `/Users/voktor/Library/Application Support/MediaHub/models/qwen2.5-coder-1.5b-instruct/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf`.
- The legacy FCC env file `~/Library/Application Support/MediaHub/fcc.env` was changed atomically (mode `0600`) to select the FCC `llamacpp` provider and `LLAMACPP_BASE_URL=http://127.0.0.1:8081/v1`. No secret value was printed or copied into the repository.
- A user LaunchAgent plist `com.mediahub.fcc-server.plist` was created and validated. The attempted launch exposed a configuration-precedence issue: FCC became reachable on its default `8082` endpoint, while configured `18093` stayed unavailable. The LaunchAgent was unloaded, but a subsequent probe still returned HTTP 200 from `8082`; the listener PID/owner could not be verified because SentinelX disconnected during inspection. The managed `~/.fcc/.env` exists with mode `0600`, but the relevant effective settings were not confirmed. Treat the local FCC runtime as **BLOCKED / NOT VERIFIED**; do not submit a task or claim authentication/model routing is correct.
- No local model inference, signed-task submission or qualification occurred.

## Verification / exact evidence

Latest source blobs on the PR branch at time of this report:
- Router `.github/ai/model-router.yml`: `f319a24a1323ce68393633b08a6cb232ed2dfcff`
- Cloud FCC workflow: `384eee5209d2ec129ff2d0e92e953d3cad0fa863`
- AI Factory verifier: `49946c462baf344201cd2fce7e952fe1046a88b5`
- Routing tests: `0fa4f103db3707de7bcbaeeeafad9a0c69402ee8`
- FCC workflow contract tests: `40402074f8e7af5f320cf964380fe65136fd07b9`

On prior code head `fdb73f9155c16c1679f156fe2265eaa80f5b6ffe`, all six observed workflows succeeded: AI Factory `39921151754`, Astra agent verification `39921151870`, provider contract `39921151809`, FCC workflow `39921151867`, Astra Verify `39921151755`, Cloud Runtime `39921151758`. That run preceded the final ECC PR-only preflight change. A query for the current head `64bfba5efe6f5b5759854379b4f1c903a2e0c85c` returned no workflow runs and no status contexts; current exact-head CI is therefore **NOT VERIFIED**, not PASS. No formal PR review exists; PR #530 remains draft/open/unmerged.

A fresh `/next` comment was created on Issue #301 (comment ID `6360168955`). The controller run ID and all three child run/job IDs could not be independently retrieved in this pass, so Gemini dispatch outcome is **NOT VERIFIED**; no agent success is claimed.

## Governance and next step

- Astra remains the sole control plane and claim/promotion/qualification authority. ECC is guidance only.
- Cloud free-route policy is proposed, not accepted; no provider inference, merge, deployment or production authorization.
- First verify exact-head CI including `ecc-profile-preflight`, then obtain independent security/governance review.
- In parallel, resolve the FCC managed-config precedence and identify the surviving loopback listener before changing it. Only after authenticated FCC `/v1/models` on the intended port and a validated `llamacpp` model reference pass should the existing Astra issuer submit a bounded signed task.
