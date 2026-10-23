# Wave 403 — free-provider quota assessment for GitHub-hosted Claude Code (2026-10-23)

## Decision summary

- **OpenRouter API credential:** `AUTH_SUCCESS` for a non-inference catalog request on main; live inference and remaining quota were **NOT CHECKED**.
- **Claude Code CLI through FCC + OpenRouter free router:** PR #502 remains draft; exact-head CI has a successful run, but live inference, route/model provenance, no-paid-fallback behavior, independent security review, and operational qualification are **NOT VERIFIED**.
- No provider secret values were read. No provider other than the already-recorded OpenRouter catalog GET was contacted in this pass. No inference request was made in this pass.

## Existing runtime evidence

- Main HEAD: `3b054cc8fac38d2fbd58305e9d185d307c6a18bf`.
- OpenRouter catalog probe: [run 39847014875](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39847014875), job `120062857263`, artifact `12454669532`, artifact digest `sha256:8e95e32e1ebe6d36ae4047424c9a3de12af00c8cc9bd7b37c7533a3db36defe1`.
- Probe result: HTTP 200, `GET /api/v1/models`, 468 catalog entries, credential present, 0 Qwen entries matched the probe's strict `:free` suffix filter. This was **catalog authentication only**, not a quota check or inference test.
- PR #502: [Draft FCC Claude worker](https://github.com/VlDMlNSh/mediahub-os/pull/502), head `acf0713924e98f64c8fcb8f637058ab5039d5107). Exact-head workflow run [39878467537](https://github.com/VlDMlNSh/mediahub-os/actions/runs/39878467537) succeeded for PR-triggered smoke/contract jobs; this did not call an inference provider. Formal independent review and live inference remain NOT VERIFIED.
- The existing FCC route `open_router/openrouter/free` is a dynamic free-model router. It does **not** promise a particular model such as Qwen, and it does not mean the underlying model is Anthropic Claude.

## Provider policy comparison

Published free tiers are policy baselines, not the actual quota of the listed GitHub secret. Account-level eligibility, model availability, current limits, terms and expiration must be checked at runtime.

| Provider / secret family | Published free policy | Assessment for a multi-week, no-spend pool |
|---|---|---|
| OpenRouter / `OPENROUTER_API_KEY` | Free models; published cap is 20 requests/minute and 50 requests/day for a free account. The cap can change; free model availability is dynamic. | **Primary candidate for a bounded CLI smoke**, with a strict free-only route and explicit failure on exhaustion. Not a production guarantee. |
| Groq / `GROQ_API_KEY` | Free-plan model-specific RPM/RPD/TPM/TPD limits; exact organization limits are shown in its console and response headers. Free tier returns rate-limit errors rather than billing beyond the cap. | **Strong secondary candidate** if the account remains on Free and the exact model is supported by the client adapter. Must check current per-model limits. |
| Google Gemini / `GEMINI_API_KEY*` | Free tier exists for eligible models; limits vary by model and project, and quotas reset by provider-defined windows. | **Secondary candidate** after verifying active project/model limits and data-use policy. Multiple keys do not necessarily mean independent quota if they share one project. |
| Cloudflare Workers AI / `CF_API_TOKEN_*` | Workers Free includes 10,000 Neurons/day, reset at 00:00 UTC; some newer models require paid plan or prepaid credits. | **Potential durable daily reserve** for eligible models. Verify account entitlement and choose a model explicitly marked available on Free. |
| Mistral / `MISTRAL_KEY_*` | Free API mode exists, with the lowest limits and organization-level rate caps. | **Reserve only**; inspect current Limits page and avoid assuming a multi-week allowance. |
| Hugging Face / `HF_TOKEN` | Free accounts receive a published $0.10/month Inference Providers credit, subject to change. | **Low-priority fallback**; too small to assume sustained agent coding use. |
| SambaNova / `SAMBANOVA_KEY` | Current plan page describes a Free onboarding path requiring a payment method and purchase of credits for requests. | **Do not count as a no-spend reserve** without confirming actual no-cost balance and billing behavior. |
| DeepSeek / `DEEPSEEK_API_KEY`; Kimi / `KIMI_API_KEY`; Novita / `NOVITA_KEY_*`; Z.ai / `ZAI_KEY_*`; SiliconFlow / `SILICON_KEY_*` | Public API pricing is primarily usage/credit based or account-specific; no verified persistent free inference quota was established in this pass. | **Unqualified / exclude from automatic free fallback** until official account-level free quota is confirmed. |
| LLM7, Nara, Orca, MiMo, UnoRouter | Available secret names alone do not establish official quota, model eligibility, free-only routing, or no-paid-fallback behavior. | **Unqualified** pending official terms and a bounded provider-specific probe. |

## Recommended order

1. Keep OpenRouter as the first candidate for FCC because its free router is already configured and catalog authentication succeeded.
2. Qualify Groq and eligible Cloudflare Workers AI as independent reserves. Qualify Gemini next, with project-level quota and data policy recorded.
3. Keep Mistral as a low-quota reserve; treat Hugging Face as a small testing credit, not a multi-week worker.
4. Do not enable automatic provider fallback merely because a secret exists. Every route needs an explicit provider/model allowlist, documented zero-cost behavior, quota telemetry, prompt/data classification, and fail-closed exhaustion handling.
5. For the first live test, use one tiny, non-sensitive, no-write prompt through PR #502 only after its independent review and security findings are closed. Verify model ID returned by the provider, usage/billing fields if exposed, and that the route cannot reach a paid model. If any of these cannot be proven, classify the run NOT VERIFIED and stop.

## Sources

- [OpenRouter pricing and free-model limits](https://openrouter.ai/pricing)
- [OpenRouter current API key / usage endpoint](https://openrouter.ai/docs/api/api-reference/api-keys/get-current-key)
- [Groq rate limits](https://console.groq.com/docs/rate-limits)
- [Gemini API rate limits](https://ai.google.dev/gemini-api/docs/rate-limits)
- [Cloudflare Workers AI pricing/free allocation](https://developers.cloudflare.com/workers-ai/platform/pricing/)
- [Mistral free mode and API key setup](https://docs.mistral.ai/getting-started/quickstarts/studio/activate-and-generate-api-key)
- [Hugging Face Inference Providers pricing](https://huggingface.co/docs/inference-providers/pricing)
- [SambaNova plans](https://cloud.sambanova.ai/plans)
- [Issue #301 governance](https://github.com/VlDMlNSh/mediahub-os/issues/301)
- [Canonical chat tree map](../architecture/MEDIAHUB-CHAT-TREE-MAP.md)

## Status

Quota policy research: **PARTIAL**. OpenRouter catalog authentication: **SUCCEEDED**. Per-account remaining quota: **NOT CHECKED**. Live inference: **NOT RUN in this pass**. FCC PR #502: **OPEN/DRAFT**. Independent review: **NOT VERIFIED**. No-spend route qualification: **NOT VERIFIED**. Contour A: **NOT ACCEPTED**.
