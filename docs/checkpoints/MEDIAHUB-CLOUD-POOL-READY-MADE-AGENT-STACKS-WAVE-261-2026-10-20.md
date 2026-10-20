# Wave 261 — Ready-made multi-agent systems and corporation-enabling components (2026-10-20)

## Owner direction
The cloud-pool track must not be limited to adding model API endpoints. It must evaluate and integrate mature, ready-made multi-agent orchestration systems, agent runtimes, workflow/queue/state components and components for scaling from a small agent pool to a governed agent corporation. Prefer adopting stable existing components over writing equivalent orchestration from scratch.

## Existing source evidence read
- Registry: `ops/qualification/provider_model_registry.json`, blob SHA `62328126fd2cd8879a73bb6812adcacd3e2abe84`. It contains a provider/model candidate inventory, but labels such as `free` and `permanent_free` are registry assertions, not proof of current provider terms, eligibility, quota or runtime reachability.
- Existing ECC decision: `docs/operations/ASTRA-ECC-INTEGRATION.md`, blob SHA `c707a83777ae5970081bd6bb1e3027c88bbf3fa1`. It explicitly rejects ECC as a dependency or second controller, while selectively applying ECC-derived development patterns. Do not silently reverse this authority decision; re-open it only through explicit architecture/governance change control.
- Existing cloud router ADR: `docs/architecture/MEDIAHUB-CLOUD-MULTIAGENT-ROUTER-ADR-WAVE-42-2026-10-17.md`, blob SHA `f445e2ab6b43dfcae275ffa598e44ab18049e504`, status PROPOSED / SOURCE REVIEW PARTIAL / IMPLEMENTATION GATED. It evaluates a provider-aware router and durable state; Supabase Edge Functions + Postgres is a candidate, not an accepted deployment target.
- Existing runtime: `runtime/mediahub_runtime/agent_fabric.py`, blob SHA `3c70dda5df8c6caa9411201d754ead6b3bfdf6dd`, provides bounded file-backed claim/lease primitives. It is not by itself a distributed cloud queue or corporate agent platform.
- Existing routing qualification contract: `ops/agent-fabric/providers/local-executor-routing-v2.yaml`, blob SHA `af3d96fe91055af6ba79eded9c800d28d8c0c5c9`, marks ASTRA Gold qualification gated and requires identity, exact source SHA, isolated workspace, independent verification and bounded concurrency.
- Main branch snapshot at `80be45a70732b1d568164571d4273a6397792c3b` includes these files; this read is source inventory only, not integration/acceptance.

## Architecture direction — reuse first, authority remains singular
1. **Multi-agent framework layer:** shortlist mature projects such as LangGraph, AutoGen, CrewAI, OpenHands/SWE-agent, and ECC as *candidates for comparative review*, not automatic dependencies. Evaluate license, activity/security posture, provider adapters, resumability, tool sandboxing, durable state, tracing, cancellation, deterministic tests, self-hosted/GitHub-hosted compatibility and upgrade cost. The correct shortlist may change after source review.
2. **Agent lifecycle/orchestration:** task decomposition, typed task envelopes, role/capability assignment, bounded retries, lease/heartbeat, deadlines/cancellation, idempotency and result reconciliation. Adopt the smallest compatible existing component rather than deploying several overlapping orchestrators.
3. **Provider/model router:** reuse existing provider registry and proposed router ADR; add provider/model/account quota state, reset/cooldown evidence, concurrency reservations and fail-closed fallback. Key rotation alone is not quota management.
4. **Durable state/queue:** evaluate PostgreSQL-backed queue/state or a managed workflow engine for atomic leases, retries, recovery, audit and outbox/idempotency. Keep the current file-backed claim store for its intended local scope unless evidence supports a governed migration.
5. **Execution substrate:** GitHub-hosted ephemeral runners for repository engineering tasks; any separate cloud runner/runtime requires isolated workspace, egress controls, least privilege, exact-SHA checkout, pinned dependencies/actions and runtime-only credentials.
6. **Evidence and observability:** common task/run IDs, exact source/model/provider refs, redacted logs, artifact digests, test outcomes, quota/cost metadata, reviewer disposition and immutable evidence manifests.
7. **Corporation-enabling control plane:** organization chart/role catalogue, specialist pools, task queue, coordinator/supervisor, planning and verification stages, shared knowledge retrieval, budget/quota allocation, conflict-free work claims, escalation/human approvals, audit and revocation. These are capabilities to compose from existing components; do not introduce an alternative authority or let agent memory become the product-state source of truth.

## Explicit ECC handling
ECC is a valuable pattern source and may be re-evaluated as a narrowly scoped development workflow component. The currently checked-in decision rejects adopting ECC as a second controller/dependency because Astra must remain the sole control plane and qualification authority. Therefore:
- reuse compatible practices or isolated modules only after license/security/source review;
- no ECC hooks, MCP tools, memory, or plugins may gain independent write/promotion authority;
- any proposal to adopt ECC's orchestration/controller requires an explicit ADR/governance change and migration analysis;
- until such change is approved, keep ECC integration guidance-only and subordinate to executable Astra gates.

## Candidate integration gates
For each candidate component, record source URL and exact commit/tag, license, maintenance and security evidence, dependencies/SBOM, permission model, secret handling, network egress, sandbox boundary, persistence/recovery, provider support, quota semantics, observability, tests, rollback and owner of operational lifecycle. Run a thin vertical proof with fake/mock providers before connecting credentials or invoking a real provider. No secret is added to source or artifacts.

## Sequence
A. Finish the minimal Gemini controller gates; avoid allowing this narrow track to block source research of the broader pool.
B. In parallel, census registry consumers and compare candidate multi-agent/orchestration components against the contracts above.
C. Validate schemas and negative fixtures; prototype selected orchestration/router/state components with mocked providers.
D. Qualify one read-only cloud route and one small multi-agent workflow; then add further routes/components incrementally.
E. Deploy and independently accept the cloud pool only after security, operational, quota, recovery, evidence and rollback gates pass.
F. Only after that acceptance, start local executor/Jarvis reference architecture and component selection. Preserve the independent ASTRA A0 / Jarvis / MediaHub Product State Authority boundaries. Contour B remains blocked until Contour A is deployed and independently accepted.

## Status and non-actions
This is a planning and source-inventory update. No candidate framework was installed, no provider route was enabled, no API was called, no agent was dispatched, no secret was accessed, and no deployment/qualification/acceptance occurred. The registry's free-tier labels remain unverified. Existing ECC authority decision remains in force.

## Next bounded step
Create a candidate component comparison matrix grounded in exact upstream repositories/releases and existing MediaHub contracts; prioritize components that cover multiple missing capabilities without duplicating the control plane. Then prototype orchestration and quota behavior with mock providers only.
