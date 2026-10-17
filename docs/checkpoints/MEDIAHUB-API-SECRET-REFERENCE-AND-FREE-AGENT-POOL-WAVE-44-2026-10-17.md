# API Secret Reference Audit and Free-Agent Pool Plan — Wave 44

- Date: 2026-10-17
- Repository: `VlDMlNSh/mediahub-os`
- Contour: A — Developer Fabric
- Status: **SOURCE AUDIT COMPLETE / POOL PROPOSED / RUNTIME CONNECTION PENDING**
- Main HEAD observed: `4712c30c3e0296cf1d792c4c69e49cdb798d99fe`
- Documentation branch HEAD before this update: `a0c432273914fa5c4bd9e756736f9c9b72b41a77`
- Baseline 2.0 is canonical; Baseline 1.0 remains historical.

## 1. Scope and evidence limits

Reviewed current `main` workflow definitions, `ops/qualification/provider_model_registry.json`, `profiles/agent-registry.json`, `profiles/providers/astra-gold-hybrid-agent-fabric.yaml`, `ops/qualification/qualify_execution_backends.py`, the cloud multi-agent router ADR and official provider quota/pricing pages.

GitHub repository-content APIs expose workflow references, not configured secret values. The Actions secrets-list endpoint was unavailable through the current repository-content integration. Therefore:
- Names below are **observed secret references**, not proof that every named secret exists in repository settings.
- Credential validity, billing state, account/project identity, and remaining quota are **UNKNOWN** unless explicitly supported by current official documentation.
- Secret values were neither requested nor exposed. No provider call or workflow dispatch was performed.

## 2. Observed secret references

### Gemini and Google

| Secret reference | Observed use | Status |
|---|---|---|
| `GEMINI_API_KEY` | Existing Gemini workflow, provider qualification, read-only audit | Referenced |
| `GEMINI_API_KEY_2` | Gemini Agent 2 | Referenced |
| `GEMINI_API_KEY_3` | Gemini Agent 3 | Referenced |
| `GOOGLE_API_KEY` | Fallback expression in read-only Gemini audit workflows | Referenced; account/model identity unknown |

### Provider qualification pool

The current `.github/workflows/astra-provider-qualification.yml` maps these names into a self-hosted provider qualification job:

