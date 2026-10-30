# Wave 479 — multi-provider cloud model router component selection (2026-10-30)

## Status

**RESEARCH COMPLETE / COMPONENT NOT SELECTED / NOT ADOPTED / RUNTIME NOT RUN.**

This is a bounded source-discovery and architecture pass. It does not authorize provider calls, credential reads, workflow dispatch, deployment, quota pooling, or changes to the active routing policy.

## Immutable source baseline

- Repository main observed commit: `f0448f28c7cfa61e4450c38529f09afbfdbbc7c7`.
- Canonical documentation branch: `docs/mediahub-chat-tree-map-20261012`; canonical map blob `75f62685459ec99ebf8be478f4e9096cdb842b1d).
- Bootstrap was fetched from the canonical branch; the checkpoint blob was `fd312ded05dd1898bd36d776a9669bb02920720d`; Master Roadmap blob `ea7e94e921045253f3e6494438e197c4bafae3a0`.
- Main router policy blob `e249333c1c0ce6c1c586a5f498dbfd3979418f6e`.
- Gemini controller blob `0a1246f6755020faf8b7e48d07bfff790bbaece3`.
- Issue [#301](https://github.com/VlDMlNSh/mediahub-os/issues/301) remains OPEN; its current acceptance gates include A0 issuer/ingress/lease/cancel/recovery, R-06 audit/privacy, authoritative runner target acceptance, schema validation and negative fixtures, independent review, then only a bounded read-only worker.
- PR [#590](https://github.com/VlDMlNSh/mediahub-os/pull/590) is OPEN/DRAFT/UNMERGED, head `98d466b3f372c541bd7301be087004b4e218d9b2`, base `bfb2a6d73ba64839e783d6ee30d0d8ae2e3074a4). PR workflow-run query and combined-status query returned empty arrays: exact-head CI **NOT VERIFIED**, not PASS. No formal PR review was returned.
- The canonical map fetch through Contents returned empty content; the blob endpoint returned the complete file. The canonical map is >1 MB and was not rewritten in this pass. A dedicated addendum is provided and linked here.

## Existing MediaHub policy boundary

The main `.github/ai/model-router.yml` is explicitly a **policy-only contract**, not a runtime dispatcher:
- `mode: policy_only`; `direct_provider_api_calls: false`.
- Only the Gemini batch controller and FCC/OpenRouter Free workflow are currently listed as admitted cloud-agent transports.
- Paid fallback is false; unknown routes fail closed; exact target SHA, independent review, runtime qualification and human production authorization are required.
- The same policy still lists a local FCC/Ollama route. This conflicts with the current Contour A cloud-only direction and is a policy reconciliation item, not permission to activate a local route.
- The existing FCC worker's OpenRouter `openrouter/free` route is not proof that the underlying model is Claude. The worker checks the concrete returned model ID for the `:free` suffix; any qualification must record that actual ID.

**Consequently, none of the candidate gateways below may be inserted into the allowlist or used as a direct provider transport in this wave.** A new gateway requires a reviewed contract change and all Issue #301 gates.

## OSS component comparison

Research date: 2026-10-30. Repository documentation and release pages were checked; no binaries were installed, no container was run, and no vulnerability scan or provider test was performed.

