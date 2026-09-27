# Live provider qualification — 2026-09-26

## Scope
Trusted GitHub Actions workflow, workflow_dispatch only, target ref `engineering/mh21-sandbox-lifecycle-20260910`, 16-token smoke, credentials suppressed.

## Results
- OpenAI / `gpt-5.6-luna`: NOT QUALIFIED — HTTP 429 RATE_LIMITED.
- Anthropic / `claude-haiku-4-5-20251001`: NOT QUALIFIED — HTTP 400.
- Anthropic / `claude-sonnet-5`: NOT QUALIFIED — HTTP 400.
- Gemini / `gemini-2.5-flash-lite`: NOT QUALIFIED — HTTP 404 for selected model.
- Gemini / `gemini-3.5-flash-lite`: LIVE QUALIFIED — HTTP 200, exact marker returned.
- OpenRouter / `openrouter/free`: LIVE QUALIFIED — HTTP 200, exact marker returned; route selected `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`.
- Groq / `openai/gpt-oss-20b`: NOT QUALIFIED — HTTP 403 POLICY_OR_CREDENTIAL_FAILURE.
- Together / `Qwen/Qwen3.8-Flash`: NOT QUALIFIED — HTTP 403 POLICY_OR_CREDENTIAL_FAILURE.
- Hugging Face / `openai/gpt-oss-120b:groq`: NOT QUALIFIED — HTTP 403 POLICY_OR_CREDENTIAL_FAILURE.
- Zhipu/GLM: contract-level qualified; no live credential was used.
- local Qwen/llama.cpp: previously live qualified.
- DF2 Ollama: local route present; live model qualification remains separate.
- OmniRoute: local API live qualified.
- Claude Code → OmniRoute: E2E remains unqualified.

## Interpretation
HTTP 429/403/400/404 are recorded as evidence, not retried into a false PASS. A provider is marked LIVE QUALIFIED only after a real HTTP 200 response and exact marker verification.

## Security
No API key values were printed, stored in the evidence, or committed. The live workflow is trusted/manual and has `contents: read` only.
