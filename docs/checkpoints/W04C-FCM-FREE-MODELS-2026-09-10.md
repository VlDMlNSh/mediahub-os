# W04C — Free Coding Models Qualification / FCM

Date: 2026-09-10

## Evidence

- Tool: `vava-nessa/free-coding-models`
- Installed npm version: `0.5.90`
- Node runtime: `v22.23.2`
- Local catalog observed: 24 provider entries, 228 model records.
- Public README currently advertises 24 providers / 229 live models; local package source is the execution evidence and therefore wins over marketing count.
- FCM config: `/home/mediahub/.free-coding-models.json`, mode 0600.
- FCM telemetry disabled.
- FCM Smart Router disabled.
- OpenRouter explicitly disabled in FCM config.

## Architectural decision

FCM is accepted as a **discovery / benchmarking / model-catalog intelligence source**, not as MediaHub runtime authority.

MediaHub runtime remains:

`Canonical Protocol -> Capability Matrix -> Provider Adapter -> Provider Registry -> Routing Authority`

FCM cannot bypass Credential Broker, Policy Engine, Egress Controller, Model Registry, sandbox or provenance gates.

## Provider disposition

### Candidate for qualification

NVIDIA NIM, Groq, Cerebras, Google AI, Mistral LP, Cloudflare AI, SambaNova,
OVHcloud AI, Codestral, ZAI, Scaleway, Alibaba DashScope, OpenCode Zen,
Kilo, LLM7, Routeway, Pollinations AI, SiliconFlow, Requesty, OrcaRouter,
Vercel AI Gateway, Ollama Cloud.

These are **CANDIDATE only** until MediaHub-native adapter, credential,
policy, egress, protocol and live smoke evidence exist.

### Excluded

- OpenRouter: permanent MediaHub runtime DENY; existing 403 policy denial remains authoritative.
- GitHub Models: FCM catalog marks the service retired / HTTP 410.
- Novita AI: local catalog states no zero-price models as of its recorded audit.

## Top static candidates from the local catalog

S+/S candidates include Mistral GLM-5.2, NVIDIA DeepSeek V4 Flash,
SambaNova MiniMax M3/M2.7, OVHcloud Qwen3.6/Qwen3.5, Groq Qwen3.6,
Google Gemini Flash family, ZAI GLM family, Scaleway GLM-5.2/Qwen3.6,
Alibaba Qwen3.6/Qwen3.7/Qwen3-Coder, and Pollinations MiniMax.

The tier/SWE values are catalog metadata and are **not qualification evidence**.
Live protocol/latency/stability tests must be performed only after provider policy
and credentials are explicitly approved.

## Free/local strategy for MediaHub

1. Local llama.cpp remains the canonical no-cost local AI tier.
2. FCM supplies discovery data for external free/free-limited models.
3. Provider credentials remain optional and absent until legitimately provisioned.
4. No provider is activated merely because FCM lists it as free.
5. No OpenRouter traffic is permitted.
6. No provider-specific proxy, stealth, geo-bypass or ToS-avoidance mechanism is permitted.
7. Free-provider failover must use the same bounded retry/fail-closed semantics as all other external providers.

## Current qualification status

- FCM installation: PASS
- FCM config hardening: PASS
- Static catalog extraction: PASS
- OpenRouter exclusion in FCM config: PASS
- MediaHub runtime integration: NOT YET QUALIFIED
- External free-provider credentials: ABSENT
- OmniRoute: INSTALLATION/CLI qualification BLOCKED pending clean npm install completion
- Production/runtime cutover: DENY

## Next wave

Build a MediaHub-native read-only FCM catalog importer with an explicit denylist,
map only qualified models into Model Registry candidates, then run protocol-specific
smoke tests one provider at a time. Never auto-enable a provider from catalog data.
