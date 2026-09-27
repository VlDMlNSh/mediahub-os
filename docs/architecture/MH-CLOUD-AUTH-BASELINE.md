# MediaHub Cloud Authorization Baseline — direct HTTPS, VPN-independent

## Scope
This document defines the canonical credential names and routing policy for direct public-cloud API access. Secret values are never stored here or in Git.

## Credential matrix

| Provider | Environment variable | Direct endpoint | Recommended development lane | Cost note |
|---|---|---|---|---|
| OpenRouter | OPENROUTER_API_KEY | https://openrouter.ai/api/v1 | MEDIAHUB_OPENROUTER_MODEL=openrouter/free | Free plan currently exposes 25+ free models and 50 requests/day; free models have low limits. |
| Gemini | GEMINI_API_KEY | https://generativelanguage.googleapis.com | A free-tier model/project where available | Gemini has a Free tier with model-specific limits; new AI Studio keys are authorization keys. |
| DeepSeek | DEEPSEEK_API_KEY | https://api.deepseek.com | deepseek-flash | Paid API; off-peak pricing is lower. |
| Kimi | KIMI_API_KEY | https://api.moonshot.ai/v1 | selected low-cost model | Credential must be created at the provider; no free guarantee assumed. |
| Perplexity | PERPLEXITY_API_KEY | https://api.perplexity.ai | research-only routing | Paid API; use only when web/research capability is actually required. |
| OpenAI | OPENAI_API_KEY | https://api.openai.com/v1 | low-cost model selected by current pricing | Paid API; reserve for tasks needing OpenAI-specific capability. |
| Claude direct (future optional adapter) | ANTHROPIC_API_KEY | https://api.anthropic.com | Haiku/Sonnet class according to current pricing | Paid API; current repository adapter remains OmniRoute and is not replaced by this document. |
| UnoRouter | UNOROUTER_API_KEY | https://api.unorouter.com/v1 | qualification/fallback only | Existing provider-side blocks remain authoritative. |
| ZeroRouter | ZEROUTER_API_KEY | provider endpoint | qualification only | Existing authentication/billing blocks remain authoritative. |
| OmniRoute | OMNIROUTE_API_KEY | OMNIROUTE_BASE_URL | qualification only | Not considered directly cloud-authorized until live inference qualification passes. |

## Required model variables
- MEDIAHUB_OPENROUTER_MODEL
- MEDIAHUB_GEMINI_MODEL
- MEDIAHUB_DEEPSEEK_MODEL
- MEDIAHUB_KIMI_MODEL
- MEDIAHUB_PERPLEXITY_MODEL
- MEDIAHUB_OPENAI_MODEL
- MEDIAHUB_CLAUDE_MODEL

## Indexed credential failover
The orchestrator supports:
- PROVIDER_KEY
- PROVIDER_KEY_1
- PROVIDER_KEY_2
and model lists through:
- MEDIAHUB_PROVIDER_MODEL
- MEDIAHUB_PROVIDER_MODELS

Secrets are consumed from the runtime environment and are never emitted into evidence.

## Cost-optimized policy
Set:
MEDIAHUB_CLOUD_ROUTING_PROFILE=cost_optimized

For cloud development this orders candidate providers as:
OpenRouter -> Gemini -> DeepSeek -> Kimi -> Perplexity -> UnoRouter -> OpenAI -> Claude -> remaining routes.

This ordering is a cost/availability policy, not a qualification verdict. Provider auth, quota, billing, and rate limits are never bypassed.

Recommended free-first configuration:
- OPENROUTER_API_KEY present
- MEDIAHUB_OPENROUTER_MODEL=openrouter/free
- GEMINI_API_KEY present
- MEDIAHUB_CLOUD_ROUTING_PROFILE=cost_optimized

Local-first remains preferable for private data: keep allow_local_extension enabled and use FreeLLMAPI/local inference before sending confidential material to cloud.

## Direct-without-VPN qualification
A provider is considered DIRECT_REACHABLE only after a fresh inference request from the actual MediaHub execution environment returns a non-empty marker response.

Credential presence alone is not qualification.

## Security
Never commit secret values. Never put API keys in evidence. Never rotate or copy credentials automatically without explicit authorization. HTTP 401/403/402/429 remain provider failures and trigger bounded fallback rather than bypass attempts.
