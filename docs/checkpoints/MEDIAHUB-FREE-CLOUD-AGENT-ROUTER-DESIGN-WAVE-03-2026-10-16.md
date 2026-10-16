# MediaHub OS — Free Cloud Agent Router and Quota Failover Design, Wave 03
Date: 2026-10-16
Repository: https://github.com/VlDMlNSh/mediahub-os
Documentation ref: `docs/mediahub-chat-tree-map-20261012`
Status: DESIGN / PROPOSED / RUNTIME-UNVERIFIED / NO PROVIDER ENABLEMENT

## 1. Decision summary

Use GitHub-hosted Actions runners as the first cloud execution surface. Keep the provider adapter stateless, read-only by default, and separate from the legacy Astra control/supervisor workflows. The first admission candidate is the existing Gemini read-only workflow pair. Add further provider adapters only after account-level quota, current terms, data handling, model availability, key ownership, and successful bounded runtime evidence are documented.

This pass is documentation-only. It does not change workflow source, configure GitHub secrets, dispatch a workflow, call a model, inspect secret values, install software, execute tests, inspect a host/runner, change infrastructure, deploy, or merge branches. The connected GitHub interface available for this pass does not expose repository-secret listing or workflow-dispatch actions.

## 2. Cloud agents suitable for evaluation

Provider free tiers and model availability change over time. The entries below are candidates, not confirmation that an API key exists in the repository or that a particular account currently has free quota.

| Agent/provider path | Potential role | Current evidence and limits | Admission status |
|---|---|---|---|
| Google Gemini API through existing GitHub Actions workflows | Architecture review, source reconciliation, bounded security triage | Source-confirmed workflows: `.github/workflows/gemini-readonly-audit.yml` blob `0d10efdda251f2ceca43175981c919102303572b` and retry workflow blob `96fcc9ed4e45659d0118f0b9f3593a0c736200f0`. Current provider documentation describes a free tier with model- and project-specific RPM/TPM/RPD limits. Existing workflow expects `GEMINI_API_KEY` or `GOOGLE_API_KEY`. | FIRST CANDIDATE; key metadata, quota, and current successful run remain UNKNOWN |
| GroqCloud API | Fast bounded code review, classification, summarization, secondary inference provider | Official rate-limit documentation describes Free Plan limits varying by model and organization; exact live limits belong to the account's Limits page. A 429 response and `retry-after` must drive bounded cooldown. | CANDIDATE; account/key/terms/data policy/runtime proof required |
| OpenRouter free-model API | Provider/model diversity through one OpenAI-compatible API | Official pricing page lists free models and currently documents 50 requests/day on the Free plan; the free-model limit is also documented as 20 requests/minute. Free models may be unavailable or throttled upstream; failed attempts can consume quota. Free plan lacks paid-plan routing/budget controls. | CANDIDATE; daily quota is low and provider data-routing must be reviewed |
| GitHub Models | Model-assisted issue triage and bounded repository reasoning, if model access is enabled for the account | GitHub Actions is already the execution surface, but this pass did not establish account entitlement, a usable model endpoint/key, or current free model quota. Treat as an unverified candidate pending official account-specific evidence. | DEFER / UNVERIFIED |
| Cerebras Inference API | Potential fast secondary provider | No account-specific entitlement, current free quota, or accepted integration evidence was established in this pass. | DEFER / UNVERIFIED |
| Local inference adapter (for example, Ollama) | Offline/local-only assistance where a separately approved host is available | No cloud per-token inference fee, but hardware, electricity, installation, model license, data handling and runtime qualification still apply. This is outside the requested serverless cloud path and remains a separate candidate. | OUT OF SCOPE for this wave |

Official references:
- Gemini rate limits: https://ai.google.dev/gemini-api/docs/rate-limits
- Gemini pricing/free tier: https://ai.google.dev/gemini-api/docs/pricing
- Groq rate limits: https://console.groq.com/docs/rate-limits
- Groq model catalog: https://console.groq.com/docs/models
- OpenRouter pricing and free limits: https://openrouter.ai/pricing
- OpenRouter free-model limits and failure caveats: https://openrouter.ai/blog/tutorials/free-llm-apis-compared/

