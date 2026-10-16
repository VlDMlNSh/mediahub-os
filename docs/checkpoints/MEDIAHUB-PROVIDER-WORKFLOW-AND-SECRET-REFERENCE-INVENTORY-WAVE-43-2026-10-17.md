# MediaHub OS — Provider Workflow and Secret-Reference Inventory, Wave 43

- Date: 2026-10-17
- Contour: A — Developer Fabric
- Status: READ-ONLY SOURCE INVENTORY / SECRET-SCOPE FINDINGS OPEN / PROVIDER ELIGIBILITY MATRIX PENDING
- Canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
- Previous checkpoint: [Wave 42](mediahub-next-continuation-checkpoint-2026-10-17-wave42.md)
- Previous hosting comparison: [Wave 42 CPRG hosting alternatives](MEDIAHUB-CPRG-HOSTING-ALTERNATIVES-AND-REUSE-READINESS-WAVE-42-2026-10-17.md)

## 1. Outcome

This pass used GitHub repository contents and raw-file reads only. Desktop Commander and agent-browser were intentionally omitted because repository API access supplied the evidence needed for this source inventory.

The current source tree exposes several materially different provider paths. These must remain separate in the readiness matrix:
1. Hosted provider APIs using repository Actions secrets.
2. A multi-provider qualification job that injects 32 provider-related secret references into one job environment.
3. A local FreeLLMAPI-compatible gateway using a local key file and Actions variables for URL/model/path.
4. A Claude-compatible local executor that reads a local FCC environment file.
5. A metered Anthropic worker with a dedicated Actions secret and explicit opt-in variable.

A credential reference proves only that source code names a secret. It does not prove the secret exists, has a value, is valid, has eligible account/region status, or is safe for a particular task.

## 2. Current workflow source inventory

| Workflow | Source blob SHA | Credential / configuration path | Source-level observation |
|---|---|---|---|
| `.github/workflows/astra-provider-qualification.yml` | `d3160088fbef4fce152ed7335f0acaa3bb440378` | 32 secret references at job scope, listed below | All references are exposed to the same provider qualification job on the `mediahub-provider` self-hosted runner; the job invokes the multi-provider qualification script |
| `.github/workflows/freellmapi-qualification.yml` | `708ddeffc4664fd03f5ca6475a117348cf3666dc` | Actions variables `MEDIAHUB_FREELLMAPI_URL`, `MEDIAHUB_FREELLMAPI_KEY_FILE`, `MEDIAHUB_FREELLMAPI_MODEL`; key loaded from a local file | This is a local gateway path; endpoint defaults to loopback. Configurable URL, key-file path, live provider call and test installation are in the workflow source; this pass did not dispatch it |
| `.github/workflows/mediahub-claude-worker.yml` | `e1260cfef88ac02bcc9d0cce67bb497820f5f63c` | `ANTHROPIC_API_KEY`; gated by `vars.MEDIAHUB_ALLOW_METERED_ANTHROPIC == 'true'` | Separate hosted Anthropic worker with explicit metered-cost opt-in |
| `.github/workflows/astra-local-claude-qualification.yml` | `7f7dc2d65481e2cc80a1db94b41a1e60ed117ffd` | `ANTHROPIC_AUTH_TOKEN` loaded from `/home/mediahub/.config/mediahub/fcc.env` | Local FCC/Ollama path; the credential source is a local environment file rather than a repository secret reference |
| Gemini workflow | N/A in current workflow directory inventory | Historical documentation references `GEMINI_API_KEY` and a successful run at commit `b45324009ac3aa65322a702c28069b12190bc4b8` | No Gemini-named workflow file appeared in the current `.github/workflows` directory inventory. Historical run evidence remains historical; current workflow continuity requires separate reconciliation |

## 3. Exact secret references in the multi-provider qualification job

The current `astra-provider-qualification.yml` source references these 32 secret names:

| Provider / purpose grouping | Secret names |
|---|---|
| Mimo | `MIMO_API_KEY` |
| SiliconFlow | `SILICONFLOW_API_KEY_1`, `SILICONFLOW_API_KEY`, `SILICONFLOW_API_KEY_2` |
| Novita | `NOVITA_API_KEY_1`, `NOVITA_API_KEY`, `NOVITA_API_KEY_2` |
| Z.AI | `ZAI_API_KEY_1`, `ZAI_API_KEY`, `ZAI_API_KEY_2` |
| Kimi / Moonshot | `KIMI_API_KEY`, `MOONSHOT_API_KEY` |
| LLM7 | `LLM7_API_KEY` |
| SambaNova | `SAMBANOVA_API_KEY` |
| AIonLabs | `AIONLABS_API_KEY` |
| Cloudflare | `CLOUDFLARE_API_TOKEN_1`, `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_API_TOKEN_2`, `CLOUDFLARE_ACCOUNT_ID_1`, `CLOUDFLARE_ACCOUNT_ID_2` |
| NaraRouter | `NARAROUTER_API_KEY_1`, `NARAROUTER_API_KEY` |
| OrcaRouter | `ORCAROUTER_API_KEY` |
| UnoRouter | `UNOROUTER_API_KEY` |
| ZeroRouter | `ZEROUTER_API_KEY` |
| DeepSeek | `DEEPSEEK_API_KEY` |
| Gemini | `GEMINI_API_KEY` |
| Groq | `GROQ_API_KEY` |
| Mistral | `MISTRAL_API_KEY_1`, `MISTRAL_API_KEY_2` |
| OpenRouter | `OPENROUTER_API_KEY` |
| Hugging Face | `HF_TOKEN` |