| Candidate | Current evidence observed | Useful capabilities | Material constraints / risks | Wave 479 disposition |
|---|---|---|---|---|
| [LiteLLM](https://github.com/BerriAI/litellm) | Latest stable release observed: `v1.106.6` (2026-10-28); `v1.109.0-dev.2` is pre-release (2026-10-30). Core repository license is MIT, with `enterprise/` separately licensed. | Broad provider abstraction; routing/fallbacks; virtual keys; budgets and RPM/TPM controls. | Budget enforcement requires a database; without DB some global budget enforcement fails open. Public advisories include a Critical privilege-escalation advisory (2026-09-30) and multiple SSRF/credential-exposure advisories. Must verify patched commit/version and secure config before any trial. | **Leading candidate for a later isolated qualification**, not selected/adopted. Pin stable release only after security review; do not use dev/RC. |
| [Bifrost](https://github.com/boelabs/bifrost) | Current repository identifies MIT license and production-oriented backend gateway. Documentation states Bun 1.4+, PostgreSQL 18+, Redis 8+. | Pools, least-busy/usage-based routing, cooldowns, retry/fallback chains, virtual keys, RPM/TPM and budgets. | Requires durable shared Postgres + Redis; this is not provided by separate ephemeral GitHub jobs. Native handling of provider-specific free-tier eligibility, quota reset semantics and account-level quota identity is not yet demonstrated. | **Secondary candidate**. Strong architecture features, but deployment/state prerequisites and free-tier semantics remain unqualified. |
| [Portkey Gateway](https://github.com/Portkey-AI/gateway) | Repository advertises MIT; latest stable release observed `v1.15.2` (2026-01-12); repository marks 2.0 as pre-release. | Retry/fallback, load balancing, broad provider catalog and guardrails. | Release cadence/current maintenance and the boundary between open-source and hosted/enterprise functionality need a deeper audit. No proof of native free-quota ledger semantics. | **Defer** pending maintenance and feature-boundary audit. |
| [New API](https://github.com/QuantumNous/new-api) | Latest release observed `v1.0.0-rc.47` (2026-10-25), signed tag; license is AGPLv3 with additional attribution/link conditions. | Channel management, upstream aggregation, quota/usage accounting, model format conversion. | Release is a pre-release; latest release notes include a warning that production use is not recommended. AGPLv3 and additional Section 7 attribution requirements require legal review. Channel/key distribution is not evidence of permission to multiply or bypass provider quotas. | **Exclude from first qualification wave**; reconsider only after stable release and license/security review. |

### Comparative conclusion

1. **No gateway is yet qualified as a drop-in free-provider quota router.** Generic model routing, retries, RPM/TPM limits and spend budgets do not establish provider-specific free-tier limits, reset windows, account ownership, or permission to use multiple credentials.
2. LiteLLM is the best first candidate for a *non-production compatibility/security spike* because of its broad provider support and mature proxy abstractions. Its critical security advisory history and database-backed budget semantics are explicit blockers to adoption until independently reviewed.
3. Bifrost is a strong alternative if a durable shared gateway and its Postgres/Redis dependencies become acceptable. Its routing model is promising, but provider free-tier quota semantics must be proven.
4. Do not deploy a long-lived gateway inside a GitHub-hosted job and mistake that for shared quota coordination: each job has an isolated ephemeral VM. A central atomic quota ledger would be required for parallel workers, with durable reservations and idempotent settlement.

## Required MediaHub router contract (proposed, not implemented)

The MediaHub-owned policy/ledger layer must remain authoritative even if a third-party gateway is used as a transport adapter.

Required records:
- Provider identity, provider account identity, credential reference (never credential value), model allowlist, plan/entitlement, data classification, quota unit, quota ceiling/remaining, reset timestamp/timezone, route expiry, cost class, fallback policy, status and provenance.
- Multiple API keys must be grouped by provider account/entitlement. They are **not** independent quotas unless the provider explicitly documents that they are.
- Quota reservations must be atomic across workers. A request cannot be sent until a reservation is granted; retries must be idempotent; actual usage must settle the reservation; uncertain outcomes must reconcile without double-spending.
- On 429, honor `Retry-After`, update the relevant account/model/window state, and choose only another independently authorized provider/account route. Never cycle keys to evade a limit.
- On 401/403 or policy/entitlement failure, block the route and fail closed; do not endlessly retry credentials.
- No silent paid fallback. Unknown plan, unknown account identity, unknown reset time, or ambiguous provider terms => BLOCKED.
- Record non-secret evidence: target SHA, task ID, provider/account identifiers, actual model ID, reservation/settlement IDs, quota window, fallback reason, response class, usage and timestamps.
- Keep lint, unit/integration tests, static analysis, builds and evidence generation off model API quota.

## Acceptance sequence for a future qualification spike

1. Reconcile `.github/ai/model-router.yml` with cloud-only Contour A; explicitly retire or segregate local FCC/Ollama policy without silently changing authority.
2. Complete Issue #301 A0/R-06/runner-target/schema gates and independently accept the runner/network target.
3. Select one candidate and pin an immutable release digest; review license, SBOM, transitive dependencies, advisories, image signature and source provenance.
4. Build deterministic synthetic tests only: quota reservation races, 429 + Retry-After, reset rollover, duplicate settlement, unknown entitlement, same-account multi-key grouping, provider outage, 401/403, timeout ambiguity, paid-fallback prohibition, data-class denial and revocation.
5. Demonstrate durable atomic ledger semantics across at least two independent ephemeral jobs without provider credentials.
6. Independently review gateway configuration, secret isolation, egress controls and evidence provenance.
7. Only then request a separately authorized, bounded live provider qualification. No automatic dispatch is implied.

## Execution record

- Gemini controller: **NOT RUN**; no controller run ID or child job IDs.
- Claude/FCC: **NOT RUN**; no host/session ID; no provider API call.
- Provider credentials: **NOT READ**.
- Provider calls: **NOT RUN**.
- Gateway installation/benchmark: **NOT RUN**.
- Tests/security scan/SBOM/signature verification: **NOT RUN**.
- Merge/deployment/qualification/adoption: **NOT RUN**.
- Exact-head CI for this documentation branch: pending/not yet available at report creation; must be checked on final head.
- No secret values or credentials were accessed.

## Next step

Prepare a bounded LiteLLM-versus-Bifrost security and quota-ledger design spike using synthetic providers and synthetic keys only, after the outstanding Issue #301 governance and runner-target gates are reconciled. Do not activate either gateway or make provider calls.

## References

- LiteLLM releases: https://github.com/BerriAI/litellm/releases
- LiteLLM license: https://github.com/BerriAI/litellm/blob/main/LICENSE
- LiteLLM budget/rate-limit documentation: https://docs.litellm.ai/docs/proxy/users
- LiteLLM security advisories: https://github.com/BerriAI/litellm/security/advisories
- Bifrost repository: https://github.com/boelabs/bifrost
- Bifrost routing: https://bifrost.boelabs.com/docs/routing
- Bifrost fallbacks: https://bifrost.boelabs.com/docs/fallbacks
- Portkey Gateway repository: https://github.com/Portkey-AI/gateway
- Portkey releases: https://github.com/Portkey-AI/gateway/releases
- New API README/license: https://github.com/QuantumNous/new-api/blob/main/README.en.md
- New API releases: https://github.com/QuantumNous/new-api/releases
- MediaHub Issue #301: https://github.com/VlDMlNSh/mediahub-os/issues/301
- MediaHub canonical map: https://github.com/VlDMlNSh/mediahub-os/blob/docs/mediahub-chat-tree-map-20261012/docs/architecture/MEDIAHUB-CHAT-TREE-MAP.md
