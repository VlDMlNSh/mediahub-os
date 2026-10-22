# MediaHub Next — Wave 358: Local Claude route comparison and bounded qualification

Date: 2026-10-22

## Decision summary

**SELECTED FOR THE NEXT QUALIFICATION ITERATION: FCC AS THE PRIMARY CLAUDE-COMPATIBLE GATEWAY; OMNIROUTE AS THE SECONDARY, BROADER PROVIDER ROUTER. AUTONOMOUS CLAUDE CODE EXECUTION: NOT QUALIFIED.**

The choice is deliberately limited. Both routes pass simple local inference tests, but neither completed a genuine Claude Code tool-use task. Do not promote either route to an accepted autonomous executor until the tool invocation is actually executed and the expected file-derived result is returned.

## Immutable scope and host evidence

- Repository worktree: `/Users/voktor/dev/mediahub-pr437-sync`, branch `work/wave356-pr437-sync`, HEAD `2e23f9a99e655369672340329c4c1b6de25f1576`; worktree remained clean.
- Host: `Voktors-Mini.Dlink`, macOS 14.7.4, Claude Code 2.1.282, OmniRoute 3.8.50, Ollama 0.34.4.
- SentinelX host ID `host_5f7264034bdf0b51` is operational; capability query succeeded. Its bounded exec attempt timed out at the agent boundary, so interactive runtime tests were completed using the authorized Remote Desktop Commander device `e264f341-2e21-4dfc-9f97-9b95cd08bcd3`.
- Runtime listeners remained loopback-only: llama.cpp `127.0.0.1:8081`, FCC `127.0.0.1:8082`, OmniRoute `127.0.0.1:20128`, Ollama `127.0.0.1:11434`.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Related evidence: [Wave 357](MEDIAHUB-NEXT-OMNIROUTE-LOCAL-INFERENCE-AND-CLAUDE-CODE-QUALIFICATION-WAVE-357-2026-10-22.md), [Wave 356](MEDIAHUB-NEXT-PR437-CI-REPAIR-AND-LOCAL-ROUTE-PROBE-WAVE-356-2026-10-22.md), [Wave 351 historical FCC/Ollama evidence](MEDIAHUB-NEXT-CLAUDE-FCC-OLLAMA-HISTORICAL-EVIDENCE-WAVE-351-2026-10-22.md).

## Configuration changes

1. Added an OmniRoute local Ollama provider connection through the supported `omniroute providers add` CLI:
   - connection ID `b93485b9-434a-4cf3-b344-21bad449244a`
   - provider `ollama-local`, connection name `mediahub-local-ollama`
   - active, default model `qwen3:4b`
   - upstream `http://127.0.0.1:11434/v1`
   - local adapter requires credential-shaped connection metadata; a non-secret placeholder is stored, not an external provider credential.
2. No FCC route configuration was changed. Current FCC settings were inspected without reading secret values:
   - `MODEL=ollama/qwen3:4b`
   - `MODEL_OPUS=MODEL_SONNET=MODEL_HAIKU=ollama/qwen3:4b`
   - `OLLAMA_BASE_URL=http://127.0.0.1:11434`
   - `MODEL_FALLBACKS` is empty
   - `REASONING_POLICY=off`
3. OmniRoute now has two active local provider connections: `llama-cpp` at `127.0.0.1:8081` and `ollama-local` at `127.0.0.1:11434/v1`. No external provider connection was active in its local connection inventory.
4. No public listener was opened. No paid provider was called. No secrets or real provider credentials were read or printed.

## Test matrix

