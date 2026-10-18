# Contour A — cloud model/provider candidate register (Wave 148)
Date: 2026-10-18
Status: CANDIDATE INVENTORY / NOT ACCOUNT-VERIFIED / NOT ENABLED FOR AUTONOMOUS DISPATCH
Governing plan: [Master Development Roadmap](MEDIAHUB-MASTER-DEVELOPMENT-ROADMAP-1.0.md)
Manual fallback: [Wave 147 operating plan](MEDIAHUB-CONTOUR-A-CLOUD-AGENT-ENABLEMENT-AND-MANUAL-FALLBACK-ROADMAP-ADDENDUM-2026-10-18.md)
Control issue: [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301)

## Purpose and evidence boundary
This register turns the owner-provided candidate list into an ordered verification backlog. Names, model IDs, secret-name patterns and quota figures below are **reported candidate information**, not verified live account entitlements. Quotas, free-tier availability, reset times, model availability, service terms, data retention and geographic eligibility change. No credentials were read, no provider API was called, no model invocation was performed, and no provider was activated in this pass.

A route may be marked ENABLED only after the project records official current documentation, account/project-level quota evidence, model ID verification, non-secret credential-reference mapping, budget ceiling, data/egress policy, timeout/retry/rate-limit handling, observability and negative tests. Never store key values in this register.

## Candidate order and verification checklist

| Priority | Provider / candidate | Intended role | Reported model/limit hypothesis (unverified) | Blocking checks |
|---|---|---|---|---|
| P1 | Cloudflare Workers AI | low-cost general fallback | `@cf/meta/llama-3.1-8b-instruct`; reported 10,000 Neurons/day and 00:00 UTC reset | Verify current account plan, current model availability and exact billing/quota docs; map Cloudflare account binding securely; test quota exhaustion and reset behavior. |
| P1 | Groq | low-latency general/code work | `openai/gpt-oss-20b`, `openai/gpt-oss-120b`; RPD/RPM/TPM/TPD vary by model/org | Verify exact model IDs, organization limits and current rate-limit headers; classify retryable 429s; avoid assuming one key means one independent quota. |
| P1 | Gemini profiles 1/2/3 | implementation, research, independent review | Existing three profile labels; quota is project-scoped per the supplied note | Inspect existing registry/workflows without exposing secret values; map each profile to an actual distinct role/model/project; verify project-level quota and independent review separation; no claim that three keys multiply quota. |
| P1 | Z.ai / GLM Flash | fast general tasks | Existing `ZAI_API_KEY*` naming and GLM Flash candidates | Resolve exact secret-name-to-runtime-binding mismatch, model IDs, terms, free quota and reset evidence. |
| P1 | SiliconFlow | code/instructions/reasoning | Qwen 2.5, DeepSeek R1 Distill, GLM-4.9B as reported registry candidates | Verify exact model identifiers (including the reported GLM-4.9B name), secret mapping, quota, model availability, retention and provider terms. |
| P2 | Novita | reserve executor | Llama 3.2 1B, Qwen 2.5 7B | Verify current free-credit/plan status, exact model IDs, key/account quota independence, reset/expiry and terms. |
| P2 | Mistral | analysis and code review | Studio Free mode reported | Verify current Free-mode eligibility, allowed models and actual account rate limits; do not assume every model is free. |
| P2 | OpenRouter | limited free-model reserve | Reported 20 RPM and 50 requests/day for free models | Verify current official limits and eligible model routing; inspect upstream provider selection, data policy, fallback semantics and headers. Treat this as an opportunistic reserve, not a guaranteed daily pool. |
| P3 | Hugging Face Inference Providers | small reserve | Reported $0.10 monthly credits | Verify current credit amount/expiry, provider-specific model support, billing stop behavior and spend ceilings. Not a dependable daily pool absent account evidence. |
| P4 | Kimi / Moonshot | additional candidate | Free quota/reset not established in supplied audit | Verify current official plans, model IDs, quota and terms before admission. |
| P4 | LLM7 | additional candidate | Free quota/reset not established | Establish operator/API identity, current terms, limits and reliability before sending project data. |
| P4 | Aion Labs | additional candidate | Free quota/reset not established | Verify exact service/provider identity, official API/docs, current model catalog and quota; keep blocked until identity is unambiguous. |
| P4 | UnoRouter | additional candidate | Free quota/reset not established; routing identity unresolved in roadmap | Establish upstream identities, routing behavior, terms, quota accounting and provenance; do not treat as independent capacity until verified. |
| HOLD | SambaNova | not in guaranteed-free pool | Free entitlement not established | Verify plan/credit, rate limits, terms and budget before considering. |
| HOLD | DeepSeek Trial | not in guaranteed-free pool | Trial conditions not established | Verify current trial limits, expiration, data policy and billing behavior. |
| HOLD | MiMo | not in guaranteed-free pool | Provider/model/entitlement not established | Confirm exact provider and model identity, current official access, limits and terms. |

