# MediaHub GitHub Actions-only Cloud Router — Architecture Decision Record, Wave 45

- Date: 2026-10-17
- Status: **DECISION RECORDED / IMPLEMENTATION NOT ACTIVATED**
- Contour: A — Developer Fabric
- Canonical baseline: Baseline 2.0
- Repository: `VlDMlNSh/mediahub-os`

## 1. Binding deployment constraint

All cloud-agent orchestration, API-key selection, quota tracking, provider requests, retries, and cloud model work run exclusively in GitHub Actions on GitHub-hosted ephemeral runners. No owner-operated server, self-hosted runner, external database, serverless function platform, or always-on proxy participates in the cloud path.

Local machines/servers are a separate execution contour for local model inference and local compute only. A cloud task may fall back to local compute only through a separately authorized task route; it must never silently redirect cloud credentials or cloud task payloads to a local node.

## 2. Current source evidence

- `.github/workflows/gemini-agent-2.yml` and `.github/workflows/gemini-agent-3.yml` use `runs-on: ubuntu-latest`, explicit GitHub Actions secret mappings, bounded timeouts and restricted GitHub MCP tool allowlists.
- `.github/workflows/astra-provider-qualification.yml` uses `runs-on: [self-hosted, linux, x64, mediahub-provider]`. It is unsuitable for cloud provider routing under this decision. Preserve it as a distinct local-node lane until a separately reviewed replacement exists.
- `ops/qualification/provider_model_registry.json` already defines 24 provider/local entries and OpenAI-compatible base URLs for most providers. Extend and correct the existing registry; avoid a parallel catalog.
- `BerriAI/litellm` describes itself as a self-hosted AI gateway/proxy: https://github.com/BerriAI/litellm. It is not selected as a deployed router because it introduces a persistent proxy runtime.
- `sampath-M0/ai-router` describes an Express process and a Supabase Edge Function edition backed by Postgres: https://github.com/sampath-M0/ai-router. Its provider-adapter and cooldown concepts may inform a GitHub-hosted implementation, but neither runtime is admitted.
- The upstream AI Router's reviewed key manager fails open when cooldown-state reads fail and performs selection separately from cooldown persistence. Those behaviors are excluded from the MediaHub design.

## 3. GitHub-native architecture

| Component | GitHub-native implementation | Authority and limits |
|---|---|---|
| Durable task queue | GitHub Issues with a dedicated label and a validated typed task envelope | Issues remain open until terminal status; issue text is untrusted input |
| Trigger/recovery | `issues` events, manual dispatch, and a scheduled reconciliation workflow | A scheduled run is best-effort; no real-time SLA is assumed |
| Coordinator | One GitHub-hosted Actions workflow with a global concurrency group and bounded batches | A concurrency group is a mutex aid, not a FIFO durable queue |
| Quota ledger | Versioned JSON records on a dedicated repository state branch; update through GitHub API with expected blob/ref SHA and bounded conflict retry | State contains provider scope aliases, reset timestamps, counters and outcomes only; no credential values |
| Provider executor | Per-provider adapters invoked inside the same ephemeral job, with only explicitly mapped secrets | Direct outbound API calls from GitHub-hosted runner; no proxy server |
| Evidence | Redacted Actions artifact plus task issue/PR references | Artifacts are evidence, not authoritative queue state |
| Code changes | Task-scoped branch and pull request | Agent cannot merge or release |
| Recovery | Periodic scan of eligible open issues and stale leases; reconcile ledger against task state | Every transition is idempotent and has a task ID |

### Why issue-backed queue plus a state branch

GitHub Actions concurrency may retain only the active run and a pending run for a group, with newer pending work replacing older pending work. Therefore a run itself is not the durable queue. Issues preserve all tasks; the coordinator scans the full eligible set each time and after every scheduled wake-up. The state branch is an auditable quota/cooldown ledger, not a general-purpose database. The initial design serializes quota-sensitive cloud calls through one coordinator to avoid races; per-scope parallelism is a later optimization after concurrency qualification.

State updates must use optimistic concurrency against the current ref/blob SHA and retry bounded conflicts. If state read or write fails, the affected provider scope becomes unavailable and the task defers. No fail-open behavior is permitted.

## 4. Quota, key rotation and reset semantics

