# MediaHub OS — Chat Context Handoff (2026-10-23)

## Purpose

This file is the durable handoff for continuing MediaHub OS engineering in a new ChatGPT conversation. It captures the work context and the exact current state known at handoff time. Re-check live GitHub state before acting; this document is not a substitute for source/CI verification.

## Canonical project references

- Repository: https://github.com/VlDMlNSh/mediahub-os
- Bootstrap instruction: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CONTEXT-BOOTSTRAP-INSTRUCTION.md
- Canonical chat tree map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Current continuation checkpoint: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-NEXT-CONTINUATION-WAVE-396-2026-10-23.md
- Master roadmap: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/checkpoints/MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md
- Cloud-agent governance Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- FCC free-route proposal PR #502: https://github.com/VlDMlNSh/mediahub-os/pull/502
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`
- Main HEAD observed during handoff: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf` (recheck live).
- PR #502 HEAD observed during handoff: `56f5558b5d664f0a85bddfc4533be89d48e116e2` (recheck live).

## User goal and recent conversation

The user wants to continue autonomously with `/next`, preserve all context between chats, and prioritize getting a usable Claude Code-style worker through free API routes without physical hardware. The user specifically corrected the architecture distinction: Ollama CLI can run inside GitHub Actions while inference is made through an external API; in that case the provider performs the model computation, not GitHub. The user asked to test Claude first via API keys such as OpenRouter and other providers offering free model access (including Qwen and similar models), then asked which providers/keys could sustain free use over multiple weeks.

The user listed these GitHub secret/variable names as present (names only; values must never be read or printed):
- AIONLABS_API_KEY
- ASTRA_COMMAND_HMAC_KEY
- ASTRA_NODE_HMAC_KEY_MH_DEV_01
- ASTRA_NODE_HMAC_KEY_MH_DEV_02
- ASTRA_NODE_HMAC_KEY_VOKTORS_MAC
- CF_ACCOUNT_ID_1, CF_ACCOUNT_ID_2
- CF_API_TOKEN_1, CF_API_TOKEN_2
- DEEPSEEK_API_KEY
- GEMINI_API_KEY, GEMINI_API_KEY_2, GEMINI_API_KEY_3
- GROQ_API_KEY
- HF_TOKEN
- KIMI_API_KEY
- LLM7_TOKEN
- MEDIAHUB_DISPATCH_HMAC_KEY
- MEDIAHUB_GITHUB_TOKEN
- MIMO_API_KEY
- MISTRAL_KEY_1, MISTRAL_KEY_2
- NARA_KEY_1
- NOVITA_KEY_1, NOVITA_KEY_2
- OPENROUTER_API_KEY
- ORCA_KEY
- PAT_DISPATCH
- SAMBANOVA_KEY
- SENTINEL_REQUEST_API_KEY
- SILICON_KEY_1, SILICON_KEY_2, SILICON_KEY_3
- UNOROUTER_API_KEY
- ZAI_KEY_1, ZAI_KEY_2
- ZEROUTER_ (listed as incomplete; do not assume valid or configured)

These names are not proof of current validity, remaining quota, provider terms, or permission to send project data. Do not access secret values. Provider eligibility, quotas, free-model availability, and free-only routing must be verified from official live sources and safe runtime evidence. Do not promise permanent free access. Never enable a paid fallback unless explicitly authorized for that exact provider/model and budget.

## FCC / Claude route status

PR #502 is a draft, open, unmerged proposal:
https://github.com/VlDMlNSh/mediahub-os/pull/502

Feature branch: `contour-a/github-hosted-fcc-openrouter-free-wave400`
Last observed PR head: `56f5558b5d664f0a85bddfc4533be89d48e116e2`
Pinned FCC upstream commit: `3d2ae2306752dbdf504714a5489bcfcf69b2d04a`
Candidate router: `open_router/openrouter/free` (dynamic free-model router, not a stable promise of a specific Qwen/model ID).
Workflow: `.github/workflows/mediahub-fcc-free-claude-worker.yml`
Contract test: `tests/test_mediahub_fcc_free_claude_workflow_contract.py`

Latest checkpoint recorded:
- FCC install smoke succeeded.
- Contract tests passed 4/4.
- Astra Verify and Astra Cloud Runtime Validation succeeded at the recorded intermediate exact head.
- Pull-request event skipped the dispatch-gate and bounded-worker jobs; no provider/model request occurred.
- Formal independent review is NOT VERIFIED.
- Four technical findings remain open: actual provider/model provenance; repository file/data scope too broad; patch artifact secret scanning absent; effective no-fallback configuration not proven.
- Live inference: NOT RUN.
- Live dispatch: BLOCKED pending resolution of findings and gates.
- Contour A: NOT ACCEPTED.