A free label is not a perpetual quota guarantee. Review each provider's current account terms and data-use policy before sending repository content. Gemini's published free tier states that submitted content may be used to improve products; exclude secrets, private user data, credentials, and sensitive operational evidence from its context.

## 3. Target execution topology

```text
GitHub event / manually approved task
              |
              v
      Cloud Agent Dispatcher
      - task schema + task ID
      - immutable source SHA
      - explicit context allowlist
      - free-only provider allowlist
      - bounded token/output budget
              |
              v
      Quota & Policy Router
      - provider/model registry
      - per-provider quota bucket
      - circuit breaker / cooldown
      - cost ceiling = USD 0
      - no paid fallback
              |
       +------+------+
       |             |
       v             v
   Gemini API     Groq/OpenRouter
   adapter        adapters (future)
       |             |
       +------+------+
              |
              v
     Untrusted advisory output
              |
              v
     Evidence envelope + artifact
     - source commit SHA
     - file path/blob SHA/digest
     - provider/model ID
     - run ID/time/status
     - quota/fallback reason
     - output digest/redaction status
              |
              v
     Human/governance review
     No direct merge, deployment, or
     canonical product-state mutation
```

Execution should use a GitHub-hosted runner such as `ubuntu-latest` for the cloud-agent job. The existing Gemini workflows already use a GitHub-hosted runner and `contents: read`. Keep cloud-agent workflows separate from legacy Astra workflows that target self-hosted labels and historical host identities. A self-hosted runner is a different trust and network boundary and is not required for this design.

## 4. Key and quota switching contract

### 4.1 Registry fields

Each provider entry should declare:
- stable provider ID and enabled status;
- API base URL allowlist and authentication-header type;
- approved model IDs and free-only eligibility;
- secret *name* reference (never the secret value);
- quota scope: account, organization, project, model, and reset window as applicable;
- concurrency cap, RPM/TPM/RPD guard, maximum input/output tokens;
- request timeout and bounded retry count;
- retryable statuses and provider-specific quota signals;
- data classification allowed for egress;
- last successful evidence reference, current status and review expiry.

### 4.2 Rotation rules

1. Prefer switching providers after a confirmed quota response, provider outage, or model unavailability, provided the alternate provider has an independently documented available quota.
2. Retry the same provider only for transient errors and only within a small bounded attempt count. Honor `Retry-After`; use exponential backoff with jitter.
3. Treat HTTP 401/403 as credential/configuration or policy failures. Stop that provider and raise an alert; do not cycle keys to evade an authorization decision.
4. Treat HTTP 429 as quota/rate limiting. Cool down the relevant quota bucket until the documented reset or `Retry-After`; avoid repeatedly probing it.
5. Multiple keys within the same account/project may share a quota. A new key is not a new quota bucket unless the provider explicitly documents independent quota scope.
6. Rotate among keys only when each key belongs to an explicitly authorized integration/account/project and the provider's terms permit the usage pattern. Never create or cycle identities to bypass rate limits, regional restrictions, billing controls, or abuse prevention.
7. Keep a hard free-only policy: provider/model registry entries must explicitly state `free=true`, and any ambiguous or paid model selection must fail closed. No automatic paid fallback, auto-top-up, or credit purchase.
8. Do not store key values in repository files, workflow inputs, prompts, logs, artifacts, generated reports, or Git history. Inject secrets only through GitHub Actions secrets/environment at the job boundary.
9. Do not print request URLs containing credentials, authorization headers, full provider error bodies, or prompts containing secret-like values. Sanitize diagnostics before logging.
10. If every admitted provider is exhausted, pause the task and preserve the queue item. Never spin retries or silently switch to a paid endpoint.

### 4.3 Provider selection state machine