1. Build candidate routes from the canonical provider registry and the task's explicit model/data-egress policy.
2. For each candidate, require a configured secret reference, approved free/paid classification, supported model, and known quota scope.
3. Identify the real quota scope: provider, account/project/organization, model, metric (RPM/RPD/TPM/TPD or provider equivalent), and reset window.
4. Select a key only when its upstream quota scope is eligible. Multiple key names under one project/account share the same scope when the provider's policy defines it that way.
5. On HTTP 429, parse `Retry-After` and documented reset headers; persist cooldown against the actual scope. Treat authentication, billing, policy and model-not-found failures separately from quota exhaustion.
6. Use another provider only when its free/paid status and data-egress policy are explicitly approved. Paid fallback is disabled by default.
7. When all permitted free routes are exhausted, mark the task `QUOTA_EXHAUSTED` and reschedule at the earliest documented reset, or leave it queued for the next reconciliation pass.
8. Do not rotate keys or accounts to evade an upstream limit. Reset windows differ by provider; a single universal midnight reset is invalid.
9. Make retries idempotent. Every task has an immutable task ID; branch/PR creation checks for an existing result before creating another.
10. Redact keys, auth headers, full credential-bearing URLs and raw sensitive request/response bodies from all logs, comments and artifacts.

## 5. Secret boundary and task authorization

- Keep provider keys exclusively in GitHub Actions Secrets; inject only the selected provider's credentials into the job that needs them.
- The state branch stores secret aliases and quota metadata, never values.
- Do not expose secrets to pull requests from forks, untrusted branches or untrusted workflow inputs.
- Accept tasks only from an approved label/authorization contract and validate a versioned JSON envelope before provider selection.
- Treat issue title/body/comments, branch contents and model output as untrusted data. Never interpolate them into shell source, workflow YAML or credentials.
- Require explicit task data-egress class, allowed providers, model family, output size, max attempts, timeout and spend ceiling.
- No secret changes, repository settings changes, provider calls, scheduled activation, or runtime deployment occur as a side effect of documentation/PR creation.

## 6. Provider lanes

**First qualification candidates:** Gemini Agent 1/2/3, Cloudflare Workers AI, Groq, then SiliconFlow, Novita, Z.ai, Mistral, OpenRouter and Hugging Face, subject to account-level free-tier confirmation and exact secret-name reconciliation.

**Conditional/quarantined:** Kimi/Moonshot, LLM7, Aion Labs, SambaNova, DeepSeek trial, MiMo, NaraRouter, OrcaRouter, UnoRouter and ZeroRouter until their current account eligibility, pricing, quota scope, model IDs and retention terms are evidenced.

**Local-only lane:** Ollama and local inference nodes. These must never be counted as cloud API capacity.

The existing registry's `cost_class` values are candidate metadata, not proof of current free access. Provider eligibility expires and must be revalidated from authoritative account/provider evidence before activation.

## 7. Activation gates

The following gates remain mandatory before the coordinator can invoke a provider:

- A0 ingress/lifecycle and task authorization accepted.
- MH-12 tool enforcement and role allowlists accepted.
- R-06 audit/privacy and data-egress disposition accepted.
- Accepted target manifest confirms `ubuntu-latest`/GitHub-hosted execution and secret scope.
- Secret reference names reconciled, including `SILICON_KEY_2` versus `SILICONFLOW_API_KEY_2`.
- Schema validation and negative fixtures for task envelopes and state ledger.
- Quota/reset policy source evidence and provider-specific redaction rules.
- Independent review of concurrency, duplicate task/PR prevention, stale leases, ledger corruption and fail-closed recovery.
- Separate authorization for workflow dispatch, provider calls, tests, qualification and activation.

## 8. Next implementation slice

Create a manual-dispatch-only coordinator with no schedule trigger initially. It should read an approved issue/task ID, validate the task envelope, load the canonical registry, select one eligible provider, write a redacted ledger transition with optimistic concurrency, call no more than one provider per run, and publish a sanitized artifact. Add periodic issue reconciliation and daily-reset scheduling only after independent review of the first slice. The cloud execution path must remain on GitHub-hosted runners.

## 9. Source references

- Provider registry: https://github.com/VlDMlNSh/mediahub-os/blob/main/ops/qualification/provider_model_registry.json
- Gemini Agent 2: https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-2.yml
- Gemini Agent 3: https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/gemini-agent-3.yml
- Self-hosted provider qualification workflow: https://github.com/VlDMlNSh/mediahub-os/blob/main/.github/workflows/astra-provider-qualification.yml
- LiteLLM: https://github.com/BerriAI/litellm
- AI Router candidate: https://github.com/sampath-M0/ai-router
- Current project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