Do not treat green PR CI as proof of live inference or model qualification. Do not merge solely to unlock workflow_dispatch. First resolve the four findings, add negative tests, run exact-head CI, obtain independent review, then consider one bounded, no-write, low-risk inference smoke. Keep `ANTHROPIC_API_KEY` unset/unmapped and disallow all paid fallback. Ensure the actual selected model/provider is recorded without leaking credentials. Scope filesystem access to an explicit disposable workspace, scan generated patch/artifacts for secrets, and fail closed if provider/model or no-fallback semantics cannot be verified.

## Ollama versus hosted API

- Ollama runtime on a GitHub-hosted Actions runner uses ephemeral GitHub compute and disappears when the job ends; it is not a permanent service.
- If Ollama CLI is only used as a client to a hosted API, inference compute is performed by that provider, not by GitHub.
- A local model such as Llama on a GitHub-hosted runner is a separate architecture and is constrained by the runner's RAM/CPU, runtime duration, download cost/time, and runner policy.
- Keep the first qualification experiment bounded, no secrets in the prompt/workspace, read-only/no-write by default, and record runtime, exact model/provider ID, response status, quota/rate-limit outcome, and evidence digests.

## Free API provider evaluation

OpenRouter and Groq were discussed as possible providers with free model routes. GitHub Models was also mentioned as a possible GitHub-integrated option, but availability and model eligibility must be checked against current official docs and account entitlements. Do not rely on rough quota figures from conversation. For each provider, verify official current terms and route-specific limits, model IDs, RPM/RPD/token limits, reset behavior, data policy, account/region restrictions, and whether a request can ever fall back to paid capacity. Use only explicit free routes; on quota exhaustion or unavailable free capacity, fail closed rather than paying or silently switching.

## Mandatory governance and working rules

- At each `/next`, refresh live GitHub refs/HEAD/SHA, Bootstrap, canonical map, checkpoint, Master Roadmap, Issue #301, relevant PRs, exact-head CI, governance and executor availability.
- Read files and inspect exact SHA; if Contents API is blank, retrieve via raw/blob SHA.
- Work autonomously on routine engineering choices, but never bypass issuer/capability, security, provider/quota, branch protection, independent review, budget, or acceptance gates.
- Keep Jarvis, ASTRA A0, and MediaHub Product State Authority permissions separate. Technical capability is not authorization.
- Preserve Functional Baseline 2.0 and historical IDs.
- Distinguish PLANNED, DISPATCHED, RUNNING, SUCCEEDED, VERIFIED, QUALIFIED, ACCEPTED, NOT RUN, BLOCKED, FAILED, NOT VERIFIED.
- Never claim a provider call, agent run, test, review, qualification, merge, deployment, or acceptance without evidence.
- Do not read, echo, or place secret values in logs, prompts, source, commits, artifacts, reports, or chat.
- For Gemini, use only the approved `.github/workflows/gemini-batch-dispatch-controller.yml` controller after all current gates pass. Do not create an ad-hoc transport.
- For each bounded pass, create a dated report, update this continuation checkpoint and the canonical map/addendum when appropriate, include commit/blob SHA, exact-head CI, test evidence, blockers, and next step. Re-read changed files after writes.
- The owner action block is only required if an actual owner action is necessary; when present, make the heading bold uppercase and provide exact steps and links.

## Recommended next step

Continue Wave 403 from current live state:
1. Re-check main, canonical docs branch, PR #502 head/status/reviews/checks, latest checkpoint and Issue #301 comments.
2. Review PR #502 findings against current workflow and contract tests; fix the four findings on its feature branch without triggering live provider inference.
3. Add negative tests for unknown model IDs, no-fallback enforcement, secret/artifact scanning, and out-of-scope file access.
4. Re-run exact-head CI and read back changed files/blob SHAs.
5. Only after independent review and all security gates pass, perform a single bounded no-write inference test through a verified explicit free route. Record provider/model ID and usage/quota evidence, never the key.
6. Separately compare free API providers using current official evidence; do not assume an API key is unlimited or permanently free.

## Short command to resume in a new chat

`/next — Прочитай MEDIAHUB-CHAT-CONTEXT-HANDOFF-2026-10-23.md и актуальные Bootstrap, карту, checkpoint, Master Roadmap, Issue #301 и PR #502; перепроверь live refs/SHA/CI/reviews, продолжи с исправления F1–F4 в PR #502 без live inference до прохождения security gates, затем квалифицируй один explicit free API route и зафиксируй evidence. Не читай секреты и не используй платный fallback.`
