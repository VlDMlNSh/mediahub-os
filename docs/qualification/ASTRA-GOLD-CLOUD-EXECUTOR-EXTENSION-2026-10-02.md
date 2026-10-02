# ASTRA GOLD — Cloud Executor Extension

Status: ARCHITECTURE EXTENSION / NO GATE PROMOTED
Date: 2026-10-02
Related: `architecture/ASTRA-GOLD-REFERENCE-ARCHITECTURE.md`,
`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`

## 1. Question

ASTRA GOLD currently qualifies two local executors (Codex and Claude Code).
Does adding **cloud executors** contradict the reference architecture?

## 2. Answer

**No.** Cloud executors are an *intended* extension of the execution fabric, not
a new authority plane. The reference architecture already separates:

- local execution clients (Codex, Claude Code, Cursor, DeepSeek Harness, Stagewise);
- local model/gateway layer (Ollama, Kimi K3 In-C, FreeLLMAPI);
- **direct cloud providers / agent identities** (Gemini, Perplexity, Kimi,
  DeepSeek, ChatGPT/OpenAI, GigaChat, SiliconFlow, Novita, Z.AI, LLM7, SambaNova,
  AionLabs, Cloudflare, Groq, Mistral, Hugging Face);
- cloud routing/gateway providers (OpenRouter, UnoRouter, ZeroRouter, NaraRouter,
  OrcaRouter, Claude gateway).

The unified system model ships a `cloud_executor_fabric` section for exactly this.
Adding cloud executors is therefore *consistent* with the architecture, provided
the admission rules below are preserved.

## 3. Rules the extension must satisfy

1. **Executor-only authority.** A cloud executor carries no coordination,
   architecture, verification, provider or state authority. It executes only.
2. **One admission ladder.** Credential presence is not qualification. Each cloud
   executor path must traverse
   `REGISTERED → CREDENTIAL_PRESENT → AUTH_SUCCESS → MODEL_DISCOVERY_PASS →
   PROBE_PASS → EXECUTION_PASS → RESULT_VALIDATION_PASS → A3_VERIFIED`.
3. **Fresh rounds per path.** G4 requires 23 fresh isolated rounds per path. New
   cloud paths require their own 23 fresh rounds; historical or gateway success
   does not transfer.
4. **Gateway ≠ native provider.** Success through OpenRouter/UnoRouter/ZeroRouter/
   NaraRouter/OrcaRouter proves an executor+gateway path, not native-provider
   qualification. Provider identity must be preserved in evidence.
5. **Credential boundary.** Credentials never enter Git or evidence, are isolated
   per provider, and follow the rotation/expiry/revocation contract in the
   governance file. Only Human creates credentials.
6. **Isolation, timeout, replay, recovery.** Each path must prove workspace
   isolation, timeout enforcement, malformed-result rejection, replay
   idempotency and worker recovery.
7. **Independent A3.** A cloud executor or its provider can never certify its own
   qualification.
8. **Mandatory paths unchanged.** Cloud paths are candidates; they do not replace
   the five mandatory paths until independently qualified.

## 4. Candidate cloud executor paths

Enumerated machine-readably in
`architecture/ASTRA-GOLD-GOVERNANCE-CONTRACT.yaml`
(`executor_classes.candidate_cloud_executor_paths`) and summarized in
`architecture/ASTRA-GOLD-UNIFIED-AUTONOMOUS-DEVELOPMENT-SYSTEM.yaml`
(`cloud_executor_fabric.candidate_paths`):

| Path | Provider | Credential env | Status | Authority |
|---|---|---|---|---|
| GEMINI_DIRECT | gemini | GEMINI_API_KEY | NOT_PROVEN | none |
| PERPLEXITY_DIRECT | perplexity | PERPLEXITY_API_KEY | NOT_PROVEN | none |
| KIMI_DIRECT | kimi | KIMI_API_KEY | NOT_PROVEN | none |
| DEEPSEEK_DIRECT | deepseek | DEEPSEEK_API_KEY | NOT_PROVEN | none |
| OPENAI_DIRECT | chatgpt_openai | OPENAI_API_KEY | NOT_PROVEN | none |
| ANTHROPIC_DIRECT | claude | ANTHROPIC_API_KEY | NOT_PROVEN | none |
| GIGACHAT_DIRECT | gigachat | GIGACHAT_API_PERS | NOT_PROVEN | none |
| OPENROUTER_GATEWAY | openrouter | OPENROUTER_API_KEY | NOT_PROVEN | none |

All remain `NOT_PROVEN` until fresh runtime evidence exists at one frozen SHA.

## 5. Impact on the mandatory matrix

The mandatory G4 matrix is unchanged at five paths × 23 rounds = 115 rounds.
An extended manifest can be generated without altering the mandatory default:

```
python ops/qualification/build_g4_115_manifest.py \
  --source-sha <SHA> \
  --paths CODEX_FCC,CLAUDE_FCC,CODEX_OMNIROUTE,CLAUDE_OMNIROUTE,CLAUDE_CODE_DIRECT,GEMINI_DIRECT,DEEPSEEK_DIRECT \
  --out build/g4-extended.json
```

Execution remains external and fail-closed; the builder only produces the command
manifest.

## 6. Why this does not weaken the architecture

- Authority, evidence, freshness, concurrency and launch invariants are unchanged.
- The gate registry, thresholds and executor classes are now single-sourced in the
  governance contract and machine-checked, so a new executor cannot be added
  without an explicit, reviewed change.
- Extending the fabric increases *execution capacity*, never *authority*.
