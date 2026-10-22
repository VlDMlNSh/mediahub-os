# Canonical map addendum — Wave 357 OmniRoute/Ollama qualification boundary (2026-10-22)

- Report: [Wave 357 — OmniRoute local inference probe and Claude Code qualification boundary](../checkpoints/MEDIAHUB-NEXT-OMNIROUTE-LOCAL-INFERENCE-AND-CLAUDE-CODE-QUALIFICATION-WAVE-357-2026-10-22.md).
- Historical OmniRoute request logs recovered: 442 entries from 2026-10-07; 24 status 200, 408 status 504, 8 status 499, 2 status 502. Historical provider was local `llama-cpp`; timeouts are material evidence and are not hidden.
- Current OmniRoute 3.8.50 launched on explicit loopback `127.0.0.1:20128`; health endpoints returned HTTP 200. A pinned local llama.cpp chat returned exact marker `OMNIROUTE_LOCAL_PROBE_OK_20261022`, exit 0, 5.481 s; OmniRoute call log confirms HTTP 200, provider `llama-cpp`, 4.524 s.
- Current database contains exactly one active provider connection, `llama-cpp` at `127.0.0.1:8081`; no active Ollama connection. Ollama is separately available at `127.0.0.1:11434` with local models, but OmniRoute→Ollama is NOT CONFIGURED.
- Claude Code through OmniRoute did not complete a tool-using task: the existing alias reached the local llama.cpp route but was rejected because request context 42,236 tokens exceeded the 32,768-token local context. No files changed. Claude Code tool execution remains NOT VERIFIED.
- FCC→Ollama transport HTTP 200 remains historical Wave 356 evidence, while FCC CLI autonomous task execution remains NOT VERIFIED. Do not promote either route as fully qualified based on transport-only evidence.
- Standard route decision: OmniRoute remains a **candidate**, not the default Claude execution route, until a bounded Claude Code task succeeds through an explicitly pinned local Ollama provider with no paid fallback.
- No secrets read, no Gemini dispatch, no public listener opened. [Canonical map](MEDIAHUB-CHAT-TREE-MAP.md).