```text
READY
  -> select eligible provider with available quota
  -> call once
     -> 2xx: record evidence; COMPLETE
     -> transient 5xx/network: bounded retry, then next provider
     -> 429/quota: cool down quota bucket; try next eligible provider
     -> 401/403: disable provider for this run; raise configuration alert
     -> model unavailable: mark model unavailable; try eligible alternate
  -> no eligible provider: PAUSED_QUOTA_EXHAUSTED
```

The router must distinguish `PROVIDER_QUOTA_EXHAUSTED`, `PROVIDER_UNAVAILABLE`, `AUTH_CONFIGURATION_ERROR`, `POLICY_DENIED`, `TASK_INVALID`, and `OUTPUT_REJECTED`. Fallback is permitted only for provider availability/quota conditions; it must never bypass a policy denial.

## 5. Security and data boundaries

- Provider output is untrusted advisory data. It cannot authorize workflow mutation, issue commands, alter secrets, approve its own evidence, merge code, deploy, or mutate canonical MediaHub product state.
- Default workflow permissions: `contents: read`; set job-level permissions explicitly. Use `persist-credentials: false`. Pin third-party actions to reviewed full commit SHAs before production admission.
- Pin source to an immutable approved commit SHA; record resolved SHA and selected-file digests in the artifact manifest.
- Use a positive path allowlist and canonical path resolution. Exclude workflow source from model context until a dedicated security exception is approved.
- Bound task size, context bytes, token budget, output bytes, runtime, retries, concurrency, and artifact retention.
- Publish only sanitized Markdown/JSON and an evidence manifest. Treat model findings as claims requiring source-level verification.
- Never give model jobs `actions: write`, issue write, repository contents write, HMAC node secrets, self-hosted runner access, or `secrets: inherit` by default.
- Any future patch-producing agent must work on a disposable branch/worktree with a narrowly scoped token and open a reviewable pull request; direct push to `main` remains out of scope.
- Keep the cloud agent in Contour A. It does not become MediaHub Product State Authority and cannot bypass Policy → Authorization → Consumer Boundary → State Authority.

## 6. Existing repository integration points

| Path | Current source evidence | Proposed use |
|---|---|---|
| `.github/workflows/gemini-readonly-audit.yml` | Blob `0d10efdda251f2ceca43175981c919102303572b`; manual dispatch; `contents: read`; `persist-credentials: false`; GitHub-hosted runner | Existing first provider entry; harden ref/path provenance before trusted evidence use |
| `.github/workflows/gemini-readonly-audit-retry.yml` | Blob `96fcc9ed4e45659d0118f0b9f3593a0c736200f0`; bounded retry logic and sanitized error metadata | Existing retry baseline; extend only after review and separate implementation authorization |
| `docs/checkpoints/MEDIAHUB-FREE-CLOUD-AGENT-ONBOARDING-WAVE-01-2026-10-16.md` | Blob `18d99ea96e0f51d9dcd2245b46594371e29a0f56` | Existing manual onboarding/runbook |
| `docs/checkpoints/MEDIAHUB-CLOUD-AGENT-READINESS-AND-SECURITY-EVIDENCE-MATRIX-WAVE-02-2026-10-16.md` | Blob `2c5743a093b425a01e2ec413db9adb3ade22fb3b` | Existing admission matrix and security evidence ledger |
| `docs/checkpoints/MEDIAHUB-GITHUB-SECURITY-AND-UNIFIED-MATRIX-WAVE-02-2026-10-16.md` | Blob `5d7484a0dac931a6e6f671df1a1749bacc242982` | Security gates and workflow risks; alert/branch settings remain partly UNKNOWN |

