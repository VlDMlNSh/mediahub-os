# MediaHub Next — Wave 357: OmniRoute local inference probe and Claude Code qualification boundary

Date: 2026-10-22

## Status

**OMNIROUTE LOOPBACK SERVER VERIFIED / OMNIROUTE→LOCAL LLAMA.CPP CHAT VERIFIED / OMNIROUTE→OLLAMA NOT CONFIGURED / CLAUDE CODE TASK NOT VERIFIED / FCC→OLLAMA HISTORICAL TRANSPORT EVIDENCE RETAINED / DEFAULT ROUTE NOT PROMOTED.**

## Scope and target

- Host: `Voktors-Mini.Dlink`, Remote Desktop Commander device ID `e264f341-2e21-4dfc-9f97-9b95cd08bcd3`.
- Repo worktree inspected read-only: `/Users/voktor/dev/mediahub-pr437-sync`, branch `work/wave356-pr437-sync`, HEAD `2e23f9a99e655369672340329c4c1b6de25f1576`; worktree remained unchanged.
- OmniRoute CLI: `3.8.50`; Claude Code CLI: `2.1.282`; macOS `14.7.4`.
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Prior evidence: [Wave 351 historical evidence](MEDIAHUB-NEXT-CLAUDE-FCC-OLLAMA-HISTORICAL-EVIDENCE-WAVE-351-2026-10-22.md), [Wave 352 OmniRoute/Claude evidence](MEDIAHUB-NEXT-OMNIROUTE-CLAUDE-RUNTIME-AND-GEMINI-EFFORT-WAVE-352-2026-10-22.md), [Wave 356 FCC probe](MEDIAHUB-NEXT-PR437-CI-REPAIR-AND-LOCAL-ROUTE-PROBE-WAVE-356-2026-10-22.md).

## Historical evidence recovered

- `~/.omniroute/call_logs` contains 442 historical JSON request logs dated 2026-10-07. Safe metadata aggregation found 24 status-200 records, 408 status-504 records, 8 status-499 records, and 2 status-502 records. The dominant historical provider/model was local `llama-cpp`; the 504 entries report local execution expiration. This establishes historical use but also a material timeout risk.
- `~/.omniroute/storage.sqlite` has one active provider connection: `llama-cpp`, connection label `df3-llama`, model `qwen2.5-coder-1.5b-instruct-q4_k_m`, upstream `http://127.0.0.1:8081`. No active Ollama provider connection was present.
- Local Ollama separately reports models `qwen2.5-coder:3b`, `qwen3:4b`, and `qwen2.5-coder:1.5b` on `127.0.0.1:11434`.
- Existing OmniRoute alias `claude-sonnet-4-5` maps to the local llama.cpp model path, not to Ollama. Do not conflate this with an OmniRoute→Ollama route.

## Fresh runtime evidence

1. Started OmniRoute with explicit `OMNIROUTE_SERVER_HOST=127.0.0.1` and `omniroute serve --port 20128 --no-open --no-tray --log`. Listener inspection confirmed only `127.0.0.1:20128`; the model endpoint `127.0.0.1:8081`, Ollama `127.0.0.1:11434`, and FCC `127.0.0.1:8082` were also loopback-only.
2. `GET /api/health` returned HTTP 200 and `GET /api/monitoring/health` returned `{"status":"healthy","setupComplete":false}`.
3. A bounded `omniroute chat` request pinned to the exact local llama.cpp model returned the exact marker `OMNIROUTE_LOCAL_PROBE_OK_20261022`, exit code 0, in 5.481 seconds. OmniRoute's own call log recorded HTTP 200, provider `llama-cpp`, local connection `df3-llama`, duration 4524 ms, no error. This is verified local OmniRoute chat/inference, not Claude Code task execution and not Ollama.
4. Claude Code launch attempts were kept read-only and bounded. A non-provider-prefixed Anthropic model was rejected as unavailable; the exact local filesystem model ID was rejected as an unrecognized model. Using the existing `claude-sonnet-4-5` alias reached the local route but failed with HTTP 400 because the prompt/context footprint was 42,236 tokens while the local llama-server context is 32,768. No repository files were changed. No successful Claude Code tool execution was captured.
5. No OmniRoute provider configuration was changed. No paid provider was invoked by the successful pinned local chat test. The OmniRoute server was deliberately bound to loopback; no public listener was opened.

## Route disposition

| Route / property | State | Evidence |
|---|---|---|
| FCC → Ollama HTTP transport | **VERIFIED HISTORICALLY / fresh retest not run here** | Wave 356: HTTP 200, exact marker, upstream log to `127.0.0.1:11434` |
| FCC → autonomous Claude Code task | **NOT VERIFIED** | Wave 356 bounded CLI attempt produced no completed task result |
| OmniRoute server on loopback | **VERIFIED** | health HTTP 200; listener only `127.0.0.1:20128` |
| OmniRoute → local llama.cpp chat | **VERIFIED** | fresh exact-marker response, HTTP 200, 4.524 s in call log |
| OmniRoute → Ollama | **NOT CONFIGURED / NOT VERIFIED** | no active Ollama provider connection; active connection points to llama.cpp |
| Claude Code tool execution through OmniRoute | **NOT VERIFIED** | context-limit failure; no successful Read tool result |
| OmniRoute promoted to default Claude execution route | **NOT PROMOTED** | full Claude Code task acceptance criterion not met |
| Paid fallback absent for the pinned local chat | **VERIFIED FOR THAT REQUEST** | exact local model pinned and only active provider connection is local llama.cpp |

## Next bounded step

1. Reuse the existing OmniRoute installation; do not rebuild it.
2. Configure a distinct local Ollama provider connection through OmniRoute's supported UI/API only after confirming its exact schema and fail-closed routing behavior. Keep it loopback-only and explicitly pin `ollama/qwen3:4b` or another locally installed model; no cloud fallback.
3. Solve the Claude Code context constraint with a supported local model/context configuration, then rerun one read-only task and capture the successful tool invocation plus matching OmniRoute call-log provider/model/status.
4. Freshly retest FCC→Ollama through the Claude CLI, not just direct HTTP, before labeling the FCC executor fully qualified.
5. Only promote OmniRoute as the standard Claude work route after a completed read-only or bounded engineering task, verified Ollama upstream, no paid fallback, and a clean worktree.

## Safety and change record

- No secrets, provider credentials, API keys, or token values were read or printed.
- No Gemini dispatch or GitHub workflow was triggered. The Mac remains a separate local executor and was not used for Gemini.
- No repo files were changed; the inspected worktree remained at `2e23f9a99e655369672340329c4c1b6de25f1576`.
- OmniRoute server PID observed: 23645; process launched by CLI PID 23599. Loopback bind was explicit.
- Status is **PARTIAL VERIFIED / NOT QUALIFIED / NOT ACCEPTED** for the requested Claude-OmniRoute-Ollama standard route.