## Admission contract for every provider/model route
1. Stable provider ID and exact model ID; official documentation URL and access date.
2. Account/project/organization scope and quota dimensions (RPM, RPD, TPM, TPD, neurons/credits/currency), reset timezone, expiry, and source of evidence.
3. Secret *name/reference* only, mapped through approved runtime secret injection; no secret values in source, prompts, artifacts, logs or docs.
4. Explicit task capability and allowed data classes; provider terms, retention/training policy and egress/region eligibility reviewed.
5. Budget/spend ceiling; no paid fallback unless that exact destination and budget are independently authorized.
6. Rate-limit headers and normalized error classes; bounded backoff/jitter; no retry storms; per-route circuit breaker and quota ledger.
7. Immutable request/task ID and evidence binding; record provider/model/version, route, request time, result status, usage/headers when available, artifact digest and source SHA without logging sensitive prompt contents.
8. Expiry/revocation and disable switch; fail closed when identity, quota, policy, cost or destination is unknown.
9. Negative tests: invalid credentials, denied model, quota exhausted, 429, timeout, 5xx, malformed response, provider substitution, route mismatch, disabled/expired profile, and budget exhausted.
10. Independent validation before registry admission. Provider output cannot qualify itself.

## Routing policy recommendation
- Start with a **manual, read-only evaluation matrix** for the P1 routes; no autonomous task execution until worker issuer/capability and evidence provenance gates pass.
- Do not encode a fixed provider priority as a guarantee of free service. Choose only among routes whose current eligibility, remaining quota, data policy and budget are known for the specific task.
- Keep separate quotas by provider/account/project/model where the upstream service does so; do not multiply quotas by creating multiple keys under one project/account.
- Treat fallback as a new destination requiring policy/budget approval, not as a transparent retry.
- Distinguish three Gemini roles logically (implementation, research, independent review). Independent review must not be represented as independent if the same context/agent authored the patch and simply rubber-stamps it.
- The runtime registry should have explicit states: CANDIDATE → DOCS_VERIFIED → ACCOUNT_VERIFIED → POLICY_APPROVED → TESTED → ENABLED; failures/unknowns remain BLOCKED. Registry state transitions require evidence references and authorized review.

## Next actions
1. Locate the existing provider/model registry and secret-name mapping in the repository; compare it against this candidate register without reading or printing secret values.
2. Validate official provider docs and current account-level limits one route at a time, starting Cloudflare Workers AI, Groq and Gemini, then resolve Z.ai/SiliconFlow naming discrepancies.
3. Add/update machine-readable provider registry schema and negative fixtures only after finding the existing canonical schema/contract; do not create a parallel authority registry.
4. Exercise routes with a non-secret, read-only test only after explicit runtime credential and data-egress gates; record evidence and spend.
5. Keep all candidates blocked from autonomous queue admission until A0 signed ingress, immutable source/workspace, authoritative provenance and queue recovery gates are accepted.

## Status
Wave 148 records the plan and candidate register only. It does not establish current free quotas, account access, successful invocations, provider connectivity, or autonomous queue readiness.