Source review of `.github/workflows/astra-chat-control.yml` at `main` blob `51b17ec2410032772f9baa1de4afedb6b000f3c4` shows an issue-comment-triggered controller on self-hosted runner labels with workflow-level write permissions and legacy host checks. Source review of `.github/workflows/astra-autonomous-supervisor.yml` at `main` blob `a0209a2d01122354d19e95d2f362a6ecfa3d6186` shows self-hosted control labels, downstream dispatch, HMAC secrets, `secrets: inherit` through a provider-qualification call, and persisted checkout credentials in a later job. These are separate high-authority paths and should remain outside the new cloud-agent router until their existing P0 review gates are resolved.

## 7. Rollout gates

| Gate | Required evidence | Status |
|---|---|---|
| AGENT-G0: provider inventory | Official terms, current free tier, quota scope/reset, model IDs, data-use policy | PARTIAL; Gemini/Groq/OpenRouter official pages reviewed; account-specific quota UNKNOWN |
| AGENT-G1: key inventory | Owner-visible secret names/update metadata; no secret values exported | BLOCKED on owner-visible GitHub UI evidence |
| AGENT-G2: router contract | Provider registry schema, state machine, cost=0 enforcement, failure taxonomy | DESIGNED in this document; implementation absent |
| AGENT-G3: workflow isolation | Hosted runner, minimal permissions, pinned actions, immutable source SHA | PARTIAL; existing Gemini source has some controls; provenance hardening open |
| AGENT-G4: quota handling | Provider-specific 429/reset tests, bounded retries, exhausted-quota pause | DESIGNED; tests/runtime evidence absent |
| AGENT-G5: data egress | Approved data classes, provider retention/use policy, redaction review | OPEN |
| AGENT-G6: one-provider proof | Manual bounded run, HTTP status, run ID, resolved SHA, artifact digest and redaction review | RUNTIME-UNVERIFIED |
| AGENT-G7: second-provider proof | Separate successful bounded run and fallback evidence | DEFERRED |
| AGENT-G8: independent acceptance | Reviewer verifies source, logs, artifact manifest, cost=0 and fail-closed behavior | OPEN |

## 8. Implementation sequence after authorization

1. Owner reviews current GitHub Actions secret metadata and provider terms; secret values remain private.
2. Record approved provider/model allowlist and data-egress classes.
3. Prepare a narrow workflow source patch on a separate branch after explicit implementation authorization; leave the legacy Astra workflows unchanged.
4. Add provider registry schema, router module, sanitized evidence manifest and fail-closed quota state.
5. Add tests for 429/Retry-After, shared quota buckets, invalid credentials, paid-model rejection, prompt/path bounds, secret redaction, all-provider exhaustion, output integrity and duplicate task IDs. Test execution requires separate explicit authorization under current project rules.
6. Run one owner-approved manual Gemini job; verify run ID, exact commit SHA, artifact digest, output redaction and zero paid usage.
7. Admit a second provider only after the first path is reviewed and its own key/quota/data policy is verified.
8. Independently review the evidence package; only then consider enabling recurring scheduling or any patch-producing agent.
9. Keep Contour B blocked until Contour A deployment and independent acceptance gates are satisfied.

## 9. Current status and limitations

Confirmed:
- The repository has two source-confirmed Gemini workflows on `main`.
- Both are designed for GitHub-hosted execution and use read-only repository permissions.
- Official provider documentation currently describes free access for Gemini, a free Groq plan with account/model rate limits, and OpenRouter free models with a published 50-requests/day allowance.
- The current main branch also contains legacy Astra control/supervisor workflows with materially greater authority; the new agent path should be isolated from them.

Unknown:
- Whether any expected provider key is currently configured in repository Actions secrets.
- Which providers have active owner-controlled accounts, valid keys, free quota, or acceptable regional/data terms.
- Current account-specific rate limits, reset times, model availability, billing status and actual data-retention settings.
- Branch protection and security-alert state, which remain partly UNKNOWN in the prior security report.
- Whether a new router or provider integration has passed runtime verification.

No credentials were read, no model/provider was called, no workflow was dispatched, no tests or scanners were executed, and no infrastructure or deployment action occurred. This artifact is a proposed design, not an implemented or accepted system.

Project map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