- Xiaomi MiMo: `MIMO_API_KEY`
- SiliconFlow: `SILICONFLOW_API_KEY_1`, `SILICONFLOW_API_KEY`, `SILICONFLOW_API_KEY_2`
- Novita: `NOVITA_API_KEY_1`, `NOVITA_API_KEY`, `NOVITA_API_KEY_2`
- Z.ai: `ZAI_API_KEY_1`, `ZAI_API_KEY`, `ZAI_API_KEY_2`
- Kimi/Moonshot: `KIMI_API_KEY`, `MOONSHOT_API_KEY`
- LLM7: `LLM7_API_KEY`
- SambaNova: `SAMBANOVA_API_KEY`
- Aion Labs: `AIONLABS_API_KEY`
- Cloudflare: `CLOUDFLARE_API_TOKEN_1`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_API_TOKEN_2`, plus account identifiers `CLOUDFLARE_ACCOUNT_ID_1`, `CLOUDFLARE_ACCOUNT_ID_2`
- NaraRouter: `NARAROUTER_API_KEY_1`, `NARAROUTER_API_KEY`
- OrcaRouter: `ORCAROUTER_API_KEY`
- UnoRouter: `UNOROUTER_API_KEY`
- ZeroRouter: `ZEROUTER_API_KEY`
- DeepSeek: `DEEPSEEK_API_KEY`
- Groq: `GROQ_API_KEY`
- Mistral: `MISTRAL_API_KEY_1`, `MISTRAL_API_KEY_2`
- OpenRouter: `OPENROUTER_API_KEY`
- Hugging Face: `HF_TOKEN`

### Additional workflow and profile references

- Anthropic workflow: `ANTHROPIC_API_KEY`; the local Claude qualification workflow also uses an `ANTHROPIC_AUTH_TOKEN` process variable, with its origin determined by that workflow's runtime configuration.
- SiliconFlow probe workflows: `SILICON_KEY_2`.
- Astra node attestation: `ASTRA_NODE_HMAC_KEY_MH_DEV_01`, `ASTRA_NODE_HMAC_KEY_MH_DEV_02`, `ASTRA_NODE_HMAC_KEY_VOKTORS_MAC`.
- GitHub Actions `GITHUB_TOKEN` is an automatically provided workflow token, rather than a provider API key.
- The provider/agent profiles also reference `PERPLEXITY_API_KEY`, `OPENAI_API_KEY`, `GIGACHAT_API_PERS`, and `OMNIROUTE_API_KEY`; this source review did not establish current use by a provider qualification workflow.

**Alias discrepancy:** the SiliconFlow probe YAML uses `SILICON_KEY_2`; the provider registry and qualification workflow use `SILICONFLOW_API_KEY_2`. Reconcile the intended mapping in GitHub settings and workflow configuration before relying on this lane. Do not copy values into issues, artifacts, or source files.

## 3. Existing registry candidates

The existing `ops/qualification/provider_model_registry.json` (blob `62328126fd2cd8879a73bb6812adcacd3e2abe84`) already defines 24 provider/local entries. Reuse that registry rather than creating a parallel catalog.

| Candidate lane | Existing model IDs in registry | Credentials referenced | Proposed disposition |
|---|---|---|---|
| Gemini 1/2/3 | `gemini-3.8-flash`, `gemini-3.5-flash-lite` | `GEMINI_API_KEY`, `_2`, `_3` | Keep three specialist workflows; quota is project-scoped, so keys in one project do not provide three independent daily quotas |
| Cloudflare Workers AI | `@cf/meta/llama-3.1-8b-instruct` | Cloudflare tokens + matching account IDs | Priority daily free candidate; verify which account IDs are distinct and which model aliases remain free |
| Groq | `openai/gpt-oss-20b`, `openai/gpt-oss-120b` | `GROQ_API_KEY` | Priority free-tier fallback; enforce per-model/org RPM, RPD, TPM and TPD |
| SiliconFlow | `THUDM/glm-4-9b-chat`, `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B`, `Qwen/Qwen2.5-7B-Instruct` | Three key aliases | Candidate; verify exact account/project quota scope and current model terms |
| Novita | `meta-llama/Llama-3.2-1B-Instruct`, `Qwen/Qwen2.5-7B-Instruct`, `THUDM/glm-4-9b-chat` | Three key aliases | Candidate; free eligibility and reset window require account-level evidence |
| Z.ai | `glm-4.7-flash`, `glm-4.5-flash` | Three key aliases | Candidate; verify model availability, free quota and account scope |
| Mistral | `mistral-small-latest`, `mistral-large-latest` | Two key aliases | Free Studio mode exists; use only models explicitly available in the free account tier |
| OpenRouter | `openai/gpt-oss-120b:free`, `google/gemini-2.5-flash:free` | `OPENROUTER_API_KEY` | Useful low-volume fallback; official free tier lists 20 RPM / 50 RPD; paid-plan auto-routing is separate |
| Hugging Face | `openai/gpt-oss-120b:fastest`, `Qwen/Qwen3-Coder-480B-A35B-Instruct:fastest` | `HF_TOKEN` | Small monthly-credit fallback; free users receive $0.10/month, so this is not a daily renewable pool |
| Kimi/Moonshot | `kimi-k2.5` | `KIMI_API_KEY`, `MOONSHOT_API_KEY` | Conditional candidate; confirm free eligibility and quota semantics |
| LLM7 | provider default model | `LLM7_API_KEY` | Conditional candidate; pin discovered model ID and verify current free limits |
| Aion Labs | `aion-labs/aion-3.5-mini`, `aion-labs/aion-3.5` | `AIONLABS_API_KEY` | Conditional candidate; quota and terms evidence required |
| UnoRouter | `gpt-oss-120b:free` | `UNOROUTER_API_KEY` | Conditional gateway fallback; provider-level quota, model origin and retention terms require review |
| SambaNova | `DeepSeek-V3.1`, `Meta-Llama-3.3-70B-Instruct` | `SAMBANOVA_API_KEY` | Exclude from guaranteed-zero-cost pool until account terms are verified; current public plan page describes adding a payment method and purchasing credits |
| DeepSeek | `deepseek-chat`, `deepseek-reasoner` | `DEEPSEEK_API_KEY` | Trial lane only; exclude from renewable-free baseline |
| Xiaomi MiMo | `mimo-v2.6-flash`, `mimo-v2.6-pro` | `MIMO_API_KEY` | Registry marks this as paid API; exclude from free baseline |
| NaraRouter / OrcaRouter / ZeroRouter | gateway-defined models | respective router keys | Keep quarantined until identity, free quota, auth, model catalog and terms are source-verified |
| Ollama local | `qwen2.5-coder:3b` | no cloud key | Optional local fallback only; separate from cloud quota and subject to local-node availability |
| FreeLLMAPI | routed free-model catalog | local key file / local gateway | Existing local gateway candidate; upstream description limits it to personal experimentation, so production admission requires separate review |

## 4. Verified free-tier facts from official sources

- **Cloudflare Workers AI:** 10,000 Neurons/day included at no charge; reset at 00:00 UTC. Some models require a paid plan or prepaid credits. Source: https://developers.cloudflare.com/workers-ai/platform/pricing/ and https://developers.cloudflare.com/workers-ai/platform/limits/
- **Gemini API:** request/token quotas are scoped per project rather than per key; requests/day reset at midnight Pacific time. Active quotas vary by model and tier. Source: https://ai.google.dev/gemini-api/docs/rate-limits
- **Groq:** rate limits are measured by model and organization, including RPM/RPD/TPM/TPD; HTTP 429 and reset headers guide cooldown. Source: https://console.groq.com/docs/rate-limits
- **OpenRouter:** free models are limited to 20 RPM and 50 RPD on the free plan; its pricing page describes automatic routing for paid plans. Source: https://openrouter.ai/pricing
- **Hugging Face Inference Providers:** free accounts receive $0.10 monthly credits, subject to change. Source: https://huggingface.co/docs/inference-providers/pricing
- **Mistral:** Studio starts in Free mode by default; exact model availability and limits must be checked in the account. Source: https://docs.mistral.ai/getting-started/quickstarts/developer/first-api-request
- **SambaNova:** current public plan page says the Free plan requires adding a payment method and purchasing credits; treat as conditional, rather than guaranteed free. Source: https://cloud.sambanova.ai/plans

The current official evidence reviewed does not establish durable free quota/reset guarantees for SiliconFlow, Novita, Z.ai, Kimi/Moonshot, LLM7, Aion Labs, NaraRouter, OrcaRouter or UnoRouter. Their registry labels are candidate classifications, not current account qualification.

## 5. Proposed agent pool and routing roles

1. **Research and architecture:** Gemini Agent 2; use the existing workflow and credential binding.
2. **Independent security reviewer:** Gemini Agent 3; independent evidence review and risk findings.
3. **General planner / low-cost reasoning:** Gemini Agent 1 plus Groq, Cloudflare and Z.ai candidates, selected by task policy and current quota.
4. **Coding executor:** SiliconFlow / Novita / Groq candidate routes; use the model-specific capability allowlist and isolated workspace.
5. **High-context review:** conditional Mistral / Kimi / Hugging Face routes; model context and free eligibility must be confirmed before task assignment.
6. **Gateway fallback:** OpenRouter free models, then UnoRouter only after its exact free terms and auth are verified.
7. **Daily reset recovery:** Cloudflare Workers AI first for a documented daily free allocation, then permitted alternatives; Gemini and Groq use their own project/org/model reset scopes.
8. **Local fallback:** Ollama remains separate and optional; local execution is not a cloud agent and consumes local compute rather than API quota.

No route becomes active solely because its secret name appears in the repository. Admission requires confirmed secret presence, provider auth, model discovery, a bounded non-mutating probe, quota scope, data-egress approval, and independent evidence review.

## 6. Key rotation, cooldown and quota rules

- Track quota by the provider's actual scope: account, project/organization, model, metric and reset window. A key alias is only a credential identifier.
- When a 429 or quota-exhausted response arrives, honor `Retry-After` and provider reset headers; persist cooldown against that scope.
- Select another credential only when its quota scope is independently eligible and its use is permitted by provider terms. Keys within the same project/account must share the tracked quota where provider policy says so.
- Prefer cross-provider fallback only when task data-egress policy explicitly allows that destination and retention/security review is complete.
- If all permitted routes are exhausted, persist `QUOTA_EXHAUSTED` and defer until a provider-approved reset time.
- Prevent paid spend: no paid fallback, billing activation, or credit purchase without separate approval.
- Use task idempotency keys and duplicate-PR detection; quota retries must not create duplicate branches or PRs.
- Redact credentials, authorization headers and credential-bearing URLs from logs and artifacts.

## 7. Implementation boundary and blockers

The existing provider qualification script performs bounded probes, but its retry loop uses short fixed sleeps and does not honor `Retry-After`; it is a qualification utility, not a durable task router. The current provider qualification workflow also targets a self-hosted runner. This pass did not run it.

A real shared router requires accepted ingress/authorization, durable task state and atomic quota reservations, credential-store placement, egress policy, concurrency fencing, queue recovery and an accepted runner/workspace target. The existing architecture records Supabase as a candidate but records zero projects connected; no cloud router is currently deployed. GitHub Actions secrets are available only to workflows that receive them, and a separate runtime requires its own approved secret store.

### Recommended rollout order

1. Reconcile the SiliconFlow key-name discrepancy and confirm configured secret **names** in GitHub Settings; keep values hidden.
2. Read-only source review of existing router candidates and choose the stable reusable component before custom router implementation.
3. Approve the runtime secret store and durable state target; avoid a new owner-operated always-on server.
4. Run one explicitly authorized, isolated connectivity qualification per provider with fresh source SHA, bounded calls, redacted evidence and no paid fallback.
5. Activate only qualified free-tier routes; keep conditional providers quarantined.
6. Add durable quota ledger, atomic reservation, `Retry-After` cooldowns, per-scope key selection and `QUOTA_EXHAUSTED` defer semantics.
7. Independently verify concurrency, duplicate-PR prevention, egress policy, secret redaction, reset recovery and fail-closed behavior before production acceptance.

## 8. Source references

- [Provider model registry](https://github.com/VlDMlNSh/mediahub-os/blob/main/ops/qualification/provider_model_registry.json)
- [Provider qualification workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-provider-qualification.yml)
- [Gemini Agent 2 workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-2.yml)
- [Gemini Agent 3 workflow](https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-3.yml)
- [Cloud multi-agent router ADR](https://github.com/VlDMlNSh/mediahub-os/blob/main/docs/architecture/MEDIAHUB-CLOUD-MULTIAGENT-ROUTER-ADR-WAVE-42-2026-10-17.md)
- [Issue #301 — Contour A qualification and operationalization](https://github.com/VlDMlNSh/mediahub-os/issues/301)

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
