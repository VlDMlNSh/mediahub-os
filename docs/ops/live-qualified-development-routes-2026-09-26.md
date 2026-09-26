# Live-qualified development routes — 2026-09-26

Status: ACTIVE ROUTING POLICY

## Current live evidence

- Gemini `gemini-3.5-flash-lite`: LIVE_QUALIFIED, HTTP 200, exact marker; run 36240130439.
- OpenRouter `openrouter/free`: LIVE_QUALIFIED, HTTP 200, exact marker; selected upstream `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`; run 36239718035.
- OpenAI `gpt-5.6-luna`: prior live qualification attempt remains NOT QUALIFIED after HTTP 429 rate limiting.
- Anthropic `claude-haiku-4-5-20251001`: NOT QUALIFIED, HTTP 400; run 36239684629.
- Anthropic `claude-sonnet-5`: NOT QUALIFIED, HTTP 400; run 36240145963.
- Gemini `gemini-2.5-flash-lite`: NOT QUALIFIED, HTTP 404; run 36239702836.
- Groq `openai/gpt-oss-20b`: NOT QUALIFIED, HTTP 403; run 36239740054.
- Together `Qwen/Qwen3.8-Flash`: NOT QUALIFIED, HTTP 403; run 36239756517.
- Hugging Face `openai/gpt-oss-120b:groq`: NOT QUALIFIED, HTTP 403; run 36239775610.

## Persistent development routing

The autonomous local coding agent now uses this deterministic order when authorized credentials are present:

1. Gemini `gemini-3.5-flash-lite`
2. OpenRouter `openrouter/free`
3. FCM
4. local OmniRoute
5. local llama.cpp model

Cloud credentials remain external inputs and are never committed. Missing or rejected cloud credentials fall through without retry amplification.

## Boundary

Only routes with current live evidence are promoted to the preferred cloud lane. Contract-level or failed routes remain non-qualified and are not promoted by this policy.