This is a source-level name inventory only. Secret values, existence, access scopes, account ownership and provider status were not inspected.

## 4. Security and architecture findings

### F-43-01 — Broad secret exposure at job scope

The provider qualification workflow exposes 32 secret references to a single job environment, even though each individual provider request should require only that provider's credential. This increases the blast radius of a compromised runner, dependency or qualification script.

**Disposition:** HIGH PRIORITY DESIGN FINDING. Recommend splitting qualification into provider-scoped jobs or dynamically granting only the selected provider's secret references after a task-scoped policy decision. Each job must have an explicit provider allowlist, destination allowlist, data-class authorization and bounded quota. Implement only in a separately authorized change pass.

### F-43-02 — Provider identity and secret name are not sufficient admission evidence

The registry schema supports provider identity, enabled state, priority and selection policy, including FAILOVER. The schema alone does not prove current provider eligibility, region compatibility, quota, terms, model availability or data-handling approval.

**Disposition:** Add provider-specific evidence fields or a linked readiness record before any automatic failover is admitted. Every alternate provider is a separate destination decision, consistent with existing provider identity/egress contracts.

### F-43-03 — FreeLLMAPI gateway classification remains a known contract conflict

The existing provider identity crosswalk records FreeLLMAPI as a cloud-model path in architecture text and a `local_gateway` in registry metadata, with `PENDING` status. The live qualification workflow treats it as a local configurable endpoint. Preserve this conflict until deployment identity and endpoint ownership are evidenced.

**Disposition:** OPEN. Do not infer that loopback defaults prove a cloud provider or a local-only service.

### F-43-04 — Historical Gemini proof versus current source inventory

A prior checkpoint records one successful Gemini workflow run at a historical commit. The current workflow directory inventory contains no Gemini-named workflow. Historical success remains valid for that run, while current integration continuity and current secret binding require source reconciliation.

**Disposition:** OPEN. No workflow was dispatched and no provider was called in this pass.

### F-43-05 — Local and hosted credentials must remain distinct

The local FCC environment file, local FreeLLMAPI key file, GitHub Actions Secrets and provider-side account/key creation are different credential custody paths. A future CPRG host must not silently become a second secret authority or general-purpose proxy.

**Disposition:** Retain the existing MH-12 lifecycle and CPRG boundary. Any additional vault requires an explicit capability gap, trust-root/recovery design and an approved decision record.

## 5. Provider readiness status

The matrix below records what this source pass can establish and leaves policy/account facts UNKNOWN until official public policy evidence is captured.

| Provider/path | Workflow reference found | Secret reference found | Account/region eligibility | Free-tier/reset/failover | Current disposition |
|---|---|---|---|---|---|
| Gemini | Historical workflow/run only; current Gemini-named workflow absent from directory inventory | `GEMINI_API_KEY` in provider qualification workflow | UNKNOWN | UNKNOWN | CONDITIONAL / reconcile current integration first |
| Anthropic hosted | `mediahub-claude-worker.yml` | `ANTHROPIC_API_KEY` | UNKNOWN | Metered path guarded by explicit opt-in; quota and spend cap still require evidence | GATED |
| Anthropic-compatible local FCC/Ollama | `astra-local-claude-qualification.yml` | `ANTHROPIC_AUTH_TOKEN` from local env file | Local transport; upstream/provider eligibility separate | Local model path is distinct from hosted Anthropic billing | SOURCE-DECLARED / runtime status outside this pass |
| FreeLLMAPI local gateway | `freellmapi-qualification.yml` | Local key file; URL/model/path in Actions variables | Gateway ownership and ultimate upstream route UNKNOWN | UNKNOWN | OPEN CONTRACT CONFLICT |
| Mimo, SiliconFlow, Novita, Z.AI, Kimi/Moonshot, LLM7, SambaNova, AIonLabs, Cloudflare, NaraRouter, OrcaRouter, UnoRouter, ZeroRouter, DeepSeek, Groq, Mistral, OpenRouter, Hugging Face | Multi-provider qualification workflow | Exact names listed in §3 | UNKNOWN per provider/account/target | UNKNOWN per provider/account/model | BLOCKED from automatic admission pending provider-specific evidence |

Required evidence per provider:
1. Official terms, supported regions and account eligibility, with URL and observation date.
2. Exact product/API endpoint, execution-region and source-network restrictions.
3. Free-tier entitlement, quota units, reset window, rate limits, and whether retries/fallback are allowed.
4. Data retention/training policy and approved data classes.
5. Secret scope, storage location, rotation/revocation owner and expiry metadata.
6. Model availability and price/spend guard.
7. Provider-specific job boundary and sanitized evidence contract.
8. Explicit admission state: PASS, FAIL, UNKNOWN or CONDITIONAL.

## 6. Status and next bounded step

- Current source inventory: completed from GitHub contents and raw-file reads.
- Broad multi-provider job secret scope: documented as a high-priority design finding; implementation remains unauthorized.
- Provider-specific official policy matrix: still open.
- Current Gemini workflow continuity: open source reconciliation.
- CPRG host selection: remains open; self-owned Linux is first candidate to evaluate, European VPS remains first-class alternative.
- No provider calls, credentials, tests, workflow dispatch, host inspection, installation, infrastructure changes, deployment or branch integration occurred.

Next pass: research official provider policy sources for a small, prioritized subset grounded in existing secret/workflow references; record region eligibility, free quota/reset behavior, retention/training, and permitted fallback. Prioritize providers with an existing integration path and keep every unverified provider blocked from automatic routing.

- Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
