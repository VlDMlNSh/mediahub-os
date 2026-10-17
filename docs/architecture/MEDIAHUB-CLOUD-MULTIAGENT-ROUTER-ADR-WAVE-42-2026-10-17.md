# MediaHub Cloud Multi-Agent Router — Architecture Decision Record, Wave 42

- Date: 2026-10-17
- Status: **PROPOSED / SOURCE REVIEW PARTIAL / IMPLEMENTATION GATED**
- Contour: A — Developer Fabric
- Canonical functional baseline: Baseline 2.0
- Related implementation proposal: [Gemini Agent Pool PR branch](https://github.com/VlDMlNSh/mediahub-os/tree/automation/gemini-agent-pool-wave42)

## Context

Two additional Gemini credentials have been registered in GitHub Actions Secrets as `GEMINI_API_KEY_2` and `GEMINI_API_KEY_3`. Two dedicated workflow profiles are proposed, each using its explicitly mapped secret. The next architectural goal is a shared multi-agent system with durable task state, provider-aware quota management, bounded retries, independent specialist roles, and evidence-producing task completion.

The project roadmap separates Contour A (Developer Fabric) from Contour B (MediaHub OS product). This design applies to Contour A only. Existing A0 ingress, MH-12 tool enforcement, MH-04 security/trust, MH-11 diagnostics, and P0-07 authorization/publication/API contracts remain authoritative dependencies. Any unresolved contract blocks runtime activation.

## Decision proposed

1. Keep GitHub Actions as the bounded task execution substrate for repository engineering agents.
2. Treat each specialist agent as a separately invoked role with a dedicated workflow, task scope, provider credential reference, timeout, tool allowlist, and evidence output.
3. Evaluate a serverless router with durable Postgres state as the shared API and queue boundary. Supabase Edge Functions + Postgres are the leading candidate for source evaluation, not an accepted deployment target.
4. Use provider/account/project/model quota metadata to choose eligible capacity. API key rotation alone is not a quota model.
5. Honor provider terms and the actual quota scope. When a quota is exhausted, respect cooldown/reset guidance, use only an independently permitted provider fallback, or defer the task.
6. Keep provider credentials in the secret store of the runtime that consumes them. GitHub Actions secrets are not automatically available to Supabase functions.
7. Require explicit caller authorization, typed task envelopes, data-egress policy, idempotency, bounded retries, concurrency/budget limits, and redacted audit events.
8. Keep runtime deployment, secret transfer, provider calls, tests, qualification, schedule activation, and production acceptance as separately authorized stages.

## Existing component review — initial findings

Candidate repository: https://github.com/sampath-M0/ai-router

The reviewed `supabase/functions/_shared/keyManager.js` implements persistent cooldown records in Postgres and leaves raw key strings in runtime environment variables. The reviewed Gemini adapter recognizes HTTP 429 and reads `Retry-After`. These are useful patterns for further review.

Source-level issues observed in the candidate:
- A cooldown-state database read error returns an empty cooldown set, which is fail-open. A quota-aware router should treat unknown state as unavailable or use an explicitly governed fallback.
- Key selection and cooldown writes are separate operations; concurrent requests can select the same key before cooldown persistence. A reservation/lease or equivalent atomic state transition is required.
- The reviewed Gemini adapter places the key in the URL query string. URL logging and tracing can leak it; credential transport and redaction need an explicit security review.
- Per-key cooldowns alone cannot model a project-wide or model-wide quota.
- The free-form request shape lacks MediaHub's typed task envelope, caller authorization, tool constraints, data-egress class, and output/time budgets.
- The complete upstream repository, migration policies, endpoint authentication, dependency chain, and deployment configuration require review before adoption.

Disposition: reuse selected patterns after a pinned-revision source/security review; no wholesale upstream deployment.

## Proposed logical components

| Component | Responsibility | State/authority |
|---|---|---|
| Task ingress | Authenticate requester, validate typed task, assign task ID and idempotency key | A0 ingress and accepted authorization contract |
| Task queue | Durable task state, retry scheduling, leases, dead-letter/quota-exhausted states | Engineering task state only; never canonical MediaHub product state |
| Policy evaluator | Enforce role, tools, scope, data-egress, provider allowlist, budgets | Accepted policy and authorization contracts |
| Provider router | Select eligible provider/model/account within quota policy | Provider telemetry and durable quota/cooldown state |
| Agent executor | Invoke one specialist role within its bounded context | Task-scoped execution only |
| Evidence collector | Store redacted logs, artifact references, source revisions, PR and verification state | Evidence record; no automatic acceptance authority |
| Independent reviewer | Review source evidence and PR against task acceptance criteria | Review findings; human retains merge/release authority |
| Scheduler | Start permitted work on events or schedules | Queue only; no indefinite process assumption |

## Routing algorithm requirements

1. Authenticate caller and validate the request envelope before reading or selecting credentials.
2. Determine task policy: allowed providers/models, data-egress class, deadline, max attempts, concurrency slot, and budget.
3. Determine quota scope for each candidate: provider, account/project, model, request/token metric, and reset window.
4. Atomically reserve an eligible quota slot or concurrency lease before dispatch.
5. On HTTP 429, classify the provider's exact error and use Retry-After/reset details when available. Persist cooldown at the actual quota scope, not just a credential index.
6. Retry only idempotent operations with bounded exponential backoff and jitter. Engineering tasks that create branches/PRs require task-level idempotency and duplicate-PR detection.
7. Cross-provider fallback is allowed only when the task's data-egress policy explicitly permits the destination and provider retention/security terms are approved.
8. If all eligible providers are exhausted, return `QUOTA_EXHAUSTED` and a safe retry hint, or queue for the provider's permitted reset window.
9. If authorization, quota state, or data-egress policy is unknown, fail closed. Never use a different credential identity solely to bypass exhausted quota.
10. Log task ID, provider/model alias, quota scope alias, timing, outcome category, and retry/cooldown metadata. Exclude API keys, authorization headers, and raw request URLs containing credentials.

## Credential boundary

- GitHub Actions workflows may consume only the secret explicitly mapped to that workflow.
- A Supabase function consumes Supabase project secrets; it cannot read GitHub repository secrets directly.
- Any future secret transfer requires a reviewed deployment mechanism, least-privilege access, redaction checks, rotation/revocation procedure, and owner authorization.
- Secret values stay out of Git files, issue/PR bodies, prompts, artifacts, and ordinary logs.
- Secret-name presence does not prove credential validity or provider quota availability.

## Current environment evidence

- GitHub repository main HEAD observed after merging the Gemini runbook PR: `9e8b44367897a6805ba88a7ff79ed9fd8715271b`.
- Existing Gemini workflow blob SHA: `09523d809530ae5b7bf528eab5fa53bc5deaf92d`.
- Supabase account connection returned zero projects; one organization is visible. No project was created.
- Agent workflow definitions are proposed on branch `automation/gemini-agent-pool-wave42`; source read-back has been performed.
- The two new workflows have not been dispatched. Provider credential validity, quota, runtime behavior, and PR creation are unverified.
- No router code, database, edge function, schedule, deployment, or infrastructure has been activated.

## Acceptance gates

- [ ] Complete source/license/dependency review at a pinned upstream commit.
- [ ] Crosswalk task ingress, MH-04, MH-11, MH-12, A0, and P0-07 authority/security contracts.
- [ ] Approve typed task envelope and explicit provider/data-egress policy.
- [ ] Design atomic quota reservation, durable cooldowns, idempotency, and queue recovery.
- [ ] Approve credential-store placement and transfer mechanism.
- [ ] Obtain separate authorization for tests, provider calls, cloud project/configuration, and deployment.
- [ ] Verify concurrent 429 handling, provider outage behavior, secret redaction, policy-preserving fallback, idempotency, and quota exhaustion with revision-bound evidence.
- [ ] Independently accept runtime and operational recovery behavior before calling the system production-ready.

## Next bounded step

Use Agent 2 to complete pinned-revision source/license inventory and contract crosswalk. Use Agent 3 to independently review the evidence and routing threat model. Only then propose the smallest implementation PR consistent with accepted authority and security contracts.