| Test | Result | Evidence / limitation |
|---|---|---|
| FCC health | **PASS** | `GET /health` HTTP 200 |
| FCC model catalog | **PASS** | `GET /v1/models` HTTP 200; 14 entries, all current local Ollama aliases/Claude-compatible aliases |
| FCC → Ollama text inference | **PASS** | `POST /v1/messages`, pinned `anthropic/ollama/qwen2.5-coder:1.5b`; HTTP 200, exact marker `FCC_OLLAMA_ROUTE_OK_20261022`, 0.50 s |
| FCC → Claude Code read-only task | **NOT VERIFIED** | Attempt with Claude alias remained without a completed task result and was stopped after ~51 s; FCC log confirmed an upstream Ollama HTTP 200, which is transport evidence only |
| FCC → Claude Code with exact local 1.5B model | **NOT QUALIFIED** | CLI emitted a JSON-looking `Read` tool request as plain text; no actual Read tool execution/result was observed |
| FCC → Claude Code with qwen3:4b | **NOT VERIFIED** | Bounded 30 s attempt ended by alarm (exit 142), with no tool result |
| Direct Ollama native tool-call probe | **FAIL / INCOMPATIBLE UNDER TEST** | `qwen2.5-coder:1.5b` returned JSON in plain content and zero native `tool_calls`; `qwen2.5-coder:3b` and `qwen3:4b` each exceeded an 18 s bound |
| OmniRoute health | **PASS** | `GET /api/health` HTTP 200; `GET /api/monitoring/health` previously returned healthy |
| OmniRoute → Ollama text inference | **PASS** | Pinned `ollama/qwen2.5-coder:1.5b`; exact marker `OMNIROUTE_OLLAMA_ROUTE_OK_20261022`, exit 0; OmniRoute call log HTTP 200, provider `ollama`, 570 ms |
| OmniRoute → llama.cpp text inference | **PASS with exact live model ID** | Exact marker `OMNIROUTE_LLAMACPP_ROUTE_OK_20261022`, exit 0, 3.832 s |
| OmniRoute short llama.cpp alias | **FAIL** | `llamacpp/qwen2.5-coder-1.5b-instruct-q4_k_m` rejected as absent from the active live catalog; the server's actual model ID is its full local GGUF path |
| OmniRoute → Claude Code with Ollama | **FAIL / NOT QUALIFIED** | Claude Code request to `ollama/qwen2.5-coder:1.5b` rejected HTTP 400 because the model does not support the thinking request. A separate `claude-sonnet-4-5` alias hit a 42,236-token request against 32,768 available context |
| External free API provider | **NOT RUN / NOT CONFIGURED** | Catalog entries exist, but no external provider was configured and qualified in this pass; no external API call was made |
| Repository integrity | **PASS** | Worktree clean at exact HEAD; no project source file changed |

## Catalog breadth and free-route policy

- FCC documentation describes 25 provider backends, including local Ollama and llama.cpp plus external provider adapters. FCC supports per-tier model routing and an ordered fallback list. This host's current fallback list is empty, so requests do not silently spill into a different configured provider.
- OmniRoute 3.8.50 exposes a catalog of 352 provider definitions across categories including local, free/API-key, no-auth, OAuth, search, audio, and cloud-agent. Its local catalog contains 14 provider types, including Ollama and llama.cpp.
- Catalog availability is not the same as an active, free, qualified route. External free-tier APIs may require provider-issued credentials, have quotas, or impose model/tool limits. No external provider was activated or called here. Before adding any external route, require explicit free-tier evidence, quota policy, expiry/revocation behavior, tool-use test, and a fail-closed no-paid-fallback configuration.
- Sources: FCC provider overview https://github.com/Factix/fcc ; FCC provider setup https://pypi.org/project/free-claude-code/6.16.5/ ; OmniRoute v3.8.50 provider reference https://github.laiyagushi.com/diegosouzapw/OmniRoute/blob/release/v3.8.50/docs/reference/PROVIDER_REFERENCE.md .

## Route selection

1. **Primary Claude gateway candidate: FCC.** It exposes the Anthropic Messages protocol used by Claude Code, its direct local Ollama path is freshly verified, its current tier routes all point to local Ollama, and its fallback list is empty. This is the simpler Claude-specific execution gateway.
2. **Secondary broad provider router: OmniRoute.** It has the broader catalog and now has verified text inference through both local Ollama and llama.cpp. It is the preferred place to qualify additional local/free provider routes one at a time.
3. **Current safe model choice for fast route smoke tests:** `qwen2.5-coder:1.5b`. It answers quickly, but failed native tool-use qualification; do not use it as evidence of an autonomous Claude worker.
4. **Do not qualify qwen3:4b or the current Claude aliases yet.** Under these bounded tests, qwen3:4b timed out in direct tool probing/CLI; the existing llama.cpp alias exceeded the local context limit; the local Ollama model was rejected when Claude Code sent thinking.
5. **Autonomous engineering status remains NOT QUALIFIED.** The next pass should repair model/tool compatibility: use a local model proven to emit native tool calls, ensure the proxy strips/normalizes unsupported thinking fields, keep a bounded system prompt and enough context, and then run one read-only task whose output proves that Read actually executed. Only after that should a local route be promoted as the standard Claude work route.

## Security and provenance

- No external provider was called; no paid fallback was configured or used.
- Gemini was not dispatched and this Mac was not used for Gemini transport.
- No repository source changes; worktree remains clean at `2e23f9a99e655369672340329c4c1b6de25f1576`.
- Runtime configuration change is limited to one local OmniRoute provider connection; both new and existing model servers remain bound to loopback.
- Final status: **LOCAL INFERENCE ROUTES VERIFIED / FCC SELECTED AS PRIMARY GATEWAY CANDIDATE / OMNIROUTE SECONDARY ROUTER VERIFIED FOR TEXT / CLAUDE TOOL EXECUTION NOT VERIFIED / AUTONOMOUS ROUTE NOT QUALIFIED / NOT ACCEPTED**.
